# Paso 2: Infraestructura Docker

**Alumno:** Lucia Camacho

---

## 2.1 Mi docker-compose.yml explicado

Explica **cada seccion** de tu archivo YAML con tus propias palabras.
No copies definiciones de internet; demuestra que entiendes lo que escribiste.

### Servicio: PostgreSQL

```yaml
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
```

**Que hace:** [Explica con tus palabras para que sirve este servicio,
que significan los parametros que usaste (ports, environment, volumes, etc.)]

### Servicio: Spark Master

```yaml
# Pega aqui la seccion del Spark Master de tu YAML
```

**Que hace:** [Explica el rol del Master en un cluster Spark.
Que puertos usa y para que? Por que necesita una red compartida?]

### Servicio: Spark Worker

```yaml
# Pega aqui la seccion del Worker de tu YAML
```

**Que hace:** [Explica como el Worker se conecta al Master.
Que pasa si agregas mas Workers? Que recursos le asignaste?]

### Otros servicios (si los tienes)

[Si agregaste servicios adicionales, explicalos aqui]

---

## 2.2 Healthchecks

[Explica que son los healthchecks y por que los necesitas.
Que pasa si PostgreSQL no tiene healthcheck y Spark intenta conectarse
antes de que este listo?]

---

## 2.3 Evidencia: Captura Spark UI

[Inserta aqui tu captura de pantalla del Spark UI mostrando el Worker conectado]

![Spark UI](capturas/spark_ui.png)

**Que se ve en la captura:** [Describe que muestra: cuantos workers, cuanta
memoria, que URL tiene el Master, etc.]

---

## 2.4 Prompts utilizados para la infraestructura

**OBLIGATORIO:** Pega aqui los prompts EXACTOS que usaste para construir tu
docker-compose.yml. Si no usaste IA, ve a la seccion 2.5.

> **Por que pedimos esto?** No evaluamos si usaste IA o no. Evaluamos si
> ENTIENDES lo que generaste. Un buen prompt demuestra que sabes lo que
> necesitas. Un prompt generico ("hazme un docker-compose") demuestra que no.

### Prompt 1 (el primero que usaste):

**Herramienta:** [Gemini]

**Tu prompt exacto:**
```
quiero montar una infraestructura para Big data siguiendo las siguientes indicaciones ejercicios-bigdata/ejercicios/07_infraestructura_bigdata/7.2_cluster_spark/README.md at main · luuuuru/ejercicios-bigdata el docker-compose lo tengo ubicado ahi:

"D:\Ejemplo\docker-compose.yml"
```

**Que te devolvio (resumen en 2-3 lineas):**
Me dió las indicaciones para que en primer lugar abriera la terminal de PowerShell como Administrador y, navegue a la carpeta: cd D:\Ejemplo.
En segundo lugar, configure el archivo docker-compose.yml (generó un código yaml para que lo pegara en un editor de texto, aun así utilicé el ejemplo del profesor)
En tercer lugar, 
**Que tuviste que cambiar de esa respuesta y por que:**

[Que partes NO funcionaron o tuviste que adaptar.
Si funciono todo a la primera, explicalo tambien.]

---

### Prompt 2 (si iteraste o pediste correccion):

**Herramienta:** [Gemini]

**Tu prompt exacto:**
```
se ejecuta desde spark? C:\DOCUMENTOS\BigData\ADNI_Project\.venv\Scripts\python.exe D:\Ejemplo\scripts\pipeline.py 
✅ Datos cargados. Dimensiones iniciales: (7889, 346)
✅ Se han calculado 3 variables compuestas (Totales).
D:\Ejemplo\scripts\pipeline.py:50: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  df[f'{nombre}_Total'] = df[izq] + df[der]
dime los pasos que tengo que seguir para completar este ejercicio ejercicios-bigdata/ejercicios/07_infraestructura_bigdata/7.2_cluster_spark at main · TodoEconometria/ejercicios-bigdata```
```

**Que te devolvio y que cambiaste:**
Viendo tu captura de pantalla, tu infraestructura ya está perfectamente operativa: el Master, el Worker y Postgres están en ejecución (Up) y el Master ha sido elegido líder y está en estado ALIVE.
Sin embargo, respondiendo a tu pregunta: No se está ejecutando desde Spark.
[Tu respuesta]

---

### Prompt 3 (si necesitaste mas iteraciones):

[Repite el formato. Agrega tantos como hayas necesitado.]

---

## 2.5 Recursos web consultados (si NO usaste IA)

Si en lugar de IA consultaste documentacion, tutoriales o videos:

| Recurso | URL | Que aprendiste de el |
|---------|-----|---------------------|
| | | |
| | | |
| | | |
