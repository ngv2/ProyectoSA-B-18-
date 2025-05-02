from app.models.descuentos import DescuentoProducto, DescuentoUsuario, DescuentoTemporada
from app.config import db
from app.utils.api_helper import verificar_descuento_usuario, inactivar_descuento_usuario
from datetime import datetime, timedelta
from flask import g

### --------- PRODUCTO ---------

def crear_descuento_producto(data):
    descuento = DescuentoProducto(**data)
    db.session.add(descuento)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento creado para producto."}

def obtener_descuentos_producto():
    descuentos = DescuentoProducto.query.all()
    return {"OK": True, "RESPUESTA": [d.__dict__ for d in descuentos]}

def actualizar_descuento_producto(id_descuento, data):
    d = DescuentoProducto.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}
    d.id_producto = data['id_producto']
    d.porcentaje_descuento = data['porcentaje_descuento']
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento actualizado."}

def eliminar_descuento_producto(id_descuento):
    d = DescuentoProducto.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}
    db.session.delete(d)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento eliminado."}

### --------- USUARIO ---------

def crear_descuento_usuario(data):
    descuento = DescuentoUsuario(**data)
    db.session.add(descuento)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento creado para usuario."}

def obtener_descuentos_usuario():
    descuentos = DescuentoUsuario.query.all()
    return {"OK": True, "RESPUESTA": [d.__dict__ for d in descuentos]}

def actualizar_descuento_usuario(id_descuento, data):
    d = DescuentoUsuario.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}
    d.id_usuario = data['id_usuario']
    d.id_producto = data['id_producto']
    d.porcentaje_descuento = data['porcentaje_descuento']
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento actualizado."}

def eliminar_descuento_usuario(id_descuento):
    d = DescuentoUsuario.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}
    db.session.delete(d)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento eliminado."}

### --------- TEMPORADA ---------

### --------- TEMPORADA ---------

def crear_descuento_temporada(data):
    # data debe incluir: id_categoria, id_marca, id_temporada, porcentaje_descuento
    descuento = DescuentoTemporada(
        id_categoria         = data['id_categoria'],
        id_marca             = data['id_marca'],
        id_temporada         = data['id_temporada'],
        porcentaje_descuento = data['porcentaje_descuento']
    )
    db.session.add(descuento)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento de temporada creado."}

def obtener_descuentos_temporada():
    descuentos = DescuentoTemporada.query.all()
    respuesta = []
    for d in descuentos:
        respuesta.append({
            "id_descuento_temporada": d.id_descuento_temporada,
            "id_categoria": d.id_categoria,
            "id_marca": d.id_marca,
            "id_temporada": d.id_temporada,
            "porcentaje_descuento": float(d.porcentaje_descuento)
        })
    return {"OK": True, "RESPUESTA": respuesta}

def actualizar_descuento_temporada(id_descuento, data):
    d = DescuentoTemporada.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}

    # actualizar todos los campos, incluido id_temporada
    d.id_categoria         = data.get('id_categoria', d.id_categoria)
    d.id_marca             = data.get('id_marca', d.id_marca)
    d.id_temporada         = data.get('id_temporada', d.id_temporada)
    d.porcentaje_descuento = data.get('porcentaje_descuento', d.porcentaje_descuento)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento de temporada actualizado."}

def eliminar_descuento_temporada(id_descuento):
    d = DescuentoTemporada.query.get(id_descuento)
    if not d:
        return {"OK": False, "DESCRIPCION": "Descuento no encontrado."}
    db.session.delete(d)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Descuento de temporada eliminado."}


def listar_descuentos_usuario(auth_header):
    id_usuario = int(g.user.get("sub"))

    # 1) Consultar desconto exclusivo en user-service
    resp = verificar_descuento_usuario(id_usuario, auth_header)
    if not resp.get("OK"):
        return {"OK": False, "DESCRIPCION": "Error al verificar descuento exclusivo.", "RESPUESTA": {}}

    exclusivo_info = resp["RESPUESTA"]
    # 2) Si existe y expiró (>30 días), inactivar
    if exclusivo_info.get("descuento_exclusivo"):
        fecha_ini = datetime.fromisoformat(exclusivo_info["fecha_inicio_descuento"]).date()
        if (datetime.today().date() - fecha_ini).days > 30:
            inactivar_descuento_usuario(id_usuario, auth_header)
            exclusivo_info = {"descuento_exclusivo": False, "fecha_inicio_descuento": None}

    # 3) Listar descuentos de usuario con id_producto (automáticos)
    user_discounts = DescuentoUsuario.query.filter(
        DescuentoUsuario.id_usuario == id_usuario,
        DescuentoUsuario.id_producto.isnot(None)
    ).all()

    lista = [{
        "id_descuento": int(d.id_descuento),
        "id_producto": int(d.id_producto),
        "porcentaje_descuento": float(d.porcentaje_descuento)
    } for d in user_discounts]

    return {
        "OK": True,
        "DESCRIPCION": "Descuentos de usuario obtenidos.",
        "RESPUESTA": {
            "descuentos_por_producto": lista,
            "descuento_exclusivo": exclusivo_info.get("descuento_exclusivo", False),
            "fecha_inicio_descuento": exclusivo_info.get("fecha_inicio_descuento")
        }
    }