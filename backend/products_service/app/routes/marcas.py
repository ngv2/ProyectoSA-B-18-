from flask import Blueprint, request, jsonify
from app.controllers.marca_controller import actualizar_marcas_producto
from app.utils.jwt_generator import token_required, admin_required

asignacion_marcas_bp = Blueprint("asignacion_marcas", __name__)

@asignacion_marcas_bp.route('/<int:id_producto>/brands', methods=['PUT'])
@token_required
@admin_required
def actualizar_marcas(id_producto):
    data = request.get_json()
    nuevas_marcas = data.get("marcas", [])
    return jsonify(actualizar_marcas_producto(id_producto, nuevas_marcas))
