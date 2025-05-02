from sqlalchemy import Column, Integer, String, Text
from app.config import db

class CategoriaProducto(db.Model):
    __tablename__ = 'categoria_producto'
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
