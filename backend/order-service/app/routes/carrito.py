from flask import Blueprint, jsonify, request, g
from app.utils.jwt_generator import token_required
from app.controllers.carrito_controller import (
    obtener_carrito_usuario,
    agregar_producto_carrito,
    eliminar_producto_carrito,
    vaciar_carrito
)

carrito_bp = Blueprint("carrito", __name__, url_prefix="/carrito")

@carrito_bp.route('/', methods=['GET'])
@token_required
def obtener():
    id_usuario = int(g.user.get("sub"))
    return jsonify(obtener_carrito_usuario(id_usuario))

@carrito_bp.route('/<int:id_producto>', methods=['POST'])
@token_required
def agregar(id_producto):
    id_usuario = int(g.user.get("sub"))
    data = request.get_json()
    cantidad = data.get("cantidad", 1)
    return jsonify(agregar_producto_carrito(id_usuario, id_producto, cantidad))

@carrito_bp.route('/<int:id_producto>', methods=['DELETE'])
@token_required
def eliminar(id_producto):
    id_usuario = int(g.user.get("sub"))
    return jsonify(eliminar_producto_carrito(id_usuario, id_producto))

@carrito_bp.route('/vaciar', methods=['DELETE'])
@token_required
def vaciar():
    id_usuario = int(g.user.get("sub"))
    return jsonify(vaciar_carrito(id_usuario))
