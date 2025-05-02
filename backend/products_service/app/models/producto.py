from app.config import db

class Producto(db.Model):
    __tablename__ = "productos"
    id_producto = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria_producto.id_categoria"))
    precio = db.Column(db.Numeric(10,2), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    disponibilidad = db.Column(db.Integer)
    codigo = db.Column(db.String(100))
    valor = db.Column(db.Numeric(10,2))
    ventas = db.Column(db.Integer, default=0)
    calificacion = db.Column(db.Numeric(3,2))
    fecha_de_carga = db.Column(db.Date)
