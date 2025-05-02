from app.models.producto import Producto
from app.models.marca import Marca
from app.models.marca_producto import MarcaProducto
from app.config import db

def actualizar_marcas_producto(id_producto, nuevas_marcas):
    producto = Producto.query.get(id_producto)
    if not producto:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}

    if not isinstance(nuevas_marcas, list) or len(nuevas_marcas) == 0:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar al menos una marca.", "RESPUESTA": {}}
    
    try:
        # Eliminar marcas anteriores
        MarcaProducto.query.filter_by(id_producto=id_producto).delete()

        # Agregar nuevas marcas
        for id_marca in nuevas_marcas:
            if not Marca.query.get(id_marca):
                return {"OK": False, "DESCRIPCION": f"No se encontraron algunas marcas.", "RESPUESTA": {}}
            nueva_relacion = MarcaProducto(id_producto=id_producto, id_marca=id_marca)
            db.session.add(nueva_relacion)

        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Marcas actualizadas correctamente.", "RESPUESTA": {}}
    
    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al actualizar marcas del producto.", "RESPUESTA": {"error": str(e)}}
