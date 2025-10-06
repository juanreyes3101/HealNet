from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from models.user import User
from app import db

auth = Blueprint('auth', __name__)

# Ruta de registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('contraseña')

        # Validación básica
        if not nombre or not correo or not password:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('auth.register'))

        # Verificar si el correo ya existe
        existing_user = User.query.filter_by(correo=correo).first()
        if existing_user:
            flash('Este correo ya está registrado', 'error')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario
        nuevo_usuario = User(nombre=nombre, correo=correo)
        nuevo_usuario.set_contraseña(password)  # usa tu método del modelo

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada con éxito. Ahora inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')



# Ruta de login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        usuario = User.query.filter_by(correo=correo).first()

        if usuario and usuario.check_contraseña(contraseña):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'error')

    return render_template('login.html')


# Ruta de logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
