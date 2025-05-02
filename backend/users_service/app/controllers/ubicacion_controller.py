from app.models.departamento import Departamento
from app.models.ciudad import Ciudad

def obtener_departamentos():
    departamentos = Departamento.query.all()
    datos = [{"id_departamento": d.id_departamento, "nombre": d.nombre, "descripcion": d.descripcion} for d in departamentos]
    return {"OK": True, "DESCRIPCION": "Departamentos obtenidos correctamente.", "RESPUESTA": datos}

def obtener_ciudades_por_departamento(id_departamento):
    ciudades = Ciudad.query.filter_by(id_departamento=id_departamento).all()
    if not ciudades:
        return {"OK": False, "DESCRIPCION": "No se encontraron ciudades para el departamento.", "RESPUESTA": []}
    datos = [{"id_ciudad": c.id_ciudad, "nombre": c.nombre, "descripcion": c.descripcion} for c in ciudades]
    return {"OK": True, "DESCRIPCION": "Ciudades obtenidas correctamente.", "RESPUESTA": datos}
