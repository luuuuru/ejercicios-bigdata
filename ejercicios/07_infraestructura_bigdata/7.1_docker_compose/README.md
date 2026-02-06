# 7.1 Docker Compose: Contenedores y Orquestacion de Servicios

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

Nivel: Intermedio
Tipo: Teorico-Conceptual con ejemplos practicos

---

## Indice

1. [7.1.1 - Que es Docker y por que existe](#711-que-es-docker-y-por-que-existe)
2. [7.1.2 - Imagenes y contenedores](#712-imagenes-y-contenedores)
3. [7.1.3 - Docker Compose: orquestando servicios](#713-docker-compose-orquestando-servicios)
4. [7.1.4 - Ejemplo completo comentado](#714-ejemplo-completo-comentado)
5. [7.1.5 - Redes en Docker](#715-redes-en-docker)
6. [7.1.6 - Volumenes](#716-volumenes)
7. [7.1.7 - Comandos esenciales](#717-comandos-esenciales)
8. [7.1.8 - Errores comunes y como resolverlos](#718-errores-comunes-y-como-resolverlos)
9. [7.1.9 - Principio de orquestacion](#719-principio-de-orquestacion)
10. [7.1.10 - Patrones utiles](#7110-patrones-utiles)

---

## 7.1.1 Que es Docker y por que existe

### El problema: "En mi maquina funciona"

Toda persona que ha trabajado en equipo con software conoce esta situacion:

```
Desarrollador A:  "El script funciona perfecto."
Desarrollador B:  "A mi me da error. Que version de Python tienes?"
Desarrollador A:  "3.11"
Desarrollador B:  "Yo tengo 3.8... y no tengo instalada la libreria X."
```

Este fenomeno se conoce como **dependency hell** (infierno de dependencias). El software
no solo depende de su propio codigo, sino de:

- La version del lenguaje (Python 3.8 vs 3.11)
- Las librerias instaladas (y sus versiones exactas)
- El sistema operativo (Windows vs Linux vs macOS)
- Variables de entorno, puertos, rutas de archivos
- Servicios externos (bases de datos, colas de mensajes)

Docker resuelve esto **empaquetando la aplicacion junto con TODAS sus dependencias**
en una unidad estandarizada llamada **contenedor**.

### La analogia del contenedor de barco

Antes de que existieran los contenedores intermodales (inventados en 1956 por
Malcolm McLean), el comercio maritimo era caotico. Cada producto tenia forma,
tamano y empaque diferente. Cargar un barco tomaba dias.

```
ANTES de los contenedores:                DESPUES de los contenedores:
+-------+                                 +----------+----------+
| Sacos |  +---------+                     |          |          |
+-------+  | Barriles|  +------+           | CONTENEDOR ESTANDAR |
           +---------+  |Cajas |           |          |          |
  +----+                +------+           +----------+----------+
  |Otro|   = CAOS, lento, caro            = Rapido, estandar, eficiente
  +----+
```

Docker hace exactamente lo mismo con el software: sin importar que haya dentro
(Python, Java, PostgreSQL, Spark), el contenedor tiene un formato estandar que
cualquier maquina con Docker puede ejecutar.

### Contenedores vs Maquinas Virtuales

Es comun confundir contenedores con maquinas virtuales (VMs). Ambos aislan
software, pero de maneras fundamentalmente diferentes:

```
     MAQUINA VIRTUAL                         CONTENEDOR
+------------------------+           +------------------------+
|     Aplicacion A       |           |     Aplicacion A       |
+------------------------+           +------------------------+
|   Librerias/Bins       |           |   Librerias/Bins       |
+------------------------+           +------------------------+
|  Sistema Operativo     |           |                        |
|  Invitado (Ubuntu,     |           |  (Comparte el kernel   |
|   Windows, etc.)       |           |   del host)            |
+------------------------+           +------------------------+
|     Hypervisor         |           |     Docker Engine      |
+------------------------+           +------------------------+
|  Sistema Operativo     |           |  Sistema Operativo     |
|       Host             |           |       Host             |
+------------------------+           +------------------------+
|      Hardware          |           |      Hardware          |
+------------------------+           +------------------------+

Peso: ~GBs                           Peso: ~MBs
Arranque: minutos                    Arranque: segundos
Overhead: alto                       Overhead: minimo
```

**Diferencia clave:** una VM virtualiza todo el hardware e incluye un sistema
operativo completo. Un contenedor comparte el kernel del sistema host y solo
aisla los procesos y el sistema de archivos. Por eso los contenedores son
mucho mas ligeros y rapidos.

**Para Big Data esto es critico:** levantar un cluster de 5 nodos Spark con
VMs requeriria 5 sistemas operativos completos. Con contenedores, esos 5
nodos comparten el mismo kernel y arrancan en segundos.

---

## 7.1.2 Imagenes y contenedores

### Que es una imagen

Una **imagen** de Docker es una **plantilla inmutable** (de solo lectura) que
contiene todo lo necesario para ejecutar una aplicacion:

- Sistema de archivos base (ej: Ubuntu, Alpine Linux)
- Lenguaje de programacion instalado
- Librerias y dependencias
- Codigo de la aplicacion
- Configuracion de como ejecutarse

Piensa en una imagen como una **receta de cocina**: describe exactamente que
ingredientes se necesitan y como prepararlos, pero no es el plato servido.

### Que es un contenedor

Un **contenedor** es una **instancia en ejecucion** de una imagen. Es el
"plato servido". Cuando ejecutas `docker run postgres`, Docker:

1. Toma la imagen `postgres`
2. Crea una capa de escritura sobre ella
3. Inicia el proceso principal (el servidor PostgreSQL)

```
         IMAGEN                    CONTENEDORES
    (plantilla, fija)        (instancias vivas, multiples)

    +---------------+         +---------------+
    |   postgres    |  --->   | contenedor_1  |  (bd desarrollo)
    |   :16         |  --->   | contenedor_2  |  (bd testing)
    +---------------+  --->   | contenedor_3  |  (bd produccion)
                              +---------------+

    UNA imagen puede generar N contenedores independientes.
    Cada contenedor tiene su propio estado (datos, logs, etc.)
```

### El Dockerfile: como se construye una imagen

Un **Dockerfile** es un archivo de texto que describe, paso a paso, como
construir una imagen. Cada instruccion crea una **capa** (layer).

```dockerfile
# Dockerfile basico para una app Python
FROM python:3.11-slim          # Capa 1: imagen base (Python sobre Debian)
WORKDIR /app                   # Capa 2: crear directorio de trabajo
COPY requirements.txt .        # Capa 3: copiar archivo de dependencias
RUN pip install -r requirements.txt  # Capa 4: instalar dependencias
COPY . .                       # Capa 5: copiar codigo fuente
EXPOSE 8000                    # Documentar que el contenedor usa el puerto 8000
CMD ["python", "app.py"]       # Comando por defecto al ejecutar el contenedor
```

### Capas: por que importan

Cada instruccion del Dockerfile crea una capa inmutable. Docker **cachea**
estas capas. Si no cambias `requirements.txt`, Docker no reinstala las
dependencias (reutiliza la capa cacheada).

```
+-----------------------------------+
|  CMD ["python", "app.py"]         |  <-- Capa 5 (cambia seguido)
+-----------------------------------+
|  COPY . .                         |  <-- Capa 4 (cambia seguido)
+-----------------------------------+
|  RUN pip install -r requirements  |  <-- Capa 3 (cambia poco)
+-----------------------------------+
|  COPY requirements.txt .          |  <-- Capa 2 (cambia poco)
+-----------------------------------+
|  FROM python:3.11-slim            |  <-- Capa 1 (casi nunca cambia)
+-----------------------------------+

Regla de oro: las instrucciones que cambian MAS van al FINAL.
Asi Docker reutiliza las capas superiores (cache).
```

### Docker Hub: el repositorio de imagenes

[Docker Hub](https://hub.docker.com/) es un registro publico donde se
almacenan imagenes listas para usar. Imagenes oficiales comunes:

| Imagen | Que es | Uso tipico |
|--------|--------|------------|
| `postgres:16` | Base de datos PostgreSQL | Almacenamiento relacional |
| `python:3.11-slim` | Python sobre Debian minimal | Apps Python |
| `bitnami/spark:3.5` | Apache Spark | Procesamiento distribuido |
| `dpage/pgadmin4` | pgAdmin (interfaz web para PostgreSQL) | Administracion BD |
| `redis:7` | Base de datos en memoria | Cache, colas |
| `nginx:latest` | Servidor web | Proxy reverso, servir archivos |

La notacion `imagen:tag` indica la version. `postgres:16` es PostgreSQL
version 16. `latest` es la ultima version disponible (no recomendado en
produccion porque puede cambiar sin aviso).

---

## 7.1.3 Docker Compose: orquestando servicios

### El problema que resuelve

Un sistema real casi nunca es un solo contenedor. Un pipeline de Big Data
tipico necesita:

- Una base de datos (PostgreSQL)
- Una interfaz de administracion (pgAdmin)
- Un procesador de datos (Spark master + workers)
- Quiza un broker de mensajes (Kafka)

Sin Docker Compose, habria que ejecutar cada contenedor manualmente:

```bash
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name pgadmin -p 8080:80 -e PGADMIN_EMAIL=admin@test.com dpage/pgadmin4
docker run -d --name spark-master -p 8081:8080 bitnami/spark:3.5
# ... y asi por cada servicio, recordando todos los parametros
```

Docker Compose permite definir **todos los servicios en un solo archivo YAML**
y levantarlos con **un solo comando**: `docker compose up`.

### Estructura del archivo docker-compose.yml

Vamos a analizar cada directiva del YAML linea por linea.

#### `services` (antes se usaba `version`)

```yaml
services:          # Bloque principal: define los servicios (contenedores)
  mi_servicio:     # Nombre logico del servicio
    ...
```

> **Nota:** En versiones antiguas de Compose se requeria declarar `version: "3.8"` al
> inicio del archivo. Desde Docker Compose V2 (2023+), el campo `version` es
> **opcional y esta deprecado**. Se puede omitir.

#### `image` vs `build`

```yaml
services:
  # Opcion 1: Usar una imagen existente de Docker Hub
  postgres:
    image: postgres:16

  # Opcion 2: Construir la imagen desde un Dockerfile local
  mi_app:
    build:
      context: ./app           # Directorio donde esta el Dockerfile
      dockerfile: Dockerfile   # Nombre del Dockerfile (opcional si es el default)
```

Usa `image` cuando existe una imagen oficial que sirve tal cual.
Usa `build` cuando necesitas una imagen personalizada (tu propia app).

#### `ports` (mapeo de puertos)

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"    # formato:  "PUERTO_HOST:PUERTO_CONTENEDOR"
```

```
   Tu maquina (host)              Contenedor
  +------------------+          +------------------+
  |                  |          |                  |
  |  localhost:5432 ------>------ :5432 (postgres) |
  |                  |          |                  |
  +------------------+          +------------------+

  Si el puerto 5432 del host ya esta ocupado, puedes cambiar solo el del host:
  "5433:5432"  --> accedes por localhost:5433, pero el contenedor sigue en 5432
```

#### `environment` (variables de entorno)

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: alumno           # Usuario de la base de datos
      POSTGRES_PASSWORD: bigdata2026  # Contrasena (nunca hardcodear en produccion)
      POSTGRES_DB: curso_bigdata      # Nombre de la base de datos inicial
```

Las variables de entorno son el mecanismo estandar para configurar contenedores.
Cada imagen documenta que variables acepta.

#### `volumes` (persistencia de datos)

```yaml
services:
  postgres:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data    # Named volume
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # Bind mount

volumes:
  pgdata:         # Declarar el named volume al nivel superior
```

Sin volumes, los datos se **pierden** al eliminar el contenedor.
Los volumes persisten datos mas alla del ciclo de vida del contenedor.
(Se explican en detalle en la seccion 7.1.6.)

#### `networks` (comunicacion entre contenedores)

```yaml
services:
  postgres:
    image: postgres:16
    networks:
      - red_bigdata

  pgadmin:
    image: dpage/pgadmin4
    networks:
      - red_bigdata        # Mismo nombre de red = se pueden comunicar

networks:
  red_bigdata:
    driver: bridge         # Tipo de red (bridge es el default)
```

Los contenedores en la misma red se ven entre si **por nombre del servicio**.
pgAdmin puede conectarse a PostgreSQL usando el hostname `postgres` (no una IP).

#### `depends_on` (orden de arranque)

```yaml
services:
  postgres:
    image: postgres:16

  pgadmin:
    image: dpage/pgadmin4
    depends_on:
      - postgres           # pgadmin arranca DESPUES de postgres
```

**CUIDADO:** `depends_on` solo garantiza que el contenedor se **inicie** despues.
NO garantiza que el servicio dentro este **listo** para recibir conexiones.
PostgreSQL puede tardar varios segundos en estar disponible despues de arrancar.
Para eso existe `healthcheck`.

#### `healthcheck` (verificar que el servicio esta listo)

```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U alumno"]   # Comando para verificar
      interval: 10s        # Ejecutar cada 10 segundos
      timeout: 5s          # Si tarda mas de 5s, fallo
      retries: 5           # Intentar 5 veces antes de declarar "unhealthy"
      start_period: 30s    # Esperar 30s antes de empezar a verificar

  pgadmin:
    image: dpage/pgadmin4
    depends_on:
      postgres:
        condition: service_healthy  # Esperar a que postgres este HEALTHY
```

Este es el patron correcto: `healthcheck` + `depends_on` con `condition`.
Asi pgAdmin no intenta conectarse a PostgreSQL antes de que este listo.

#### `restart` (politicas de reinicio)

```yaml
services:
  postgres:
    image: postgres:16
    restart: unless-stopped    # Reiniciar siempre, excepto si se detuvo manualmente
```

| Politica | Comportamiento |
|----------|---------------|
| `no` | No reiniciar (default) |
| `always` | Reiniciar siempre, incluso si se detuvo manualmente |
| `on-failure` | Reiniciar solo si el proceso termino con error (exit code != 0) |
| `unless-stopped` | Reiniciar siempre, excepto si se detuvo con `docker stop` |

#### `container_name` (nombre personalizado)

```yaml
services:
  postgres:
    image: postgres:16
    container_name: bd_curso_bigdata   # Nombre fijo para el contenedor
```

Sin esto, Docker genera nombres automaticos como `7.1_docker_compose-postgres-1`.
Usar `container_name` hace mas facil identificar contenedores en `docker ps`.

#### `command` y `entrypoint`

```yaml
services:
  mi_app:
    image: python:3.11-slim
    command: ["python", "analisis.py", "--verbose"]  # Sobreescribe el CMD del Dockerfile
```

- **`entrypoint`**: el ejecutable principal del contenedor (ej: `python`)
- **`command`**: los argumentos que recibe (ej: `analisis.py --verbose`)
- En la practica, `command` es lo que mas se sobreescribe en Compose

---

## 7.1.4 Ejemplo completo comentado

Este ejemplo levanta tres servicios: PostgreSQL, una aplicacion Python y pgAdmin.
**Cada linea esta explicada** con comentarios.

```yaml
# ============================================================
# docker-compose.yml - Pipeline basico de Big Data
# Curso: Big Data con Python - Prof. Gutierrez Miranda
# ============================================================

services:

  # ----------------------------------------------------------
  # SERVICIO 1: Base de datos PostgreSQL
  # ----------------------------------------------------------
  postgres:
    image: postgres:16                          # Imagen oficial de PostgreSQL v16
    container_name: bigdata_postgres            # Nombre facil de identificar
    restart: unless-stopped                     # Reiniciar si se cae, salvo stop manual
    environment:                                # Variables de configuracion
      POSTGRES_USER: alumno                     # Usuario de la BD
      POSTGRES_PASSWORD: bigdata2026            # Contrasena (en produccion, usar secrets)
      POSTGRES_DB: curso_bigdata                # BD que se crea automaticamente al inicio
    ports:
      - "5432:5432"                             # Exponer puerto para herramientas locales
    volumes:
      - pgdata:/var/lib/postgresql/data         # Persistir datos en un named volume
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql  # Script SQL de inicializacion
    networks:
      - red_bigdata                             # Conectar a la red interna
    healthcheck:                                # Verificar que PostgreSQL esta listo
      test: ["CMD-SHELL", "pg_isready -U alumno -d curso_bigdata"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ----------------------------------------------------------
  # SERVICIO 2: Aplicacion Python (ETL)
  # ----------------------------------------------------------
  app_etl:
    build:                                      # Construir imagen desde Dockerfile local
      context: ./app                            # Directorio con el Dockerfile
      dockerfile: Dockerfile                    # Nombre del Dockerfile
    container_name: bigdata_etl                 # Nombre del contenedor
    environment:
      DB_HOST: postgres                         # Hostname = nombre del servicio en Compose
      DB_PORT: 5432                             # Puerto INTERNO del contenedor postgres
      DB_USER: alumno
      DB_PASSWORD: bigdata2026
      DB_NAME: curso_bigdata
    volumes:
      - ./app:/app                              # Bind mount: editar codigo sin rebuild
      - ./datos:/datos                          # Montar directorio de datos
    networks:
      - red_bigdata
    depends_on:                                 # Orden de arranque
      postgres:
        condition: service_healthy              # Esperar a que postgres este healthy
    command: ["python", "etl_pipeline.py"]      # Comando a ejecutar

  # ----------------------------------------------------------
  # SERVICIO 3: pgAdmin (interfaz web para PostgreSQL)
  # ----------------------------------------------------------
  pgadmin:
    image: dpage/pgadmin4:latest                # Imagen oficial de pgAdmin
    container_name: bigdata_pgadmin             # Nombre del contenedor
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@curso.com    # Email para login en pgAdmin
      PGADMIN_DEFAULT_PASSWORD: admin123        # Contrasena de pgAdmin
    ports:
      - "8080:80"                               # pgAdmin escucha en puerto 80 interno
    networks:
      - red_bigdata
    depends_on:
      - postgres                                # Arrancar despues de postgres

# ============================================================
# VOLUMENES: Persistencia de datos
# ============================================================
volumes:
  pgdata:                                       # Docker gestiona este volumen
    driver: local                               # Almacenamiento local (default)

# ============================================================
# REDES: Comunicacion entre servicios
# ============================================================
networks:
  red_bigdata:                                  # Red interna para los 3 servicios
    driver: bridge                              # Tipo bridge (default para Compose)
```

### Como levantar este stack

```bash
# Levantar todos los servicios (en segundo plano)
docker compose up -d

# Verificar que estan corriendo
docker compose ps

# Ver los logs en tiempo real
docker compose logs -f

# Acceder a pgAdmin en el navegador:  http://localhost:8080
# Acceder a PostgreSQL desde el host: localhost:5432
```

### Diagrama de la arquitectura

```
   +--------------------------------------------------+
   |             RED: red_bigdata (bridge)             |
   |                                                  |
   |  +-----------+    +-----------+    +-----------+ |
   |  | postgres  |    | app_etl   |    | pgadmin   | |
   |  | :5432     |<---| (Python)  |    | :80       | |
   |  |           |<---|           |    |           |-+--> localhost:8080
   |  |           |    |           |    |           | |
   |  +-----------+    +-----------+    +-----------+ |
   |       |                                          |
   +-------|------------------------------------------+
           |
     +-----v-----+
     |  pgdata   |  (volumen persistente)
     |  (volume) |
     +-----------+

   El host accede a pgAdmin por localhost:8080
   El host accede a PostgreSQL por localhost:5432
   app_etl se conecta a postgres usando el hostname "postgres" (DNS interno)
   pgAdmin se conecta a postgres usando el hostname "postgres" (DNS interno)
```

---

## 7.1.5 Redes en Docker

### Tipos de red

| Tipo | Descripcion | Uso tipico |
|------|-------------|------------|
| `bridge` | Red aislada en una sola maquina. Los contenedores se comunican entre si. | Desarrollo local, Docker Compose |
| `host` | El contenedor comparte la red del host (sin aislamiento). | Rendimiento maximo, sin mapeo de puertos |
| `overlay` | Red que abarca multiples maquinas (hosts). | Docker Swarm, clusters |
| `none` | Sin red. El contenedor esta completamente aislado. | Seguridad extrema, procesamiento offline |

En Docker Compose, la red por defecto es `bridge`. Es la que se usa en el
99% de los casos de desarrollo y aprendizaje.

### DNS interno: comunicacion por nombre

Cuando dos contenedores estan en la misma red de Docker Compose, pueden
comunicarse usando el **nombre del servicio** como hostname.

```
   Dentro del contenedor "app_etl":

   psycopg2.connect(
       host="postgres",          # <-- Nombre del servicio, NO una IP
       port=5432,
       user="alumno",
       password="bigdata2026",
       dbname="curso_bigdata"
   )
```

Docker mantiene un **servidor DNS interno** que resuelve automaticamente
el nombre `postgres` a la IP interna del contenedor de PostgreSQL.

### Por que no necesitas IPs

Las IPs internas de los contenedores son **dinamicas**: cambian cada vez que
se recrean los contenedores. Depender de una IP es fragil. El DNS interno
de Docker resuelve esto automaticamente.

```
   INCORRECTO (fragil):
   host="172.18.0.2"    # Esta IP puede cambiar en cualquier momento

   CORRECTO (robusto):
   host="postgres"      # Docker resuelve el nombre al IP actual
```

### Red por defecto vs red personalizada

Docker Compose crea automaticamente una red por defecto llamada
`<nombre_proyecto>_default`. Todos los servicios se conectan a ella.
Declarar redes explicitamente es opcional, pero es buena practica porque:

1. Documenta la arquitectura
2. Permite separar grupos de servicios (ej: red publica vs red interna)
3. Facilita el debugging

---

## 7.1.6 Volumenes

### El problema: datos efimeros

Por defecto, todo lo que un contenedor escribe en su sistema de archivos
**se pierde** cuando el contenedor se elimina. Esto es un problema para
bases de datos, archivos de configuracion, logs, etc.

```
   SIN volumen:
   docker compose down   -->   Base de datos VACIA (datos perdidos)
   docker compose up     -->   Hay que cargar todo de nuevo

   CON volumen:
   docker compose down   -->   Datos seguros en el volumen
   docker compose up     -->   La BD retoma donde quedo
```

### Tipos de volumenes

#### 1. Named Volumes (volumenes con nombre)

Docker gestiona completamente donde se almacenan los datos.

```yaml
services:
  postgres:
    volumes:
      - pgdata:/var/lib/postgresql/data   # "pgdata" es el nombre del volumen

volumes:
  pgdata:       # Declarar al nivel superior
```

**Cuando usarlo:** Bases de datos, datos que deben persistir pero no necesitas
acceder directamente desde tu maquina.

#### 2. Bind Mounts (montar directorio del host)

Conecta un directorio de tu maquina directamente al contenedor.

```yaml
services:
  app:
    volumes:
      - ./codigo:/app          # Directorio local "./codigo" se monta en "/app"
      - ./datos:/datos         # Directorio local "./datos" se monta en "/datos"
```

**Cuando usarlo:** Desarrollo (editar codigo en tu IDE y que el contenedor lo
vea en tiempo real), compartir datasets entre host y contenedor.

#### 3. tmpfs (memoria temporal)

Monta un directorio en memoria RAM. Los datos desaparecen al apagar el
contenedor.

```yaml
services:
  app:
    tmpfs:
      - /tmp                   # /tmp vive en RAM, no en disco
```

**Cuando usarlo:** Datos temporales sensibles que no deben escribirse a disco
(tokens, archivos de sesion), o para mejorar rendimiento de escritura.

### Comparacion de tipos

```
   +------------------+-------------------+-------------------+
   |  Named Volume    |  Bind Mount       |  tmpfs            |
   +------------------+-------------------+-------------------+
   |  Docker gestiona |  Tu eliges la     |  Vive en RAM      |
   |  la ubicacion    |  ruta del host    |                   |
   |                  |                   |                   |
   |  Persistente     |  Persistente      |  Efimero          |
   |                  |                   |                   |
   |  Ideal para BD   |  Ideal para       |  Ideal para       |
   |  y datos criticos|  desarrollo       |  datos temporales |
   +------------------+-------------------+-------------------+
```

---

## 7.1.7 Comandos esenciales

### Comandos de Docker Compose

| Comando | Que hace |
|---------|----------|
| `docker compose up` | Levanta todos los servicios definidos en el YAML |
| `docker compose up -d` | Igual, pero en segundo plano (detached) |
| `docker compose down` | Detiene y elimina los contenedores y redes |
| `docker compose down -v` | Igual, pero TAMBIEN elimina los volumenes (datos) |
| `docker compose ps` | Lista los contenedores del proyecto y su estado |
| `docker compose logs` | Muestra los logs de todos los servicios |
| `docker compose logs -f postgres` | Sigue los logs de un servicio especifico |
| `docker compose exec postgres bash` | Abre una terminal dentro del contenedor |
| `docker compose exec postgres psql -U alumno` | Ejecutar psql dentro del contenedor |
| `docker compose build` | Reconstruye las imagenes (sin levantar) |
| `docker compose restart` | Reinicia todos los servicios |
| `docker compose stop` | Detiene sin eliminar (se puede reanudar con start) |
| `docker compose start` | Reanuda servicios detenidos con stop |

### Comandos de Docker (nivel contenedor individual)

| Comando | Que hace |
|---------|----------|
| `docker ps` | Lista contenedores en ejecucion |
| `docker ps -a` | Lista TODOS los contenedores (incluso los detenidos) |
| `docker images` | Lista las imagenes descargadas |
| `docker volume ls` | Lista los volumenes |
| `docker network ls` | Lista las redes |
| `docker system prune` | Elimina contenedores, imagenes y redes sin uso |
| `docker system prune -a --volumes` | Limpieza profunda (elimina TODO lo no usado) |

### Flujo tipico de trabajo

```bash
# 1. Levantar el stack
docker compose up -d

# 2. Verificar que todo esta corriendo
docker compose ps

# 3. Ver logs si algo falla
docker compose logs -f

# 4. Entrar a un contenedor para depurar
docker compose exec postgres psql -U alumno -d curso_bigdata

# 5. Cuando terminas de trabajar
docker compose down

# 6. Si quieres empezar de cero (BORRA datos)
docker compose down -v
```

---

## 7.1.8 Errores comunes y como resolverlos

### Error 1: Puerto ocupado

```
Error: Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Causa:** Ya hay algo escuchando en el puerto 5432 de tu maquina (quiza
otra instancia de PostgreSQL, o un contenedor anterior que no se detuvo).

**Solucion:**
```bash
# Opcion A: Cambiar el puerto del host en el YAML
ports:
  - "5433:5432"    # Usar 5433 en vez de 5432

# Opcion B: Buscar y detener lo que ocupa el puerto
# En Windows:
netstat -ano | findstr :5432
# En Linux/Mac:
lsof -i :5432
```

### Error 2: Contenedor no arranca (sale con exit code)

```
bigdata_etl exited with code 1
```

**Causa:** Error en el codigo o en la configuracion.

**Solucion:**
```bash
# Ver los logs del contenedor que fallo
docker compose logs app_etl

# Ejecutar manualmente para depurar
docker compose run --rm app_etl bash
# (Esto abre una terminal dentro del contenedor para investigar)
```

### Error 3: "Connection refused" entre servicios

```
psycopg2.OperationalError: could not connect to server: Connection refused
    Is the server running on host "postgres" and accepting TCP/IP connections on port 5432?
```

**Causas posibles:**
1. PostgreSQL aun no esta listo (solucion: usar `healthcheck` + `depends_on` con `condition`)
2. Los servicios no estan en la misma red (solucion: verificar que comparten red)
3. Usaste `localhost` en vez del nombre del servicio

```yaml
# INCORRECTO (desde dentro de un contenedor):
DB_HOST: localhost       # "localhost" es el propio contenedor, no postgres

# CORRECTO:
DB_HOST: postgres        # Nombre del servicio en Compose
```

### Error 4: depends_on no espera a que el servicio este listo

```yaml
# INSUFICIENTE: solo espera a que el contenedor ARRANQUE
depends_on:
  - postgres

# CORRECTO: espera a que el contenedor pase el healthcheck
depends_on:
  postgres:
    condition: service_healthy
```

`depends_on` sin condicion solo garantiza el **orden de inicio** del contenedor.
No verifica que el servicio dentro (PostgreSQL, Kafka, etc.) este aceptando
conexiones. Esto es una fuente MUY comun de errores intermitentes.

### Error 5: Datos perdidos al recrear contenedores

```bash
docker compose down      # Elimina contenedores
docker compose up -d     # La base de datos esta vacia!
```

**Causa:** No se configuro un volumen para persistir datos.

**Solucion:** Agregar un named volume (ver seccion 7.1.6).

**Nota:** `docker compose down -v` elimina los volumenes intencionalmente.
No usar `-v` si quieres conservar los datos.

### Error 6: Imagen desactualizada (cache)

```bash
# Si cambiaste el Dockerfile pero Compose sigue usando la imagen vieja:
docker compose build --no-cache    # Reconstruir sin cache
docker compose up -d
```

---

## 7.1.9 Principio de orquestacion

### Que es orquestacion

Orquestacion es el proceso de **coordinar, gestionar y automatizar**
multiples contenedores para que trabajen juntos como un sistema.

Docker Compose es el **nivel mas basico** de orquestacion:

```
   Nivel de orquestacion:

   +-----------------------------------------------------------+
   |                                                           |
   |   Docker Compose    -->    Docker Swarm    -->   Kubernetes|
   |   (1 maquina)             (varias maquinas,   (muchas     |
   |                            cluster simple)     maquinas,  |
   |   Desarrollo local,       Produccion           produccion |
   |   aprendizaje,            pequena-mediana      a gran     |
   |   CI/CD                                        escala)    |
   |                                                           |
   +-----------------------------------------------------------+
         Mas simple                              Mas complejo
         Menos escalable                         Mas escalable
```

### Docker Compose vs Kubernetes vs Docker Swarm

| Caracteristica | Docker Compose | Docker Swarm | Kubernetes (K8s) |
|---------------|---------------|-------------|-----------------|
| Maquinas | 1 (local) | Varias | Muchas |
| Escalabilidad | Manual | Basica (`replicas: 3`) | Automatica (HPA) |
| Alta disponibilidad | No | Si | Si |
| Curva de aprendizaje | Baja | Media | Alta |
| Uso tipico | Desarrollo, educacion | Produccion simple | Produccion enterprise |
| Archivo de config | docker-compose.yml | docker-compose.yml | Manifiestos YAML |

### Por que empezamos con Docker Compose

Para Big Data, Docker Compose permite:

1. **Levantar un cluster Spark** en tu laptop con un solo comando
2. **Reproducir el entorno** del profesor exactamente
3. **Experimentar** sin miedo a romper tu sistema
4. **Aprender los conceptos** que se aplican directamente en Kubernetes

> **Principio fundamental:** Docker Compose es a la orquestacion de contenedores
> lo que SQLite es a las bases de datos: perfecto para aprender, prototipar y
> desarrollar. Cuando se necesite escalar a produccion, los conceptos aprendidos
> (servicios, redes, volumenes, healthchecks) se transfieren directamente a
> herramientas como Kubernetes.

---

## 7.1.10 Patrones utiles

### Patron 1: Archivos .env para variables sensibles

En vez de poner contrasenas directamente en el YAML:

```
# Archivo: .env (NO subirlo a git, agregar a .gitignore)
POSTGRES_USER=alumno
POSTGRES_PASSWORD=bigdata2026
PGADMIN_EMAIL=admin@curso.com
PGADMIN_PASSWORD=admin123
```

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

Docker Compose lee automaticamente el archivo `.env` del mismo directorio.
Esto permite:
- No versionar contrasenas en git
- Cambiar configuracion sin tocar el YAML
- Tener un `.env.example` con valores de referencia

### Patron 2: docker-compose.override.yml

Docker Compose combina automaticamente `docker-compose.yml` con
`docker-compose.override.yml` si este ultimo existe.

```yaml
# docker-compose.yml (base, se comparte con todo el equipo)
services:
  app:
    build: ./app
    networks:
      - red_bigdata

# docker-compose.override.yml (personalizado, no se sube a git)
services:
  app:
    ports:
      - "9999:8000"         # Puerto personalizado para mi maquina
    volumes:
      - ./mi_codigo:/app    # Mi directorio local
```

Esto es util cuando cada miembro del equipo tiene configuraciones ligeramente
diferentes (puertos, rutas) sin modificar el archivo base compartido.

### Patron 3: Multi-stage builds (imagenes optimizadas)

Un Dockerfile puede tener multiples etapas. Esto permite crear imagenes
finales mas pequenas separando la fase de compilacion de la fase de ejecucion.

```dockerfile
# Etapa 1: Compilacion (imagen grande, con herramientas de build)
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Etapa 2: Ejecucion (imagen pequena, solo lo necesario)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

```
   Sin multi-stage:   1.2 GB  (incluye compiladores, headers, cache de pip)
   Con multi-stage:   350 MB  (solo Python slim + librerias instaladas)
```

### Patron 4: Profiles (activar servicios opcionalmente)

```yaml
services:
  postgres:
    image: postgres:16
    # Sin profile: siempre se levanta

  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - debug               # Solo se levanta si se activa el profile "debug"

  adminer:
    image: adminer
    profiles:
      - debug
```

```bash
# Solo levanta postgres (sin herramientas de debug)
docker compose up -d

# Levanta postgres + pgadmin + adminer
docker compose --profile debug up -d
```

---

## Resumen del modulo

```
   +------------------------------------------------------------------+
   |                    MAPA CONCEPTUAL - DOCKER                      |
   +------------------------------------------------------------------+
   |                                                                  |
   |  Dockerfile  ---build--->  Imagen  ---run--->  Contenedor        |
   |  (receta)                  (plantilla)         (instancia viva)  |
   |                                                                  |
   |  docker-compose.yml  ---up--->  Stack de servicios               |
   |  (orquesta N servicios)        (N contenedores conectados)       |
   |                                                                  |
   |  Volumes  = persistencia de datos                                |
   |  Networks = comunicacion entre contenedores (DNS interno)        |
   |  Ports    = acceso desde el host al contenedor                   |
   |  Healthcheck = verificar que un servicio esta LISTO              |
   |                                                                  |
   +------------------------------------------------------------------+
```

### Conceptos que deberias poder explicar

- Que es un contenedor y en que se diferencia de una maquina virtual
- Que es una imagen y como se construye (Dockerfile, capas, cache)
- Como Docker Compose orquesta multiples servicios
- Para que sirven volumes, networks, ports, healthcheck y depends_on
- Por que los contenedores se comunican por nombre (DNS interno)
- Cual es la diferencia entre named volumes y bind mounts
- Que pasa con los datos si no usas volumenes
- Por que `depends_on` solo no es suficiente (necesitas healthcheck)
- Donde se ubica Docker Compose en el espectro de orquestacion (vs K8s)

---

## Referencias

---

Siguiente: [7.2 - Cluster Apache Spark](../7.2_cluster_spark/README.md)

---

-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA:
- Merkel, D. (2014). Docker: Lightweight Linux Containers for Consistent Development and Deployment. Linux Journal, 2014(239), 2.
- Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.
- Turnbull, J. (2014). The Docker Book: Containerization is the new virtualization. James Turnbull.
- Nickoloff, J. & Kuenzli, S. (2019). Docker in Action (2nd ed.). Manning Publications.
- Kane, S. & Matthias, K. (2018). Docker: Up & Running (2nd ed.). O'Reilly Media.
- Docker Inc. (2024). Docker Documentation. https://docs.docker.com/
-------------------------
