# Ejercicio 3.1: Parquet y Optimización de Formatos

Nivel: Intermedio
Duración estimada: 5 horas

---

## Objetivos

- Entender las diferencias entre formatos de archivo (CSV, Parquet, Feather)
- Aprender a convertir datasets a Parquet
- Practicar particionamiento de datos
- Optimizar lectura selectiva de columnas
- Medir performance y espacio en disco

---

## Conceptos Teóricos

### ¿Por qué Parquet?

- **Almacenamiento columnar:** Lee solo las columnas necesarias
- **Compresión eficiente:** Reduce espacio en disco 5-10x
- **Metadata incorporada:** Tipos de datos, estadísticas por columna
- **Lectura rápida:** Especialmente para queries analíticos

### Comparación de Formatos

| Formato | Tipo | Compresión | Velocidad Lectura | Uso Típico |
|---------|------|------------|-------------------|------------|
| CSV | Texto plano | No | Lenta | Intercambio de datos |
| Parquet | Binario columnar | Sí (snappy, gzip) | Rápida | Análisis de datos |
| Feather | Binario fila | Ligera | Muy rápida | Intercambio Python/R |

---

## Tareas del Ejercicio

### Tarea 1: Comparar Formatos (2h)

**Objetivo:** Convertir un CSV grande a diferentes formatos y comparar.

**Pasos:**
1. Descargar un dataset CSV de ~1-2GB (ej: NYC Taxi, Stack Overflow)
2. Leer el CSV con pandas
3. Guardar en formato Parquet (con diferentes compresiones: snappy, gzip, zstd)
4. Guardar en formato Feather
5. Medir:
   - Tamaño en disco de cada formato
   - Tiempo de escritura
   - Tiempo de lectura completa
   - Tiempo de lectura de solo 3 columnas

**Entregable:**
- Script `comparar_formatos.py`
- Tabla de resultados en README.md
- Conclusiones sobre cuál formato usar en qué caso

### Tarea 2: Particionamiento (2h)

**Objetivo:** Particionar un dataset grande por columnas.

**Pasos:**
1. Tomar un dataset con fechas (ej: ventas por día)
2. Particionar por año y mes: `datos/year=2024/month=01/data.parquet`
3. Escribir queries que aprovechen las particiones
4. Medir velocidad de lectura con vs sin particiones

**Ejemplo de estructura:**
```
datos_particionados/
├── year=2023/
│   ├── month=01/
│   │   └── data.parquet
│   ├── month=02/
│   │   └── data.parquet
│   └── ...
└── year=2024/
    └── ...
```

**Entregable:**
- Script `particionamiento.py`
- Dataset particionado (en .gitignore, no subir)
- Benchmarks de lectura

### Tarea 3: Lectura Selectiva (1h)

**Objetivo:** Leer solo las columnas necesarias.

**Pasos:**
1. Crear un dataset Parquet con 50 columnas
2. Leer solo 3 columnas
3. Comparar tiempo y memoria vs leer todas

**Entregable:**
- Script `lectura_selectiva.py`
- Mediciones de tiempo y memoria

---

## Datasets Sugeridos

1. **NYC Taxi Trip Data** (recomendado):
   - Peso: ~2GB por mes
   - Descarga: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

2. **Stack Overflow Posts**:
   - Peso: ~5GB
   - Descarga: Kaggle Stack Overflow dataset

3. **Crear dataset sintético:**
   ```python
   import pandas as pd
   import numpy as np

   df = pd.DataFrame({
       'fecha': pd.date_range('2020-01-01', periods=10_000_000, freq='S'),
       'valor': np.random.randn(10_000_000),
       'categoria': np.random.choice(['A', 'B', 'C'], 10_000_000)
   })
   df.to_csv('dataset_grande.csv', index=False)
   ```

---

## Tecnologías

- pandas
- pyarrow (para leer/escribir Parquet)
- fastparquet (alternativa a pyarrow)

Instalación:
```bash
pip install pandas pyarrow fastparquet
```

---

## Recursos

- Documentación Parquet: https://parquet.apache.org/docs/
- PyArrow: https://arrow.apache.org/docs/python/
- Pandas IO Tools: https://pandas.pydata.org/docs/user_guide/io.html

---

## Evaluación

- Correctitud de scripts (30%)
- Mediciones completas (30%)
- Conclusiones bien fundamentadas (20%)
- Código limpio y documentado (20%)

---

## Notas

- NO subas datasets grandes a Git (añádelos al .gitignore)
- Usa `time.time()` o `%%timeit` de Jupyter para medir tiempos
- Documenta tus resultados en tablas Markdown

---

Siguiente: [Ejercicio 3.2 - Dask](../3.2_dask_introduccion/README.md)
