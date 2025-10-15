from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import User, Cita
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para verificar que sea admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Ruta donde el admin ve el dashboard con estadísticas

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard principal del administrador"""
    # Estadísticas
    total_usuarios = User.query.count()
    total_pacientes = User.query.filter_by(rol='paciente').count()
    total_doctores = User.query.filter_by(rol='doctor').count()
    total_admins = User.query.filter_by(rol='admin').count()
    total_citas = Cita.query.count()
    citas_pendientes = Cita.query.filter_by(estado='pendiente').count()
    
    # Últimos usuarios registrados
    ultimos_usuarios = User.query.order_by(User.creado_en.desc()).limit(5).all()
    
    # Próximas citas
    proximas_citas = Cita.query.filter(
        Cita.fecha_hora >= datetime.now()
    ).order_by(Cita.fecha_hora).limit(5).all()
    
    return render_template('dashboard_admin.html',
                         stats={
                             'total_usuarios': total_usuarios,
                             'total_pacientes': total_pacientes,
                             'total_doctores': total_doctores,
                             'total_admins': total_admins,
                             'total_citas': total_citas,
                             'citas_pendientes': citas_pendientes
                         },
                         ultimos_usuarios=ultimos_usuarios,
                         proximas_citas=proximas_citas)


#Ruta para gestionar usuarios (listar, crear, editar, eliminar)

@admin.route('/usuarios')
@login_required
@admin_required
def usuarios():
    """Lista de todos los usuarios"""
    rol_filter = request.args.get('rol', 'todos')
    buscar = request.args.get('buscar', '')
    
    query = User.query
    
    # Filtrar por rol
    if rol_filter != 'todos':
        query = query.filter_by(rol=rol_filter)
    
    # Búsqueda
    if buscar:
        query = query.filter(
            (User.nombre.contains(buscar)) | 
            (User.correo.contains(buscar))
        )
    
    usuarios = query.order_by(User.creado_en.desc()).all()
    
    return render_template('usuarios.html', 
                         usuarios=usuarios,
                         rol_filter=rol_filter,
                         buscar=buscar)


# Ruta para crear un nuevo usuario

@admin.route('/usuario/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    """Crear nuevo usuario (paciente, doctor o admin)"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip().lower()
        contraseña = request.form.get('contraseña', '')
        rol = request.form.get('rol', 'paciente')
        numero = request.form.get('numero', '').strip()
        especialidad = request.form.get('especialidad', '').strip()
        licencia = request.form.get('licencia', '').strip()
        
        # Validaciones
        if not (nombre and correo and contraseña):
            flash('Por favor completa todos los campos obligatorios', 'danger')
            return redirect(url_for('admin.crear_usuario'))
        
        if User.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('admin.crear_usuario'))
        
        # Crear usuario
        nuevo_usuario = User(
            nombre=nombre,
            correo=correo,
            rol=rol,
            numero=numero
        )
        
        # Si es doctor, agregar campos adicionales
        if rol == 'doctor':
            nuevo_usuario.especialidad = especialidad
            nuevo_usuario.licencia_medica = licencia
        
        nuevo_usuario.set_contraseña(contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash(f'Usuario {nombre} creado exitosamente como {rol}', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/crear_usuario.html')


# Ruta para editar un usuario existente


@admin.route('/usuario/<int:user_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(user_id):
    """Editar usuario existente"""
    usuario = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre', '').strip()
        usuario.correo = request.form.get('correo', '').strip().lower()
        usuario.rol = request.form.get('rol', 'paciente')
        usuario.numero = request.form.get('numero', '').strip()
        usuario.activo = request.form.get('activo') == 'on'
        
        # Si es doctor
        if usuario.rol == 'doctor':
            usuario.especialidad = request.form.get('especialidad', '').strip()
            usuario.licencia_medica = request.form.get('licencia', '').strip()
        
        # Cambiar contraseña solo si se proporciona una nueva
        nueva_contraseña = request.form.get('nueva_contraseña', '').strip()
        if nueva_contraseña:
            usuario.set_contraseña(nueva_contraseña)
        
        db.session.commit()
        flash(f'Usuario {usuario.nombre} actualizado exitosamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/editar_usuario.html', usuario=usuario)


# Ruta para eliminar un usuario


@admin.route('/usuario/<int:user_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(user_id):
    """Eliminar usuario"""
    if user_id == current_user.id:
        flash('No puedes eliminarte a ti mismo', 'danger')
        return redirect(url_for('admin.usuarios'))
    
    usuario = User.query.get_or_404(user_id)
    nombre = usuario.nombre
    
    db.session.delete(usuario)
    db.session.commit()
    
    flash(f'Usuario {nombre} eliminado exitosamente', 'success')
    return redirect(url_for('admin.usuarios'))


# Ruta para activar/desactivar un usuario

@admin.route('/usuario/<int:user_id>/toggle-activo', methods=['POST'])
@login_required
@admin_required
def toggle_activo(user_id):
    """Activar/desactivar usuario"""
    usuario = User.query.get_or_404(user_id)
    usuario.activo = not usuario.activo
    db.session.commit()
    
    estado = "activado" if usuario.activo else "desactivado"
    flash(f'Usuario {usuario.nombre} {estado}', 'success')
    return redirect(url_for('admin.usuarios'))


# Ruta para ver el calendario con todas las citas


@admin.route('/calendario')
@login_required
@admin_required
def calendario():
    """Calendario con todas las citas"""
    return render_template('admin/calendario.html')


# API para obtener citas en formato JSON para el calendario


@admin.route('/api/citas')
@login_required
@admin_required
def api_citas():
    """API para obtener citas en formato JSON para el calendario"""
    citas = Cita.query.all()
    
    eventos = []
    for cita in citas:
        color = {
            'pendiente': '#ffc107',
            'confirmada': '#17a2b8',
            'completada': '#28a745',
            'cancelada': '#dc3545'
        }.get(cita.estado, '#6c757d')
        
        eventos.append({
            'id': cita.id,
            'title': f'{cita.paciente.nombre} - Dr. {cita.doctor.nombre}',
            'start': cita.fecha_hora.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'paciente': cita.paciente.nombre,
                'doctor': cita.doctor.nombre,
                'motivo': cita.motivo,
                'estado': cita.estado
            }
        })
    
    return jsonify(eventos)