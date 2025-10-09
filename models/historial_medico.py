from extensions import db
from datetime import datetime
import pytz

def hora_bogota():
    return datetime.now(pytz.timezone('America/Bogota'))

class HistorialMedico(db.Model):
    __tablename__ = "HistorialMedico"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    
    # Información médica general
    tipo_sangre = db.Column(db.String(5), nullable=True)  # A+, O-, etc.
    alergias = db.Column(db.Text, nullable=True)
    enfermedades_cronicas = db.Column(db.Text, nullable=True)
    medicamentos_actuales = db.Column(db.Text, nullable=True)
    cirugias_previas = db.Column(db.Text, nullable=True)
    
    # Información adicional
    peso = db.Column(db.Float, nullable=True)  # en kg
    altura = db.Column(db.Float, nullable=True)  # en cm
    
    # Contacto de emergencia
    contacto_emergencia_nombre = db.Column(db.String(100), nullable=True)
    contacto_emergencia_telefono = db.Column(db.String(20), nullable=True)
    contacto_emergencia_relacion = db.Column(db.String(50), nullable=True)
    
    # Fechas
    creado_en = db.Column(db.DateTime, default=hora_bogota)
    actualizado_en = db.Column(db.DateTime, default=hora_bogota, onupdate=hora_bogota)

    def calcular_imc(self):
        """Calcula el Índice de Masa Corporal"""
        if self.peso and self.altura:
            altura_metros = self.altura / 100
            return round(self.peso / (altura_metros ** 2), 2)
        return None
    
    def categoria_imc(self):
        """Retorna la categoría del IMC"""
        imc = self.calcular_imc()
        if not imc:
            return "No disponible"
        
        if imc < 18.5:
            return "Bajo peso"
        elif 18.5 <= imc < 25:
            return "Peso normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"

    def __repr__(self):
        return f"<HistorialMedico paciente_id={self.paciente_id}>"