from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from extensions import db
from models.user import User




auth = Blueprint('auth', __name__)


#Encargado de redirigir al login o al dashboard principal

@auth.route('/')
def index():
    """Redirige al login si no está autenticado, al dashboard si lo está"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


#Funcion encargada del registro de nuevos usuarios

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip().lower()
        password = request.form.get('contraseña', '')
        
        # Validación básica
        if not nombre or not correo or not password:
            flash('Por favor completa todos los campos', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validación de longitud de contraseña
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('auth.register'))
        
        # Verificar si el correo ya existe
        if User.query.filter_by(correo=correo).first():
            flash('Este correo ya está registrado', 'danger')
            return redirect(url_for('auth.register'))
        
        # Crear nuevo usuario
        nuevo_usuario = User(nombre=nombre, correo=correo)
        nuevo_usuario.set_contraseña(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Cuenta creada con éxito. Ahora inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


#Funcion encargada del login de usuarios

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirigir según rol
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip().lower()
        contraseña = request.form.get('contraseña', '')

        user = User.query.filter_by(correo=correo).first()
        if user and user.check_contraseña(contraseña):
            login_user(user)
            flash(f"Bienvenido, {user.nombre}", "success")
            
            # Redirigir según rol
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

#Funcion encargada del logout de usuarios

@auth.route('/logout')
def logout():
    """Cierre de sesión"""
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))