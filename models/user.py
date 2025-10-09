from extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
import pytz

def hora_bogota():
    "Retorna la hora actual en timezone de Bogotá"
    return datetime.now(pytz.timezone('America/Bogota'))

class User(db.Model, UserMixin):
    __tablename__ = "Usuarios"

    # Campos básicos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True)
    contraseña_encriptada = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), default="paciente")  # paciente, doctor, admin
    
    # Información de contacto
    numero = db.Column(db.String(20), nullable=True)
    cumpleaños = db.Column(db.Date, nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    
    # Campos específicos para doctores
    especialidad = db.Column(db.String(100), nullable=True)
    licencia_medica = db.Column(db.String(50), nullable=True)
    biografia = db.Column(db.Text, nullable=True)
    
    # Estado y fecha
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=hora_bogota)
    actualizado_en = db.Column(db.DateTime, default=hora_bogota, onupdate=hora_bogota)

    # RELACIONES

    # Citas como paciente
    citas_como_paciente = db.relationship('Cita', 
                                          foreign_keys='Cita.paciente_id',
                                          backref='paciente', 
                                          lazy=True,
                                          cascade='all, delete-orphan')
    
    # Citas como doctor
    citas_como_doctor = db.relationship('Cita', 
                                        foreign_keys='Cita.doctor_id',
                                        backref='doctor', 
                                        lazy=True)
    
    # Historial médico (solo para pacientes)
    historial_medico = db.relationship('HistorialMedico', 
                                       backref='paciente', 
                                       lazy=True,
                                       cascade='all, delete-orphan')
    
    # Posts del foro
    posts = db.relationship('Post', 
                           backref='autor', 
                           lazy=True,
                           cascade='all, delete-orphan')

    # MÉTODOS
    
    def set_contraseña(self, contraseña):
        self.contraseña_encriptada = bcrypt.generate_password_hash(contraseña).decode("utf-8")

    def check_contraseña(self, contraseña):
        return bcrypt.check_password_hash(self.contraseña_encriptada, contraseña)
    
    def is_admin(self):
        return self.rol == 'admin'
    
    def is_doctor(self):
        return self.rol == 'doctor'
    
    def is_paciente(self):
        return self.rol == 'paciente'

    def __repr__(self):
        return f"<User {self.nombre} ({self.rol})>"