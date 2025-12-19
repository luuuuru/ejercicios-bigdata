-- *******************************************************************
-- Script de Creación de la Base de Datos "jardineria"
-- Autor: Juan Marcelo Gutierrez M. (Adaptado para SQL)
-- *******************************************************************

-- 1. Tabla: oficina
CREATE TABLE oficina (
    codigo_oficina VARCHAR(10) PRIMARY KEY,
    ciudad VARCHAR(30) NOT NULL,
    pais VARCHAR(50) NOT NULL,
    region VARCHAR(50),
    codigo_postal VARCHAR(10) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    linea_direccion1 VARCHAR(50) NOT NULL,
    linea_direccion2 VARCHAR(50)
);

-- 2. Tabla: gama_producto
CREATE TABLE gama_producto (
    gama VARCHAR(50) PRIMARY KEY,
    descripcion_texto TEXT,
    descripcion_html TEXT,
    imagen VARCHAR(256)
);

-- 3. Tabla: empleado
CREATE TABLE empleado (
    codigo_empleado INTEGER PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    apellido2 VARCHAR(50),
    extension VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    codigo_oficina VARCHAR(10) NOT NULL,
    codigo_jefe INTEGER,
    puesto VARCHAR(50),
    FOREIGN KEY (codigo_oficina) REFERENCES oficina(codigo_oficina),
    FOREIGN KEY (codigo_jefe) REFERENCES empleado(codigo_empleado)
);

-- 4. Tabla: cliente
CREATE TABLE cliente (
    codigo_cliente INTEGER PRIMARY KEY,
    nombre_cliente VARCHAR(50) NOT NULL,
    nombre_contacto VARCHAR(30),
    apellido_contacto VARCHAR(30),
    telefono VARCHAR(15) NOT NULL,
    fax VARCHAR(15) NOT NULL,
    linea_direccion1 VARCHAR(50) NOT NULL,
    linea_direccion2 VARCHAR(50),
    ciudad VARCHAR(50) NOT NULL,
    region VARCHAR(50),
    pais VARCHAR(50),
    codigo_postal VARCHAR(10),
    codigo_empleado_rep_ventas INTEGER,
    limite_credito NUMERIC(15, 2),
    FOREIGN KEY (codigo_empleado_rep_ventas) REFERENCES empleado(codigo_empleado)
);

-- 5. Tabla: pedido
CREATE TABLE pedido (
    codigo_pedido INTEGER PRIMARY KEY,
    fecha_pedido DATE NOT NULL,
    fecha_esperada DATE NOT NULL,
    fecha_entrega DATE,
    estado VARCHAR(15) NOT NULL, -- Ej. 'Pendiente', 'Entregado', 'Rechazado'
    comentarios TEXT,
    codigo_cliente INTEGER NOT NULL,
    FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente)
);

-- 6. Tabla: producto
CREATE TABLE producto (
    codigo_producto VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    gama VARCHAR(50) NOT NULL,
    dimensiones VARCHAR(25),
    proveedor VARCHAR(50),
    descripcion TEXT,
    cantidad_en_stock SMALLINT NOT NULL,
    precio_venta NUMERIC(15, 2) NOT NULL,
    precio_proveedor NUMERIC(15, 2),
    FOREIGN KEY (gama) REFERENCES gama_producto(gama)
);

-- 7. Tabla: detalle_pedido
CREATE TABLE detalle_pedido (
    codigo_pedido INTEGER NOT NULL,
    codigo_producto VARCHAR(15) NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unidad NUMERIC(15, 2) NOT NULL,
    numero_linea SMALLINT NOT NULL,
    PRIMARY KEY (codigo_pedido, codigo_producto),
    FOREIGN KEY (codigo_pedido) REFERENCES pedido(codigo_pedido),
    FOREIGN KEY (codigo_producto) REFERENCES producto(codigo_producto)
);

-- 8. Tabla: pago
CREATE TABLE pago (
    codigo_cliente INTEGER NOT NULL,
    forma_pago VARCHAR(40) NOT NULL,
    id_transaccion VARCHAR(50) PRIMARY KEY,
    fecha_pago DATE NOT NULL,
    total NUMERIC(15, 2) NOT NULL,
    FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo_cliente)
);

-- *******************************************************************
-- Fin del Script
-- *******************************************************************