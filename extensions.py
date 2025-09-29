# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Inicializamos las extensiones pero sin ligarlas aún a la app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
