from flask import Blueprint, request, jsonify
from app.controllers.usuario_controller import *

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json()
    resultado = crear_usuario(data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@usuario_bp.route("/confirmation", methods=["PATCH"])
def confirmar():
    token = request.args.get("token")
    if not token:
        return jsonify({"OK": False, "DESCRIPCION": "Token requerido", "RESPUESTA": {}}), 400

    resultado = confirmar_usuario_por_token(token)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    resultado = login_usuario(data)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@usuario_bp.route("/pass-recover", methods=["POST"])
def pass_recover():
    usuario_input = request.args.get("usuario")
    resultado = solicitar_recuperacion_contrasena(usuario_input)
    return jsonify(resultado), 200 if resultado["OK"] else 400


@usuario_bp.route("/pass-recover", methods=["PUT"])
def put_pass_recover():
    token = request.args.get("token")
    data = request.get_json()

    if not token:
        return jsonify({"OK": False, "DESCRIPCION": "Falta el token en la URL.", "RESPUESTA": {}}), 400

    if not data or "contrasena" not in data:
        return jsonify({"OK": False, "DESCRIPCION": "Debe proporcionar una nueva contraseña.", "RESPUESTA": {}}), 400

    resultado = restablecer_contrasena(token, data["contrasena"])
    status_code = 200 if resultado["OK"] else 400
    return jsonify(resultado), status_code
