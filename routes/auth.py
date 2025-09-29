from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.user import User
from app import db

auth = Blueprint('auth', __name__)
# Ruta de registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        # Encriptamos la contraseña
        hashed_password = generate_password_hash(password, method='sha256')

        # Creamos usuario y lo guardamos
        nuevo_usuario = User(nombre=nombre, email=email, password=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada con éxito, ahora inicia sesión')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# Ruta de login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = User.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Correo o contraseña incorrectos')

    return render_template('login.html')

# Ruta de logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
