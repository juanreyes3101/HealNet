# models/user.py
from extensions import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"  # nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # identificador único
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # 🛠 Guardar contraseña encriptada
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # 🛠 Verificar contraseña en login
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
