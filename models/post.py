from extensions import db
from datetime import datetime
import pytz

class Post(db.Model):

    
    """Modelo para los posts/foros creados por pacientes"""
    
    __tablename__ = "Posts"
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), default="General")  # General, Urgente, Consulta, etc.
    
    # Relación con usuario (autor del post) - usando string para evitar import circular
    autor_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    # La relación se define en User, no aquí para evitar imports circulares
    
    # Metadatos
    creado_en = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Bogota')))
    actualizado_en = db.Column(db.DateTime, onupdate=lambda: datetime.now(pytz.timezone('America/Bogota')))
    
    # Estadísticas
    vistas = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f"<Post {self.titulo}>"
    
    def tiempo_transcurrido(self):
        """Retorna el tiempo transcurrido desde la creación"""
        bogota_tz = pytz.timezone('America/Bogota')
        now = datetime.now(bogota_tz)
        
        if self.creado_en.tzinfo is None:
            fecha = bogota_tz.localize(self.creado_en)
        else:
            fecha = self.creado_en
            
        delta = now - fecha
        
        if delta.days > 0:
            return f"Hace {delta.days} día{'s' if delta.days > 1 else ''}"
        elif delta.seconds >= 3600:
            horas = delta.seconds // 3600
            return f"Hace {horas} hora{'s' if horas > 1 else ''}"
        elif delta.seconds >= 60:
            minutos = delta.seconds // 60
            return f"Hace {minutos} minuto{'s' if minutos > 1 else ''}"
        else:
            return "Hace un momento"