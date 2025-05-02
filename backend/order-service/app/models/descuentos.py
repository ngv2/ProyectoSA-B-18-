from app.config import db

class DescuentoProducto(db.Model):
    __tablename__ = 'descuento_producto'
    id_descuento = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    porcentaje_descuento = db.Column(db.Numeric(5,2), nullable=False)

class DescuentoUsuario(db.Model):
    __tablename__ = 'descuento_usuario'
    id_descuento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer)   # puede ser null
    porcentaje_descuento = db.Column(db.Numeric(5,2), nullable=False)

class DescuentoTemporada(db.Model):
    __tablename__ = 'descuento_temporada'
    id_descuento_temporada = db.Column(db.Integer, primary_key=True)
    id_categoria         = db.Column(db.Integer, nullable=False)
    id_marca             = db.Column(db.Integer, nullable=False)
    id_temporada         = db.Column(
        db.Integer,
        db.ForeignKey('temporadas.id_temporada', ondelete='CASCADE'),
        nullable=False
    )
    porcentaje_descuento = db.Column(db.Numeric(5,2), nullable=False)