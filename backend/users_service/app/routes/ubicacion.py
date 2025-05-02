from flask import Blueprint, jsonify
from app.controllers.ubicacion_controller import obtener_departamentos, obtener_ciudades_por_departamento

ubicacion_bp = Blueprint("ubicacion", __name__)

@ubicacion_bp.route('/departments', methods=['GET'])
def get_departamentos():
    return jsonify(obtener_departamentos())

@ubicacion_bp.route('/departments/<int:id_departamento>/cities', methods=['GET'])
def get_ciudades(id_departamento):
    return jsonify(obtener_ciudades_por_departamento(id_departamento))
