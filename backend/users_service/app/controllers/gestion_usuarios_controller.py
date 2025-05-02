from app.models.usuario import Usuario
from app.models.direccion import Direccion
from app.config import db
from app.utils.validations import validate_email, validate_phone, validate_age, validate_password
from app.utils.jwt_generator import admin_required
from app.utils.token_confirmar_cuenta import generate_confirmation_token
from app.utils.email_sender import send_confirmation_email
from sqlalchemy import or_, asc, desc
import bcrypt


def crear_usuario_admin(data):
    if not validate_email(data['correo_electronico']):
        return {"OK": False, "DESCRIPCION": "Correo electrónico inválido.", "RESPUESTA": {}}
    if not validate_phone(data['telefono']):
        return {"OK": False, "DESCRIPCION": "El teléfono debe tener 8 dígitos numéricos.", "RESPUESTA": {}}
    if not validate_age(data['fecha_nacimiento']):
        return {"OK": False, "DESCRIPCION": "El usuario debe tener entre 18 y 99 años.", "RESPUESTA": {}}
    if not validate_password(data['contrasena']):
        return {"OK": False, "DESCRIPCION": "La contraseña no cumple con los requisitos de seguridad.", "RESPUESTA": {}}
    if 'direcciones' not in data or not isinstance(data['direcciones'], list) or len(data['direcciones']) == 0:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar al menos una dirección.", "RESPUESTA": {}}

    existente = Usuario.query.filter(
        (Usuario.correo_electronico == data['correo_electronico']) |
        (Usuario.username == data['username'])
    ).first()
    if existente:
        return {"OK": False, "DESCRIPCION": "Correo o usuario ya en uso.", "RESPUESTA": {}}

    hashed_pass = bcrypt.hashpw(data['contrasena'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    nuevo = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo_electronico=data['correo_electronico'],
        username=data['username'],
        telefono=data['telefono'],
        fecha_nacimiento=data['fecha_nacimiento'],
        sexo=data['sexo'],
        foto=data.get('foto'),
        contrasena=hashed_pass,
        estado=data['estado'],
        tipo=data['tipo'],
        total_compra=0,
        descuento_exclusivo=False,
        fecha_inicio_descuento=None
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

    if data.get("enviar_confirmacion", False):
        try:
            token, expira = generate_confirmation_token()
            nuevo.token_confirmacion = token
            nuevo.token_confirmacion_expira = expira
            db.session.commit()
            send_confirmation_email(data['correo_electronico'], token)
        except Exception:
            return {"OK": False, "DESCRIPCION": "Error al enviar el correo de confirmación.", "RESPUESTA": {}}

    return {"OK": True, "DESCRIPCION": "Usuario creado exitosamente.", "RESPUESTA": {}}



def actualizar_usuario_por_id(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    # Validaciones
    if not validate_email(data['correo_electronico']):
        return {"OK": False, "DESCRIPCION": "Correo electrónico inválido.", "RESPUESTA": {}}
    if not validate_phone(data['telefono']):
        return {"OK": False, "DESCRIPCION": "El teléfono debe tener 8 dígitos numéricos.", "RESPUESTA": {}}
    if not validate_age(data['fecha_nacimiento']):
        return {"OK": False, "DESCRIPCION": "El usuario debe tener entre 18 y 99 años.", "RESPUESTA": {}}

    existente = Usuario.query.filter(
        ((Usuario.correo_electronico == data['correo_electronico']) |
         (Usuario.username == data['username'])) &
        (Usuario.id_usuario != id_usuario)
    ).first()
    if existente:
        return {"OK": False, "DESCRIPCION": "Correo o usuario ya en uso por otro usuario.", "RESPUESTA": {}}

    try:
        usuario.nombre = data['nombre']
        usuario.apellido = data['apellido']
        usuario.correo_electronico = data['correo_electronico']
        usuario.username = data['username']
        usuario.telefono = data['telefono']
        usuario.fecha_nacimiento = data['fecha_nacimiento']
        usuario.sexo = data['sexo']
        usuario.tipo = data['tipo']
        usuario.estado = data['estado']
        usuario.foto = data.get('foto', None)

        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Usuario actualizado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar usuario.", "RESPUESTA": {"error": str(e)}}
    

def inactivar_usuario_por_id(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    if usuario.estado != "activo":
        return {"OK": False, "DESCRIPCION": "El usuario ya se encuentra inactivo.", "RESPUESTA": {}}

    try:
        usuario.estado = "inactivo"
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Usuario inactivado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al inactivar usuario.", "RESPUESTA": {"error": str(e)}}


def reactivar_usuario_por_id(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    if usuario.estado == "activo":
        return {"OK": False, "DESCRIPCION": "El usuario ya se encuentra activo.", "RESPUESTA": {}}

    try:
        usuario.estado = "activo"
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Usuario reactivado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al reactivar usuario.", "RESPUESTA": {"error": str(e)}}


def obtener_usuarios_dashboard(page, size, sort_by, sort_dir, search):
    columnas_validas = {
        "id_usuario": Usuario.id_usuario,
        "nombre": Usuario.nombre,
        "apellido": Usuario.apellido,
        "correo_electronico": Usuario.correo_electronico,
        "username": Usuario.username,
        "telefono": Usuario.telefono,
        "estado": Usuario.estado,
        "tipo": Usuario.tipo
    }

    sort_column = columnas_validas.get(sort_by.lower(), Usuario.id_usuario)
    orden = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    query = Usuario.query

    if search:
        query = query.filter(
            or_(
                Usuario.nombre.ilike(f"%{search}%"),
                Usuario.apellido.ilike(f"%{search}%"),
                Usuario.username.ilike(f"%{search}%"),
                Usuario.correo_electronico.ilike(f"%{search}%")
            )
        )

    total = query.count()
    usuarios = query.order_by(orden).offset(page * size).limit(size).all()

    datos = []
    for u in usuarios:
        datos.append({
            "id_usuario": u.id_usuario,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "correo_electronico": u.correo_electronico,
            "username": u.username,
            "telefono": u.telefono,
            "estado": u.estado,
            "tipo": u.tipo,
        })

    return {
        "OK": True,
        "DESCRIPCION": "Usuarios obtenidos correctamente.",
        "RESPUESTA": {
            "total": total,
            "pagina": page,
            "tamanio": size,
            "usuarios": datos
        }
    }


def obtener_usuario_con_direcciones(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    direcciones = Direccion.query.filter_by(id_usuario=usuario.id_usuario).all()
    direcciones_list = [{
        "id_direccion": d.id_direccion,
        "id_departamento": d.id_departamento,
        "id_ciudad": d.id_ciudad,
        "otras_senas": d.otras_senas
    } for d in direcciones]

    datos_usuario = {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "correo_electronico": usuario.correo_electronico,
        "username": usuario.username,
        "telefono": usuario.telefono,
        "fecha_nacimiento": str(usuario.fecha_nacimiento),
        "sexo": usuario.sexo,
        "tipo": usuario.tipo,
        "estado": usuario.estado,
        "foto": usuario.foto,
        "direcciones": direcciones_list
    }

    return {
        "OK": True,
        "DESCRIPCION": "Usuario obtenido correctamente.",
        "RESPUESTA": datos_usuario
    }


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