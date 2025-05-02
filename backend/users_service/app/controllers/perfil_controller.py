from app.models.usuario import Usuario
from app.models.direccion import Direccion
from app.config import db
from app.utils.validations import validate_email, validate_phone

def actualizar_perfil_usuario(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    if "correo_electronico" in data:
        if not validate_email(data["correo_electronico"]):
            return {"OK": False, "DESCRIPCION": "Correo electrónico inválido.", "RESPUESTA": {}}
        usuario.correo_electronico = data["correo_electronico"]

    if "telefono" in data:
        if not validate_phone(data["telefono"]):
            return {"OK": False, "DESCRIPCION": "Teléfono inválido (8 dígitos numéricos).", "RESPUESTA": {}}
        usuario.telefono = data["telefono"]

    try:
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Perfil actualizado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar perfil.", "RESPUESTA": {"error": str(e)}}


def crear_direccion_usuario_autenticado(id_usuario, data):
    campos = ["id_departamento", "id_ciudad", "otras_senas"]
    for campo in campos:
        if campo not in data:
            return {"OK": False, "DESCRIPCION": f"Campo requerido: {campo}", "RESPUESTA": {}}

    try:
        nueva = Direccion(
            id_usuario=id_usuario,
            id_departamento=data["id_departamento"],
            id_ciudad=data["id_ciudad"],
            otras_senas=data["otras_senas"]
        )
        db.session.add(nueva)
        db.session.commit()
        return {
            "OK": True,
            "DESCRIPCION": "Dirección creada correctamente.",
            "RESPUESTA": {"id_direccion": nueva.id_direccion}
        }
    except Exception as e:
        db.session.rollback()
        return {
            "OK": False,
            "DESCRIPCION": "Error al crear dirección.",
            "RESPUESTA": {"error": str(e)}
        }


def actualizar_direccion_usuario(id_direccion, user_info, data):
    direccion = Direccion.query.get(id_direccion)
    if not direccion:
        return {"OK": False, "DESCRIPCION": "Dirección no encontrada.", "RESPUESTA": {}}

    if user_info["tipo"] != "admin" and direccion.id_usuario != int(user_info["sub"]):
        return {"OK": False, "DESCRIPCION": "No tiene permisos para actualizar esta dirección.", "RESPUESTA": {}}

    direccion.id_departamento = data.get("id_departamento", direccion.id_departamento)
    direccion.id_ciudad = data.get("id_ciudad", direccion.id_ciudad)
    direccion.otras_senas = data.get("otras_senas", direccion.otras_senas)

    try:
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Dirección actualizada correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar dirección.", "RESPUESTA": {"error": str(e)}}


def eliminar_direccion_usuario(id_direccion, user_info):
    direccion = Direccion.query.get(id_direccion)
    if not direccion:
        return {"OK": False, "DESCRIPCION": "Dirección no encontrada.", "RESPUESTA": {}}

    if user_info["tipo"] != "admin" and direccion.id_usuario != int(user_info["sub"]):
        return {"OK": False, "DESCRIPCION": "No tiene permisos para eliminar esta dirección.", "RESPUESTA": {}}

    try:
        db.session.delete(direccion)
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Dirección eliminada correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al eliminar dirección.", "RESPUESTA": {"error": str(e)}}
