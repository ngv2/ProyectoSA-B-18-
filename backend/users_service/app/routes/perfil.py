from flask import Blueprint, request, jsonify, g
from app.controllers.perfil_controller import *
from app.utils.jwt_generator import token_required, admin_required

perfil_bp = Blueprint("perfil", __name__)

@perfil_bp.route('/profile', methods=['PUT'])
@token_required
def actualizar_perfil():
    data = request.get_json()
    id_usuario = int(g.user.get("sub"))
    resultado = actualizar_perfil_usuario(id_usuario, data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@perfil_bp.route('/address', methods=['POST'])
@token_required
def crear_direccion():
    id_usuario = int(g.user.get("sub"))
    data = request.get_json()
    resultado = crear_direccion_usuario_autenticado(id_usuario, data)
    return jsonify(resultado), 201 if resultado["OK"] else 400


@perfil_bp.route('/address/<int:id_direccion>', methods=['PUT'])
@token_required
def actualizar_direccion(id_direccion):
    data = request.get_json()
    resultado = actualizar_direccion_usuario(id_direccion, g.user, data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@perfil_bp.route('/address/<int:id_direccion>', methods=['DELETE'])
@token_required
def eliminar_direccion(id_direccion):
    resultado = eliminar_direccion_usuario(id_direccion, g.user)
    return jsonify(resultado), 200 if resultado["OK"] else 400
