import sys
sys.path.insert(0, '.')

# Importar directamente
from flask import Flask
from extensions import db
from models import User, Cita, HistorialMedico, Post

# Crear app temporal
app = Flask(__name__)
app.config['SECRET_KEY'] = "juanreyes_06"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///healnet.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("⚠️  Eliminando tablas existentes...")
    db.drop_all()
    
    print("✓ Creando nuevas tablas...")
    db.create_all()
    
    print("\n✓ Base de datos actualizada correctamente")
    print("\n📊 Tablas creadas:")
    print("   • Usuarios")
    print("   • Citas")
    print("   • HistorialMedico")
    print("   • Posts")
    
    print("\n🔑 Ejecuta la siguiente ruta para crear el admin:")
    print("   http://127.0.0.1:5000/setup-admin-secret-route-2025")