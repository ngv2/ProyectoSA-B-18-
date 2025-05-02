from flask import Blueprint, request, jsonify
from app.controllers.imagen_controller import actualizar_imagenes_producto
from app.utils.jwt_generator import token_required, admin_required

imagen_producto_bp = Blueprint("imagen_producto", __name__)

@imagen_producto_bp.route('/<int:id_producto>/images', methods=['PUT'])
@token_required
@admin_required
def actualizar_imagenes(id_producto):
    data = request.get_json()
    return jsonify(actualizar_imagenes_producto(id_producto, data.get("imagenes", [])))
