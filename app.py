from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt, login_manager
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "clave_super_secreta_para_dev"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///healnet.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones con la app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Cómo cargar un usuario por ID (requerido por flask-login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas si no existen (solo en desarrollo)
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('nombre', '').strip()  
        email = request.form.get('correo', '').strip().lower()  
        password = request.form.get('contraseña', '')  

        if not (name and email and password):
            flash("Por favor completa todos los campos", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(correo=email).first(): 
            flash("El correo ya está registrado", "danger")
            return redirect(url_for("register"))

        user = User(nombre=name, correo=email)  
        user.set_contraseña(password)  
        db.session.add(user)
        db.session.commit()

        flash("Registro exitoso. Ya puedes iniciar sesión", "success")
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('correo', '').strip().lower()  
        password = request.form.get('contraseña', '')  
        user = User.query.filter_by(correo=email).first() 
        if user and user.check_contraseña(password): 
            login_user(user)
            flash("Bienvenido a HealNet", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # aquí ponerías un template real; por ahora respuesta simple
    return f"Hola {current_user.nombre}, esto es tu dashboard privado."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
