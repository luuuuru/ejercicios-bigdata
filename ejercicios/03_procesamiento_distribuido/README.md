# Módulo 03: Procesamiento Distribuido

Nivel: Avanzado
Duración estimada: 50 horas

---

## Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- Trabajar con formatos de archivo eficientes para Big Data (Parquet)
- Procesar datasets que NO caben en RAM usando Dask
- Entender sistemas de archivos distribuidos (Hadoop HDFS)
- Procesar Big Data usando Apache Spark (PySpark)
- Optimizar queries de Spark para producción
- Orquestar pipelines ETL con Apache Airflow
- Integrar todas las tecnologías en un proyecto completo

---

## Tecnologías del Módulo

- Apache Parquet: Formato columnar comprimido
- Dask: Procesamiento paralelo en Python
- Hadoop HDFS: Sistema de archivos distribuido
- Apache Spark: Motor de procesamiento distribuido
- PySpark: API de Spark en Python
- Apache Airflow: Orquestación de workflows

---

## Estructura del Módulo

```
03_procesamiento_distribuido/
├── 3.1_parquet_optimizacion/     (5 horas)
├── 3.2_dask_introduccion/         (8 horas)
├── 3.3_hadoop_hdfs/               (6 horas)
├── 3.4_pyspark_basico/            (10 horas)
├── 3.5_pyspark_avanzado/          (12 horas)
├── 3.6_airflow_orquestacion/      (9 horas)
└── 3.7_proyecto_final_modulo/     (10 horas)
```

---

## Requisitos Previos

- Haber completado Módulo 01 (Bases de Datos)
- Haber completado Módulo 02 (ETL y Limpieza)
- Conocimientos de Python y Pandas
- Docker Desktop instalado
- 16GB RAM mínimo

---

## Orden Recomendado

1. Empezar con 3.1 (Parquet) - formatos eficientes
2. Continuar con 3.2 (Dask) - procesamiento out-of-core
3. Hacer 3.3 (Hadoop) - entender almacenamiento distribuido
4. Aprender 3.4 (PySpark básico) - fundamentos de Spark
5. Profundizar en 3.5 (PySpark avanzado) - optimizaciones
6. Automatizar con 3.6 (Airflow) - orquestación
7. Integrar todo en 3.7 (Proyecto final)

---

## Evaluación

- 40% Funcionalidad (el código ejecuta sin errores)
- 30% Optimización (uso correcto de las tecnologías)
- 20% Arquitectura (código modular y bien organizado)
- 10% Documentación (READMEs y comentarios claros)

---

## Recursos

- Documentación Apache Spark: https://spark.apache.org/docs/latest/
- Documentación Dask: https://docs.dask.org/
- Documentación Airflow: https://airflow.apache.org/docs/
- Dataset NYC Taxi: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

---

## Notas Importantes

- Todos los ejercicios usan Docker para evitar instalaciones complejas
- Los datasets son grandes (5GB - 50GB), necesitas espacio en disco
- Algunos ejercicios pueden tardar varios minutos en ejecutarse (es normal)
- Levanta solo los servicios Docker que necesites para cada ejercicio

---

Siguiente: [Ejercicio 3.1 - Parquet y Optimización](./3.1_parquet_optimizacion/README.md)
