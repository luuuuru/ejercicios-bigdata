# Ejercicio 3.4: PySpark Básico

Duración estimada: 10 horas

## Objetivos

- Aprender fundamentos de Apache Spark
- Trabajar con Spark DataFrames
- Ejecutar transformaciones y acciones
- Usar Spark SQL

## Levantar Spark

Desde el directorio donde se generó tu `docker-compose.yml` (ver [Infraestructura](../../../docs/infraestructura.md)):

```bash
docker compose up -d spark-master spark-worker-1 spark-worker-2
```

Web UI: http://localhost:8080

## Tareas

### 1. Spark DataFrames (3h)

Operaciones básicas:
- Leer Parquet
- select(), filter(), groupBy(), agg()
- Joins
- Window functions
- Escribir resultado

Dataset: NYC Taxi (50GB)

Entregable: `spark_dataframes.py`

### 2. Spark SQL (3h)

Usar SQL sobre Spark DataFrames:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("spark://localhost:7077").getOrCreate()
df = spark.read.parquet("data.parquet")
df.createOrReplaceTempView("taxi")

spark.sql("""
    SELECT date, COUNT(*) as trips
    FROM taxi
    GROUP BY date
    ORDER BY trips DESC
    LIMIT 10
""").show()
```

Entregable: `spark_sql.py`

### 3. Transformaciones vs Acciones (2h)

Entender lazy evaluation:
- Transformaciones: map, filter, groupBy (lazy)
- Acciones: count, collect, show (eager)

Entregable: `spark_transformaciones.py`

### 4. Proyecto Mini (2h)

Analizar dataset NYC Taxi:
- Total viajes por día
- Propina promedio por zona
- Top 10 rutas más populares
- Guardar en Parquet particionado por mes

Entregable: Script completo + resultados

## Recursos

- PySpark Docs: https://spark.apache.org/docs/latest/api/python/
- Spark SQL Guide: https://spark.apache.org/docs/latest/sql-programming-guide.html

---

Siguiente: [Ejercicio 3.5 - PySpark Avanzado](../3.5_pyspark_avanzado/README.md)
