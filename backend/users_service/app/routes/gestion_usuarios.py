from flask import Blueprint, request, jsonify, g
from app.controllers.gestion_usuarios_controller import *
from app.utils.jwt_generator import token_required, admin_required

gestion_usuarios_bp = Blueprint("gestion_usuarios", __name__)


@gestion_usuarios_bp.route('/new', methods=['POST'])
@token_required
@admin_required
def crear_usuario():
    data = request.get_json()
    resultado = crear_usuario_admin(data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@gestion_usuarios_bp.route('/<int:id_usuario>', methods=['PUT'])
@token_required
@admin_required
def actualizar_usuario(id_usuario):
    data = request.get_json()
    resultado = actualizar_usuario_por_id(id_usuario, data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@gestion_usuarios_bp.route('/<int:id_usuario>', methods=['DELETE'])
@token_required
@admin_required
def inactivar_usuario(id_usuario):
    resultado = inactivar_usuario_por_id(id_usuario)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@gestion_usuarios_bp.route('/<int:id_usuario>', methods=['PATCH'])
@token_required
@admin_required
def reactivar_usuario(id_usuario):
    resultado = reactivar_usuario_por_id(id_usuario)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@gestion_usuarios_bp.route('/', methods=['GET'])
@token_required
@admin_required
def obtener_usuarios_dashboard_route():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    sort_by = request.args.get("sortBy", "id_usuario")
    sort_dir = request.args.get("sortDir", "asc")
    search = request.args.get("search", "")
    resultado = obtener_usuarios_dashboard(page, size, sort_by, sort_dir, search)
    return jsonify(resultado), 200


@gestion_usuarios_bp.route('/<int:id_usuario>', methods=['GET'])
@token_required
def obtener_usuario_por_id(id_usuario):

    usuario_actual = g.user
    if usuario_actual.get("tipo") != "admin" and int(usuario_actual.get("sub")) != id_usuario:
        return jsonify({
            "OK": False,
            "DESCRIPCION": "Permisos insuficientes para acceder a esta información.",
            "RESPUESTA": {}
        }), 403

    resultado = obtener_usuario_con_direcciones(id_usuario)
    return jsonify(resultado), 200 if resultado["OK"] else 404

@gestion_usuarios_bp.route('/address/<int:id_usuario>', methods=['POST'])
@token_required
@admin_required
def crear_direccion_para_usuario(id_usuario):
    data = request.get_json()
    resultado = crear_direccion_usuario(id_usuario, data)
    return jsonify(resultado), 201 if resultado["OK"] else 400



