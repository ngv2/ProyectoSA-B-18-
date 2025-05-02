from app.config import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.Enum('masculino', 'femenino'))
    foto = db.Column(db.Text)
    token_confirmacion = db.Column(db.String(255), unique=True)
    token_confirmacion_expira = db.Column(db.DateTime)
    token_recuperacion = db.Column(db.String(255), unique=True)
    estado = db.Column(db.Enum('activo', 'inactivo'), default='inactivo')
    tipo = db.Column(db.Enum('user', 'admin'), default='user')
    total_compra = db.Column(db.Integer, default=0)
    descuento_exclusivo = db.Column(db.Boolean, default=False)
    fecha_inicio_descuento = db.Column(db.Date)
    contrasena = db.Column(db.String(255), nullable=False)
    token_recuperacion_expira = db.Column(db.DateTime)

