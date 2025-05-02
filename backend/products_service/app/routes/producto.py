from flask import Blueprint, request, jsonify
from app.controllers.producto_controller import (
    crear_producto,
    obtener_productos_dashboard,
    obtener_producto_por_id,
    actualizar_producto,
    eliminar_producto
)
from app.utils.jwt_generator import token_required, admin_required

producto_bp = Blueprint("producto", __name__)

@producto_bp.route('/', methods=['POST'])
@token_required
@admin_required
def crear_producto_route():
    data = request.get_json()
    return jsonify(crear_producto(data))

@producto_bp.route('/', methods=['GET'])
@token_required
@admin_required
def obtener_productos_route():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    sort_by = request.args.get("sort_by", "id_producto")
    sort_dir = request.args.get("sort_dir", "asc")
    search = request.args.get("search", "")
    return jsonify(obtener_productos_dashboard(page, size, sort_by, sort_dir, search))

@producto_bp.route('/<int:id_producto>', methods=['GET'])
@token_required
def obtener_producto_route(id_producto):
    return jsonify(obtener_producto_por_id(id_producto))

@producto_bp.route('/<int:id_producto>', methods=['PUT'])
@token_required
@admin_required
def actualizar_producto_route(id_producto):
    data = request.get_json()
    return jsonify(actualizar_producto(id_producto, data))

@producto_bp.route('/<int:id_producto>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_producto_route(id_producto):
    return jsonify(eliminar_producto(id_producto))
