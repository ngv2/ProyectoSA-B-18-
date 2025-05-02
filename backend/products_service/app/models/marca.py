from sqlalchemy import Column, Integer, String, Text
from app.config import db

class Marca(db.Model):
    __tablename__ = 'marcas'
    id_marca = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(100))
    fabricante = Column(String(100))
    descripcion = Column(Text)
