from app.config import db
from datetime import datetime

class Reporte(db.Model):
    __tablename__ = "reporte_usuario"

    id_reporte = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref=db.backref("reportes", lazy=True))
