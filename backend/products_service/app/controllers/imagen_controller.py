from app.models.imagen_producto import ImagenProducto
from app.config import db

def actualizar_imagenes_producto(id_producto, imagenes):
    if not isinstance(imagenes, list) or len(imagenes) == 0:
        return {"OK": False, "DESCRIPCION": "Debe enviar una lista de imágenes.", "RESPUESTA": {}}

    try:
        # Eliminar imágenes anteriores
        ImagenProducto.query.filter_by(id_producto=id_producto).delete()

        # Agregar nuevas imágenes
        for img in imagenes:
            nueva = ImagenProducto(
                id_producto=id_producto,
                imagen=img.get("imagen"),
                descripcion=img.get("descripcion", "")
            )
            db.session.add(nueva)

        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Imágenes actualizadas correctamente.", "RESPUESTA": {}}
    
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar imágenes.", "RESPUESTA": {"error": str(e)}}
