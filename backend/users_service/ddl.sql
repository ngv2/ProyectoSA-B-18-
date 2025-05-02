create database users_db;

use users_db;
-- Tabla: usuarios
CREATE TABLE usuarios (
  id_usuario               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre                   VARCHAR(100)  NOT NULL,
  apellido                 VARCHAR(100)  NOT NULL,
  correo_electronico       VARCHAR(150)  NOT NULL,
  username                 VARCHAR(100)  NOT NULL,
  telefono                 VARCHAR(20),
  fecha_nacimiento         DATE,
  sexo                     ENUM('masculino', 'femenino'),
  foto                     TEXT,
  contrasena               VARCHAR(255)  NOT NULL,

  -- Gestión de confirmación de cuenta
  token_confirmacion       VARCHAR(255),
  token_confirmacion_expira DATETIME,

  -- Gestión de recuperación de contraseña
  token_recuperacion       VARCHAR(255),
  token_recuperacion_expira DATETIME,

  estado                   ENUM('activo', 'inactivo') DEFAULT 'inactivo',
  tipo                     ENUM('user', 'admin')      DEFAULT 'user',

  total_compra             INT UNSIGNED DEFAULT 0,
  descuento_exclusivo      BOOLEAN      DEFAULT FALSE,
  fecha_inicio_descuento   DATE,

  /* === Índices y restricciones === */
  UNIQUE KEY uq_correo_electronico  (correo_electronico),
  UNIQUE KEY uq_username            (username),
  UNIQUE KEY uq_token_confirmacion  (token_confirmacion),
  UNIQUE KEY uq_token_recuperacion  (token_recuperacion)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


-- Tabla: departamentos
CREATE TABLE departamentos (
  id_departamento INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT
);

-- Tabla: ciudades
CREATE TABLE ciudades (
  id_ciudad INT AUTO_INCREMENT PRIMARY KEY,
  id_departamento INT NOT NULL,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT,
  FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tabla: direcciones
CREATE TABLE direcciones (
  id_direccion INT AUTO_INCREMENT PRIMARY KEY,
  otras_senas TEXT,
  id_departamento INT NOT NULL,
  id_ciudad INT NOT NULL,
  id_usuario INT UNSIGNED NOT NULL,
  FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tabla: reporte_usuario (corregida)
CREATE TABLE reporte_usuario (
  id_reporte INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT UNSIGNED NOT NULL,
  descripcion TEXT NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
