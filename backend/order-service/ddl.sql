-- Tabla: restriccion_regional
CREATE TABLE restriccion_regional (
  id_restriccion_regional INT AUTO_INCREMENT PRIMARY KEY,
  id_producto INT NOT NULL,
  id_ciudad INT NOT NULL,
  id_departamento INT NOT NULL
);

-- Tabla: compras
CREATE TABLE compras (
  id_compra INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_direccion INT NOT NULL,
  calificacion INT,
  fecha_compra DATE,
  descuento INT,
  total DECIMAL(10,2)
);

-- Tabla: detalle_compras
CREATE TABLE detalle_compras (
  id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
  id_compra INT NOT NULL,
  id_producto INT NOT NULL,
  descuento INT,
  precio DECIMAL(10,2),
  cantidad INT
);

-- Tabla: carrito
CREATE TABLE carrito (
  id_carrito INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL
);

-- Tabla: detalle_carrito
CREATE TABLE detalle_carrito (
  id_detalle_carrito INT AUTO_INCREMENT PRIMARY KEY,
  id_carrito INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL
);

-- Tabla: temporadas
CREATE TABLE temporadas (
  id_temporada INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) UNIQUE NOT NULL,
  fecha_inicio DATE,
  fecha_fin DATE
);

-- Tabla: descuento_temporada
CREATE TABLE descuento_temporada (
  id_descuento_temporada INT AUTO_INCREMENT PRIMARY KEY,
  id_categoria INT NOT NULL,
  id_marca INT NOT NULL,
  id_temporada INT NOT NULL,
  porcentaje_descuento DECIMAL(5,2),
  FOREIGN KEY (id_temporada) REFERENCES temporadas(id_temporada)
);

-- Tabla: descuento_usuario
CREATE TABLE descuento_usuario (
  id_descuento INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_producto INT,
  porcentaje_descuento DECIMAL(5,2)
);


-- Tabla: descuento_usuario
CREATE TABLE descuento_producto (
  id_descuento INT AUTO_INCREMENT PRIMARY KEY,
  id_producto INT NOT NULL,
  porcentaje_descuento DECIMAL(5,2)
);
