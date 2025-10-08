from flask import Flask
from extensions import db, bcrypt, login_manager
from models.user import User
from models.post import Post  # Importamos el modelo Post

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = "clave_super_secreta_para_dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///healnet.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
    login_manager.login_message_category = 'info'
    
    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Crear tablas (incluyendo Posts)
    with app.app_context():
        db.create_all()
        print("✅ Base de datos creada/actualizada correctamente")
    
    # Registrar Blueprints
    from routes.auth import auth
    from routes.main import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)