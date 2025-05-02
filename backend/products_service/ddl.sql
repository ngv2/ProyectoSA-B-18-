-- Tabla: categoria_producto
CREATE TABLE categoria_producto (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) UNIQUE NOT NULL,
  descripcion TEXT
);

-- Tabla: productos
CREATE TABLE productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  id_categoria INT,
  precio DECIMAL(10,2) NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  disponibilidad INT,
  codigo VARCHAR(100),
  valor DECIMAL(10,2),
  ventas INT DEFAULT 0,
  calificacion DECIMAL(3,2),
  fecha_de_carga DATE,
  FOREIGN KEY (id_categoria) REFERENCES categoria_producto(id_categoria)
);

-- Tabla: marcas
CREATE TABLE marcas (
  id_marca INT AUTO_INCREMENT PRIMARY KEY,
  marca VARCHAR(100),
  fabricante VARCHAR(100),
  descripcion TEXT
);

-- Tabla: marca_producto
CREATE TABLE marca_producto (
  id_marca_producto INT AUTO_INCREMENT PRIMARY KEY,
  id_marca INT,
  id_producto INT,
  FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
  FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

-- Tabla: imagen_producto
CREATE TABLE imagen_producto (
  id_imagen_producto INT AUTO_INCREMENT PRIMARY KEY,
  imagen TEXT NOT NULL,
  descripcion TEXT,
  id_producto INT,
  FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

-- Tabla: favoritos
CREATE TABLE favoritos (
  id_favoritos INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_producto INT,
  FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
