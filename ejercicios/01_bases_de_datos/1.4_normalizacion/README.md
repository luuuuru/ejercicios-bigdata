# 📝 Ejercicio 1.4: Normalización y Diseño de Esquemas

## 🎯 Objetivos de Aprendizaje

- ✅ Comprender las Formas Normales (1NF, 2NF, 3NF, BCNF)
- ✅ Identificar problemas de diseño en esquemas
- ✅ Normalizar tablas desnormalizadas
- ✅ Crear diagramas Entidad-Relación (ER)
- ✅ Diseñar esquemas desde requisitos de negocio
- ✅ Evaluar trade-offs entre normalización y performance

---

## 📚 Contenido Teórico

### Formas Normales

**1NF (Primera Forma Normal):**
- Valores atómicos (no listas en columnas)
- Cada columna tiene un solo valor
- Cada fila es única (tiene PK)

**2NF (Segunda Forma Normal):**
- Cumple 1NF
- No hay dependencias parciales de la clave
- Cada columna no-clave depende de TODA la PK

**3NF (Tercera Forma Normal):**
- Cumple 2NF
- No hay dependencias transitivas
- Columnas no-clave NO dependen de otras columnas no-clave

**BCNF (Boyce-Codd Normal Form):**
- Versión más estricta de 3NF
- Cada determinante debe ser clave candidata

---

## 📋 Ejercicios Prácticos

### Parte 1: Identificar Violaciones

Se te proporciona una tabla desnormalizada de una biblioteca:

```sql
CREATE TABLE prestamos_desnormalizado (
    prestamo_id INTEGER,
    fecha_prestamo DATE,
    usuario_id INTEGER,
    nombre_usuario TEXT,
    email_usuario TEXT,
    libro_id INTEGER,
    titulo_libro TEXT,
    autor_libro TEXT,
    isbn TEXT,
    editorial TEXT,
    ciudad_editorial TEXT,
    pais_editorial TEXT
);
```

**Tarea:**
1. Identifica qué forma normal viola
2. Lista todas las dependencias funcionales
3. Diseña un esquema normalizado (3NF)
4. Crea diagrama ER del nuevo diseño

---

### Parte 2: Normalizar Base de Datos Real

Dada esta tabla de ventas:

```sql
CREATE TABLE ventas (
    venta_id INTEGER,
    fecha DATE,
    vendedor_nombre TEXT,
    vendedor_email TEXT,
    vendedor_comision REAL,
    cliente_nombre TEXT,
    cliente_direccion TEXT,
    producto_nombre TEXT,
    producto_categoria TEXT,
    producto_fabricante TEXT,
    cantidad INTEGER,
    precio_unitario REAL,
    descuento REAL
);
```

**Tareas:**
1. Normaliza a 3NF
2. Crea script SQL con las nuevas tablas
3. Escribe query que migra datos del modelo antiguo al nuevo
4. Compara ventajas/desventajas

---

### Parte 3: Diseño Desde Cero

**Requisitos de negocio:**

Una universidad necesita sistema para:
- Gestionar estudiantes (nombre, email, carrera)
- Gestionar profesores (nombre, email, departamento)
- Gestionar cursos (nombre, código, créditos)
- Registrar inscripciones (estudiante → curso)
- Cada curso es impartido por UN profesor
- Un estudiante puede tomar múltiples cursos
- Un profesor puede impartir múltiples cursos

**Tarea:**
1. Diseña esquema completo en 3NF
2. Crea diagrama ER (ASCII y Mermaid)
3. Escribe script SQL CREATE TABLE
4. Inserta datos de ejemplo (5 estudiantes, 3 profesores, 4 cursos)
5. Escribe 5 consultas útiles

---

### Parte 4: Desnormalización Intencional

**Escenario:**
Tienes una aplicación de reportes que consulta ventas constantemente:

```sql
-- Esta query se ejecuta 1000 veces por minuto
SELECT
    v.fecha,
    c.nombre AS cliente,
    p.nombre AS producto,
    v.cantidad,
    v.total
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha >= '2024-01-01';
```

**Tarea:**
1. Diseña tabla desnormalizada para optimizar esta query
2. Explica cómo mantener sincronización con tablas normalizadas
3. Evalúa cuándo vale la pena desnormalizar

---

## 📦 Entregables

1. `normalizacion_parte1.md` - Análisis de violaciones
2. `normalizacion_parte2.sql` - Script de migración
3. `diseno_universidad.sql` - Diseño completo
4. `diagramas/` - Carpeta con diagramas ER
5. `reflexion_desnormalizacion.md` - Análisis de trade-offs

---

## 🎓 Nivel: Intermedio-Avanzado

**Creado:** 2025-12-11
