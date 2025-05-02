import re
from datetime import datetime

def validate_email(email):
    regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(regex, email)

def validate_phone(telefono):
    return telefono.isdigit() and len(telefono) == 8


def validate_age(fecha_nacimiento):
    if isinstance(fecha_nacimiento, str):
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()

    hoy = datetime.today().date()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return 18 <= edad <= 99

def validate_password(password):
    patron = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#])[A-Za-z\d@$!%*?&.#]{8,}$")
    return bool(patron.match(password))