# Ejercicio 3.2: Dask - Procesamiento Out-of-Core

Nivel: Intermedio
Duración estimada: 8 horas

---

## Objetivos

- Procesar datasets que NO caben en RAM
- Entender lazy evaluation y task graphs
- Usar Dask DataFrames como alternativa a Pandas
- Paralelizar operaciones con Dask Delayed

---

## ¿Qué es Dask?

Dask es una librería de Python para computación paralela que permite:
- Trabajar con datasets más grandes que la RAM
- Paralelizar código de Pandas/NumPy
- Escalar de laptop a cluster

---

## Tareas

### Tarea 1: Dask vs Pandas (2h)

Comparar performance entre Pandas y Dask con un dataset de 20GB.

Operaciones a probar:
- Lectura de CSV grande
- GroupBy + Aggregations
- Merge de dos DataFrames
- Cálculos con apply()

Entregable: `dask_vs_pandas.py` con benchmarks

### Tarea 2: Dask DataFrames (3h)

Trabajar con un dataset de Stack Overflow Posts (20GB).

Tareas:
- Leer dataset con Dask
- Calcular top 100 tags más usados por año
- Filtrar posts con score > 10
- Calcular estadísticas por tag
- Guardar resultado en Parquet particionado

Entregable: `dask_dataframes.py`

### Tarea 3: Dask Delayed (2h)

Paralelizar funciones custom con Dask Delayed.

Ejemplo:
```python
import dask

@dask.delayed
def process_file(filename):
    # Tu código aquí
    return result

results = [process_file(f) for f in files]
total = dask.delayed(sum)(results)
total.compute()
```

Entregable: `dask_delayed.py`

### Tarea 4: Visualizar Task Graph (1h)

Generar y analizar el task graph de Dask.

```python
import dask.dataframe as dd

df = dd.read_csv('large.csv')
result = df.groupby('col').mean()
result.visualize('graph.png')  # Ver el DAG
```

Entregable: Screenshots de task graphs + explicación

---

## Instalación

```bash
pip install dask[complete] graphviz
```

---

## Dataset Sugerido

Stack Overflow Posts desde Kaggle (~20GB comprimido).

O crear dataset sintético:
```python
import dask.dataframe as dd
import pandas as pd

# Crear 100 archivos de 200MB cada uno
for i in range(100):
    df = pd.DataFrame({
        'id': range(i*1_000_000, (i+1)*1_000_000),
        'value': np.random.randn(1_000_000),
        'category': np.random.choice(['A','B','C'], 1_000_000)
    })
    df.to_csv(f'data/part_{i:03d}.csv', index=False)

# Leer con Dask
ddf = dd.read_csv('data/part_*.csv')
```

---

## Recursos

- Documentación Dask: https://docs.dask.org/
- Dask Tutorial: https://tutorial.dask.org/
- Dask Best Practices: https://docs.dask.org/en/latest/best-practices.html

---

Siguiente: [Ejercicio 3.3 - Hadoop HDFS](../3.3_hadoop_hdfs/README.md)
