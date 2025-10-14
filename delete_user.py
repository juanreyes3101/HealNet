from app import app, db
from models.user import User

def eliminar_usuario(correo):
    with app.app_context():
        user = User.query.filter_by(correo=correo).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"Usuario {user.nombre} ({correo}) eliminado")
        else:
            print(f"No se encontró usuario con correo {correo}")

if __name__ == "__main__":
    correo = input("Ingresa el correo del usuario a eliminar: ")
    eliminar_usuario(correo)