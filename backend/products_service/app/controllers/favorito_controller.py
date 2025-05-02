from app.models.favorito import Favorito
from app.models.producto import Producto
from app.models.imagen_producto import ImagenProducto
from flask import request
from sqlalchemy import asc, desc, or_
from app.config import db

def agregar_a_favoritos(id_usuario, id_producto):
    if not Producto.query.get(id_producto):
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}

    ya_fav = Favorito.query.filter_by(id_usuario=id_usuario, id_producto=id_producto).first()
    if ya_fav:
        return {"OK": False, "DESCRIPCION": "Producto ya está en favoritos.", "RESPUESTA": {}}

    favorito = Favorito(id_usuario=id_usuario, id_producto=id_producto)
    db.session.add(favorito)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto agregado a favoritos.", "RESPUESTA": {}}

def quitar_de_favoritos(id_usuario, id_producto):
    favorito = Favorito.query.filter_by(id_usuario=id_usuario, id_producto=id_producto).first()
    if not favorito:
        return {"OK": False, "DESCRIPCION": "Producto no está en favoritos.", "RESPUESTA": {}}

    db.session.delete(favorito)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto eliminado de favoritos.", "RESPUESTA": {}}


def obtener_favoritos_dashboard(id_usuario):
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    sort_by = request.args.get("sort_by", "id_producto")
    sort_dir = request.args.get("sort_dir", "asc")
    search = request.args.get("search", "")

    columnas_validas = {
        "id_producto": Producto.id_producto,
        "nombre": Producto.nombre,
        "precio": Producto.precio,
        "valor": Producto.valor,
    }

    sort_column = columnas_validas.get(sort_by.lower(), Producto.id_producto)
    orden = asc(sort_column) if sort_dir.lower() == "asc" else desc(sort_column)

    ids_favoritos = [f.id_producto for f in Favorito.query.filter_by(id_usuario=id_usuario).all()]
    query = Producto.query.filter(Producto.id_producto.in_(ids_favoritos))

    if search:
        query = query.filter(
            or_(
                Producto.nombre.ilike(f"%{search}%"),
                Producto.codigo.ilike(f"%{search}%"),
                Producto.descripcion.ilike(f"%{search}%")
            )
        )

    total = query.count()
    productos = query.order_by(orden).offset(page * size).limit(size).all()

    datos = []
    for p in productos:
        imagen_destacada = ImagenProducto.query.filter_by(id_producto=p.id_producto).first()
        datos.append({
            "id_producto": p.id_producto,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "valor": float(p.valor),
            "disponibilidad": p.disponibilidad,
            "imagen": imagen_destacada.imagen if imagen_destacada else None
        })

    return {
        "OK": True,
        "DESCRIPCION": "Favoritos obtenidos correctamente.",
        "RESPUESTA": {
            "total": total,
            "pagina": page,
            "tamanio": size,
            "productos": datos
        }
    }