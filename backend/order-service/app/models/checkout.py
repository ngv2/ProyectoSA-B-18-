from app.config import db

class Compra(db.Model):
    __tablename__ = 'compras'
    id_compra = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_direccion = db.Column(db.Integer, nullable=False)
    calificacion = db.Column(db.Integer)
    fecha_compra = db.Column(db.Date)
    descuento = db.Column(db.Integer)
    total = db.Column(db.Numeric(10, 2))


class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compras'
    id_detalle_compra = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer, nullable=False)
    descuento = db.Column(db.Integer)
    precio = db.Column(db.Numeric(10, 2))
    cantidad = db.Column(db.Integer)
