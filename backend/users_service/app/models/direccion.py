from app.config import db

class Direccion(db.Model):
    __tablename__ = 'direcciones'

    id_direccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    otras_senas = db.Column(db.Text)
    id_departamento = db.Column(db.Integer, nullable=False)
    id_ciudad = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
