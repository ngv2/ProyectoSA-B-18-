from flask import Blueprint, request, jsonify
from app.controllers.shared_controller import actualizar_ventas_producto
from app.utils.jwt_generator import token_required, admin_required

shared_bp = Blueprint("shared", __name__)

@shared_bp.route('/ventas/<int:id_producto>', methods=['PUT'])
@token_required
@admin_required
def actualizar_ventas(id_producto):
    data = request.get_json()
    cantidad = data.get("cantidad_vendida")

    if cantidad is None:
        return jsonify({
            "OK": False,
            "DESCRIPCION": "Se requiere el campo 'cantidad_vendida'.",
            "RESPUESTA": {}
        }), 400

    return jsonify(actualizar_ventas_producto(id_producto, cantidad))
