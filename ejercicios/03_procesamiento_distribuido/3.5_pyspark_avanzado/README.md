# Ejercicio 3.5: PySpark Avanzado

Duración estimada: 12 horas

## Objetivos

- Optimizar performance de Spark
- Entender particionamiento
- Usar broadcast joins
- Crear UDFs (User Defined Functions)
- Debuggear Spark jobs

## Tareas

### 1. Optimización de Particiones (3h)

- repartition() vs coalesce()
- Detectar skew en particiones
- Salting para balancear

Entregable: `particionamiento.py`

### 2. Broadcast Joins (3h)

Joins eficientes para tablas pequeñas (<10MB).

```python
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_df), "key")
```

Entregable: `broadcast_joins.py` con benchmarks

### 3. Window Functions (3h)

Ranking, running totals, lead/lag.

Entregable: `window_functions.py`

### 4. UDFs y Pandas UDFs (3h)

```python
from pyspark.sql.functions import udf, pandas_udf
from pyspark.sql.types import DoubleType

@udf(returnType=DoubleType())
def custom_func(value):
    return value * 2

@pandas_udf(DoubleType())
def pandas_custom_func(series):
    return series * 2  # Vectorizado, más rápido
```

Entregable: `udf_custom.py` con comparación performance

## Dataset

Stack Overflow + GitHub (100GB combinado)

## Recursos

- Spark Performance Tuning: https://spark.apache.org/docs/latest/sql-performance-tuning.html
- Pandas UDFs: https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html

---

Siguiente: [Ejercicio 3.6 - Airflow](../3.6_airflow_orquestacion/README.md)
