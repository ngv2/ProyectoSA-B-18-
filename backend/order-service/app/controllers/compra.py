# app/controllers/checkout_controller.py

from flask import Blueprint, request, jsonify, g
from datetime import datetime, date
from app.config import db
from app.models.checkout import *
from app.models.carrito import *
from app.models.descuentos import *
from app.models.detalle_carrito import *
from app.utils.jwt_generator import token_required
from app.utils.api_helper import (
    get_product_by_id,
    verificar_descuento_usuario,
    inactivar_descuento_usuario
)

checkout_bp = Blueprint("checkout", __name__, url_prefix="/order")

def calcular_descuento_exclusivo(total_compra):
    if 10000 <= total_compra <= 12999:
        return 5.0
    elif 13000 <= total_compra <= 16999:
        return 10.0
    elif total_compra >= 17000:
        return 20.0
    return 0.0

@checkout_bp.route('/checkout', methods=['GET'])
@token_required
def get_checkout():
    id_usuario = int(g.user.get("sub"))
    uso_exclusivo = request.args.get("descuento_exclusivo", "0") == "1"
    id_descuento_usuario = request.args.get("descuento_usuario", type=int)
    auth_header = request.headers.get("Authorization")

    # 1) Obtener carrito
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if not carrito:
        return jsonify({"OK": True, "DESCRIPCION": "Carrito vacío", "RESPUESTA": {"productos": [], "total": 0}})

    detalles = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).all()
    if not detalles:
        return jsonify({"OK": True, "DESCRIPCION": "Carrito vacío", "RESPUESTA": {"productos": [], "total": 0}})

    hoy = date.today()

    # 2) Cargar descuentos de temporada
    temporada = Temporada.query.filter(Temporada.fecha_inicio <= hoy, Temporada.fecha_fin >= hoy).first()
    temp_map = {}
    if temporada:
        for d in DescuentoTemporada.query.all():
            temp_map[(d.id_categoria, d.id_marca)] = float(d.porcentaje_descuento)

    # 3) Descuentos por producto
    prod_map = {d.id_producto: float(d.porcentaje_descuento) for d in DescuentoProducto.query.all()}

    # 4) Descuentos por usuario
    user_discs = DescuentoUsuario.query.filter_by(id_usuario=id_usuario).all()
    user_prod_map = {d.id_producto: float(d.porcentaje_descuento) for d in user_discs if d.id_producto}
    total_user_map = {d.id_descuento: float(d.porcentaje_descuento) for d in user_discs if not d.id_producto}
    descuento_usuario_total = total_user_map.get(id_descuento_usuario, 0.0)

    # 5) Validar descuento exclusivo
    if uso_exclusivo:
        ver = verificar_descuento_usuario(id_usuario, auth_header)
        if not ver.get("OK") or not ver["RESPUESTA"].get("descuento_exclusivo"):
            return jsonify({"OK": False, "DESCRIPCION": "Descuento exclusivo no disponible.", "RESPUESTA": {}}), 400
        fecha_ini = datetime.fromisoformat(ver["RESPUESTA"]["fecha_inicio_descuento"]).date()
        if (hoy - fecha_ini).days > 30:
            inactivar_descuento_usuario(id_usuario)
            return jsonify({"OK": False, "DESCRIPCION": "Descuento exclusivo expirado.", "RESPUESTA": {}}), 400

    # 6) Construir listado y calcular subtotal
    productos_out = []
    total = 0.0

    for item in detalles:
        prod_json = get_product_by_id(item.id_producto)
        precio = float(prod_json["precio"])
        cantidad = item.cantidad
        subtotal = precio * cantidad

        descuento = 0.0
        if not uso_exclusivo:
            descuento += prod_map.get(item.id_producto, 0.0)
            descuento += user_prod_map.get(item.id_producto, 0.0)
            for m in prod_json.get("marcas", []):
                key = (prod_json["id_categoria"], m["id_marca"])
                if key in temp_map:
                    descuento += temp_map[key]

        total_line = subtotal * (1 - descuento / 100)
        productos_out.append({
            "id_producto": item.id_producto,
            "nombre": prod_json["nombre"],
            "precio_unitario": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
            "descuento_aplicado": descuento,
            "total_con_descuento": round(total_line, 2)
        })
        total += total_line

    # 7) Aplicar descuento por usuario total
    if not uso_exclusivo and descuento_usuario_total:
        total *= (1 - descuento_usuario_total / 100)

    # 8) Aplicar descuento exclusivo sobre total acumulado
    if uso_exclusivo:
        total_compra_acum = g.user.get("total_compra", 0)
        perc = calcular_descuento_exclusivo(total_compra_acum)
        total *= (1 - perc / 100)

    # 9) Preparar lista de descuentos globales disponibles
    disponibles = [{"id_descuento": k, "porcentaje": v} for k, v in total_user_map.items()]

    return jsonify({
        "OK": True,
        "DESCRIPCION": "Checkout obtenido correctamente.",
        "RESPUESTA": {
            "productos": productos_out,
            "total": round(total, 2),
            "descuento_exclusivo_aplicado": uso_exclusivo,
            "descuento_usuario_total_aplicado": descuento_usuario_total,
            "descuentos_disponibles": disponibles
        }
    })
