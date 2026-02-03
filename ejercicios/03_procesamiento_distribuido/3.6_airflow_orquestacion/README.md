# Ejercicio 3.6: Airflow - Orquestación de Pipelines

Duración estimada: 9 horas

## Objetivos

- Automatizar pipelines ETL con Airflow
- Crear DAGs (Directed Acyclic Graphs)
- Usar operators, sensors y dependencies
- Configurar email alerts

## Levantar Airflow

Desde el directorio donde se generó tu `docker-compose.yml` (ver [Infraestructura](../../../docs/infraestructura.md)):

```bash
docker compose up -d postgres_airflow airflow-webserver airflow-scheduler
```

Web UI: http://localhost:8090
Login: admin / admin123

## Tareas

### 1. DAG Simple (3h)

Crear pipeline ETL básico:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    # Tu código
    pass

def transform():
    # Tu código
    pass

def load():
    # Tu código
    pass

with DAG('etl_simple', start_date=datetime(2024, 1, 1), schedule='@daily') as dag:
    task_extract = PythonOperator(task_id='extract', python_callable=extract)
    task_transform = PythonOperator(task_id='transform', python_callable=transform)
    task_load = PythonOperator(task_id='load', python_callable=load)

    task_extract >> task_transform >> task_load
```

Guardar en: `dags/dag_etl_simple.py` (dentro de tu directorio de trabajo Docker)

Entregable: DAG funcional visible en UI

### 2. DAG con Spark (3h)

Ejecutar job de Spark desde Airflow.

Entregable: `dag_etl_spark.py`

### 3. Sensors y Alertas (3h)

- FileSensor: Esperar archivo nuevo
- EmailOperator: Enviar email si falla
- Retry logic

Entregable: `dag_sensores.py`

## Recursos

- Airflow Tutorial: https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html
- Operators: https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html

---

Siguiente: [Ejercicio 3.7 - Proyecto Final](../3.7_proyecto_final_modulo/README.md)
