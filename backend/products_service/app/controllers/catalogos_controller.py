from flask import request
from sqlalchemy import desc, asc
from app.models.producto import Producto
from app.models.imagen_producto import ImagenProducto
from app.config import db

def obtener_catalogo_base(query, page, size):
    total = query.count()
    productos = query.offset(page * size).limit(size).all()

    respuesta = []
    for p in productos:
        img = ImagenProducto.query.filter_by(id_producto=p.id_producto).first()
        respuesta.append({
            "id_producto": p.id_producto,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "valor": float(p.valor),
            "ventas": p.ventas,
            "calificacion": float(p.calificacion or 0),
            "imagen": img.imagen if img else None
        })

    return {
        "OK": True,
        "DESCRIPCION": "Productos obtenidos.",
        "RESPUESTA": {
            "total": total,
            "pagina": page,
            "tamanio": size,
            "productos": respuesta
        }
    }

def catalogo_mas_vendidos():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.order_by(desc(Producto.ventas))
    return obtener_catalogo_base(query, page, size)

def catalogo_ofertas():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.filter(Producto.valor < Producto.precio)
    return obtener_catalogo_base(query, page, size)

def catalogo_por_categoria(id_categoria):
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.filter_by(id_categoria=id_categoria)
    return obtener_catalogo_base(query, page, size)

def catalogo_por_calificacion():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.order_by(desc(Producto.calificacion))
    return obtener_catalogo_base(query, page, size)

def catalogo_nuevos():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.order_by(desc(Producto.fecha_de_carga))
    return obtener_catalogo_base(query, page, size)

def catalogo_por_rango(precio_min, precio_max):
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    query = Producto.query.filter(Producto.precio.between(precio_min, precio_max))
    return obtener_catalogo_base(query, page, size)

def catalogo_por_marca(id_marca):
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    from app.models.marca_producto import MarcaProducto
    productos_ids = db.session.query(MarcaProducto.id_producto).filter_by(id_marca=id_marca)
    query = Producto.query.filter(Producto.id_producto.in_(productos_ids))
    return obtener_catalogo_base(query, page, size)


