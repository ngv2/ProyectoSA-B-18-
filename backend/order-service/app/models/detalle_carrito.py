from app.config import db

class DetalleCarrito(db.Model):
    __tablename__ = 'detalle_carrito'
    id_detalle_carrito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_carrito = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
