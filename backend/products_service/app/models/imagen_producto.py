from sqlalchemy import Column, Integer, Text, ForeignKey
from app.config import db

class ImagenProducto(db.Model):
    __tablename__ = 'imagen_producto'
    id_imagen_producto = Column(Integer, primary_key=True, autoincrement=True)
    imagen = Column(Text, nullable=False)
    descripcion = Column(Text)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
