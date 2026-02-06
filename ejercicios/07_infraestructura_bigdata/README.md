# Modulo 07: Infraestructura Big Data

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

Nivel: Intermedio-Avanzado

---

## Objetivo

Entender **como se construye** la infraestructura que soporta el procesamiento
de grandes volumenes de datos. No solo usar las herramientas, sino comprender
por que existen, como se conectan entre si y como se orquestan.

Este modulo es **teorico-conceptual** con ejemplos practicos. Sienta las bases
para el Trabajo Final donde cada alumno construye su propia infraestructura.

---

## Estructura

```
07_infraestructura_bigdata/
    7.1_docker_compose/       Docker: contenedores, imagenes, YAML, orquestacion
    7.2_cluster_spark/        Spark: arquitectura master-worker, clusters, tuning
    7.3_hadoop_hdfs/          Proximamente
```

---

## Orden de Estudio

| Orden | Seccion | Tema central | Pregunta que responde |
|-------|---------|-------------|----------------------|
| 1 | 7.1 | Docker Compose | Como empaqueto y conecto servicios? |
| 2 | 7.2 | Cluster Spark | Como proceso datos en paralelo? |
| 3 | 7.3 | Hadoop + HDFS | Proximamente |

**Recomendacion:** Estudiar en orden. Docker es la base sobre la que se
monta Spark.

---

## Relacion con otros modulos

| Modulo | Conexion |
|--------|----------|
| 03 - Procesamiento Distribuido | Ejercicios practicos de PySpark y Hadoop |
| 06 - Analisis de Datos de Panel | Pipeline Spark completo sobre QoG |
| Trabajo Final | El alumno construye infraestructura Docker + Spark desde cero |

---

## Conceptos Clave del Modulo

Estos son los terminos que deberias poder explicar al terminar:

**Docker:** contenedor, imagen, volumen, red, puerto, healthcheck, docker-compose.yml
**Spark:** driver, executor, master, worker, SparkSession, lazy evaluation, DAG, Catalyst

---

## Requisitos

- Docker Desktop instalado
- Haber completado al menos el Modulo 01 (Bases de Datos)
- Conocimientos basicos de terminal/PowerShell

---

---

Comenzar: [7.1 - Docker Compose](./7.1_docker_compose/README.md)

---

-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA:
- Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.
- Zaharia, M., et al. (2016). Apache Spark: A unified engine for big data processing. Communications of the ACM, 59(11), 56-65.
- Dean, J. & Ghemawat, S. (2008). MapReduce: Simplified data processing on large clusters. Communications of the ACM, 51(1), 107-113.
- Shvachko, K., et al. (2010). The Hadoop Distributed File System. IEEE MSST, 1-10.
- Merkel, D. (2014). Docker: Lightweight Linux Containers for Consistent Development and Deployment. Linux Journal, 2014(239), 2.
-------------------------
