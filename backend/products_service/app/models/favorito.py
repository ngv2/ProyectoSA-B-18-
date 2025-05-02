from sqlalchemy import Column, Integer, ForeignKey
from app.config import db

class Favorito(db.Model):
    __tablename__ = 'favoritos'
    id_favoritos = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
