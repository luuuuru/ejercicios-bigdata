# Ejercicio 3.3: Hadoop HDFS

Duración estimada: 6 horas

## Objetivos

- Entender sistemas de archivos distribuidos
- Trabajar con HDFS (Hadoop Distributed File System)
- Subir y leer archivos desde HDFS
- Ejecutar MapReduce básico

## Requisitos Previos

Docker Desktop instalado y funcionando.

## Levantar Hadoop

Desde el directorio donde se generó tu `docker-compose.yml` (ver [Infraestructura](../../../docs/infraestructura.md)):

```bash
docker compose up -d namenode datanode1 datanode2
```

Web UI: http://localhost:9870

## Tareas

### 1. Operaciones Básicas HDFS (2h)

Comandos a practicar:
```bash
# Ver archivos
docker exec -it curso_namenode hdfs dfs -ls /

# Crear directorio
docker exec -it curso_namenode hdfs dfs -mkdir /user/data

# Subir archivo
docker exec -it curso_namenode hdfs dfs -put /ruta/local/file.txt /user/data/

# Descargar archivo
docker exec -it curso_namenode hdfs dfs -get /user/data/file.txt /ruta/local/

# Ver contenido
docker exec -it curso_namenode hdfs dfs -cat /user/data/file.txt

# Borrar archivo
docker exec -it curso_namenode hdfs dfs -rm /user/data/file.txt
```

Entregable: Script `hdfs_operations.sh` con todos los comandos

### 2. Subir Dataset Grande (2h)

Subir un dataset de 1GB+ a HDFS desde Python.

```python
from hdfs import InsecureClient

client = InsecureClient('http://localhost:9870', user='root')
client.upload('/user/data/dataset.csv', 'local_dataset.csv')
```

Entregable: `subir_archivo_hdfs.py`

### 3. MapReduce WordCount (2h)

Implementar el clásico WordCount con MapReduce.

Entregable: `mapreduce_wordcount.py`

## Recursos

- HDFS Commands: https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html
- Python HDFS Client: https://hdfscli.readthedocs.io/

---

Siguiente: [Ejercicio 3.4 - PySpark Básico](../3.4_pyspark_basico/README.md)
