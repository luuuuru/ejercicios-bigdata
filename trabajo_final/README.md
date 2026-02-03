# Trabajo Final: Pipeline de Big Data con Infraestructura Docker

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

---

## Objetivo

Construir **desde cero** una infraestructura de procesamiento de datos usando Docker,
Apache Spark y PostgreSQL. A partir del dataset Quality of Government (QoG),
disenar y ejecutar un pipeline ETL + analisis que responda una pregunta de
investigacion formulada por ti.

**Lo que se evalua:** No solo el codigo, sino tu **proceso de aprendizaje**.
Puedes usar herramientas de IA (ChatGPT, Copilot, Claude, etc.) pero debes
documentar como las usaste y que aprendiste.

---

## Dataset

**Quality of Government Standard Dataset (QoG)** - Enero 2024

- Archivo: `datos/qog/qog_std_ts_jan24.csv`
- ~15,500 filas (paises x anios) x ~1,990 columnas
- Variables: democracia, corrupcion, PIB, salud, educacion, estabilidad politica...
- Documentacion: https://www.gu.se/en/quality-government/qog-data

---

## Estructura: 4 Bloques

### Bloque A: Infraestructura Docker (30%)

**Tarea:** Escribir un `docker-compose.yml` que levante un mini-cluster:

| Servicio | Requisito minimo |
|----------|-----------------|
| PostgreSQL | Base de datos para almacenar resultados |
| Spark Master | Coordinador del cluster |
| Spark Worker | Al menos 1 nodo de procesamiento |

**Pasos:**

1. Investiga que es Docker Compose y como se estructura un archivo YAML
2. Escribe tu `docker-compose.yml` con los 3 servicios minimos
3. Agrega `healthcheck` al menos para PostgreSQL
4. Ejecuta `docker compose up -d` y verifica que todo arranca
5. Abre el Spark UI en tu navegador y toma una **captura de pantalla** mostrando el worker conectado
6. Escribe `INFRAESTRUCTURA.md` explicando **cada seccion** de tu YAML con tus palabras

**Pistas:**
- Imagen Spark: `apache/spark:3.5.4-python3` (o `bitnami/spark:3.5`)
- Imagen PostgreSQL: `postgres:15-alpine`
- El Master de Spark usa el puerto 7077 para comunicacion y 8080 para la UI web
- Los Workers necesitan saber la URL del Master para conectarse

**Entregables del Bloque A:**
- `docker-compose.yml` (funcional)
- `02_INFRAESTRUCTURA.md` (explicacion + prompts IA usados + captura Spark UI)

---

### Bloque B: Pipeline ETL con Spark (25%)

**Tarea:** Escribir un script Python que procese QoG usando Apache Spark.

**Pasos:**

1. Elige **5 paises** que te interesen (no pueden ser los del ejemplo del profesor: KAZ, UZB, TKM, KGZ, TJK)
2. Elige **5 variables numericas** del dataset QoG (explora las columnas disponibles)
3. Formula una **pregunta de investigacion** (ejemplo: "Como ha evolucionado la democracia en Sudamerica comparado con Europa del Este?")
4. Escribe `pipeline.py` que:
   - Cree una SparkSession
   - Lea el CSV con `spark.read.csv()`
   - Seleccione tus paises y variables
   - Filtre un rango de anios (ej: 2000-2023)
   - Cree al menos 1 variable derivada (ej: ratio, indice, categorizacion)
   - Guarde el resultado como Parquet

**Ejemplo de variable derivada:**
```python
# Categorizar nivel de democracia
from pyspark.sql import functions as F
df = df.withColumn("nivel_demo",
    F.when(F.col("vdem_polyarchy") > 0.7, "Alta")
     .when(F.col("vdem_polyarchy") > 0.4, "Media")
     .otherwise("Baja")
)
```

**Importante:** Tu seleccion de paises y variables debe ser UNICA. Si dos alumnos
entregan los mismos 5 paises, se considerara copia.

**Entregable del Bloque B:**
- `pipeline.py` (incluye ETL + analisis del Bloque C)

---

### Bloque C: Analisis y Visualizacion (25%)

**Tarea:** Analizar tus datos procesados y responder tu pregunta de investigacion.

**Elige UNA opcion:**

| Opcion | Que hacer | Ejemplo |
|--------|-----------|---------|
| **Clustering** | K-Means sobre tus paises | "Que paises se parecen segun democracia + PIB?" |
| **Serie temporal** | Grafico de evolucion por pais | "Como cambio la corrupcion en mis paises entre 2000-2023?" |
| **Comparacion** | Antes/despues de un evento | "Cambio el PIB de estos paises tras la crisis de 2008?" |

**Requisitos minimos:**
- 2 graficos (matplotlib, plotly, o seaborn)
- Cada grafico debe tener titulo, ejes etiquetados, y leyenda
- Parrafo de interpretacion: que ves en el grafico y que significa

**Entregable del Bloque C:**
- Graficos incluidos en `03_RESULTADOS.md`
- Interpretacion escrita de cada grafico
- Prompt usado para generar cada grafico (pegado bajo cada uno)

---

### Bloque D: Reflexion IA - "3 Momentos Clave" (20%)

**Tarea:** Documentar tu proceso de aprendizaje Y compartir tus prompts.

Para **cada bloque** (A, B, C), responde estas 3 preguntas:

| Momento | Pregunta |
|---------|----------|
| **Arranque** | Que fue lo primero que le pediste a la IA (o buscaste en internet)? |
| **Error** | Que fallo y como lo resolviste? Pega el error si lo tienes. |
| **Aprendizaje** | Que aprendiste que NO sabias antes de empezar este bloque? |

**Ademas, para cada bloque:** Pega el **texto exacto** del prompt de IA que
mas te ayudo. No lo resumas ni lo parafrasees: copia y pega el texto tal cual.

**Ademas:** Adjunta 1 captura de pantalla del prompt que mas te ayudo
(o del recurso web/video si no usaste IA). Guardala en `capturas/`.

**IMPORTANTE - Donde van los prompts:**

Los prompts se documentan en **varios archivos** segun el bloque:

| Archivo | Que prompts van ahi |
|---------|---------------------|
| `02_INFRAESTRUCTURA.md` (seccion 2.4) | Todos los prompts usados para el docker-compose.yml |
| `03_RESULTADOS.md` (bajo cada grafico) | El prompt que genero cada grafico |
| `04_REFLEXION_IA.md` (bajo cada bloque) | El prompt CLAVE de cada bloque (A, B, C) |

**Se evalua:**
- Que tus prompts sean **reales** (pegados tal cual, no inventados despues)
- Que tus respuestas sean **especificas** (no "aprendi Docker" sino "aprendi que el puerto 8080 del master se mapea al 18080 porque...")
- Que los errores sean **reales** (todos cometemos errores, documentarlos no baja nota)
- Que el proceso sea **coherente** con tu codigo (si el codigo es perfecto pero la reflexion esta vacia, hay un problema)

**Nota:** No importa si usaste IA o no. Lo que importa es que demuestres
que ENTIENDES lo que entregaste. Un alumno que usa IA bien y lo explica
saca mejor nota que uno que copia y no puede explicar nada.

**Entregable del Bloque D:**
- `04_REFLEXION_IA.md`

---

## Preguntas de Comprension (obligatorias)

Responde en `05_RESPUESTAS.md`:

1. **Infraestructura:** Si tu worker tiene 2 GB de RAM y el CSV pesa 3 GB, que pasa? Como lo solucionarias?
2. **ETL:** Por que `spark.read.csv()` no ejecuta nada hasta que llamas `.count()` o `.show()`?
3. **Analisis:** Interpreta tu grafico principal: que patron ves y por que crees que ocurre?
4. **Escalabilidad:** Si tuvieras que repetir este ejercicio con un dataset de 50 GB, que cambiarias en tu infraestructura?

---

## Entrega

### Formato

```
entregas/trabajo_final/apellido_nombre/
    01_README.md               <- (1) Tus datos + pregunta de investigacion
    02_INFRAESTRUCTURA.md      <- (2) Explicacion YAML + prompts IA + captura Spark UI
    03_RESULTADOS.md           <- (3) Graficos + interpretacion + prompts de graficos
    04_REFLEXION_IA.md         <- (4) 3 Momentos Clave x 3 bloques + prompts clave
    05_RESPUESTAS.md           <- (5) 4 preguntas de comprension
    docker-compose.yml         <- Tu YAML funcional
    pipeline.py                <- ETL + Analisis
    requirements.txt           <- Dependencias (pip freeze)
    capturas/                  <- Tus capturas de pantalla (Spark UI, prompts, graficos)
    .gitignore                 <- Excluir datos, venv, __pycache__
```

Los numeros indican el **orden en que debes completarlos**. Empieza por el 01.

Copia la plantilla desde `trabajo_final/plantilla/` a tu carpeta de entrega.

### Proceso

1. Sincroniza tu fork con el repositorio principal
2. Crea una rama: `git checkout -b apellido-trabajo-final`
3. Copia la plantilla: `cp -r trabajo_final/plantilla/ entregas/trabajo_final/apellido_nombre/`
4. Crea la carpeta de capturas: `mkdir entregas/trabajo_final/apellido_nombre/capturas/`
5. Completa los archivos **en orden** (01 al 05), junto con `docker-compose.yml` y `pipeline.py`
6. Commit y push a tu fork
7. Crea un Pull Request con titulo: `[TF] Apellido Nombre - Tu Pregunta de Investigacion`

### Prohibido incluir en el PR

- Archivos de datos (.csv, .parquet, .db)
- Entornos virtuales (venv/, .venv/)
- Archivos .env con credenciales reales
- Carpetas __pycache__/

---

## Evaluacion

| Bloque | Peso | Que se evalua |
|--------|------|---------------|
| A. Infraestructura | 30% | YAML funcional + explicacion con tus palabras |
| B. Pipeline ETL | 25% | Spark API + paises/variables propios + pregunta |
| C. Analisis | 25% | Graficos + interpretacion que responda tu pregunta |
| D. Reflexion IA | 20% | Proceso de aprendizaje real y especifico |

**Penalizaciones:**
- Copiar los mismos paises/variables que otro alumno: -50%
- Copiar los paises del ejemplo del profesor (Asia Central): -30%
- YAML que no funciona sin explicacion de por que: -15%
- Reflexion IA ausente o generica: -20%

---

## Recursos

- **Material teorico del curso:** `ejercicios/07_infraestructura_bigdata/` (Docker, Spark, Hadoop)
- **Spark Documentation:** https://spark.apache.org/docs/3.5.4/
- **Docker Compose:** https://docs.docker.com/compose/
- **QoG Codebook:** https://www.gu.se/en/quality-government/qog-data (descargar codebook para ver que significa cada variable)
- **Spark UI:** Una vez levantado tu cluster, http://localhost:8080 (o el puerto que hayas configurado)

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
- Teorey, T., et al. (2011). Quality of Government Standard Dataset. University of Gothenburg.
- Merkel, D. (2014). Docker: Lightweight Linux Containers for Consistent Development and Deployment. Linux Journal, 2014(239), 2.
-------------------------
