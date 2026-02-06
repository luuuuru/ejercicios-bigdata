# Módulo 08: Streaming con Apache Kafka

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutiérrez Miranda (@TodoEconometria)

Nivel: Avanzado | Tipo: Teórico-Práctico

---

> *"Kafka is a distributed commit log that provides pub-sub messaging capabilities"*
> -- Jay Kreps, Neha Narkhede & Jun Rao, LinkedIn (2011)

---

## Índice

- [8.1 - ¿Qué es el Streaming de Datos?](#81---qué-es-el-streaming-de-datos)
- [8.2 - Apache Kafka: Conceptos Fundamentales](#82---apache-kafka-conceptos-fundamentales)
- [8.3 - Arquitectura de Kafka](#83---arquitectura-de-kafka)
- [8.4 - Kafka con Docker Compose](#84---kafka-con-docker-compose)
- [8.5 - Productores y Consumidores en Python](#85---productores-y-consumidores-en-python)
- [8.6 - Spark Structured Streaming + Kafka](#86---spark-structured-streaming--kafka)
- [8.7 - Proyecto: Observatorio Económico en Tiempo Real](#87---proyecto-observatorio-económico-en-tiempo-real)
- [Referencias](#referencias)

---

## 8.1 - ¿Qué es el Streaming de Datos?

### Batch vs Streaming

Hasta ahora hemos trabajado con **procesamiento batch**: los datos existen completos
en un archivo, los leemos, procesamos y guardamos el resultado. Esto funciona para
análisis históricos, reportes diarios, entrenamientos de ML, etc.

```
BATCH PROCESSING (lo que hemos hecho):

  Archivo CSV     Spark Job      Resultado
  (100 GB)    →   (5 min)    →   Parquet
  [completo]      [una vez]      [completo]

  Características:
  - Datos finitos y conocidos
  - Se procesa todo de una vez
  - Latencia: minutos a horas
  - Ejemplo: "Reporte mensual de ventas"
```

El **procesamiento streaming** es diferente: los datos llegan continuamente,
sin fin, y debemos procesarlos "en vuelo":

```
STREAM PROCESSING (lo nuevo):

  Eventos         Procesamiento     Resultado
  continuos   →   continuo      →   continuo
  [infinitos]     [siempre on]      [actualizado]

  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
  │e1│→│e2│→│e3│→│e4│→│e5│→ ... (nunca termina)
  └──┘ └──┘ └──┘ └──┘ └──┘
         ↓
    ┌─────────────┐
    │ Procesador  │ (siempre escuchando)
    │ de Stream   │
    └─────────────┘
         ↓
    Alertas, dashboards, acciones en tiempo real

  Características:
  - Datos infinitos y desconocidos
  - Se procesa evento por evento (o micro-batches)
  - Latencia: milisegundos a segundos
  - Ejemplo: "Alerta cuando la acción baje 5%"
```

### Casos de uso reales de Streaming

| Industria | Caso de uso | Latencia requerida |
|-----------|-------------|-------------------|
| **Finanzas** | Detección de fraude en transacciones | < 100 ms |
| **E-commerce** | Recomendaciones mientras navegas | < 500 ms |
| **IoT** | Sensores de temperatura en fábricas | < 1 segundo |
| **Redes sociales** | Trending topics en Twitter/X | < 5 segundos |
| **Transporte** | Uber: match conductor-pasajero | < 2 segundos |
| **Gaming** | Leaderboards en tiempo real | < 1 segundo |
| **Salud** | Monitoreo de signos vitales | < 100 ms |

### El problema que resuelve Kafka

Antes de Kafka, las arquitecturas de streaming eran caóticas:

```
ANTES (point-to-point):

  App A ──→ App B
    │  ╲      │
    │   ╲     │
    ↓    ╲    ↓
  App C ←──→ App D ──→ App E
    │         │         │
    ↓         ↓         ↓
  DB 1      DB 2      DB 3

  Problemas:
  - Cada conexión es un protocolo diferente
  - Si App D muere, ¿quién guarda los mensajes?
  - Agregar App F requiere modificar 5 sistemas
  - No hay replay de mensajes históricos
```

Kafka introduce un **bus central de eventos**:

```
DESPUÉS (con Kafka):

  App A ──┐
          │
  App B ──┼──→ [ KAFKA ] ──┬──→ App D
          │                │
  App C ──┘                ├──→ App E
                           │
                           └──→ App F (nueva, sin tocar nada)

  Ventajas:
  - Un solo sistema para todos los eventos
  - Mensajes persistidos (replay posible)
  - Desacoplamiento total
  - Escalabilidad horizontal
```

---

## 8.2 - Apache Kafka: Conceptos Fundamentales

### Historia

Apache Kafka fue creado en **LinkedIn** en 2010 por Jay Kreps, Neha Narkhede y
Jun Rao para resolver el problema de mover datos entre sistemas a escala masiva.
El nombre viene del escritor Franz Kafka (según Jay Kreps, "porque es un sistema
optimizado para escritura").

```
2010 .... Kafka nace en LinkedIn
2011 .... Se libera como open-source
2012 .... Se convierte en proyecto Apache (incubadora)
2014 .... Graduación como proyecto top-level Apache
2014 .... Jay Kreps funda Confluent (empresa detrás de Kafka)
2017 .... Kafka Streams API madura
2019 .... Kafka 2.x - mejoras de rendimiento
2022 .... KRaft mode (adiós ZooKeeper)
2024 .... Kafka 3.7 - KRaft estable para producción
```

### Conceptos clave

#### 1. Evento (Message/Record)

Un **evento** es la unidad mínima de datos en Kafka. Representa "algo que pasó":

```
Evento = {
    key:       "ARG",                              // Clave (opcional, para particionado)
    value:     {"pais": "Argentina", "pib": 450},  // Payload (los datos)
    timestamp: 1707148800000,                      // Cuándo ocurrió
    headers:   {"source": "qog_api"}               // Metadatos (opcional)
}
```

#### 2. Topic

Un **topic** es una categoría o "canal" donde se publican eventos relacionados:

```
Topic: eventos_economicos
├── Evento 1: {"pais": "ARG", "tipo": "inflacion", "valor": 5.2}
├── Evento 2: {"pais": "BRA", "tipo": "pib", "valor": 2100}
├── Evento 3: {"pais": "CHL", "tipo": "desempleo", "valor": 8.1}
└── ... (millones de eventos)

Topic: alertas_corrupcion
├── Evento 1: {"pais": "VEN", "indice": 17, "alerta": "critico"}
└── ...
```

#### 3. Partición

Cada topic se divide en **particiones** para paralelismo y escalabilidad:

```
Topic: eventos_economicos (3 particiones)

Partición 0:  [e0] [e3] [e6] [e9]  ...  → Broker 1
Partición 1:  [e1] [e4] [e7] [e10] ...  → Broker 2
Partición 2:  [e2] [e5] [e8] [e11] ...  → Broker 3

- Los eventos se distribuyen por hash(key) % num_particiones
- Eventos con misma key van siempre a la misma partición (orden garantizado)
- Diferentes particiones pueden procesarse en paralelo
```

#### 4. Offset

El **offset** es la posición de un evento dentro de su partición:

```
Partición 0:
Offset:    0     1     2     3     4     5
         [e0]  [e3]  [e6]  [e9]  [e12] [e15]
                            ↑
                     Consumer está aquí
                     (ha leído hasta offset 3)
```

#### 5. Producer y Consumer

```
┌──────────────┐                         ┌──────────────┐
│   PRODUCER   │                         │   CONSUMER   │
│              │                         │              │
│ - Envía      │    ┌─────────────┐      │ - Lee        │
│   eventos    │───→│    TOPIC    │───→  │   eventos    │
│ - Elige      │    │             │      │ - Procesa    │
│   partición  │    │ [p0][p1][p2]│      │ - Guarda     │
│              │    └─────────────┘      │   offset     │
└──────────────┘                         └──────────────┘

Producer: "Tengo un dato nuevo, publícalo"
Consumer: "Dame todos los datos desde mi último offset"
```

#### 6. Consumer Group

Múltiples consumers pueden formar un **grupo** para procesar en paralelo:

```
Topic con 4 particiones + Consumer Group con 2 consumers:

         ┌─────────────────────────────┐
         │      Consumer Group A       │
         │                             │
         │  ┌──────────┐ ┌──────────┐  │
         │  │Consumer 1│ │Consumer 2│  │
         │  │ (p0, p1) │ │ (p2, p3) │  │
         │  └──────────┘ └──────────┘  │
         └─────────────────────────────┘
                      ↑
    ┌─────────────────┴─────────────────┐
    │            TOPIC                   │
    │  [p0]    [p1]    [p2]    [p3]      │
    └───────────────────────────────────┘

- Cada partición es asignada a UN solo consumer del grupo
- Si un consumer muere, sus particiones se reasignan
- Puedes tener otro Consumer Group B leyendo lo mismo (independiente)
```

---

## 8.3 - Arquitectura de Kafka

### Componentes del cluster

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         KAFKA CLUSTER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    CONTROLLER (KRaft)                           │   │
│   │  - Gestiona metadatos del cluster                               │   │
│   │  - Asigna particiones a brokers                                 │   │
│   │  - Detecta brokers caídos                                       │   │
│   │  (Antes: ZooKeeper, ahora: KRaft integrado)                     │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│   │  BROKER 1   │   │  BROKER 2   │   │  BROKER 3   │                   │
│   │             │   │             │   │             │                   │
│   │ Topic A-p0  │   │ Topic A-p1  │   │ Topic A-p2  │                   │
│   │ Topic B-p1  │   │ Topic B-p2  │   │ Topic B-p0  │                   │
│   │ (leader)    │   │ (replica)   │   │ (replica)   │                   │
│   │             │   │             │   │             │                   │
│   │ Disco: logs │   │ Disco: logs │   │ Disco: logs │                   │
│   └─────────────┘   └─────────────┘   └─────────────┘                   │
│         ↑                 ↑                 ↑                           │
│         └────────────┬────┴────────────────┘                           │
│                      │                                                  │
│              Red interna (replicación)                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          ↑                                           ↑
          │                                           │
    ┌─────┴─────┐                               ┌─────┴─────┐
    │ Producers │                               │ Consumers │
    └───────────┘                               └───────────┘
```

### Broker

Un **broker** es un servidor Kafka. Sus responsabilidades:

- Recibir mensajes de producers y guardarlos en disco
- Servir mensajes a consumers
- Replicar datos a otros brokers
- Participar en elección de líder

### KRaft vs ZooKeeper

Históricamente, Kafka dependía de **ZooKeeper** para coordinar el cluster.
Desde Kafka 3.x, **KRaft** (Kafka Raft) elimina esta dependencia:

```
ANTES (con ZooKeeper):                AHORA (KRaft):

┌───────────────┐                     ┌───────────────┐
│   ZooKeeper   │ (proceso separado)  │    Kafka      │
│   Ensemble    │                     │   Cluster     │
│  (3-5 nodos)  │                     │               │
└───────┬───────┘                     │ ┌───────────┐ │
        │                             │ │ Controller│ │ (integrado)
        │ (coordinación)              │ │  (KRaft)  │ │
        ↓                             │ └───────────┘ │
┌───────────────┐                     │               │
│    Kafka      │                     │  Brokers...   │
│   Brokers     │                     │               │
└───────────────┘                     └───────────────┘

Ventajas de KRaft:
- Menos componentes que mantener
- Mejor rendimiento (menos latencia)
- Escalabilidad mejorada (millones de particiones)
- Setup más simple
```

### Replicación y durabilidad

Kafka replica cada partición para tolerancia a fallos:

```
Topic: eventos (3 particiones, replication-factor=3)

         Broker 1          Broker 2          Broker 3
        ┌─────────┐       ┌─────────┐       ┌─────────┐
p0:     │ LEADER  │ ←───→ │ follower│ ←───→ │ follower│
        ├─────────┤       ├─────────┤       ├─────────┤
p1:     │ follower│ ←───→ │ LEADER  │ ←───→ │ follower│
        ├─────────┤       ├─────────┤       ├─────────┤
p2:     │ follower│ ←───→ │ follower│ ←───→ │ LEADER  │
        └─────────┘       └─────────┘       └─────────┘

- Solo el LEADER recibe escrituras
- Los followers replican del leader
- Si el leader muere, un follower es promovido
- ISR (In-Sync Replicas): followers que están al día
```

### Retención de mensajes

A diferencia de colas tradicionales, Kafka **no borra mensajes al consumirlos**:

```
Políticas de retención:

1. Por tiempo (default):
   retention.ms=604800000  (7 días)
   → Mensajes se borran después de 7 días

2. Por tamaño:
   retention.bytes=1073741824  (1 GB)
   → Cuando la partición supera 1 GB, borra los más viejos

3. Compactación (log compaction):
   cleanup.policy=compact
   → Solo guarda el último valor por cada key
   → Útil para tablas de estado (CDC)
```

---

## 8.4 - Kafka con Docker Compose

### Stack mínimo para desarrollo

Para este curso usamos **KRaft mode** (sin ZooKeeper) con la imagen oficial de Apache:

```yaml
# docker-compose.kafka.yml
# Stack Kafka + Kafka UI para desarrollo local

services:

  # ================================================================
  # KAFKA (modo KRaft - sin ZooKeeper)
  # ================================================================
  kafka:
    image: apache/kafka:3.7.0
    container_name: kafka
    hostname: kafka
    ports:
      - "9092:9092"      # Puerto para clientes externos
      - "9093:9093"      # Puerto para controlador
    environment:
      # Configuración KRaft
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      # Listeners
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT

      # Configuración de logs
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_LOG_RETENTION_HOURS: 168  # 7 días

      # Formato de cluster
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
    volumes:
      - kafka_data:/var/lib/kafka/data
    networks:
      - bigdata_network
    healthcheck:
      test: ["CMD-SHELL", "/opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092"]
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 30s

  # ================================================================
  # KAFKA UI - Interfaz web para gestionar Kafka
  # ================================================================
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    ports:
      - "8088:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
    depends_on:
      kafka:
        condition: service_healthy
    networks:
      - bigdata_network

volumes:
  kafka_data:

networks:
  bigdata_network:
    external: true
    name: bigdata_curso_network
```

### Comandos básicos

```bash
# Levantar Kafka
docker compose -f docker-compose.kafka.yml up -d

# Ver logs
docker logs -f kafka

# Crear un topic
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic eventos_economicos \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# Listar topics
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092

# Describir un topic
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --describe \
  --topic eventos_economicos \
  --bootstrap-server localhost:9092

# Producir mensajes desde consola
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \
  --topic eventos_economicos \
  --bootstrap-server localhost:9092

# Consumir mensajes desde consola
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic eventos_economicos \
  --from-beginning \
  --bootstrap-server localhost:9092

# Apagar
docker compose -f docker-compose.kafka.yml down
```

### Verificación

Después de levantar el stack:

1. **Kafka UI**: http://localhost:8088
   - Ver topics, particiones, mensajes
   - Monitorear consumers y lag

2. **Healthcheck**: El broker tarda ~30 segundos en estar listo

---

## 8.5 - Productores y Consumidores en Python

### Instalación

```bash
pip install confluent-kafka
```

### Producer básico

```python
"""
producer_basico.py - Enviar eventos a Kafka
"""
from confluent_kafka import Producer
import json
import time

# Configuración
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'producer-qog'
}

# Crear producer
producer = Producer(config)

# Callback para confirmación
def delivery_report(err, msg):
    if err:
        print(f'Error: {err}')
    else:
        print(f'Enviado: {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

# Enviar eventos
eventos = [
    {"pais": "ARG", "indicador": "inflacion", "valor": 5.2, "anio": 2024},
    {"pais": "BRA", "indicador": "pib_growth", "valor": 2.1, "anio": 2024},
    {"pais": "CHL", "indicador": "desempleo", "valor": 8.5, "anio": 2024},
]

for evento in eventos:
    producer.produce(
        topic='eventos_economicos',
        key=evento['pais'].encode('utf-8'),      # Key para particionado
        value=json.dumps(evento).encode('utf-8'), # Payload
        callback=delivery_report
    )

# Esperar a que se envíen todos
producer.flush()
print("Todos los eventos enviados.")
```

### Consumer básico

```python
"""
consumer_basico.py - Leer eventos de Kafka
"""
from confluent_kafka import Consumer, KafkaError
import json

# Configuración
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-analisis',
    'auto.offset.reset': 'earliest',  # Leer desde el inicio
    'enable.auto.commit': True
}

# Crear consumer
consumer = Consumer(config)

# Suscribirse al topic
consumer.subscribe(['eventos_economicos'])

print("Esperando eventos... (Ctrl+C para salir)")

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Esperar 1 segundo

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f'Fin de partición {msg.partition()}')
            else:
                print(f'Error: {msg.error()}')
            continue

        # Procesar mensaje
        key = msg.key().decode('utf-8') if msg.key() else None
        value = json.loads(msg.value().decode('utf-8'))

        print(f"""
        Topic: {msg.topic()}
        Partición: {msg.partition()}
        Offset: {msg.offset()}
        Key: {key}
        Valor: {value}
        """)

except KeyboardInterrupt:
    print("Deteniendo consumer...")

finally:
    consumer.close()
```

---

## 8.6 - Spark Structured Streaming + Kafka

### Concepto

Spark Structured Streaming trata un stream como una **tabla infinita** donde
continuamente se agregan filas:

```
Stream como tabla infinita:

Tiempo t=0:
┌─────┬───────┬───────┐
│ pais│ valor │ ts    │
├─────┼───────┼───────┤
│ ARG │  5.2  │ 00:01 │
└─────┴───────┴───────┘

Tiempo t=1: (llega nuevo evento)
┌─────┬───────┬───────┐
│ pais│ valor │ ts    │
├─────┼───────┼───────┤
│ ARG │  5.2  │ 00:01 │
│ BRA │  2.1  │ 00:02 │  ← nuevo
└─────┴───────┴───────┘

Tiempo t=2: (llegan más)
┌─────┬───────┬───────┐
│ pais│ valor │ ts    │
├─────┼───────┼───────┤
│ ARG │  5.2  │ 00:01 │
│ BRA │  2.1  │ 00:02 │
│ CHL │  8.5  │ 00:03 │  ← nuevo
│ ARG │  5.5  │ 00:03 │  ← nuevo
└─────┴───────┴───────┘

Las queries sobre esta "tabla" se re-ejecutan continuamente.
```

### Ejemplo: Leer de Kafka con Spark

```python
"""
spark_kafka_consumer.py - Leer stream de Kafka con Spark
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Crear SparkSession con soporte Kafka
spark = SparkSession.builder \
    .appName("Kafka-Spark-Streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Leer stream de Kafka
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "eventos_economicos") \
    .option("startingOffsets", "earliest") \
    .load()

# Esquema del JSON
schema = StructType([
    StructField("pais", StringType()),
    StructField("indicador", StringType()),
    StructField("valor", DoubleType()),
    StructField("anio", IntegerType())
])

# Parsear el JSON
df_parsed = df_stream \
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp") \
    .select(
        col("key").alias("pais_key"),
        from_json(col("value"), schema).alias("data"),
        col("timestamp")
    ) \
    .select("pais_key", "data.*", "timestamp")

# Agregación con ventana de tiempo
df_agregado = df_parsed \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "30 seconds"),
        col("pais")
    ) \
    .agg(
        avg("valor").alias("valor_promedio"),
        count("*").alias("num_eventos")
    )

# Escribir a consola (para debug)
query = df_agregado.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

---

## 8.7 - Proyecto: Observatorio Económico en Tiempo Real

### Descripción

Construirás un sistema que simula la llegada de datos económicos en tiempo real
y los procesa para generar alertas y dashboards actualizados.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 OBSERVATORIO ECONÓMICO EN TIEMPO REAL                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────────────┐     │
│   │  Simulador  │      │    KAFKA    │      │   Spark Streaming   │     │
│   │  de Datos   │ ───→ │             │ ───→ │                     │     │
│   │  (Python)   │      │  Topic:     │      │  - Agregaciones     │     │
│   │             │      │  eventos_   │      │  - Alertas          │     │
│   │ QoG data +  │      │  qog        │      │  - Métricas         │     │
│   │ variación   │      │             │      │                     │     │
│   │ aleatoria   │      │             │      │                     │     │
│   └─────────────┘      └─────────────┘      └──────────┬──────────┘     │
│                                                        │                │
│                                              ┌─────────▼─────────┐      │
│                                              │    PostgreSQL     │      │
│                                              │                   │      │
│                                              │  - alertas        │      │
│                                              │  - metricas_15min │      │
│                                              │  - ultimos_valores│      │
│                                              └───────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Archivos del proyecto

```
08_streaming_kafka/
├── README.md                    # Este archivo
├── docker-compose.kafka.yml     # Stack Kafka + UI
├── simulador/
│   ├── simulador_qog.py         # Genera eventos simulados
│   └── config.py                # Países y variables a simular
├── procesador/
│   ├── spark_streaming.py       # Lee Kafka, procesa, guarda en PG
│   └── alertas.py               # Lógica de alertas
└── ejercicios/
    ├── 01_producer_basico.py
    ├── 02_consumer_basico.py
    ├── 03_spark_kafka.py
    └── 04_observatorio_completo.py
```

### Entregables

1. **docker-compose.kafka.yml** funcionando
2. **Simulador** que envíe al menos 100 eventos/minuto
3. **Procesador Spark** que:
   - Calcule promedios por país en ventanas de 30 segundos
   - Genere alertas cuando un indicador supere umbral
   - Guarde resultados en PostgreSQL
4. **Captura de pantalla** de Kafka UI mostrando mensajes fluyendo

---

## Referencias

1. Kreps, J. (2011). *The Log: What every software engineer should know about real-time data's unifying abstraction*. LinkedIn Engineering Blog.

2. Narkhede, N., Shapira, G., & Palino, T. (2017). *Kafka: The Definitive Guide*. O'Reilly Media.

3. Kleppmann, M. (2017). *Designing Data-Intensive Applications*, Chapter 11: Stream Processing. O'Reilly Media.

4. Chambers, B., & Zaharia, M. (2018). *Spark: The Definitive Guide*, Chapter 21-23: Structured Streaming. O'Reilly Media.

5. Apache Kafka Documentation: https://kafka.apache.org/documentation/

6. Confluent Kafka Python Client: https://docs.confluent.io/kafka-clients/python/current/overview.html

7. Spark Structured Streaming + Kafka: https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html

---

**Siguiente módulo:** [Módulo 09 - Cloud Engineering con LocalStack](../09_cloud_localstack/README.md)

---

---
**Curso:** Big Data con Python - De Cero a Producción
**Profesor:** Juan Marcelo Gutiérrez Miranda | @TodoEconometria
**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
**Metodología:** Ejercicios progresivos con datos reales y herramientas profesionales

**Referencias académicas:**
- Kreps, J., Narkhede, N., & Rao, J. (2011). Kafka: a Distributed Messaging System for Log Processing. NetDB Workshop.
- Akidau, T., et al. (2015). The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing. VLDB.
- Zaharia, M., et al. (2016). Apache Spark: A Unified Engine for Big Data Processing. Communications of the ACM, 59(11), 56-65.
---
