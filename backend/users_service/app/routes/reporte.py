from flask import Blueprint, request, jsonify
from app.controllers.reporte_controller import *
from app.utils.jwt_generator import token_required, admin_required

reporte_bp = Blueprint("reporte", __name__)

@reporte_bp.route('/report/<int:id_usuario>', methods=['POST'])
@token_required
@admin_required
def crear_reporte(id_usuario):
    data = request.get_json()
    resultado = crear_reporte_usuario(id_usuario, data)
    return jsonify(resultado), 201 if resultado["OK"] else 400

@reporte_bp.route('/report/<int:id_reporte>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_reporte(id_reporte):
    resultado = eliminar_reporte_usuario(id_reporte)
    return jsonify(resultado), 200 if resultado["OK"] else 404

@reporte_bp.route('/report/<int:id_reporte>', methods=['PUT'])
@token_required
@admin_required
def actualizar_reporte(id_reporte):
    data = request.get_json()
    resultado = actualizar_reporte_usuario(id_reporte, data)
    return jsonify(resultado), 200 if resultado["OK"] else 400

@reporte_bp.route('/report/<int:id_usuario>', methods=['GET'])
@token_required
@admin_required
def obtener_reportes(id_usuario):
    resultado = obtener_reportes_usuario(id_usuario)
    return jsonify(resultado), 200
