from app.models.carrito import Carrito
from app.models.detalle_carrito import DetalleCarrito
from app.config import db

def obtener_carrito_usuario(id_usuario):
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if not carrito:
        return {"OK": True, "DESCRIPCION": "Carrito vacío.", "RESPUESTA": []}
    
    detalles = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).all()
    data = [{
        "id_detalle_carrito": d.id_detalle_carrito,
        "id_producto": d.id_producto,
        "cantidad": d.cantidad
    } for d in detalles]

    return {"OK": True, "DESCRIPCION": "Carrito obtenido correctamente.", "RESPUESTA": data}

def agregar_producto_carrito(id_usuario, id_producto, cantidad):
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if not carrito:
        carrito = Carrito(id_usuario=id_usuario)
        db.session.add(carrito)
        db.session.flush()  # Obtener id_carrito

    detalle = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito, id_producto=id_producto).first()
    if detalle:
        detalle.cantidad += cantidad
    else:
        detalle = DetalleCarrito(id_carrito=carrito.id_carrito, id_producto=id_producto, cantidad=cantidad)
        db.session.add(detalle)

    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto agregado al carrito.", "RESPUESTA": {}}

def eliminar_producto_carrito(id_usuario, id_producto):
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if not carrito:
        return {"OK": False, "DESCRIPCION": "Carrito no encontrado.", "RESPUESTA": {}}

    detalle = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito, id_producto=id_producto).first()
    if not detalle:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado en el carrito.", "RESPUESTA": {}}

    db.session.delete(detalle)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto eliminado del carrito.", "RESPUESTA": {}}

def vaciar_carrito(id_usuario):
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if not carrito:
        return {"OK": False, "DESCRIPCION": "Carrito no encontrado.", "RESPUESTA": {}}

    DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).delete()
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Carrito vaciado exitosamente.", "RESPUESTA": {}}
