from flask import Blueprint, request, jsonify, g
from app.controllers.favorito_controller import agregar_a_favoritos, quitar_de_favoritos, obtener_favoritos_dashboard
from app.utils.jwt_generator import token_required

favorito_bp = Blueprint("favorito", __name__)

@favorito_bp.route('/favorites/<int:id_producto>', methods=['POST'])
@token_required
def agregar(id_producto):
    id_usuario = int(g.user.get("sub"))
    return jsonify(agregar_a_favoritos(id_usuario, id_producto))

@favorito_bp.route('/favorites/<int:id_producto>', methods=['DELETE'])
@token_required
def quitar(id_producto):
    id_usuario = int(g.user.get("sub"))
    return jsonify(quitar_de_favoritos(id_usuario, id_producto))

@favorito_bp.route('/favorites', methods=['GET'])
@token_required
def obtener():
    id_usuario = int(g.user.get("sub"))
    return jsonify(obtener_favoritos_dashboard(id_usuario))
