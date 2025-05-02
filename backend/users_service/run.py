from app.routes.usuario import usuario_bp
from app.routes.gestion_usuarios import gestion_usuarios_bp
from app.routes.reporte import reporte_bp
from app.routes.ubicacion import ubicacion_bp
from app.routes.perfil import perfil_bp
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
app.register_blueprint(usuario_bp, url_prefix="/users")
app.register_blueprint(gestion_usuarios_bp, url_prefix="/users")
app.register_blueprint(reporte_bp, url_prefix="/users")
app.register_blueprint(perfil_bp, url_prefix="/users")
app.register_blueprint(ubicacion_bp, url_prefix="/users")
app.register_blueprint(shared_bp, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
