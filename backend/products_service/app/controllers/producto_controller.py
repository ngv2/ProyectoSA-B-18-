from app.models.categoria_producto import CategoriaProducto
from app.models.producto import Producto
from app.models.marca import Marca
from app.models.marca_producto import MarcaProducto
from app.models.imagen_producto import ImagenProducto
from app.models.favorito import Favorito
from sqlalchemy import asc, desc, or_
from app.config import db

def validar_unicidad_producto(nombre, id_categoria, codigo, valor, id_excluir=None):
    query = Producto.query.filter_by(nombre=nombre, id_categoria=id_categoria, codigo=codigo, valor=valor)
    if id_excluir:
        query = query.filter(Producto.id_producto != id_excluir)
    return query.first()


def crear_producto(data):
    # Validar unicidad
    if validar_unicidad_producto(data['nombre'], data['id_categoria'], data['codigo'], data['valor']):
        return {"OK": False, "DESCRIPCION": "Ya existe un producto con el mismo nombre, categoría, código y valor.", "RESPUESTA": {}}
    
    # Validar marcas e imágenes
    if 'marcas' not in data or not isinstance(data['marcas'], list) or len(data['marcas']) == 0:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar al menos una marca para el producto.", "RESPUESTA": {}}
    
    if 'imagenes' not in data or not isinstance(data['imagenes'], list) or len(data['imagenes']) == 0:
        return {"OK": False, "DESCRIPCION": "Debe proporcionar al menos una imagen para el producto.", "RESPUESTA": {}}
    
    try:
        nuevo = Producto(
            nombre=data['nombre'],
            id_categoria=data['id_categoria'],
            precio=data['precio'],
            descripcion=data.get('descripcion'),
            disponibilidad=data.get('disponibilidad', 0),
            codigo=data['codigo'],
            valor=data['valor'],
            ventas=0,
            calificacion=data.get('calificacion'),
            fecha_de_carga=data.get('fecha_de_carga')
        )
        db.session.add(nuevo)
        db.session.flush() 
        

        for id_marca in data['marcas']:
            db.session.add(MarcaProducto(id_producto=nuevo.id_producto, id_marca=id_marca))

        for imagen in data['imagenes']:
            db.session.add(ImagenProducto(id_producto=nuevo.id_producto, imagen=imagen['imagen'], descripcion=imagen.get('descripcion', '')))

        db.session.commit()
        return {"OK": True, "DESCRIPCION": "Producto creado exitosamente.", "RESPUESTA": {"id_producto": nuevo.id_producto}}

    except Exception as e:
        db.session.rollback()
        return {"OK": False, "DESCRIPCION": "Error al crear producto.", "RESPUESTA": {"error": str(e)}}
    

def obtener_productos_dashboard(page, size, sort_by, sort_dir, search):
    columnas_validas = {
        "id_producto": Producto.id_producto,
        "nombre": Producto.nombre,
        "precio": Producto.precio,
        "valor": Producto.valor,
    }

    sort_column = columnas_validas.get(sort_by.lower(), Producto.id_producto)
    orden = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    query = Producto.query

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
        "DESCRIPCION": "Productos obtenidos correctamente.",
        "RESPUESTA": {
            "total": total,
            "pagina": page,
            "tamanio": size,
            "productos": datos
        }
    }


def obtener_producto_por_id(id_producto):
    producto = Producto.query.get(id_producto)
    if not producto:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}
    
    imagenes = ImagenProducto.query.filter_by(id_producto=id_producto).all()
    marcas_rel = MarcaProducto.query.filter_by(id_producto=id_producto).all()
    marcas = [Marca.query.get(m.id_marca).marca for m in marcas_rel]

    data = {
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "categoria": producto.id_categoria,
        "descripcion": producto.descripcion,
        "codigo": producto.codigo,
        "valor": float(producto.valor),
        "disponibilidad": producto.disponibilidad,
        "fecha_de_carga": str(producto.fecha_de_carga),
        "imagenes": [{"imagen": img.imagen, "descripcion": img.descripcion} for img in imagenes],
        "marcas": marcas
    }

    return {"OK": True, "DESCRIPCION": "Producto obtenido.", "RESPUESTA": data}




def actualizar_producto(id_producto, data):
    producto = Producto.query.get(id_producto)
    if not producto:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}
    
    if validar_unicidad_producto(data['nombre'], data['id_categoria'], data['codigo'], data['valor'], id_excluir=id_producto):
        return {"OK": False, "DESCRIPCION": "Otro producto con los mismos datos ya existe.", "RESPUESTA": {}}
    
    producto.nombre = data['nombre']
    producto.id_categoria = data['id_categoria']
    producto.precio = data['precio']
    producto.descripcion = data.get('descripcion')
    producto.codigo = data['codigo']
    producto.valor = data['valor']
    producto.disponibilidad = data.get('disponibilidad', producto.disponibilidad)
    producto.fecha_de_carga = data.get('fecha_de_carga', producto.fecha_de_carga)

    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto actualizado correctamente.", "RESPUESTA": {}}

def eliminar_producto(id_producto):
    producto = Producto.query.get(id_producto)
    if not producto:
        return {"OK": False, "DESCRIPCION": "Producto no encontrado.", "RESPUESTA": {}}
    db.session.delete(producto)
    db.session.commit()
    return {"OK": True, "DESCRIPCION": "Producto eliminado correctamente.", "RESPUESTA": {}}
