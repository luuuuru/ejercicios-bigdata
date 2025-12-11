# 📝 Ejercicio 1.2: Consultas SQL Básicas

## 🎯 Objetivos de Aprendizaje

Al completar este ejercicio serás capaz de:

- ✅ Escribir consultas SELECT básicas
- ✅ Filtrar datos con WHERE
- ✅ Ordenar resultados con ORDER BY
- ✅ Limitar resultados con LIMIT
- ✅ Usar operadores de comparación (=, >, <, >=, <=, !=)
- ✅ Usar operadores lógicos (AND, OR, NOT)
- ✅ Buscar patrones con LIKE
- ✅ Filtrar valores nulos con IS NULL / IS NOT NULL
- ✅ Trabajar con rangos usando BETWEEN

---

## 📚 Pre-requisitos

- ✅ Haber completado el Ejercicio 1.1
- ✅ Tener las bases de datos `tienda_modelo_a.db`, `tienda_modelo_b.db`, `tienda_modelo_c.db`
- ✅ DB Browser for SQLite instalado (o herramienta similar)
- ✅ Haber leído el material teórico de SQL básico

---

## 🧩 Contexto del Ejercicio

Usarás las bases de datos creadas en el Ejercicio 1.1 para practicar consultas SQL básicas. El ejercicio está dividido en **3 secciones**, cada una enfocada en una base de datos diferente.

---

## 📋 Enunciado del Ejercicio

Debes completar **20 consultas SQL**, divididas en 3 partes:

### Parte 1: Consultas en Modelo A (8 consultas)
Trabaja con `tienda_modelo_a.db` (tablas desnormalizadas)

### Parte 2: Consultas en Modelo B (8 consultas)
Trabaja con `tienda_modelo_b.db` (tablas normalizadas)

### Parte 3: Consultas en Modelo C (4 consultas)
Trabaja con `tienda_modelo_c.db` (e-commerce completo)

---

## 🔧 Parte 1: Consultas en Modelo A

Abre `tienda_modelo_a.db` y resuelve las siguientes consultas.

### Consulta 1.1: Listar todas las CPUs
**Objetivo:** Practicar SELECT básico

**Requisitos:**
- Muestra: nombre, precio, core_count, core_clock
- Ordena por precio descendente
- Limita a las primeras 10

**Resultado esperado:** 10 filas con las CPUs más caras primero

---

### Consulta 1.2: CPUs de AMD baratas
**Objetivo:** Practicar WHERE con operadores

**Requisitos:**
- Solo CPUs que contengan "AMD" en el nombre
- Precio menor a $200
- Ordena por precio ascendente

**Resultado esperado:** CPUs AMD económicas

---

### Consulta 1.3: Motherboards por socket
**Objetivo:** Practicar filtrado por valores específicos

**Requisitos:**
- Solo motherboards con socket "AM5" o "LGA1700"
- Muestra: nombre, socket, precio, form_factor
- Ordena por socket y luego por precio

**Resultado esperado:** Motherboards agrupadas por socket

---

### Consulta 1.4: Memoria RAM rápida
**Objetivo:** Practicar comparaciones numéricas

**Requisitos:**
- Solo RAM con velocidad que contenga "6000" o superior
- Precio entre $80 y $150
- Ordena por price_per_gb ascendente

**Resultado esperado:** RAM rápida con buena relación precio/GB

---

### Consulta 1.5: Tarjetas gráficas NVIDIA
**Objetivo:** Practicar LIKE

**Requisitos:**
- Solo tarjetas que contengan "NVIDIA" o "GeForce" en el nombre
- Memoria >= 8 GB
- Ordena por memoria descendente, luego por precio

**Resultado esperado:** Tarjetas gráficas NVIDIA potentes

---

### Consulta 1.6: Monitores grandes
**Objetivo:** Practicar operadores y NULL

**Requisitos:**
- Screen size >= 27 pulgadas
- Refresh rate >= 144 Hz
- Excluye monitores sin precio (precio IS NOT NULL)
- Ordena por screen_size descendente

**Resultado esperado:** Monitores gaming

---

### Consulta 1.7: Rangos de precio
**Objetivo:** Practicar BETWEEN

**Requisitos:**
- Busca en tabla `keyboard`
- Precio BETWEEN $50 AND $150
- Ordena por precio
- Muestra: nombre, precio, style, switches (si tiene)

**Resultado esperado:** Teclados de gama media

---

### Consulta 1.8: Productos sin especificar
**Objetivo:** Practicar IS NULL

**Requisitos:**
- Busca en tabla `cpu`
- CPUs donde el campo `graphics` es NULL (no tiene gráficos integrados)
- Muestra: nombre, precio, core_count
- Ordena por precio descendente

**Resultado esperado:** CPUs sin GPU integrada (generalmente los de alto rendimiento)

---

## 🔧 Parte 2: Consultas en Modelo B

Abre `tienda_modelo_b.db` y resuelve las siguientes consultas.

**Nota:** Ahora usarás JOINs básicos. Si aún no los dominas, lee el material de teoría primero.

### Consulta 2.1: Productos por fabricante
**Objetivo:** SELECT simple en tabla normalizada

**Requisitos:**
- Lista todos los productos de fabricante con id = 1
- Muestra: nombre, precio, categoria_id
- Ordena por precio descendente
- Limita a 15 resultados

**Resultado esperado:** Productos de un fabricante específico

---

### Consulta 2.2: Productos de una categoría específica
**Objetivo:** Filtrar por Foreign Key

**Requisitos:**
- Productos de la categoría "CPU" (busca primero el id de la categoría)
- Precio > $100
- Ordena por precio descendente

**Resultado esperado:** CPUs de gama media-alta

---

### Consulta 2.3: Productos con color específico
**Objetivo:** Trabajar con tabla de relación N:M

**Requisitos:**
- Busca el id del color "Black"
- Busca en `productos_colores` los productos con ese color
- Muestra los primeros 20 productos

**Resultado esperado:** Productos en color negro

---

### Consulta 2.4: Fabricantes con productos
**Objetivo:** SELECT simple en tabla maestra

**Requisitos:**
- Lista todos los fabricantes
- Ordena alfabéticamente
- Muestra: id, nombre

**Resultado esperado:** Lista completa de fabricantes

---

### Consulta 2.5: Productos caros
**Objetivo:** Filtrado por precio

**Requisitos:**
- Productos con precio > $500
- Ordena por precio descendente
- Limita a 10

**Resultado esperado:** Top 10 productos más caros

---

### Consulta 2.6: Búsqueda por nombre
**Objetivo:** Practicar LIKE en modelo normalizado

**Requisitos:**
- Productos cuyo nombre contenga "RGB" (insensible a mayúsculas/minúsculas)
- Muestra: nombre, precio
- Ordena por precio

**Resultado esperado:** Productos con iluminación RGB

---

### Consulta 2.7: Productos sin fabricante
**Objetivo:** Practicar IS NULL con FKs

**Requisitos:**
- Productos donde fabricante_id es NULL
- Cuenta cuántos hay

**Resultado esperado:** Número de productos sin fabricante asignado

---

### Consulta 2.8: Rango de precios por categoría
**Objetivo:** Filtrado combinado

**Requisitos:**
- Categoría "Memory" (RAM)
- Precio BETWEEN $40 AND $120
- Ordena por precio
- Limita a 20

**Resultado esperado:** RAM de gama media

---

## 🔧 Parte 3: Consultas en Modelo C

Abre `tienda_modelo_c.db` y resuelve las siguientes consultas.

### Consulta 3.1: Clientes registrados
**Objetivo:** SELECT simple en tabla de clientes

**Requisitos:**
- Lista todos los clientes
- Muestra: nombre, apellido, email, fecha_registro
- Ordena por fecha_registro descendente

**Resultado esperado:** Clientes más recientes primero

---

### Consulta 3.2: Pedidos pendientes
**Objetivo:** Filtrar por estado

**Requisitos:**
- Solo pedidos con estado = 'pendiente' o 'procesando'
- Ordena por fecha descendente
- Muestra: id, cliente_id, fecha, estado, total

**Resultado esperado:** Pedidos que aún no han sido enviados

---

### Consulta 3.3: Productos con poco stock
**Objetivo:** Comparar columnas

**Requisitos:**
- Busca en tabla `inventario`
- Productos donde cantidad_stock < stock_minimo
- Ordena por cantidad_stock ascendente
- Muestra: producto_id, cantidad_stock, stock_minimo, ubicacion

**Resultado esperado:** Productos que necesitan reposición urgente

---

### Consulta 3.4: Carritos activos
**Objetivo:** Filtrar por boolean

**Requisitos:**
- Carritos donde activo = 1
- Muestra: id, cliente_id, fecha_creacion, ultima_modificacion
- Ordena por ultima_modificacion descendente

**Resultado esperado:** Carritos de compra activos

---

## 📦 Estructura de Entrega

Crea un archivo `consultas_basicas.sql` con todas tus consultas:

```sql
-- ═══════════════════════════════════════════════════════════════
-- EJERCICIO 1.2: CONSULTAS SQL BÁSICAS
-- Alumno: [TU NOMBRE]
-- Fecha: [FECHA]
-- ═══════════════════════════════════════════════════════════════

-- PARTE 1: MODELO A (tienda_modelo_a.db)

-- Consulta 1.1: Listar todas las CPUs
SELECT name, price, core_count, core_clock
FROM cpu
ORDER BY price DESC
LIMIT 10;

-- Consulta 1.2: CPUs de AMD baratas
-- [TU CÓDIGO AQUÍ]

-- ... (continúa con todas las consultas)

-- PARTE 2: MODELO B (tienda_modelo_b.db)

-- Consulta 2.1: Productos por fabricante
-- [TU CÓDIGO AQUÍ]

-- ... (continúa)

-- PARTE 3: MODELO C (tienda_modelo_c.db)

-- Consulta 3.1: Clientes registrados
-- [TU CÓDIGO AQUÍ]

-- ...
```

---

## ⏱️ Tiempo Estimado

- **Parte 1 (Modelo A):** 1-1.5 horas
- **Parte 2 (Modelo B):** 1-1.5 horas
- **Parte 3 (Modelo C):** 30-45 minutos
- **TOTAL:** 2.5-3.5 horas

---

## 🎓 Criterios de Evaluación

| Criterio | Peso | Qué se evalúa |
|----------|------|---------------|
| **Correctitud** | 60% | Las consultas devuelven los resultados correctos |
| **Sintaxis SQL** | 20% | Código bien formateado, uso correcto de palabras clave |
| **Optimización** | 10% | Uso eficiente de operadores, evita queries innecesariamente complejas |
| **Documentación** | 10% | Comentarios claros explicando qué hace cada consulta |

---

## 💡 Pistas y Consejos

### Pista 1: LIKE es case-insensitive en SQLite
```sql
-- Esto encuentra "AMD", "amd", "Amd"
WHERE name LIKE '%AMD%'
```

### Pista 2: Combinar AND y OR
```sql
-- Usar paréntesis para agrupar condiciones
WHERE (socket = 'AM5' OR socket = 'LGA1700')
  AND price < 200
```

### Pista 3: NULL requiere IS, no =
```sql
-- ❌ Incorrecto
WHERE graphics = NULL

-- ✅ Correcto
WHERE graphics IS NULL
```

### Pista 4: BETWEEN es inclusivo
```sql
-- Incluye 50 y 150
WHERE price BETWEEN 50 AND 150
```

### Pista 5: ORDER BY múltiples columnas
```sql
-- Primero por socket, luego por precio dentro de cada socket
ORDER BY socket, price DESC
```

---

## 📚 Material de Apoyo

Ver archivo `TEORIA.md` en esta carpeta para:
- Sintaxis completa de SELECT
- Explicación de operadores
- Ejemplos paso a paso
- Errores comunes

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar JOINs en la Parte 1 y 2?**
R: En Parte 1 no es necesario (tablas desnormalizadas). En Parte 2 puedes usar JOINs simples si quieres mostrar nombres en lugar de IDs, pero no es obligatorio para este ejercicio.

**P: ¿Cómo sé si mi consulta es correcta?**
R: Compara con los resultados esperados descritos. Si tienes dudas, pregunta al profesor.

**P: ¿Qué hago si una consulta no devuelve resultados?**
R: Verifica que la condición no sea demasiado restrictiva. Por ejemplo, si no hay CPUs de AMD < $50, la query estará vacía (y eso está bien).

**P: ¿Puedo resolver de varias formas?**
R: ¡Sí! SQL es flexible. Si tu consulta devuelve el resultado correcto, es válida.

---

## ✅ Checklist de Completitud

Antes de entregar, verifica:

- [ ] Completaste las 8 consultas de la Parte 1
- [ ] Completaste las 8 consultas de la Parte 2
- [ ] Completaste las 4 consultas de la Parte 3
- [ ] Todas las consultas ejecutan sin errores
- [ ] Agregaste comentarios explicando qué hace cada query
- [ ] El archivo está bien formateado y legible
- [ ] Probaste las consultas en DB Browser for SQLite

---

## 🚀 Desafío Extra (Opcional)

Si terminas antes y quieres práctica adicional:

1. **Consulta combinada:** Encuentra productos que cumplan 3 condiciones simultáneas usando AND/OR
2. **Top/Bottom:** Crea consultas que muestren los 5 productos más baratos Y los 5 más caros de una categoría
3. **Patrones complejos:** Usa LIKE con patrones más avanzados (%, _)
4. **Consulta de análisis:** Cuenta cuántos productos hay en cada rango de precio (0-100, 100-200, etc.)

---

**¡Éxito con las consultas!** 🎯

Recuerda: La práctica hace al maestro. No te frustres si algunas consultas no salen a la primera.

---

**Creado:** 2025-12-11
**Duración estimada:** 2.5-3.5 horas
**Nivel:** Básico
