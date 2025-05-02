from flask import Blueprint
from app.controllers.catalogos_controller import *

catalogo_bp = Blueprint("catalogo", __name__)

@catalogo_bp.route("/catalogo/mas-vendidos", methods=["GET"])
def catalogo_vendidos(): return catalogo_mas_vendidos()

@catalogo_bp.route("/catalogo/ofertas", methods=["GET"])
def catalogo_ofertas_(): return catalogo_ofertas()

@catalogo_bp.route("/catalogo/categoria/<int:id_categoria>", methods=["GET"])
def catalogo_categoria(id_categoria): return catalogo_por_categoria(id_categoria)

@catalogo_bp.route("/catalogo/calificacion", methods=["GET"])
def catalogo_calificacion(): return catalogo_por_calificacion()

@catalogo_bp.route("/catalogo/nuevos", methods=["GET"])
def catalogo_nuevos_(): return catalogo_nuevos()

@catalogo_bp.route("/catalogo/rango", methods=["GET"])
def catalogo_rango():
    min_ = float(request.args.get("min", 0))
    max_ = float(request.args.get("max", 999999))
    return catalogo_por_rango(min_, max_)

@catalogo_bp.route("/catalogo/marca/<int:id_marca>", methods=["GET"])
def catalogo_marca(id_marca): return catalogo_por_marca(id_marca)
