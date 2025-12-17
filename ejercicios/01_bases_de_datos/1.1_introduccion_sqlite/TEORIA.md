# 📖 Teoría: Introducción a SQLite y Bases de Datos Relacionales

## 🎯 Objetivos de este Material

Al terminar de leer esta guía entenderás:
- Qué es una base de datos y para qué sirve
- Qué es SQLite y cuándo usarlo
- Conceptos fundamentales: tablas, filas, columnas, claves
- Diferencia entre datos normalizados y desnormalizados
- Cómo Python interactúa con SQLite

---

## 📊 ¿Qué es una Base de Datos?

### Definición Simple
Una **base de datos** es un sistema organizado para almacenar, gestionar y recuperar información de manera eficiente.

### Analogía
Piensa en una base de datos como una **biblioteca**:
- **Libros** = Datos
- **Estanterías organizadas** = Tablas estructuradas
- **Sistema de catálogo** = Índices y claves
- **Bibliotecario** = Sistema gestor (DBMS)

### ¿Por qué NO usar solo archivos CSV?

| Característica | Archivos CSV | Base de Datos |
|----------------|--------------|---------------|
| **Velocidad búsqueda** | Lenta (lee todo) | Rápida (índices) |
| **Múltiples usuarios** | Problemas de bloqueo | Concurrencia |
| **Integridad** | No hay validación | Constraints, FK |
| **Relaciones** | Difícil | Nativo con JOINs |
| **Tamaño** | Limitado por RAM | GB/TB en disco |
| **Queries complejas** | Requiere código | SQL directo |

**Ejemplo:**
```
❌ CSV: Para buscar todos los productos de "AMD" → leer todo el archivo
✅ BD:  SELECT * FROM productos WHERE fabricante = 'AMD' → usa índice, ultra rápido
```

---

## 🗄️ ¿Qué es SQLite?

### Definición
**SQLite** es un motor de base de datos relacional **embebido**, sin servidor, que guarda toda la BD en un solo archivo.

### Características Clave

#### ✅ Ventajas:
- **Zero-configuration:** No requiere instalación de servidor
- **Portátil:** Un archivo = toda la base de datos
- **Ligero:** ~600KB de librería
- **Rápido:** Para reads, especialmente
- **Gratis:** Dominio público
- **Incluido en Python:** Módulo `sqlite3` built-in

#### ❌ Limitaciones:
- **No es para alta concurrencia:** Bloquea la BD en escrituras
- **No es distribuido:** Una máquina, un archivo
- **Sin usuarios/permisos:** A nivel de BD
- **Limitaciones de tipos:** Solo 5 tipos de datos

### SQLite vs Otros DBMS

```
SQLite        →  Archivo local, app embebida
PostgreSQL    →  Servidor robusto, alta concurrencia
MySQL         →  Servidor web-oriented
MongoDB       →  NoSQL, documentos JSON
Cassandra     →  NoSQL, distribuido, Big Data
```

---

## 🏗️ Conceptos Fundamentales

### Tabla (Table)
Estructura bidimensional: filas y columnas.

**Analogía:** Una hoja de Excel.

```
tabla: productos
┌────┬─────────────────┬─────────┬──────────┐
│ id │ nombre          │ precio  │ categoria│
├────┼─────────────────┼─────────┼──────────┤
│ 1  │ AMD Ryzen 7     │ 389.00  │ CPU      │
│ 2  │ Intel i7-13700K │ 364.99  │ CPU      │
│ 3  │ Corsair 16GB    │ 41.99   │ RAM      │
└────┴─────────────────┴─────────┴──────────┘
```

---

### Fila (Row / Record / Tupla)
Un registro individual. Una entidad.

**Ejemplo:** La fila `id=1` representa un producto específico: AMD Ryzen 7.

---

### Columna (Column / Attribute)
Un atributo de la entidad.

**Ejemplo:** `precio` es un atributo que todos los productos tienen.

---

### Clave Primaria (Primary Key - PK)
Identificador **único** de cada fila.

**Reglas:**
- ✅ Debe ser única
- ✅ No puede ser NULL
- ✅ No debe cambiar

**Ejemplos buenos:**
- `id` auto-incremental (1, 2, 3...)
- `email` en tabla de usuarios
- `isbn` en tabla de libros

**Ejemplos malos:**
- `nombre` (puede haber duplicados)
- `precio` (muchos productos al mismo precio)

---

### Clave Foránea (Foreign Key - FK)
Referencia a la PK de **otra tabla**. Establece relaciones.

**Ejemplo:**
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
```

**¿Qué hace?**
- Asegura que `categoria_id` existe en la tabla `categorias`
- Previene "categorías huérfanas"
- Permite hacer JOIN entre tablas

---

## 🔗 Relaciones entre Tablas

### 1. Uno a Muchos (1:N)
La más común. Un registro de tabla A se relaciona con varios de tabla B.

**Ejemplo: Categoría → Productos**
```
categorias               productos
┌────┬──────┐            ┌────┬───────────┬──────────────┐
│ id │nombre│            │ id │  nombre   │categoria_id  │
├────┼──────┤            ├────┼───────────┼──────────────┤
│ 1  │ CPU  │◄───────────│ 1  │ AMD R7    │ 1            │
│ 2  │ RAM  │            │ 2  │ Intel i7  │ 1            │
└────┴──────┘            │ 3  │ Corsair   │ 2            │
                         └────┴───────────┴──────────────┘

Una categoría → muchos productos
Un producto  → una categoría
```

---

### 2. Muchos a Muchos (N:M)
Un registro de A se relaciona con varios de B, y viceversa.

**Ejemplo: Productos ↔ Colores**

Un producto puede tener múltiples colores (negro, rojo).
Un color puede estar en múltiples productos.

**Solución:** Tabla intermedia

```
productos              productos_colores           colores
┌────┬────────┐        ┌────────────┬─────────┐   ┌────┬───────┐
│ id │ nombre │        │producto_id │color_id │   │ id │nombre │
├────┼────────┤        ├────────────┼─────────┤   ├────┼───────┤
│ 1  │ Mouse X│◄───────│ 1          │ 1       │───►│ 1  │ Black │
└────┴────────┘        │ 1          │ 2       │   │ 2  │ White │
                       │ 2          │ 1       │   │ 3  │ Red   │
                       └────────────┴─────────┘   └────┴───────┘

Mouse X tiene colores Black y White
Black está en Mouse X y Mouse Y
```

---

### 3. Uno a Uno (1:1)
Poco común. Un registro de A con exactamente uno de B.

**Ejemplo: Producto → Inventario**
```
productos               inventario
┌────┬────────┐         ┌────────────┬──────┐
│ id │ nombre │         │producto_id │stock │
├────┼────────┤         ├────────────┼──────┤
│ 1  │ AMD R7 │◄────────│ 1          │ 50   │
│ 2  │ Intel  │◄────────│ 2          │ 30   │
└────┴────────┘         └────────────┴──────┘
```

---

## 📐 Normalización vs Desnormalización

### Desnormalización (Modelo A)
**Datos duplicados** para simplificar queries.

**Ejemplo:**
```
tabla: productos
┌────┬─────────────┬─────────┬───────────────┬─────────┐
│ id │ nombre      │ precio  │ fabricante    │ categoria│
├────┼─────────────┼─────────┼───────────────┼─────────┤
│ 1  │ AMD Ryzen 7 │ 389.00  │ AMD           │ CPU     │
│ 2  │ AMD Ryzen 5 │ 245.00  │ AMD           │ CPU     │
│ 3  │ Intel i7    │ 364.99  │ Intel         │ CPU     │
└────┴─────────────┴─────────┴───────────────┴─────────┘

Problema: "AMD" se repite. Si queremos cambiar a "Advanced Micro Devices"
         → hay que UPDATE en múltiples filas.
```

**Ventajas:**
- ✅ Queries simples (un solo SELECT)
- ✅ Rápido en lecturas
- ✅ Fácil de entender

**Desventajas:**
- ❌ Duplicación de datos
- ❌ Inconsistencias (AMD vs amd vs A.M.D.)
- ❌ Desperdicio de espacio
- ❌ Actualizaciones complejas

---

### Normalización (Modelo B)
**Eliminar redundancia** dividiendo en múltiples tablas relacionadas.

**Ejemplo:**
```
fabricantes                   productos
┌────┬────────┐               ┌────┬─────────────┬──────────────┐
│ id │ nombre │               │ id │ nombre      │fabricante_id │
├────┼────────┤               ├────┼─────────────┼──────────────┤
│ 1  │ AMD    │◄──────────────│ 1  │ Ryzen 7     │ 1            │
│ 2  │ Intel  │               │ 2  │ Ryzen 5     │ 1            │
└────┴────────┘               │ 3  │ i7-13700K   │ 2            │
                              └────┴─────────────┴──────────────┘

Ahora "AMD" está en UN solo lugar.
Para cambiar el nombre → un solo UPDATE en tabla fabricantes.
```

**Ventajas:**
- ✅ Sin duplicación
- ✅ Integridad de datos
- ✅ Actualizaciones fáciles
- ✅ Ahorro de espacio

**Desventajas:**
- ❌ Queries más complejas (requieren JOIN)
- ❌ Menor velocidad en reads (múltiples tablas)
- ❌ Curva de aprendizaje

---

## 🔢 Formas Normales (Básico)

### Primera Forma Normal (1NF)
**Regla:** Cada columna contiene **valores atómicos** (no listas).

**❌ Violación 1NF:**
```
┌────┬─────────┬────────────────┐
│ id │ nombre  │ colores        │
├────┼─────────┼────────────────┤
│ 1  │ Mouse X │ Black, White   │  ← Lista en un campo
└────┴─────────┴────────────────┘
```

**✅ 1NF correcta:**
```
productos_colores
┌────────────┬─────────┐
│producto_id │color_id │
├────────────┼─────────┤
│ 1          │ 1       │
│ 1          │ 2       │
└────────────┴─────────┘
```

---

### Segunda Forma Normal (2NF)
**Regla:** 1NF + cada columna depende de **toda** la PK (no de parte).

**❌ Violación 2NF:**
```
PK compuesta: (producto_id, color_id)
┌────────────┬─────────┬──────────────┐
│producto_id │color_id │nombre_color  │  ← Depende solo de color_id
├────────────┼─────────┼──────────────┤
│ 1          │ 1       │ Black        │
└────────────┴─────────┴──────────────┘
```

**✅ 2NF correcta:**
Separar en dos tablas.

---

### Tercera Forma Normal (3NF)
**Regla:** 2NF + no hay dependencias transitivas.

**❌ Violación 3NF:**
```
┌────┬─────────┬──────────────┬──────────┐
│ id │ nombre  │fabricante_id │ pais_fab │  ← pais depende de fabricante
├────┼─────────┼──────────────┼──────────┤
│ 1  │ Ryzen 7 │ 1            │ USA      │
└────┴─────────┴──────────────┴──────────┘
```

**✅ 3NF correcta:**
```
productos                fabricantes
┌────┬─────────┬────┐    ┌────┬──────┬──────┐
│ id │ nombre  │fab │    │ id │nombre│ pais │
├────┼─────────┼────┤    ├────┼──────┼──────┤
│ 1  │ Ryzen 7 │ 1  │◄───│ 1  │ AMD  │ USA  │
└────┴─────────┴────┘    └────┴──────┴──────┘
```

---

## 🐍 Python + SQLite

### Método 1: Módulo `sqlite3` Nativo

```python
import sqlite3

# 1. Conectar (crea el archivo si no existe)
conn = sqlite3.connect('mi_bd.db')
cursor = conn.cursor()

# 2. Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL CHECK(precio > 0)
    )
''')

# 3. Insertar datos
cursor.execute('''
    INSERT INTO productos (nombre, precio)
    VALUES (?, ?)
''', ('AMD Ryzen 7', 389.00))

# 4. Commit (guardar cambios)
conn.commit()

# 5. Consultar
cursor.execute('SELECT * FROM productos')
for row in cursor.fetchall():
    print(row)

# 6. Cerrar
conn.close()
```

**Ventajas:**
- ✅ Control total
- ✅ Sin dependencias externas
- ✅ Educativo

**Desventajas:**
- ❌ Más verboso
- ❌ SQL como strings

---

### Método 2: Pandas + `to_sql()`

```python
import pandas as pd
import sqlite3

# 1. Leer CSV
df = pd.read_csv('productos.csv')

# 2. Conectar a BD
conn = sqlite3.connect('mi_bd.db')

# 3. Cargar DataFrame completo a tabla
df.to_sql('productos', conn, if_exists='replace', index=False)

# 4. Leer desde BD a DataFrame
df_from_db = pd.read_sql_query('SELECT * FROM productos', conn)

conn.close()
```

**Ventajas:**
- ✅ Muy rápido para cargas masivas
- ✅ Sintaxis simple
- ✅ Ideal para análisis exploratorio

**Desventajas:**
- ❌ Menos control sobre tipos de datos
- ❌ No ideal para relaciones complejas

---

### Método 3: SQLAlchemy (ORM)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Integer)

# Motor
engine = create_engine('sqlite:///mi_bd.db')
Base.metadata.create_all(engine)

# Sesión
Session = sessionmaker(bind=engine)
session = Session()

# Insertar
producto = Producto(nombre='AMD Ryzen 7', precio=389)
session.add(producto)
session.commit()

# Consultar
productos = session.query(Producto).all()
```

**Ventajas:**
- ✅ Orientado a objetos
- ✅ Portable (cambiar de BD es fácil)
- ✅ Muy usado en producción

**Desventajas:**
- ❌ Curva de aprendizaje alta
- ❌ Overhead de abstracción

---

## 🎯 ¿Cuándo Usar Cada Modelo?

### Modelo A (Desnormalizado)
**Úsalo cuando:**
- Prototipado rápido
- Análisis de datos (Data Science)
- No hay escrituras frecuentes
- Datos de solo lectura

**Ejemplo:** Dashboard de análisis de catálogo

---

### Modelo B (Normalizado)
**Úsalo cuando:**
- Aplicaciones CRUD (Create, Read, Update, Delete)
- Múltiples usuarios modificando datos
- Integridad de datos es crítica
- Base de datos relativa pequeña/mediana

**Ejemplo:** Sistema de gestión interna

---

### Modelo C (E-Commerce Completo)
**Úsalo cuando:**
- Sistema de producción
- Transacciones complejas
- Historial de eventos
- Análisis de negocio

**Ejemplo:** Tienda online, ERP

---

## 📊 Comparación Visual

```
COMPLEJIDAD:
    Simple ────────────────────────────────► Compleja
    │                  │                  │
    Modelo A          Modelo B          Modelo C

VELOCIDAD LECTURA:
    Alta ──────────────────────────────────► Baja
    │                  │                  │
    Modelo A          Modelo B          Modelo C

INTEGRIDAD DATOS:
    Baja ──────────────────────────────────► Alta
    │                  │                  │
    Modelo A          Modelo B          Modelo C

MANTENIMIENTO:
    Difícil ───────────────────────────────► Fácil
    │                  │                  │
    Modelo A          Modelo B          Modelo C
```

---

## 🚫 Errores Comunes

### 1. No usar Primary Keys
```sql
-- ❌ Mal
CREATE TABLE productos (
    nombre TEXT,
    precio REAL
);

-- ✅ Bien
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio REAL
);
```

---

### 2. No validar con Constraints
```sql
-- ❌ Mal
precio REAL

-- ✅ Bien
precio REAL NOT NULL CHECK(precio > 0)
```

---

### 3. Olvidar Índices en FKs
```sql
-- ❌ Mal
CREATE TABLE productos (
    ...
    categoria_id INTEGER
);

-- ✅ Bien
CREATE TABLE productos (
    ...
    categoria_id INTEGER
);
CREATE INDEX idx_categoria ON productos(categoria_id);
```

---

### 4. No hacer Commit
```python
cursor.execute("INSERT ...")
# ❌ Olvidaste conn.commit()
conn.close()  # Los datos se pierden!

# ✅ Bien
cursor.execute("INSERT ...")
conn.commit()
conn.close()
```

---

## 📚 Recursos Adicionales

### Documentación Oficial:
- [SQLite Official](https://www.sqlite.org/docs.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Pandas to_sql](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html)

### Tutoriales Recomendados:
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [W3Schools SQL](https://www.w3schools.com/sql/)

### Herramientas:
- **DB Browser for SQLite** - GUI para explorar bases de datos
- **DBeaver** - Cliente universal de BD
- **PyCharm Database Tools** - Integrado en el IDE

---

## ✅ Checklist de Conceptos

Antes de hacer el ejercicio, asegúrate de entender:

- [ ] Qué es una base de datos relacional
- [ ] Diferencia entre SQLite y otros DBMS
- [ ] Qué es una tabla, fila, columna
- [ ] Qué es Primary Key y Foreign Key
- [ ] Tipos de relaciones (1:N, N:M, 1:1)
- [ ] Diferencia normalización vs desnormalización
- [ ] Cuándo usar cada modelo de datos
- [ ] Cómo conectar Python con SQLite
- [ ] Cómo usar `cursor.execute()` y `conn.commit()`

---

**¡Ahora estás listo para el ejercicio!** 🚀

Vuelve a `README.md` y empieza con el Modelo A.

---

**Creado:** 2025-12-11
**Versión:** 1.0
