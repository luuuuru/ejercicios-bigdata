# 7.2 - Cluster Spark: Arquitectura y Computacion Distribuida

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

Nivel: Intermedio-Avanzado | Tipo: Teorico-Conceptual

---

> *"Apache Spark: A Unified Engine for Big Data Processing"*
> -- Zaharia, M., Xin, R. S., Wendell, P., et al. (2016). Communications of the ACM, 59(11), 56-65.

---

## Indice

- [7.2.1 - Que es Apache Spark](#721---que-es-apache-spark)
- [7.2.2 - Arquitectura Master-Worker](#722---arquitectura-master-worker)
- [7.2.3 - Spark Standalone Mode](#723---spark-standalone-mode)
- [7.2.4 - Construyendo un Cluster con Docker](#724---construyendo-un-cluster-con-docker)
- [7.2.5 - SparkSession y la Conexion al Cluster](#725---sparksession-y-la-conexion-al-cluster)
- [7.2.6 - Lazy Evaluation y el DAG](#726---lazy-evaluation-y-el-dag)
- [7.2.7 - Modos de Despliegue](#727---modos-de-despliegue)
- [7.2.8 - Recursos y Tuning Basico](#728---recursos-y-tuning-basico)
- [7.2.9 - Monitorizacion con Spark UI](#729---monitorizacion-con-spark-ui)
- [7.2.10 - Spark + PostgreSQL](#7210---spark--postgresql)
- [7.2.11 - De Standalone a Produccion](#7211---de-standalone-a-produccion)
- [Referencias](#referencias)

---

## 7.2.1 - Que es Apache Spark

### Historia

Apache Spark nacio en 2009 en el **AMPLab** (Algorithms, Machines, and People Lab)
de la **Universidad de California, Berkeley**. Fue creado por Matei Zaharia como
parte de su investigacion doctoral sobre procesamiento de datos en memoria.

**Linea de tiempo:**

```
2003 .... Google publica el paper de Google File System (GFS)
2004 .... Google publica el paper de MapReduce (Dean & Ghemawat)
2006 .... Yahoo! crea Apache Hadoop (implementacion open-source de MapReduce)
2009 .... Matei Zaharia crea Spark en UC Berkeley AMPLab
2010 .... Spark se libera como open-source (licencia BSD)
2013 .... Spark se dona a la Apache Software Foundation
2014 .... Spark 1.0 - Se convierte en proyecto top-level de Apache
2016 .... Spark 2.0 - Introduccion de Structured Streaming y Dataset API
2016 .... Paper seminal en Communications of the ACM (Zaharia et al.)
2020 .... Spark 3.0 - Adaptive Query Execution, soporte GPU
2023 .... Spark 3.5 - Spark Connect, mejoras en Pandas API on Spark
```

### Por que Spark reemplazo a MapReduce

El modelo MapReduce de Hadoop tenia un problema fundamental: **cada operacion
leia y escribia datos a disco**. En un pipeline tipico de datos, donde encadenas
multiples operaciones (leer -> filtrar -> agrupar -> ordenar), MapReduce escribia
resultados intermedios al HDFS entre cada paso.

```
MapReduce (Hadoop):

  Disco -> Map -> Disco -> Reduce -> Disco -> Map -> Disco -> Reduce -> Disco
           ↑                 ↑                 ↑                 ↑
         LENTO             LENTO             LENTO             LENTO

Spark (en memoria):

  Disco -> Map -> Memoria -> Reduce -> Memoria -> Map -> Memoria -> Reduce -> Disco
                    ↑                    ↑                   ↑
                  RAPIDO               RAPIDO              RAPIDO
```

**Resultado:** Spark es hasta **100x mas rapido** que MapReduce para cargas de
trabajo iterativas en memoria, y **10x mas rapido** incluso cuando opera sobre disco.

Esto es especialmente importante para:

- **Machine Learning:** Algoritmos iterativos (gradient descent, k-means) que
  recorren los datos multiples veces.
- **Analisis interactivo:** Consultas ad-hoc sobre grandes datasets.
- **Grafos:** Algoritmos como PageRank que requieren multiples pasadas.

### El concepto clave: RDD (Resilient Distributed Dataset)

La innovacion fundamental de Spark fue el **RDD** (Dataset Distribuido Resiliente):

| Propiedad | Significado |
|-----------|-------------|
| **Resilient** | Si un nodo falla, Spark puede recalcular los datos perdidos usando el *lineage* (historial de transformaciones) |
| **Distributed** | Los datos se particionan y distribuyen entre multiples nodos del cluster |
| **Dataset** | Es una coleccion de objetos inmutables que se pueden operar en paralelo |

> **Nota:** Hoy en dia, se trabaja con **DataFrames** y **Datasets** (construidos
> sobre RDDs). Los DataFrames proveen una API tabular similar a pandas y permiten
> al optimizador Catalyst generar planes de ejecucion mas eficientes.

---

## 7.2.2 - Arquitectura Master-Worker

### El patron de computacion distribuida

Spark sigue el patron **Master-Worker** (tambien llamado Master-Slave en
literatura mas antigua). Este es un patron fundamental en sistemas distribuidos
donde un nodo central **coordina** el trabajo y multiples nodos **ejecutan** tareas.

### Diagrama de arquitectura completo

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        SPARK APPLICATION                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌──────────────────────────────────────┐                              ║
║  │         DRIVER PROGRAM               │                              ║
║  │  ┌──────────────────────────────┐    │                              ║
║  │  │   Tu script Python           │    │                              ║
║  │  │   (mi_analisis.py)           │    │                              ║
║  │  └──────────┬───────────────────┘    │                              ║
║  │             │                        │                              ║
║  │  ┌──────────▼───────────────────┐    │                              ║
║  │  │      SparkSession            │    │                              ║
║  │  │  (punto de entrada unico)    │    │                              ║
║  │  └──────────┬───────────────────┘    │                              ║
║  │             │                        │                              ║
║  │  ┌──────────▼───────────────────┐    │                              ║
║  │  │    SparkContext               │    │                              ║
║  │  │  (conexion al cluster)       │    │                              ║
║  │  └──────────┬───────────────────┘    │                              ║
║  └─────────────┼────────────────────────┘                              ║
║                │                                                       ║
║                │  Solicita recursos                                    ║
║                ▼                                                       ║
║  ┌──────────────────────────────────────┐                              ║
║  │       CLUSTER MANAGER                │                              ║
║  │  (Standalone / YARN / K8s / Mesos)   │                              ║
║  └──────────┬───────────┬───────────────┘                              ║
║             │           │                                              ║
║      ┌──────▼───┐ ┌────▼─────┐                                        ║
║      │ WORKER 1 │ │ WORKER 2 │  ...  WORKER N                         ║
║      │          │ │          │                                         ║
║      │┌────────┐│ │┌────────┐│                                        ║
║      ││Executor││ ││Executor││  <- Procesos JVM                       ║
║      ││        ││ ││        ││                                        ║
║      ││ Task 1 ││ ││ Task 3 ││  <- Unidades de trabajo               ║
║      ││ Task 2 ││ ││ Task 4 ││                                        ║
║      ││ Cache  ││ ││ Cache  ││  <- Datos en memoria                   ║
║      │└────────┘│ │└────────┘│                                        ║
║      └──────────┘ └──────────┘                                        ║
║                                                                        ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Componentes en detalle

#### 1. Driver Program (tu script Python)

El **Driver** es el proceso principal de tu aplicacion Spark. Es donde escribes
tu codigo Python (o Scala, Java, R). Sus responsabilidades:

- Definir las transformaciones y acciones sobre los datos
- Crear el plan de ejecucion (DAG)
- Negociar recursos con el Cluster Manager
- Coordinar la ejecucion de tareas en los Executors
- Recopilar resultados (cuando usas `collect()` o `show()`)

```python
# Esto se ejecuta en el DRIVER:
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://master:7077") \
    .appName("MiAnalisis") \
    .getOrCreate()

# Esto DEFINE transformaciones (en el Driver), pero se EJECUTA en los Workers:
df = spark.read.parquet("/datos/nyc_taxi.parquet")
resultado = df.filter(df.total_amount > 50).groupBy("payment_type").count()

# Esto DISPARA la ejecucion en los Workers y TRAE resultados al Driver:
resultado.show()
```

#### 2. SparkSession

Desde Spark 2.0, **SparkSession** es el punto de entrada unificado. Antes habia
que crear por separado SparkContext, SQLContext, HiveContext... Ahora todo se
accede desde un unico objeto:

```python
spark = SparkSession.builder \
    .master("spark://master:7077") \
    .appName("MiApp") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# Acceder al SparkContext subyacente (raramente necesario):
sc = spark.sparkContext
```

#### 3. Cluster Manager

El Cluster Manager es el **administrador de recursos** del cluster. Su trabajo
es asignar CPU y memoria a las aplicaciones Spark. Existen cuatro opciones:

| Cluster Manager | Descripcion | Caso de uso |
|-----------------|-------------|-------------|
| **Standalone** | Viene incluido con Spark | Desarrollo, clusters dedicados |
| **YARN** | Hadoop's Yet Another Resource Negotiator | Clusters Hadoop existentes |
| **Mesos** | Apache Mesos (en desuso) | Legacy, siendo reemplazado por K8s |
| **Kubernetes** | Orquestador de contenedores | Produccion moderna, cloud-native |

#### 4. Master Node

El nodo Master (en modo Standalone) es quien:

- Recibe las solicitudes de los Driver Programs
- Conoce que Workers estan disponibles y sus recursos
- Asigna Executors a los Workers
- Monitorea la salud de los Workers
- Provee la Web UI (puerto 8080)

#### 5. Worker Nodes

Los Workers son las maquinas que hacen el trabajo pesado:

- Se registran con el Master al iniciar
- Reportan sus recursos disponibles (cores, memoria)
- Lanzan Executors cuando el Master se lo indica
- Monitorean la salud de sus Executors

#### 6. Executors

Un Executor es un **proceso JVM** que corre dentro de un Worker:

- Ejecuta las tareas (Tasks) asignadas por el Driver
- Almacena datos en memoria (cache/persist)
- Reporta el estado de las tareas al Driver
- Cada Executor tiene una cantidad fija de cores y memoria

#### 7. Tasks (Tareas)

Una Task es la **unidad minima de trabajo** en Spark:

- Cada Task procesa **una particion** de datos
- Si tu dataset tiene 100 particiones, Spark creara 100 tasks
- Los Tasks se distribuyen entre los Executors disponibles

```
Ejemplo con 100 particiones, 2 Workers, cada uno con 1 Executor de 4 cores:

Total de Tasks:   100
Paralelismo:      8 tasks simultaneas (4 cores x 2 executors)
Oleadas:          13 oleadas (100 / 8 = 12.5, redondeado a 13)

Worker 1 (Executor: 4 cores)    Worker 2 (Executor: 4 cores)
┌─────────────────────────┐    ┌─────────────────────────┐
│ Core 1: Task 1          │    │ Core 1: Task 5          │
│ Core 2: Task 2          │    │ Core 2: Task 6          │
│ Core 3: Task 3          │    │ Core 3: Task 7          │
│ Core 4: Task 4          │    │ Core 4: Task 8          │
└─────────────────────────┘    └─────────────────────────┘
      Oleada 1 (8 tasks en paralelo)

Cuando terminan -> Oleada 2: Tasks 9-16
                -> Oleada 3: Tasks 17-24
                -> ...
                -> Oleada 13: Tasks 97-100
```

---

## 7.2.3 - Spark Standalone Mode

### Que es el modo Standalone

Spark incluye su propio Cluster Manager llamado **Standalone**. Es la forma mas
sencilla de levantar un cluster Spark sin dependencias externas (no necesitas
Hadoop, YARN, ni Kubernetes).

### Componentes del cluster Standalone

```
┌─────────────────────────────────────────────────────────┐
│                SPARK STANDALONE CLUSTER                  │
│                                                         │
│  ┌───────────────────────────────┐                      │
│  │      spark-master             │                      │
│  │  Puerto 7077: comunicacion    │                      │
│  │  Puerto 8080: Web UI          │                      │
│  │  Puerto 6066: REST API        │                      │
│  └───────┬──────────┬────────────┘                      │
│          │          │                                   │
│   ┌──────▼───┐ ┌────▼─────┐                             │
│   │ worker-1 │ │ worker-2 │                             │
│   │ 4 cores  │ │ 4 cores  │                             │
│   │ 8 GB RAM │ │ 8 GB RAM │                             │
│   │          │ │          │                             │
│   │ Port:    │ │ Port:    │                             │
│   │  8081    │ │  8082    │                             │
│   └──────────┘ └──────────┘                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### spark-master

El proceso `spark-master` es el coordinador central:

- **Puerto 7077:** Puerto de comunicacion interna. Los Workers y los Drivers se
  conectan aqui. Cuando escribes `spark://master:7077`, te conectas a este puerto.
- **Puerto 8080:** Interfaz web para monitoreo. Muestra Workers conectados,
  aplicaciones en ejecucion, y uso de recursos.
- **Puerto 6066:** API REST para enviar aplicaciones programaticamente.

```bash
# Iniciar el master manualmente (sin Docker):
$SPARK_HOME/sbin/start-master.sh

# O especificar host y puerto:
$SPARK_HOME/sbin/start-master.sh -h 0.0.0.0 -p 7077
```

### spark-worker

Cada proceso `spark-worker` se registra con el Master:

```bash
# Iniciar un worker manualmente:
$SPARK_HOME/sbin/start-worker.sh spark://master:7077

# Especificando recursos:
$SPARK_HOME/sbin/start-worker.sh spark://master:7077 \
    --cores 4 \
    --memory 8g
```

### Asignacion de recursos

Cuando una aplicacion Spark se conecta al cluster, el Master asigna recursos
segun la configuracion solicitada:

```
Cluster total:     8 cores, 16 GB RAM (2 workers x 4 cores x 8 GB)
App solicita:      2 executors, 2 cores cada uno, 4 GB cada uno
Asignacion:        Worker 1 -> 1 executor (2 cores, 4 GB)
                   Worker 2 -> 1 executor (2 cores, 4 GB)
Recursos libres:   4 cores, 8 GB (disponible para otra aplicacion)
```

### Spark Web UI: Que muestra y como leerlo

La Web UI del Master (http://localhost:8080) tiene estas secciones:

| Seccion | Que muestra |
|---------|-------------|
| **Workers** | Lista de workers conectados, sus recursos (cores/memoria totales y en uso) |
| **Running Applications** | Aplicaciones activas, con links a la UI del Driver |
| **Completed Applications** | Historial de aplicaciones que ya terminaron |

> **Tip importante:** La UI del Master (8080) muestra el **cluster**. La UI
> del Driver (generalmente 4040) muestra la **aplicacion**. Son diferentes.

---

## 7.2.4 - Construyendo un Cluster con Docker

### Por que Docker para un cluster Spark

En un cluster real, cada nodo es una maquina fisica o virtual separada. En
desarrollo y aprendizaje, usamos Docker para **simular** un cluster donde:

- Cada **contenedor** = un nodo del cluster
- La **red Docker** = la red que conecta los nodos
- Los **volumenes** = el almacenamiento compartido

```
Cluster Real:                    Cluster Docker:
┌──────────┐                     ┌──────────────────────────┐
│ Server 1 │ ← Master           │   Docker Desktop          │
│ (fisico) │                     │                          │
├──────────┤                     │  ┌────────┐ Contenedor 1 │
│ Server 2 │ ← Worker 1         │  │ Master │              │
│ (fisico) │                     │  └────────┘              │
├──────────┤                     │  ┌────────┐ Contenedor 2 │
│ Server 3 │ ← Worker 2         │  │Worker 1│              │
│ (fisico) │                     │  └────────┘              │
├──────────┤                     │  ┌────────┐ Contenedor 3 │
│ Server 4 │ ← PostgreSQL        │  │Worker 2│              │
│ (fisico) │                     │  └────────┘              │
└──────────┘                     │  ┌────────┐ Contenedor 4 │
                                 │  │Postgres│              │
    4 maquinas, $$$$             │  └────────┘              │
                                 └──────────────────────────┘
                                     1 maquina, $0
```

### Imagenes Docker para Spark

La imagen oficial es **apache/spark**, mantenida por el proyecto Apache:

| Imagen | Estado | Notas |
|--------|--------|-------|
| **apache/spark** | **Activa** (recomendada) | Oficial del proyecto Apache, siempre actualizada |
| **bitnami/spark** | **Descontinuada** (sept. 2025) | Ya no recibe actualizaciones, no usar en proyectos nuevos |

Para este curso usamos **apache/spark:3.5.4-python3**. A diferencia de bitnami,
el arranque se hace con comandos explicitos:

```yaml
# Arrancar el Master:
command: /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master

# Arrancar un Worker (apuntando al Master):
command: >
  /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker
  spark://spark-master:7077

# Variables de entorno del Worker:
SPARK_WORKER_CORES: 2             # Cores asignados al worker
SPARK_WORKER_MEMORY: 4G           # Memoria asignada al worker
SPARK_NO_DAEMONIZE: true          # Mantiene el proceso en primer plano (necesario en Docker)
```

### Volumenes compartidos

Un problema critico en clusters Docker es: **como ven los mismos datos el
Driver y los Workers?**

```
SIN volumenes compartidos:
┌────────┐  Lee archivo  ┌────────┐
│ Driver │ ──────────── │ Worker │  ERROR! El archivo no existe en el Worker
│ /datos │               │ /???  │
└────────┘               └────────┘

CON volumenes compartidos:
┌────────┐               ┌────────┐
│ Driver │               │ Worker │  OK! Ambos ven los mismos archivos
│ /datos │               │ /datos │
└───┬────┘               └───┬────┘
    │                        │
    └────────┬───────────────┘
             │
    ┌────────▼────────┐
    │ Volumen Docker   │
    │ ./datos:/datos   │
    │ (directorio del  │
    │  host compartido)│
    └─────────────────┘
```

### El problema del driver local vs driver remoto

Cuando ejecutas tu script Python **fuera** del cluster Docker (desde tu maquina
local), surgen problemas:

1. **Resolucion de nombres:** Tu maquina no sabe que es `spark://master:7077`
2. **Acceso a archivos:** El Driver lee un archivo local, pero los Workers no
   lo tienen
3. **Puertos:** Necesitas mapear todos los puertos necesarios

**Solucion recomendada:** Ejecutar el Driver **dentro** del cluster Docker,
ya sea mediante `docker exec` o con un contenedor adicional dedicado al Driver.

### Ejemplo funcional: docker-compose.yml

Este es el **minimo funcional** para el Trabajo Final: PostgreSQL + Spark Master + 1 Worker.
Puedes copiar y pegar este archivo tal cual y funcionara.

> **Nota:** Usamos `apache/spark:3.5.4-python3` (imagen oficial de Apache).
> La imagen `bitnami/spark` fue **descontinuada en septiembre 2025** y ya
> no recibe actualizaciones. La imagen oficial de Apache requiere iniciar
> los procesos via `command` en lugar de variables de entorno.

```yaml
# docker-compose.yml - Cluster Spark + PostgreSQL (minimo para Trabajo Final)
#
# Uso:
#   docker compose up -d          # Levantar todo
#   docker compose ps             # Verificar estado
#   docker compose down           # Apagar
#
# Estructura de carpetas necesaria:
#   tu_proyecto/
#   ├── docker-compose.yml   (este archivo)
#   ├── datos/               (tu CSV del QoG va aqui)
#   ├── scripts/             (tus scripts Python van aqui)
#   └── jars/                (driver JDBC de PostgreSQL)

services:

  # ============================
  # POSTGRESQL - Base de datos
  # ============================
  postgres:
    image: postgres:16-alpine
    container_name: spark-postgres
    hostname: postgres
    environment:
      POSTGRES_USER: spark_user
      POSTGRES_PASSWORD: spark_pass
      POSTGRES_DB: resultados_spark
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - spark-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U spark_user -d resultados_spark"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================
  # SPARK MASTER
  # ============================
  spark-master:
    image: apache/spark:3.5.4-python3
    container_name: spark-master
    hostname: spark-master
    command: /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
    environment:
      - SPARK_MASTER_HOST=spark-master
      - SPARK_MASTER_PORT=7077
      - SPARK_MASTER_WEBUI_PORT=8080
      - SPARK_NO_DAEMONIZE=true
    ports:
      - "7077:7077"    # Comunicacion del cluster
      - "8080:8080"    # Web UI del Master
    volumes:
      - ./datos:/opt/spark-data        # Datos compartidos
      - ./scripts:/opt/spark-apps      # Scripts Python
      - ./jars:/opt/spark-jars         # JARs (JDBC, etc.)
    networks:
      - spark-network

  # ============================
  # SPARK WORKER
  # ============================
  spark-worker-1:
    image: apache/spark:3.5.4-python3
    container_name: spark-worker-1
    hostname: spark-worker-1
    command: >
      /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker
      spark://spark-master:7077
    environment:
      - SPARK_WORKER_MEMORY=4G
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_WEBUI_PORT=8081
      - SPARK_NO_DAEMONIZE=true
    ports:
      - "8081:8081"    # Web UI del Worker
    volumes:
      - ./datos:/opt/spark-data        # Mismos datos que el master
      - ./scripts:/opt/spark-apps      # Mismos scripts
      - ./jars:/opt/spark-jars         # Mismos JARs
    depends_on:
      - spark-master
    networks:
      - spark-network

volumes:
  postgres_data:

networks:
  spark-network:
    driver: bridge
```

**Diferencias clave vs `bitnami/spark` (descontinuada):**

| Aspecto | `bitnami/spark` (vieja) | `apache/spark` (actual) |
|---------|------------------------|------------------------|
| Arranque | Variables `SPARK_MODE=master` | Comando explicito con `spark-class` |
| Ruta de datos | Cualquiera | `/opt/spark-data` (convencion) |
| Ruta de scripts | Cualquiera | `/opt/spark-apps` (convencion) |
| Estado | **Descontinuada** (sept. 2025) | Mantenida por Apache |

**Levantar el cluster:**

```bash
# Crear las carpetas necesarias (si no existen)
mkdir datos scripts jars

# Iniciar todo el cluster
docker compose up -d

# Verificar que los servicios estan corriendo
docker compose ps

# Ver los logs del master (confirmar que el worker se conecto)
docker compose logs spark-master

# Abrir Spark UI en el navegador:
#   http://localhost:8080   -> Veras el worker conectado

# Ejecutar un script dentro del cluster
docker exec spark-master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    /opt/spark-apps/mi_analisis.py

# Apagar el cluster
docker compose down
```

> **Para agregar un segundo Worker:** Copia el bloque `spark-worker-1`,
> renombralo a `spark-worker-2`, cambia el `container_name`, `hostname`
> y mapea el puerto a `8082:8081`. Eso es todo.

---

## 7.2.5 - SparkSession y la Conexion al Cluster

### Creando una SparkSession

La **SparkSession** es el objeto central de toda aplicacion Spark. Es el
primer objeto que creas y el ultimo que cierras.

#### Conexion a un cluster remoto

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("Analisis NYC Taxi") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "2") \
    .config("spark.driver.memory", "2g") \
    .config("spark.jars", "/opt/spark-jars/postgresql-42.7.1.jar") \
    .getOrCreate()

# Tu codigo de analisis aqui...
df = spark.read.parquet("/datos/nyc_taxi.parquet")
print(f"Total registros: {df.count()}")

# SIEMPRE cerrar la sesion al finalizar
spark.stop()
```

#### Modo local para desarrollo

```python
# Para desarrollo rapido en tu maquina (sin cluster):
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Desarrollo Local") \
    .getOrCreate()

# local[*]  -> Usa TODOS los cores de tu maquina
# local[4]  -> Usa exactamente 4 cores
# local[1]  -> Usa 1 solo core (util para debugging)
# local     -> Equivalente a local[1]
```

### Configuraciones clave

| Configuracion | Descripcion | Valor tipico |
|---------------|-------------|--------------|
| `spark.executor.memory` | Memoria por executor | 2g - 8g |
| `spark.executor.cores` | Cores por executor | 2 - 5 |
| `spark.driver.memory` | Memoria del driver | 1g - 4g |
| `spark.executor.instances` | Numero de executors (en YARN/K8s) | 2 - 20 |
| `spark.sql.shuffle.partitions` | Particiones en operaciones shuffle | 200 (default) |
| `spark.default.parallelism` | Paralelismo por defecto para RDDs | 2x total cores |
| `spark.serializer` | Serializador (Kryo es mas rapido) | org.apache.spark.serializer.KryoSerializer |

### Patron recomendado para scripts

```python
"""
mi_analisis.py - Script que se ejecuta con spark-submit
"""
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

def crear_spark_session():
    """Crea la SparkSession con configuracion apropiada."""
    return SparkSession.builder \
        .appName("Mi Analisis") \
        .config("spark.sql.shuffle.partitions", "50") \
        .getOrCreate()

def main():
    spark = crear_spark_session()

    try:
        # --- Lectura ---
        df = spark.read.parquet("/datos/input/")

        # --- Transformaciones ---
        resultado = (
            df.filter(F.col("year") == 2024)
              .groupBy("month")
              .agg(
                  F.count("*").alias("total_viajes"),
                  F.avg("total_amount").alias("monto_promedio")
              )
              .orderBy("month")
        )

        # --- Accion: escribir resultado ---
        resultado.write \
            .mode("overwrite") \
            .parquet("/datos/output/resumen_mensual")

        print("Analisis completado exitosamente.")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

> **Nota:** Cuando usas `spark-submit`, el master se puede especificar en la
> linea de comando (`--master spark://master:7077`) en lugar de hardcodearlo
> en el script. Esto hace tu codigo portable entre entornos.

---

## 7.2.6 - Lazy Evaluation y el DAG

### Transformaciones vs Acciones

Este es uno de los conceptos **mas importantes** de Spark. Todas las operaciones
se dividen en dos categorias:

#### Transformaciones (LAZY - no se ejecutan inmediatamente)

Las transformaciones **definen** que hacer con los datos, pero **no hacen nada**
hasta que una accion lo dispare:

```python
# Ninguna de estas lineas ejecuta nada en el cluster:
df = spark.read.parquet("/datos/taxi.parquet")    # Transformacion
df2 = df.filter(df.total_amount > 0)              # Transformacion
df3 = df2.select("pickup_date", "total_amount")   # Transformacion
df4 = df3.groupBy("pickup_date").count()           # Transformacion
df5 = df4.orderBy("count", ascending=False)        # Transformacion

# AQUI es donde Spark realmente ejecuta TODO:
df5.show(10)  # <-- ACCION: dispara la ejecucion completa
```

#### Lista de transformaciones comunes

| Transformacion | Que hace | Ejemplo |
|----------------|----------|---------|
| `select()` | Selecciona columnas | `df.select("col1", "col2")` |
| `filter()` / `where()` | Filtra filas | `df.filter(df.age > 18)` |
| `withColumn()` | Crea/modifica columna | `df.withColumn("new", df.x * 2)` |
| `groupBy()` | Agrupa (requiere `.agg()`) | `df.groupBy("city").count()` |
| `orderBy()` / `sort()` | Ordena | `df.orderBy("date")` |
| `join()` | Une DataFrames | `df1.join(df2, "id")` |
| `drop()` | Elimina columnas | `df.drop("col_innecesaria")` |
| `distinct()` | Elimina duplicados | `df.distinct()` |
| `withColumnRenamed()` | Renombra columna | `df.withColumnRenamed("a", "b")` |
| `repartition()` | Cambia particionamiento | `df.repartition(100)` |

#### Lista de acciones comunes

| Accion | Que hace | Ejemplo |
|--------|----------|---------|
| `show()` | Muestra filas en consola | `df.show(20)` |
| `count()` | Cuenta filas | `df.count()` |
| `collect()` | Trae TODOS los datos al Driver | `df.collect()` |
| `take(n)` | Trae N filas al Driver | `df.take(5)` |
| `first()` | Trae la primera fila | `df.first()` |
| `write` | Escribe a disco | `df.write.parquet(...)` |
| `toPandas()` | Convierte a pandas DataFrame | `df.toPandas()` |
| `foreach()` | Aplica funcion a cada fila | `df.foreach(func)` |

> **Advertencia:** `collect()` y `toPandas()` traen **todos** los datos a la
> memoria del Driver. Si tu DataFrame tiene 100 GB, el Driver necesitara
> 100 GB de RAM. Usar con precaucion solo para resultados agregados pequenos.

### Por que Lazy Evaluation: El Optimizador Catalyst

La razon por la que Spark no ejecuta inmediatamente es para poder **optimizar**
el plan de ejecucion completo. El optimizador **Catalyst** analiza todas tus
transformaciones y genera el plan mas eficiente:

```
Tu codigo (Plan Logico):               Catalyst (Plan Fisico Optimizado):

1. Leer TODO el Parquet                1. Leer SOLO columnas necesarias
2. Filtrar por fecha                      (column pruning)
3. Seleccionar 3 columnas              2. Aplicar filtro DURANTE la lectura
4. Agrupar por ciudad                     (predicate pushdown)
5. Contar                              3. Agrupar y contar
                                          (combina select + group en 1 paso)

Resultado: Lee menos datos, menos operaciones, mas rapido.
```

**Ejemplo de Predicate Pushdown:**

```python
# Tu escribes esto:
df = spark.read.parquet("/datos/taxi.parquet")
df2 = df.filter(df.year == 2024)
df3 = df2.select("month", "total_amount")

# Catalyst lo convierte en:
# "Lee del Parquet SOLO las columnas month, total_amount, year
#  y SOLO las filas donde year == 2024"
# En vez de leer todo y luego filtrar.
```

### El DAG (Directed Acyclic Graph)

Cuando una accion se dispara, Spark construye un **DAG** que representa
todas las transformaciones como un grafo:

```
                    ┌──────────────┐
                    │ read.parquet │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   filter     │
                    │ (amount > 0) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   select     │   STAGE 1
                    │ (3 columnas) │   (sin shuffle)
                    └──────┬───────┘
                           │
              ─────────────┼─────────────  SHUFFLE (redistribucion de datos)
                           │
                    ┌──────▼───────┐
                    │  groupBy     │
                    │ + count      │   STAGE 2
                    └──────┬───────┘   (despues del shuffle)
                           │
                    ┌──────▼───────┐
                    │   orderBy    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    show()    │   ACCION
                    └──────────────┘
```

### Stages y Shuffles

El DAG se divide en **Stages** en cada punto donde hay un **Shuffle**:

- **Shuffle:** Redistribucion de datos entre Workers. Ocurre cuando una operacion
  necesita datos de multiples particiones (ej: `groupBy`, `join`, `orderBy`).
- **Stage:** Conjunto de transformaciones que se pueden ejecutar sin shuffle
  (en pipeline, sobre la misma particion).

```
Stage 1: read -> filter -> select     (cada particion se procesa independientemente)
                                       ↓ SHUFFLE (datos se redistribuyen por clave de group)
Stage 2: groupBy + count -> orderBy   (datos agrupados se procesan)
```

> **Regla practica:** Los shuffles son **costosos** porque mueven datos por la
> red entre Workers. Minimizar shuffles = mejor rendimiento.

---

## 7.2.7 - Modos de Despliegue

### Comparacion de modos

```
┌──────────────────────────────────────────────────────────────────────┐
│                    MODOS DE DESPLIEGUE DE SPARK                     │
├──────────────┬──────────────┬──────────────┬────────────────────────┤
│  Local       │  Standalone  │    YARN      │     Kubernetes         │
│              │              │              │                        │
│ Tu laptop   │ Cluster      │ Cluster      │ Cluster                │
│ 1 JVM       │ dedicado     │ Hadoop       │ contenedores           │
│              │ Spark        │              │                        │
│ master=     │ master=      │ master=      │ master=                │
│ "local[*]"  │ "spark://    │ "yarn"       │ "k8s://https://        │
│              │  host:7077"  │              │  api-server:443"       │
├──────────────┼──────────────┼──────────────┼────────────────────────┤
│ Desarrollo   │ Desarrollo   │ Produccion   │ Produccion             │
│ Testing      │ Equipos      │ (legacy)     │ (moderno)              │
│ Prototipado  │ dedicados    │              │                        │
│              │ Aprendizaje  │              │                        │
└──────────────┴──────────────┴──────────────┴────────────────────────┘
```

### Local Mode

- **Que es:** Todo corre en una sola JVM en tu maquina
- **Cuando usarlo:** Desarrollo, pruebas con datos pequenos, debugging
- **Ventaja:** No necesitas cluster, arranque inmediato
- **Limitacion:** No hay distribucion real, limitado a los recursos de 1 maquina

```python
spark = SparkSession.builder.master("local[*]").getOrCreate()
```

### Standalone Cluster

- **Que es:** El cluster manager incluido con Spark
- **Cuando usarlo:** Clusters dedicados a Spark, aprendizaje, equipos pequenos
- **Ventaja:** Simple de configurar, no tiene dependencias externas
- **Limitacion:** Solo gestiona Spark (no puede compartir recursos con otros frameworks)

```python
spark = SparkSession.builder.master("spark://master:7077").getOrCreate()
```

### YARN (Hadoop)

- **Que es:** El gestor de recursos de Hadoop
- **Cuando usarlo:** Cuando ya tienes un cluster Hadoop, necesitas compartir
  recursos con MapReduce, Hive, etc.
- **Ventaja:** Comparte recursos con todo el ecosistema Hadoop
- **Limitacion:** Requiere Hadoop instalado, configuracion mas compleja

```python
spark = SparkSession.builder.master("yarn").getOrCreate()
```

### Kubernetes

- **Que es:** Spark corre como pods en un cluster Kubernetes
- **Cuando usarlo:** Produccion moderna, entornos cloud, microservicios
- **Ventaja:** Escalado elastico, aislamiento por contenedores, cloud-native
- **Limitacion:** Requiere conocimiento de Kubernetes, mayor overhead operacional

```python
spark = SparkSession.builder \
    .master("k8s://https://k8s-api-server:443") \
    .config("spark.kubernetes.container.image", "apache/spark:3.5.0") \
    .getOrCreate()
```

### Resumen: Cuando usar cada uno

| Escenario | Modo recomendado |
|-----------|------------------|
| Estoy aprendiendo Spark | Local mode |
| Prototipando con datos reales (~10 GB) | Local mode o Standalone con Docker |
| Equipo de 5 data scientists, cluster dedicado | Standalone |
| Empresa con infraestructura Hadoop existente | YARN |
| Startup cloud-native, AWS/GCP/Azure | Kubernetes |
| Procesamiento a demanda (sin cluster fijo) | Kubernetes o servicios gestionados (EMR, Dataproc) |

---

## 7.2.8 - Recursos y Tuning Basico

### Dimensionando Executors

La configuracion de Executors es el factor mas importante para el rendimiento.
La regla general es:

```
No dar TODA la memoria a Spark:
  - El sistema operativo necesita RAM
  - La JVM tiene overhead
  - Executors demasiado grandes sufren pausas de Garbage Collection (GC)

Regla practica para un Worker con 16 cores y 64 GB RAM:

  Opcion A: 1 executor gordo         Opcion B: 3 executors medianos
  ┌──────────────────────┐          ┌──────────────────────┐
  │ 1 Executor           │          │ Executor 1           │
  │ 15 cores, 60 GB      │          │ 5 cores, 19 GB       │
  │ MALO: GC lento,      │          │                      │
  │ no aprovecha HDFS    │          │ Executor 2           │
  │ replicacion          │          │ 5 cores, 19 GB       │
  └──────────────────────┘          │                      │
                                    │ Executor 3           │
                                    │ 5 cores, 19 GB       │
                                    │ BUENO: GC rapido,    │
                                    │ mejor paralelismo    │
                                    └──────────────────────┘
                                    (1 core y ~7 GB para el OS y overhead)
```

**Reglas practicas:**

| Parametro | Recomendacion |
|-----------|---------------|
| Cores por executor | 3 - 5 (maximo 5) |
| Memoria por executor | Depende del cluster (evitar > 64 GB) |
| Overhead de memoria | ~10% adicional (`spark.executor.memoryOverhead`) |

### Particiones

Las **particiones** son la unidad de paralelismo en Spark. Cada particion
se procesa por un Task independiente.

```
Pocas particiones (ej: 2):
┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
│  Particion 1: 50 GB                 │  │  Particion 2: 50 GB                 │
│  Tarda 10 minutos                   │  │  Tarda 10 minutos                   │
└─────────────────────────────────────┘  └─────────────────────────────────────┘
  Solo 2 tasks, 6 cores desocupados si tienes 8

Muchas particiones (ej: 200):
┌───┐┌───┐┌───┐┌───┐┌───┐...┌───┐
│0.5│││0.5│││0.5│││0.5│││0.5││  │0.5││  200 tasks, 8 ejecutandose en paralelo
│GB ││GB ││GB ││GB ││GB │  │GB │
└───┘└───┘└───┘└───┘└───┘...└───┘
  Mejor distribucion del trabajo
```

**Configuraciones de particiones:**

```python
# Particiones durante operaciones shuffle (groupBy, join, etc.)
spark.conf.set("spark.sql.shuffle.partitions", "50")  # Default: 200

# Regla: 2-3 particiones por core disponible en el cluster
# Si tienes 8 cores total: 16-24 particiones es razonable
# Para datasets grandes: puede ser 200, 500, o mas

# Reparticionar explicitamente:
df = df.repartition(50)         # Redistribuye en 50 particiones (shuffle!)
df = df.coalesce(10)            # Reduce a 10 particiones (sin shuffle, mas eficiente)
```

### El Small File Problem

Cuando Spark escribe resultados, genera **un archivo por particion**. Si tienes
200 particiones, generara 200 archivos pequenos:

```
PROBLEMA:
output/
├── part-00000.parquet  (5 MB)
├── part-00001.parquet  (5 MB)
├── part-00002.parquet  (5 MB)
├── ...
└── part-00199.parquet  (5 MB)

200 archivos x 5 MB = 1 GB total
Lectura futura: LENTA (abrir 200 archivos tiene overhead)

SOLUCION: coalesce antes de escribir:
df.coalesce(4).write.parquet("output/")

output/
├── part-00000.parquet  (250 MB)
├── part-00001.parquet  (250 MB)
├── part-00002.parquet  (250 MB)
└── part-00003.parquet  (250 MB)

4 archivos x 250 MB = 1 GB total
Lectura futura: RAPIDA
```

### Data Locality

Spark intenta ejecutar las Tasks **cerca de donde estan los datos** para
minimizar transferencias por red:

| Nivel | Nombre | Significado |
|-------|--------|-------------|
| 1 | PROCESS_LOCAL | Datos ya estan en la memoria del Executor |
| 2 | NODE_LOCAL | Datos estan en el disco del mismo nodo |
| 3 | RACK_LOCAL | Datos estan en un nodo del mismo rack (red rapida) |
| 4 | ANY | Datos deben transferirse por red (mas lento) |

> **En Docker:** Todos los contenedores corren en la misma maquina fisica,
> asi que la data locality no es un factor relevante. En produccion con
> multiples maquinas, si lo es.

---

## 7.2.9 - Monitorizacion con Spark UI

### Acceso a la UI

| UI | URL | Que muestra |
|----|-----|-------------|
| Master UI | http://localhost:8080 | Estado del cluster, workers, apps |
| Driver UI | http://localhost:4040 | Detalle de la aplicacion en ejecucion |
| Worker UI | http://localhost:8081 | Estado de un worker especifico |
| History Server | http://localhost:18080 | Aplicaciones completadas |

### Pestanas del Spark UI (Driver - puerto 4040)

#### Jobs

```
┌────────────────────────────────────────────────────────────────────┐
│ Spark Jobs                                                         │
├────────┬─────────────────────────────┬──────────┬─────────────────┤
│ Job ID │ Description                 │ Duration │ Stages          │
├────────┼─────────────────────────────┼──────────┼─────────────────┤
│ 0      │ show at mi_script.py:25     │ 2.3 s    │ 2/2 succeeded  │
│ 1      │ count at mi_script.py:30    │ 0.8 s    │ 1/1 succeeded  │
│ 2      │ parquet at mi_script.py:35  │ 5.1 s    │ 3/3 succeeded  │
└────────┴─────────────────────────────┴──────────┴─────────────────┘

Cada ACCION (show, count, write) genera un Job.
Cada Job tiene uno o mas Stages.
```

#### Stages

```
┌─────────────────────────────────────────────────────────────────────┐
│ Stage 0 (Job 0)                                                     │
├──────────────────┬──────────────────────────────────────────────────┤
│ Tasks:           │ 50/50 succeeded                                 │
│ Input:           │ 2.3 GB (Parquet)                                │
│ Shuffle Write:   │ 450 MB                                          │
│ Duration:        │ 1.8 s                                           │
├──────────────────┴──────────────────────────────────────────────────┤
│ DAG Visualization:                                                  │
│   FileScan parquet -> Filter -> Project -> HashAggregate (partial)  │
└─────────────────────────────────────────────────────────────────────┘

Aqui puedes ver:
- Cuantas tasks se ejecutaron
- Cuanto dato se leyo y se movio (shuffle)
- El plan de ejecucion visual (DAG)
- Si alguna task tardo mucho mas que las demas (data skew)
```

#### Storage

Muestra los DataFrames que estan en **cache** (persisted):

```python
# Para que un DataFrame aparezca en Storage:
df.cache()         # Guarda en memoria
df.persist()       # Guarda en memoria (equivalente)
df.count()         # Accion necesaria para materializar el cache

# Ahora la tab Storage mostrara:
# RDD Name | Storage Level | Size in Memory | Size on Disk
# In-memory table | Memory  | 2.3 GB         | 0 B
```

#### Environment

Lista **todas** las configuraciones activas de Spark:

- Propiedades de Spark (spark.executor.memory, etc.)
- Propiedades del sistema (java.version, os.name, etc.)
- Classpath y variables de entorno

> **Tip:** Cuando algo no funciona como esperas, revisa esta tab para confirmar
> que tus configuraciones se aplicaron correctamente.

#### Executors

```
┌──────────┬────────┬────────┬──────────┬───────────┬──────────────┐
│ Executor │ Status │ Cores  │ Memory   │ Tasks     │ Shuffle Read │
│          │        │        │ Used     │ Completed │              │
├──────────┼────────┼────────┼──────────┼───────────┼──────────────┤
│ driver   │ Active │ -      │ 512 MB   │ -         │ -            │
│ 0        │ Active │ 2      │ 3.1 GB   │ 78        │ 230 MB       │
│ 1        │ Active │ 2      │ 2.9 GB   │ 72        │ 220 MB       │
└──────────┴────────┴────────┴──────────┴───────────┴──────────────┘

Si un executor tiene MUCHAS mas tasks que otro -> desbalanceo
Si un executor muere frecuentemente -> problemas de memoria (OOM)
```

### REST API

Spark expone una API REST para monitoreo programatico:

```bash
# Lista de aplicaciones
curl http://localhost:4040/api/v1/applications

# Detalle de Jobs de una aplicacion
curl http://localhost:4040/api/v1/applications/{app-id}/jobs

# Detalle de Stages
curl http://localhost:4040/api/v1/applications/{app-id}/stages

# Detalle de Executors
curl http://localhost:4040/api/v1/applications/{app-id}/executors
```

---

## 7.2.10 - Spark + PostgreSQL

### Escribir resultados de Spark a una base de datos

Una vez que Spark procesa los datos, frecuentemente necesitamos guardar los
resultados en una base de datos relacional para consumo por dashboards,
APIs, o reportes.

### Prerequisito: descargar el driver JDBC de PostgreSQL

Para que Spark pueda comunicarse con PostgreSQL necesita un **driver JDBC**.
Este es un archivo `.jar` (Java Archive) que actua como traductor entre
Spark (que corre sobre la JVM) y PostgreSQL.

**Paso 1:** Descargar el JAR desde la pagina oficial:

```
https://jdbc.postgresql.org/download/
```

Buscar la version mas reciente (al momento de escribir esto: `postgresql-42.7.1.jar`).
Tambien se puede descargar directamente desde terminal:

```bash
# Desde PowerShell (Windows)
curl -L -o jars/postgresql-42.7.1.jar https://jdbc.postgresql.org/download/postgresql-42.7.1.jar

# Desde bash (Linux/Mac)
wget -P jars/ https://jdbc.postgresql.org/download/postgresql-42.7.1.jar
```

**Paso 2:** Colocar el archivo en la carpeta `jars/` de tu proyecto Docker:

```
tu_proyecto/
├── compose.yaml
├── datos/
├── jars/
│   └── postgresql-42.7.1.jar   <-- aqui
└── ...
```

**Paso 3:** Verificar que el `compose.yaml` monta esa carpeta en los contenedores Spark:

```yaml
services:
  spark-master:
    volumes:
      - ./jars:/opt/spark-jars     # El JAR queda disponible en /opt/spark-jars/
```

Con esto, desde cualquier script PySpark puedes referenciar el driver como
`/opt/spark-jars/postgresql-42.7.1.jar`.

> **Nota:** Sin este JAR, Spark lanzara el error:
> `java.lang.ClassNotFoundException: org.postgresql.Driver`

### Metodo 1: JDBC Connector (recomendado para datasets grandes)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("Spark a PostgreSQL") \
    .config("spark.jars", "/opt/spark-jars/postgresql-42.7.1.jar") \
    .getOrCreate()

# Procesar datos
df = spark.read.parquet("/datos/taxi.parquet")
resultado = df.groupBy("payment_type").agg({"total_amount": "avg"})

# Propiedades de conexion JDBC
jdbc_url = "jdbc:postgresql://postgres:5432/resultados_spark"
jdbc_properties = {
    "user": "spark_user",
    "password": "spark_pass",
    "driver": "org.postgresql.Driver"
}

# Escribir a PostgreSQL
resultado.write.jdbc(
    url=jdbc_url,
    table="resumen_pagos",
    mode="overwrite",       # overwrite | append | ignore | error
    properties=jdbc_properties
)

spark.stop()
```

**Modos de escritura:**

| Modo | Comportamiento |
|------|----------------|
| `overwrite` | Borra la tabla y la recrea con los nuevos datos |
| `append` | Agrega filas a la tabla existente |
| `ignore` | No hace nada si la tabla ya existe |
| `error` (default) | Lanza error si la tabla ya existe |

### Metodo 2: toPandas() + pandas to_sql() (para datasets pequenos)

```python
from sqlalchemy import create_engine

# Convertir resultado de Spark a pandas (CUIDADO con el tamano)
pdf = resultado.toPandas()

# Escribir con pandas
engine = create_engine("postgresql://spark_user:spark_pass@postgres:5432/resultados_spark")
pdf.to_sql("resumen_pagos", engine, if_exists="replace", index=False)
```

> **Cuando usar cada metodo:**
>
> | Tamano del resultado | Metodo recomendado |
> |---------------------|-------------------|
> | < 100,000 filas | `toPandas()` + `to_sql()` (mas simple) |
> | > 100,000 filas | `df.write.jdbc()` (distribuido, mas rapido) |
> | > 10,000,000 filas | `df.write.jdbc()` con `batchsize` y `numPartitions` |

### Leer datos desde PostgreSQL hacia Spark

```python
# Leer una tabla completa
df = spark.read.jdbc(
    url=jdbc_url,
    table="mi_tabla",
    properties=jdbc_properties
)

# Leer con query personalizada (usa parentesis como subquery)
df = spark.read.jdbc(
    url=jdbc_url,
    table="(SELECT id, nombre, monto FROM ventas WHERE year = 2024) AS subq",
    properties=jdbc_properties
)

# Lectura particionada para paralelismo
df = spark.read.jdbc(
    url=jdbc_url,
    table="ventas",
    column="id",              # Columna para particionar
    lowerBound=1,             # Valor minimo
    upperBound=1000000,       # Valor maximo
    numPartitions=10,         # Numero de particiones (queries paralelas)
    properties=jdbc_properties
)
```

---

## 7.2.11 - De Standalone a Produccion

### Escalando el cluster

El cluster Standalone que construimos con Docker es perfecto para **aprender**,
pero para produccion necesitamos mas:

```
Desarrollo (este curso):          Produccion:
┌──────────────────┐              ┌──────────────────────────────────┐
│ Docker Desktop   │              │ Cluster de 50 maquinas           │
│ 1 master         │              │ 3 masters (alta disponibilidad)  │
│ 2 workers        │              │ 47 workers                       │
│ 8 cores total    │              │ 376 cores, 1.5 TB RAM total      │
│ 16 GB RAM total  │              │ Almacenamiento: HDFS o S3        │
│                  │              │ Monitoreo: Prometheus + Grafana   │
└──────────────────┘              └──────────────────────────────────┘
```

### Opcion 1: Mas Workers en Standalone

La forma mas simple de escalar: agregar mas workers al `docker-compose.yml`
(o agregar mas maquinas fisicas al cluster).

### Opcion 2: Kubernetes con spark-on-k8s-operator

Para entornos cloud-native, Kubernetes es el estandar actual:

```yaml
# Ejemplo conceptual de SparkApplication en Kubernetes:
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: mi-analisis-spark
spec:
  type: Python
  mode: cluster
  image: apache/spark:3.5.0
  mainApplicationFile: s3a://mi-bucket/scripts/analisis.py
  driver:
    cores: 1
    memory: 2g
  executor:
    cores: 4
    instances: 10
    memory: 8g
```

### Opcion 3: Servicios gestionados en la nube

Los proveedores cloud ofrecen Spark **como servicio**. Tu no gestionas las
maquinas, solo defines cuantos recursos necesitas:

| Servicio | Proveedor | Que ofrece |
|----------|-----------|------------|
| **Amazon EMR** | AWS | Clusters Spark/Hadoop gestionados, integracion con S3 |
| **Google Dataproc** | GCP | Clusters Spark gestionados, integracion con BigQuery |
| **Azure HDInsight** | Azure | Clusters Spark/Hadoop, integracion con Azure Storage |
| **Databricks** | Multi-cloud | Plataforma optimizada para Spark, notebooks colaborativos |

```
Ventajas de servicios gestionados:
  + Escalado automatico (autoscaling)
  + No hay que mantener hardware
  + Pago por uso (por hora de cluster)
  + Integracion nativa con storage cloud (S3, GCS, ADLS)

Desventajas:
  - Costo puede crecer rapidamente
  - Vendor lock-in (dependencia del proveedor)
  - Menos control sobre la configuracion
```

### El camino tipico en una organizacion

```
1. Aprendizaje:     local[*] en tu laptop
                         │
2. Prototipo:       Standalone con Docker (lo que hicimos en este curso)
                         │
3. Primera produccion: YARN sobre un cluster Hadoop existente
                    O   Standalone dedicado
                         │
4. Produccion moderna:  Kubernetes
                    O   Servicio gestionado (EMR, Dataproc, Databricks)
```

---

## Resumen del Modulo

| Concepto | Punto clave |
|----------|-------------|
| Spark vs MapReduce | Spark es 100x mas rapido en memoria por evitar escrituras intermedias a disco |
| Arquitectura | Master coordina, Workers ejecutan, Executors son procesos JVM con Tasks |
| Standalone | Cluster manager incluido en Spark, simple y suficiente para aprender |
| Docker | Permite simular un cluster multi-nodo en una sola maquina |
| SparkSession | Punto de entrada unico; `.master()` define donde corre |
| Lazy Evaluation | Transformaciones se acumulan, Acciones disparan la ejecucion |
| DAG + Catalyst | Spark optimiza el plan de ejecucion antes de ejecutar |
| Particiones | Unidad de paralelismo; ajustar segun tamano de datos y cores |
| Spark UI | Herramienta esencial para diagnosticar rendimiento |
| JDBC | Permite leer/escribir entre Spark y bases de datos relacionales |
| Produccion | Kubernetes o servicios gestionados (EMR, Dataproc, Databricks) |

---

## Glosario Rapido

| Termino | Definicion |
|---------|-----------|
| **Driver** | Proceso principal que ejecuta tu codigo y coordina el cluster |
| **Executor** | Proceso JVM en un Worker que ejecuta tareas y almacena datos |
| **Task** | Unidad minima de trabajo; procesa una particion |
| **Stage** | Conjunto de tasks que se ejecutan sin shuffle |
| **Shuffle** | Redistribucion de datos entre nodos (costoso en red) |
| **DAG** | Grafo dirigido aciclico que representa el plan de ejecucion |
| **Catalyst** | Optimizador de queries de Spark SQL |
| **Partition** | Fragmento de datos que se procesa de forma independiente |
| **RDD** | Resilient Distributed Dataset, abstraccion fundamental de Spark |
| **DataFrame** | Estructura tabular distribuida (como un pandas DataFrame, pero distribuido) |
| **Lazy Evaluation** | Las transformaciones no se ejecutan hasta que una accion las dispara |
| **Predicate Pushdown** | Optimizacion que aplica filtros lo antes posible (ej: al leer Parquet) |

---

## Referencias

1. Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., ... & Stoica, I. (2016).
   Apache Spark: A unified engine for big data processing. *Communications of the ACM*, 59(11), 56-65.

2. Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified data processing on large clusters.
   *Communications of the ACM*, 51(1), 107-113.

3. Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.

4. Chambers, B., & Zaharia, M. (2018). *Spark: The Definitive Guide*. O'Reilly Media.

5. Damji, J. S., Wenig, B., Das, T., & Lee, D. (2020). *Learning Spark*, 2nd Edition. O'Reilly Media.

6. Apache Spark Documentation: https://spark.apache.org/docs/3.5.4/

7. Apache Spark Docker Image: https://hub.docker.com/r/apache/spark

8. PostgreSQL JDBC Driver: https://jdbc.postgresql.org/

---

Volver a: [Modulo 07 - Infraestructura Big Data](../README.md)

---

-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA:
- Zaharia, M., et al. (2016). Apache Spark: A unified engine for big data processing. Communications of the ACM, 59(11), 56-65.
- Zaharia, M., et al. (2012). Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing. NSDI'12, 15-28.
- Armbrust, M., et al. (2015). Spark SQL: Relational Data Processing in Spark. SIGMOD'15, 1383-1394.
- Karau, H. & Warren, R. (2017). High Performance Spark. O'Reilly Media.
- Damji, J., et al. (2020). Learning Spark (2nd ed.). O'Reilly Media.
- Apache Spark Documentation. https://spark.apache.org/docs/3.5.4/
-------------------------
