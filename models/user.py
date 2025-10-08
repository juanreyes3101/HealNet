from extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
import pytz

class User(db.Model, UserMixin):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True)
    contraseña_encriptada = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), default="paciente")
    numero = db.Column(db.String(20), nullable=True)
    cumpleaños = db.Column(db.Date, nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    creado_en = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Bogota')))

    # NUEVA RELACIÓN CON POSTS
    posts = db.relationship('Post', backref='autor', lazy=True)

    def set_contraseña(self, contraseña):
        self.contraseña_encriptada = bcrypt.generate_password_hash(contraseña).decode("utf-8")

    def check_contraseña(self, contraseña):
        return bcrypt.check_password_hash(self.contraseña_encriptada, contraseña)

    def __repr__(self):
        return f"<User {self.nombre}>"