from extensions import db
from datetime import datetime
import pytz

def hora_bogota():
    return datetime.now(pytz.timezone('America/Bogota'))

class Post(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    
    # Contenido del post
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=True)  # salud, nutrición, ejercicio, noticias, etc.
    
    # Imagen destacada (opcional)
    imagen_url = db.Column(db.String(500), nullable=True)
    emoji_icono = db.Column(db.String(10), default='📰')  # Para mostrar en las cards
    
    # Control de visibilidad
    publicado = db.Column(db.Boolean, default=True)
    destacado = db.Column(db.Boolean, default=False)
    
    # Fechas
    creado_en = db.Column(db.DateTime, default=hora_bogota)
    actualizado_en = db.Column(db.DateTime, default=hora_bogota, onupdate=hora_bogota)

    def resumen(self, longitud=150):
        """Retorna un resumen del contenido"""
        if len(self.contenido) <= longitud:
            return self.contenido
        return self.contenido[:longitud] + '...'

    def __repr__(self):
        return f"<Post '{self.titulo}'>"