from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
import pytz

main = Blueprint('main', __name__)

# Filtro personalizado para calcular días desde el registro
@main.app_template_filter('timedelta_days')
def timedelta_days_filter(date):
    """Calcula los días desde una fecha hasta hoy"""
    if date:
        bogota_tz = pytz.timezone('America/Bogota')
        now = datetime.now(bogota_tz)
        # Si la fecha no tiene timezone, la convertimos
        if date.tzinfo is None:
            date = bogota_tz.localize(date)
        delta = now - date
        return delta.days
    return 0


#Ruta donde se ingresa despues del login

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario"""
    return render_template('dashboard.html', user=current_user)


#Ruta del perfil del usuario

@main.route('/perfil')
@login_required
def perfil():
    """Perfil del usuario"""
    return render_template('perfil.html', user=current_user)


#Ruta de la gestion de citas medicas

@main.route('/citas')
@login_required
def citas():
    """Gestión de citas médicas"""
    return render_template('citas.html', user=current_user)