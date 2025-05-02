from app.models.categoria_producto import CategoriaProducto
from app.models.marca import Marca

def obtener_categorias():
    categorias = CategoriaProducto.query.all()
    datos = [{
        "id_categoria": c.id_categoria,
        "nombre": c.nombre,
        "descripcion": c.descripcion
    } for c in categorias]
    return {
        "OK": True,
        "DESCRIPCION": "Categorías obtenidas correctamente.",
        "RESPUESTA": datos
    }

def obtener_marcas():
    marcas = Marca.query.all()
    datos = [{
        "id_marca": m.id_marca,
        "marca": m.marca,
        "fabricante": m.fabricante,
        "descripcion": m.descripcion
    } for m in marcas]
    return {
        "OK": True,
        "DESCRIPCION": "Marcas obtenidas correctamente.",
        "RESPUESTA": datos
    }
