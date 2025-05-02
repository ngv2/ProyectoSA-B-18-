from app.models.usuario import Usuario
from app.models.direccion import Direccion
from app.config import db
from app.utils.validations import *
from app.utils.token_confirmar_cuenta import *
from app.utils.email_sender import *
from app.utils.jwt_generator import generate_jwt_token
from datetime import datetime
import bcrypt


def crear_usuario(data):
    if not validate_email(data['correo_electronico']):
        return {"OK": False, "DESCRIPCION": "Correo electrónico inválido.", "RESPUESTA": {}}
    if not validate_phone(data['telefono']):
        return {"OK": False, "DESCRIPCION": "El teléfono debe tener 8 dígitos numéricos.", "RESPUESTA": {}}
    if not validate_age(data['fecha_nacimiento']):
        return {"OK": False, "DESCRIPCION": "El usuario debe tener entre 18 y 99 años.", "RESPUESTA": {}}
    if not validate_password(data['contrasena']):
        return {"OK": False, "DESCRIPCION": "La contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.", "RESPUESTA": {}}

    if 'direcciones' not in data or not isinstance(data['direcciones'], list) or len(data['direcciones']) == 0:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar al menos una dirección.", "RESPUESTA": {}}

    existente = Usuario.query.filter(
        (Usuario.correo_electronico == data['correo_electronico']) |
        (Usuario.username == data['username'])
    ).first()
    if existente:
        return {"OK": False, "DESCRIPCION": "Correo o usuario ya en uso.", "RESPUESTA": {}}

    token, expira = generate_confirmation_token()
    hashed_pw = bcrypt.hashpw(data['contrasena'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    nuevo = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo_electronico=data['correo_electronico'],
        username=data['username'],
        telefono=data['telefono'],
        fecha_nacimiento=data['fecha_nacimiento'],
        sexo=data['sexo'],
        foto=data.get('foto'),
        token_confirmacion=token,
        token_confirmacion_expira=expira,
        contrasena=hashed_pw
    )
    db.session.add(nuevo)
    db.session.flush()

    try:
        for dir_data in data['direcciones']:
            nueva_direccion = Direccion(
                otras_senas=dir_data['otras_senas'],
                id_departamento=dir_data['id_departamento'],
                id_ciudad=dir_data['id_ciudad'],
                id_usuario=nuevo.id_usuario
            )
            db.session.add(nueva_direccion)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al guardar las direcciones. Verifique los datos ingresados.", "RESPUESTA": {}}

    send_confirmation_email(data['correo_electronico'], token)
    return {"OK": True, "DESCRIPCION": "Usuario registrado exitosamente. Revisa tu correo para confirmar.", "RESPUESTA": {}}



def confirmar_usuario_por_token(token):
    usuario = Usuario.query.filter_by(token_confirmacion=token).first()

    if not usuario:
        return {"OK": False, "DESCRIPCION": "Token inválido o ya utilizado.", "RESPUESTA": {}}

    if not verify_token_expiration(usuario.token_confirmacion_expira):
        return {"OK": False, "DESCRIPCION": "El token ha expirado. Solicite uno nuevo.", "RESPUESTA": {}}

    usuario.estado = 'activo'
    usuario.token_confirmacion = None
    usuario.token_confirmacion_expira = None
    db.session.commit()

    jwt_token = generate_jwt_token(usuario.id_usuario, usuario.tipo)
    return {
        "OK": True,
        "DESCRIPCION": "Usuario confirmado exitosamente.",
        "RESPUESTA": {"access_token": jwt_token}
    }



def login_usuario(data):
    usuario_entrada = data.get('usuario')
    contrasena = data.get('contrasena')

    if not usuario_entrada or not contrasena:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar usuario (correo o username) y contraseña.", "RESPUESTA": {}}

    usuario = Usuario.query.filter(
        (Usuario.correo_electronico == usuario_entrada) | 
        (Usuario.username == usuario_entrada)
    ).first()

    if not usuario:
        return {"OK": False, "DESCRIPCION": "El usuario no existe.", "RESPUESTA": {}}

    if usuario.estado != 'activo':
        return {"OK": False, "DESCRIPCION": "El usuario aún no ha sido confirmado o está inactivo.", "RESPUESTA": {}}

    if not bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
        return {"OK": False, "DESCRIPCION": "Contraseña incorrecta.", "RESPUESTA": {}}

    token = generate_jwt_token(usuario.id_usuario, usuario.tipo)

    return {
        "OK": True,
        "DESCRIPCION": "Inicio de sesión exitoso.",
        "RESPUESTA": {
            "TIPO_USUARIO": usuario.tipo,
            "ACCESS_TOKEN": token
        }
    }



def solicitar_recuperacion_contrasena(usuario_input):
    if not usuario_input:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar un correo electrónico o username.", "RESPUESTA": {}}

    usuario = Usuario.query.filter(
        (Usuario.correo_electronico == usuario_input) | 
        (Usuario.username == usuario_input)
    ).first()

    if not usuario:
        return {"OK": False, "DESCRIPCION": "El usuario no existe.", "RESPUESTA": {}}

    if usuario.estado != "activo":
        return {"OK": False, "DESCRIPCION": "El usuario no está activo. Confirme su cuenta primero.", "RESPUESTA": {}}

    token, expira = generate_confirmation_token()

    usuario.token_recuperacion = token
    usuario.token_recuperacion_expira = expira
    db.session.commit()

    try:
        send_password_recovery_email(usuario.correo_electronico, token)
    except Exception:
        return {"OK": False, "DESCRIPCION": "Error al enviar el correo de recuperación. Intente más tarde.", "RESPUESTA": {}}

    return {"OK": True, "DESCRIPCION": "Se ha enviado el enlace de recuperación al correo del usuario.", "RESPUESTA": {}}



def restablecer_contrasena(token, nueva_contrasena):
    usuario = Usuario.query.filter_by(token_recuperacion=token).first()

    if not usuario:
        return {"OK": False, "DESCRIPCION": "Token inválido o ya utilizado.", "RESPUESTA": {}}

    if usuario.estado != "activo":
        return {"OK": False, "DESCRIPCION": "El usuario no está activo.", "RESPUESTA": {}}

    if not verify_token_expiration(usuario.token_recuperacion_expira):
        return {"OK": False, "DESCRIPCION": "El token ha expirado. Solicite uno nuevo.", "RESPUESTA": {}}

    if not validate_password(nueva_contrasena):
        return {"OK": False, "DESCRIPCION": "La contraseña no cumple con los requisitos de seguridad.", "RESPUESTA": {}}

    usuario.contrasena = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuario.token_recuperacion = None
    usuario.token_recuperacion_expira = None
    db.session.commit()

    return {"OK": True, "DESCRIPCION": "Contraseña actualizada exitosamente.", "RESPUESTA": {}}


def crear_direccion_usuario(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    campos_requeridos = ["id_departamento", "id_ciudad", "otras_senas"]
    for campo in campos_requeridos:
        if campo not in data:
            return {"OK": False, "DESCRIPCION": f"Campo obligatorio faltante: {campo}", "RESPUESTA": {}}

    try:
        nueva_direccion = Direccion(
            id_usuario=id_usuario,
            id_departamento=data["id_departamento"],
            id_ciudad=data["id_ciudad"],
            otras_senas=data["otras_senas"]
        )
        db.session.add(nueva_direccion)
        db.session.commit()
        return {
            "OK": True,
            "DESCRIPCION": "Dirección creada correctamente.",
            "RESPUESTA": {
                "id_direccion": nueva_direccion.id_direccion
            }
        }
    except Exception as e:
        db.session.rollback()
        return {
            "OK": False,
            "DESCRIPCION": "Error al crear la dirección.",
            "RESPUESTA": {"error": str(e)}
        }