from flask import Blueprint, jsonify
from app.controllers.categoria_controller import obtener_categorias, obtener_marcas

categoria_bp = Blueprint("categoria", __name__)

@categoria_bp.route('/categorias', methods=['GET'])
def get_categorias():
    return jsonify(obtener_categorias())

@categoria_bp.route('/marcas', methods=['GET'])
def get_marcas():
    return jsonify(obtener_marcas())
