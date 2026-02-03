# Ejercicio 3.7: Proyecto Final del Módulo

Duración estimada: 10 horas
Modalidad: Individual o Grupal (2-3 personas)

## Objetivos

Integrar todo lo aprendido en el módulo en un proyecto completo:
- Parquet
- Dask o Spark
- Airflow
- Pipeline ETL automatizado

## Opciones de Proyecto

### Opción A: Pipeline NYC Taxi Completo

**Dataset:** NYC Taxi Trip Data (50GB+)

**Pipeline:**
1. Extract: Descargar datos automáticamente (Airflow)
2. Transform: Procesar con Spark (limpiar, agregaciones)
3. Load: Guardar en PostgreSQL + Parquet particionado
4. Dashboard: Streamlit o Dash

**Análisis requeridos:**
- Viajes por día/mes/año
- Propinas por zona
- Rutas más populares
- Tendencias temporales

### Opción B: Análisis Wikipedia

**Dataset:** Wikipedia dumps (100GB+)

**Pipeline:**
1. Extract: Descargar dump de Wikipedia
2. Transform: Procesar con Spark (extraer links, categorías)
3. Análisis:
   - Top artículos más editados
   - Network de links entre artículos
   - Categorías más populares

### Opción C: Pipeline QoG Avanzado

Tomar el pipeline ETL del Módulo 02 y:
1. Escalarlo a Spark (en lugar de Pandas)
2. Automatizar con Airflow
3. Agregar validaciones con Great Expectations
4. Dashboard interactivo

## Requisitos Técnicos

### Estructura del Proyecto

```
proyecto_final/
├── README.md                 (Descripción del proyecto)
├── docker-compose.yml        (Stack completo)
├── requirements.txt
├── .env.example
│
├── dags/                     (DAGs de Airflow)
│   └── pipeline_principal.py
│
├── src/
│   ├── extract/
│   ├── transform/            (Jobs de Spark)
│   └── load/
│
├── sql/                      (Queries de análisis)
├── tests/                    (Tests unitarios)
├── docs/
│   └── ARQUITECTURA.md       (Diagramas, decisiones)
└── dashboard/                (Opcional: Streamlit/Dash)
```

### Docker Compose

Debe incluir:
- Spark (master + 2 workers)
- Airflow (webserver + scheduler + postgres)
- PostgreSQL (para datos)
- Cualquier otro servicio necesario

### Documentación

README.md debe incluir:
- Descripción del proyecto
- Instrucciones de instalación
- Cómo ejecutar el pipeline
- Análisis realizados
- Resultados y conclusiones
- Screenshots

### Código

- Modular y bien organizado
- Type hints en funciones
- Docstrings
- PEP 8
- Tests unitarios (al menos 5)

## Evaluación

- 30% Funcionalidad (pipeline completo ejecuta sin errores)
- 30% Optimización (uso correcto de Spark/Dask, particiones)
- 20% Arquitectura (código modular, separation of concerns)
- 20% Documentación (README, diagramas, comments)

## Entrega

1. Código en carpeta del proyecto
2. README completo con instrucciones
3. Presentación de 5 minutos (slides o video)
4. Pull Request a repositorio del curso

## Presentación (5 minutos)

Debe incluir:
- Problema que resuelve el proyecto
- Arquitectura del pipeline
- Tecnologías usadas y por qué
- Resultados principales
- Aprendizajes y desafíos

## Recursos

- Todos los ejercicios del Módulo 03
- Documentación oficial de Spark, Airflow, etc.
- Ejemplos proporcionados por el instructor en clase

---

Fin del Módulo 03
