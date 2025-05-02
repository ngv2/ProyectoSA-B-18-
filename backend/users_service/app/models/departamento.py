from app.config import db

class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id_departamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
