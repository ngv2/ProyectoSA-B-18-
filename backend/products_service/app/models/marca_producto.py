from sqlalchemy import Column, Integer, ForeignKey
from app.config import db

class MarcaProducto(db.Model):
    __tablename__ = 'marca_producto'
    id_marca_producto = Column(Integer, primary_key=True, autoincrement=True)
    id_marca = Column(Integer, ForeignKey('marcas.id_marca'))
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
