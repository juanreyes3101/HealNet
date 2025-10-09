from extensions import db
from datetime import datetime
import pytz

def hora_bogota():
    return datetime.now(pytz.timezone('America/Bogota'))

class Cita(db.Model):
    __tablename__ = "Citas"

    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    
    # Información de la cita
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    sintomas = db.Column(db.Text, nullable=True)
    
    # Estado de la cita
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, completada, cancelada
    
    # Notas médicas (solo el doctor puede llenarlas)
    diagnostico = db.Column(db.Text, nullable=True)
    tratamiento = db.Column(db.Text, nullable=True)
    notas_medicas = db.Column(db.Text, nullable=True)
    
    # Fechas de control
    creado_en = db.Column(db.DateTime, default=hora_bogota)
    actualizado_en = db.Column(db.DateTime, default=hora_bogota, onupdate=hora_bogota)

    def __repr__(self):
        return f"<Cita {self.id} - {self.estado} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}>"