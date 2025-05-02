from flask import Blueprint, request, jsonify
from app.controllers.descuentos_controller import *
from app.utils.jwt_generator import token_required, admin_required

descuentos_bp = Blueprint("descuentos", __name__, url_prefix="/descuentos")

# --------- PRODUCTO ---------
@descuentos_bp.route('/producto', methods=['POST'])
@token_required
@admin_required
def crear_descuento_prod():
    return jsonify(crear_descuento_producto(request.get_json()))

@descuentos_bp.route('/producto', methods=['GET'])
@token_required
@admin_required
def obtener_descuentos_prod():
    return jsonify(obtener_descuentos_producto())

@descuentos_bp.route('/producto/<int:id_descuento>', methods=['PUT'])
@token_required
@admin_required
def actualizar_descuento_prod(id_descuento):
    return jsonify(actualizar_descuento_producto(id_descuento, request.get_json()))

@descuentos_bp.route('/producto/<int:id_descuento>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_descuento_prod(id_descuento):
    return jsonify(eliminar_descuento_producto(id_descuento))


# --------- USUARIO ---------
@descuentos_bp.route('/usuario', methods=['POST'])
@token_required
@admin_required
def crear_descuento_usr():
    return jsonify(crear_descuento_usuario(request.get_json()))

@descuentos_bp.route('/usuario', methods=['GET'])
@token_required
@admin_required
def obtener_descuentos_usr():
    return jsonify(obtener_descuentos_usuario())

@descuentos_bp.route('/usuario/<int:id_descuento>', methods=['PUT'])
@token_required
@admin_required
def actualizar_descuento_usr(id_descuento):
    return jsonify(actualizar_descuento_usuario(id_descuento, request.get_json()))

@descuentos_bp.route('/usuario/<int:id_descuento>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_descuento_usr(id_descuento):
    return jsonify(eliminar_descuento_usuario(id_descuento))


# --------- TEMPORADA ---------
@descuentos_bp.route('/temporada', methods=['POST'])
@token_required
@admin_required
def crear_descuento_temp():
    return jsonify(crear_descuento_temporada(request.get_json()))

@descuentos_bp.route('/temporada', methods=['GET'])
@token_required
@admin_required
def obtener_descuentos_temp():
    return jsonify(obtener_descuentos_temporada())

@descuentos_bp.route('/temporada/<int:id_descuento>', methods=['PUT'])
@token_required
@admin_required
def actualizar_descuento_temp(id_descuento):
    return jsonify(actualizar_descuento_temporada(id_descuento, request.get_json()))

@descuentos_bp.route('/temporada/<int:id_descuento>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_descuento_temp(id_descuento):
    return jsonify(eliminar_descuento_temporada(id_descuento))



@descuentos_bp.route('/usuario/me', methods=['GET'])
@token_required
def obtener_descuentos_mios():
    auth_header = request.headers.get("Authorization")
    resultado = listar_descuentos_usuario(auth_header)
    status = 200 if resultado.get("OK") else 400
    return jsonify(resultado), status
