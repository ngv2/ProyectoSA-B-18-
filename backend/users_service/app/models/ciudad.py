from app.config import db

class Ciudad(db.Model):
    __tablename__ = 'ciudades'

    id_ciudad = db.Column(db.Integer, primary_key=True)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamentos.id_departamento', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
