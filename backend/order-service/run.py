from app.routes.carrito import carrito_bp
from app.routes.descuentos import descuentos_bp
from flask import Flask
from flask_restful import Api
from app.config import init_db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

init_db(app)
app.register_blueprint(carrito_bp, url_prefix="/orders")
app.register_blueprint(descuentos_bp, url_prefix="/orders")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
