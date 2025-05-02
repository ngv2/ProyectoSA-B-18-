from app.routes.producto import producto_bp
from app.routes.catalogos import catalogo_bp
from app.routes.favoritos import favorito_bp
from app.routes.imagenes import imagen_producto_bp
from app.routes.marcas import asignacion_marcas_bp
from app.routes.categoria import categoria_bp
from app.routes.shared import shared_bp
from flask import Flask
from flask_restful import Api
from app.config import init_db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

init_db(app)
app.register_blueprint(producto_bp, url_prefix="/products")
app.register_blueprint(catalogo_bp, url_prefix="/products")
app.register_blueprint(favorito_bp, url_prefix="/products")
app.register_blueprint(imagen_producto_bp, url_prefix="/products")
app.register_blueprint(asignacion_marcas_bp, url_prefix="/products")
app.register_blueprint(categoria_bp, url_prefix="/products")
app.register_blueprint(shared_bp, url_prefix="/products")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
