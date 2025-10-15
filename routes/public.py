from flask import Blueprint
from extensions import db
from models import User

public = Blueprint('public', __name__)

#Ruta especial para traer el usuario admin inicial


@public.route('/setup-admin-secret-route-2025')
def setup_admin():

    """Crea el usuario administrador inicial"""
    # Verificar si ya existe un admin
    admin_exists = User.query.filter_by(rol='admin').first()
    if admin_exists:
        return """
        <h1>⚠️ Ya existe un administrador</h1>
        <p>El sistema ya tiene un usuario administrador.</p>
        <a href="/login">Ir a Login</a>
        """
    
    # Crear admin
    admin = User(
        nombre="Administrador",
        correo="admin@healnet.com",
        rol="admin"
    )
    admin.set_contraseña("admin123")
    db.session.add(admin)
    db.session.commit()
    
    return """
    <h1>✅ Administrador creado exitosamente</h1>
    <p><strong>Correo:</strong> admin@healnet.com</p>
    <p><strong>Contraseña:</strong> admin123</p>
    <p>⚠️ Cambia esta contraseña después de iniciar sesión</p>
    <br>
    <a href="/login">Ir a Login</a>
    """