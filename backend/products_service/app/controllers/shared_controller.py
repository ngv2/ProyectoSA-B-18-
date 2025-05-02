from app.models.producto import Producto
from app.config import db

def actualizar_ventas_producto(id_producto, cantidad_vendida):
    producto = Producto.query.get(id_producto)
    if not producto:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}
    
    if not isinstance(cantidad_vendida, int) or cantidad_vendida <= 0:
        return {"OK": False, "DESCRIPCION": "Cantidad vendida debe ser un número entero positivo.", "RESPUESTA": {}}

    producto.ventas += cantidad_vendida
    db.session.commit()
    return {
        "OK": True,
        "DESCRIPCION": "Ventas actualizadas correctamente.",
        "RESPUESTA": {
            "id_producto": producto.id_producto,
            "ventas_totales": producto.ventas
        }
    }
