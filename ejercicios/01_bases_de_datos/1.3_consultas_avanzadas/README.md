# 📝 Ejercicio 1.3: Consultas SQL Avanzadas

## 🎯 Objetivos de Aprendizaje

Al completar este ejercicio serás capaz de:

- ✅ Realizar JOINs (INNER, LEFT, RIGHT)
- ✅ Agregar datos con GROUP BY
- ✅ Usar funciones de agregación (COUNT, SUM, AVG, MIN, MAX)
- ✅ Filtrar grupos con HAVING
- ✅ Crear subconsultas (subqueries)
- ✅ Usar DISTINCT para eliminar duplicados
- ✅ Trabajar con funciones de texto (UPPER, LOWER, SUBSTR)
- ✅ Usar funciones de fecha en SQL

---

## 📚 Pre-requisitos

- ✅ Ejercicio 1.1 completado
- ✅ Ejercicio 1.2 completado
- ✅ Dominio de consultas SELECT básicas
- ✅ Comprensión de claves primarias y foráneas

---

## 📋 Ejercicios

### Parte 1: INNER JOIN (5 consultas)

Trabajarás con `tienda_modelo_b.db`

**Ejercicio 1.1:** Productos con su categoría
- JOIN productos con categorias
- Muestra: nombre producto, categoría, precio
- Ordena por categoría, luego por precio

**Ejercicio 1.2:** Productos con fabricante y categoría
- JOIN triple: productos → fabricantes + categorias
- Solo productos con precio > $200
- Muestra fabricante, categoría, producto, precio

**Ejercicio 1.3:** Productos con colores
- JOIN productos → productos_colores → colores
- Agrupa por producto mostrando todos sus colores
- Usa GROUP_CONCAT para concatenar colores

**Ejercicio 1.4:** Top productos por fabricante
- JOIN productos con fabricantes
- Muestra el producto más caro de cada fabricante
- Usa subquery o window function

**Ejercicio 1.5:** Productos sin color asignado
- LEFT JOIN productos con productos_colores
- Filtra donde color_id IS NULL
- Muestra cuántos productos no tienen color

---

### Parte 2: Agregaciones (5 consultas)

**Ejercicio 2.1:** Contar productos por categoría
```sql
-- Usa COUNT y GROUP BY
-- Incluye categorías sin productos (LEFT JOIN)
-- Ordena por cantidad descendente
```

**Ejercicio 2.2:** Estadísticas de precios por fabricante
```sql
-- Calcula: COUNT, AVG, MIN, MAX de precios
-- Agrupa por fabricante
-- Solo fabricantes con más de 10 productos (HAVING)
```

**Ejercicio 2.3:** Productos por rango de precio
```sql
-- Usa CASE para crear rangos: Económico, Medio, Premium
-- Cuenta productos en cada rango
-- Calcula precio promedio por rango
```

**Ejercicio 2.4:** Colores más populares
```sql
-- Cuenta cuántos productos tiene cada color
-- Ordena por popularidad
-- Muestra top 10
```

**Ejercicio 2.5:** Fabricantes con productos en múltiples categorías
```sql
-- Cuenta categorías distintas por fabricante
-- Solo muestra los que tienen productos en 2+ categorías
```

---

### Parte 3: E-Commerce Analytics (Modelo C)

Trabajarás con `tienda_modelo_c.db`

**Ejercicio 3.1:** Ventas por cliente
```sql
-- JOIN clientes con pedidos y lineas_pedido
-- Calcula: total gastado, número de pedidos, ticket promedio
-- Ordena por total gastado descendente
```

**Ejercicio 3.2:** Productos más vendidos
```sql
-- JOIN productos con lineas_pedido
-- Suma cantidades vendidas por producto
-- Incluye categoría y fabricante
-- Top 20 productos
```

**Ejercicio 3.3:** Análisis de inventario
```sql
-- JOIN inventario con productos, categorias
-- Productos con stock crítico (< stock_minimo)
-- Calcula valor del stock faltante (precio × unidades_faltantes)
```

**Ejercicio 3.4:** Pedidos del último mes
```sql
-- Filtra pedidos de últimos 30 días
-- JOIN con clientes y lineas_pedido
-- Agrupa por día mostrando: num_pedidos, total_ventas, ticket_promedio
```

**Ejercicio 3.5:** Análisis de carritos abandonados
```sql
-- Clientes con carrito activo pero sin pedidos recientes
-- Calcula valor estimado de carritos
-- Identifica productos más agregados pero no comprados
```

---

## ⏱️ Tiempo Estimado

- **Parte 1:** 2-3 horas
- **Parte 2:** 2-3 horas
- **Parte 3:** 3-4 horas
- **TOTAL:** 7-10 horas

---

## 📦 Entrega

Archivo `consultas_avanzadas.sql` con todas las consultas documentadas.

---

## 🎓 Nivel: Intermedio-Avanzado

**Creado:** 2025-12-11
