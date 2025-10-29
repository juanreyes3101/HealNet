from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Cita
from datetime import datetime, timedelta
import pytz

citas = Blueprint('citas', __name__, url_prefix='/citas')

def hora_bogota():
    return datetime.now(pytz.timezone('America/Bogota'))


@citas.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    """Formulario para agendar una nueva cita"""
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo', '').strip()
        sintomas = request.form.get('sintomas', '').strip()
        
        # Validaciones
        if not (doctor_id and fecha and hora and motivo):
            flash('Por favor completa todos los campos obligatorios', 'danger')
            return redirect(url_for('citas.agendar'))
        
        # Combinar fecha y hora
        try:
            fecha_hora_str = f"{fecha} {hora}"
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            
            # Convertir a timezone de Bogotá
            bogota_tz = pytz.timezone('America/Bogota')
            fecha_hora = bogota_tz.localize(fecha_hora)
            
            # Validar que la fecha sea futura
            if fecha_hora <= hora_bogota():
                flash('La fecha y hora deben ser en el futuro', 'danger')
                return redirect(url_for('citas.agendar'))
            
        except ValueError:
            flash('Formato de fecha u hora inválido', 'danger')
            return redirect(url_for('citas.agendar'))
        
        # Verificar que el doctor existe
        doctor = User.query.filter_by(id=doctor_id, rol='doctor').first()
        if not doctor:
            flash('Doctor no encontrado', 'danger')
            return redirect(url_for('citas.agendar'))
        
        # Verificar disponibilidad
        cita_existente = Cita.query.filter_by(
            doctor_id=doctor_id,
            fecha_hora=fecha_hora
        ).first()
        
        if cita_existente:
            flash(f'El Dr. {doctor.nombre} ya tiene una cita agendada a esa hora', 'danger')
            return redirect(url_for('citas.agendar'))
        
        # Crear la cita
        nueva_cita = Cita(
            paciente_id=current_user.id,
            doctor_id=doctor_id,
            fecha_hora=fecha_hora,
            motivo=motivo,
            sintomas=sintomas,
            estado='pendiente'
        )
        
        db.session.add(nueva_cita)
        db.session.commit()
        
        flash(f'¡Cita agendada exitosamente con Dr. {doctor.nombre} para el {fecha_hora.strftime("%d/%m/%Y a las %H:%M")}!', 'success')
        return redirect(url_for('citas.mis_citas'))
    
    # GET - Mostrar formulario
    # Obtener todas las especialidades disponibles
    especialidades = db.session.query(User.especialidad).filter(
        User.rol == 'doctor',
        User.especialidad.isnot(None),
        User.activo == True
    ).distinct().all()
    especialidades = [e[0] for e in especialidades if e[0]]
    
    # Obtener todos los doctores activos y convertirlos a diccionarios
    doctores_query = User.query.filter_by(rol='doctor', activo=True).all()
    
    # Convertir doctores a diccionarios (JSON serializable)
    doctores = [{
        'id': d.id,
        'nombre': d.nombre,
        'especialidad': d.especialidad,
        'licencia_medica': d.licencia_medica
    } for d in doctores_query]
    
    # Fecha de hoy
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('agendar_cita.html', 
                         especialidades=especialidades,
                         doctores=doctores,
                         today=today)


@citas.route('/mis-citas')
@login_required
def mis_citas():
    """Ver todas las citas del usuario actual"""
    if current_user.is_doctor():
        # Si es doctor, ver las citas donde él es el doctor
        citas_usuario = Cita.query.filter_by(doctor_id=current_user.id).order_by(Cita.fecha_hora.desc()).all()
    else:
        # Si es paciente, ver sus citas
        citas_usuario = Cita.query.filter_by(paciente_id=current_user.id).order_by(Cita.fecha_hora.desc()).all()
    
    return render_template('mis_citas.html', citas=citas_usuario)


@citas.route('/<int:cita_id>/cancelar', methods=['POST'])
@login_required
def cancelar_cita(cita_id):
    """Cancelar una cita"""
    cita = Cita.query.get_or_404(cita_id)
    
    # Verificar que el usuario sea el paciente de la cita
    if cita.paciente_id != current_user.id and not current_user.is_admin():
        flash('No tienes permiso para cancelar esta cita', 'danger')
        return redirect(url_for('citas.mis_citas'))
    
    # Verificar que la cita no haya pasado
    if cita.fecha_hora < hora_bogota():
        flash('No puedes cancelar una cita que ya pasó', 'danger')
        return redirect(url_for('citas.mis_citas'))
    
    cita.estado = 'cancelada'
    db.session.commit()
    
    flash('Cita cancelada exitosamente', 'success')
    return redirect(url_for('citas.mis_citas'))


@citas.route('/api/doctores-por-especialidad/<especialidad>')
@login_required
def doctores_por_especialidad(especialidad):
    """API para obtener doctores filtrados por especialidad"""
    doctores = User.query.filter_by(
        rol='doctor',
        especialidad=especialidad,
        activo=True
    ).all()
    
    return jsonify([{
        'id': d.id,
        'nombre': d.nombre,
        'especialidad': d.especialidad,
        'licencia': d.licencia_medica
    } for d in doctores])


@citas.route('/api/horarios-disponibles/<int:doctor_id>/<fecha>')
@login_required
def horarios_disponibles(doctor_id, fecha):
    """API para obtener horarios disponibles de un doctor en una fecha"""
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        bogota_tz = pytz.timezone('America/Bogota')
        fecha_obj = bogota_tz.localize(fecha_obj)
    except ValueError:
        return jsonify({'error': 'Fecha inválida'}), 400
    
    # Horarios de atención (8am a 5pm)
    horarios = []
    for hora in range(8, 17):
        for minuto in [0, 30]:
            horario = fecha_obj.replace(hour=hora, minute=minuto)
            
            # Verificar si hay cita a esa hora
            cita_ocupada = Cita.query.filter_by(
                doctor_id=doctor_id,
                fecha_hora=horario
            ).first()
            
            if not cita_ocupada and horario > hora_bogota():
                horarios.append({
                    'hora': horario.strftime('%H:%M'),
                    'disponible': True
                })
    
    return jsonify(horarios)