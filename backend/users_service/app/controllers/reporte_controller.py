from app.models.reporte import Reporte
from app.models.usuario import Usuario
from app.config import db

def crear_reporte_usuario(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}
    
    if not data.get("descripcion"):
        return {"OK": False, "DESCRIPCION": "Debe proporcionar una descripción para el reporte.", "RESPUESTA": {}}

    try:
        nuevo = Reporte(
            id_usuario=id_usuario,
            descripcion=data["descripcion"],
            fecha=data.get("fecha")  # opcional, puede generarse automáticamente si lo deseas
        )
        db.session.add(nuevo)
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Reporte creado exitosamente.", "RESPUESTA": {"id_reporte": nuevo.id_reporte}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al crear el reporte.", "RESPUESTA": {"error": str(e)}}

def eliminar_reporte_usuario(id_reporte):
    reporte = Reporte.query.get(id_reporte)
    if not reporte:
        return {"OK": False, "DESCRIPCION": "Reporte no encontrado.", "RESPUESTA": {}}
    try:
        db.session.delete(reporte)
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Reporte eliminado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al eliminar el reporte.", "RESPUESTA": {"error": str(e)}}

def actualizar_reporte_usuario(id_reporte, data):
    reporte = Reporte.query.get(id_reporte)
    if not reporte:
        return {"OK": False, "DESCRIPCION": "Reporte no encontrado.", "RESPUESTA": {}}

    if not data.get("descripcion"):
        return {"OK": False, "DESCRIPCION": "Debe proporcionar una nueva descripción.", "RESPUESTA": {}}
    
    try:
        reporte.descripcion = data["descripcion"]
        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Reporte actualizado correctamente.", "RESPUESTA": {}}
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar el reporte.", "RESPUESTA": {"error": str(e)}}

def obtener_reportes_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"OK": False, "DESCRIPCION": "Usuario no encontrado.", "RESPUESTA": {}}

    reportes = Reporte.query.filter_by(id_usuario=id_usuario).all()
    data = [{
        "id_reporte": r.id_reporte,
        "descripcion": r.descripcion,
        "fecha": str(r.fecha)
    } for r in reportes]

    return {"OK": True, "DESCRIPCION": "Reportes obtenidos correctamente.", "RESPUESTA": data}
