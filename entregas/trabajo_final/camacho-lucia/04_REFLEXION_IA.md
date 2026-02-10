# Paso 5: Reflexion IA - Proceso de Aprendizaje

**Alumno:** [Nombre Apellido]

> **Instrucciones:** Para cada bloque (A, B, C), responde 3 preguntas y pega
> el prompt MAS IMPORTANTE que usaste en ese bloque.
>
> Se valoran respuestas **ESPECIFICAS** y **HONESTAS**. No importa si usaste
> IA o no. Lo que importa es que demuestres tu proceso de aprendizaje real.
>
> **Lo que evaluamos:** Tus prompts y tu capacidad de explicar que hiciste.
> Un codigo perfecto con reflexion vacia = nota baja.

---

## Bloque A: Infraestructura Docker

### Momento 1 - Arranque
**Que fue lo primero que le pediste a la IA o buscaste en internet?**

[Ejemplo BUENO: "Le pedi a ChatGPT: 'como escribo un docker-compose.yml
que tenga PostgreSQL y Apache Spark, necesito que el worker se conecte
al master por el puerto 7077'"]

[Ejemplo MALO: "Le pedi que me hiciera un docker-compose"]

### Momento 2 - Error
**Que fallo y como lo resolviste? (pega el error si lo tienes)**

[Ejemplo BUENO: "El worker no se conectaba al master. El error en
`docker logs` decia 'Connection refused to spark://master:7077'.
Descubri que no habia puesto los servicios en la misma red Docker.
Agrege una red compartida y funciono."]

[Ejemplo MALO: "Tuve un error y lo arregle"]

### Momento 3 - Aprendizaje
**Que aprendiste que NO sabias antes de empezar este bloque?**

[Ejemplo BUENO: "Aprendi que `depends_on` en Docker Compose NO espera
a que el servicio este listo, solo espera a que el contenedor arranque.
Por eso necesitas `healthcheck` + `condition: service_healthy` para
asegurarte de que PostgreSQL acepta conexiones antes de que Spark
intente escribir."]

[Ejemplo MALO: "Aprendi Docker"]

### Prompt clave del Bloque A

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**El prompt que mas te ayudo en este bloque:**
```
[PEGA AQUI el texto EXACTO del prompt que mas te sirvio para resolver
la infraestructura. No lo resumas. Copia y pega.]
```

**Por que fue clave:** [1-2 oraciones explicando por que este prompt
fue el mas importante para ti en este bloque]

---

## Bloque B: Pipeline ETL

### Momento 1 - Arranque
**Que fue lo primero que le pediste a la IA o buscaste en internet?**

[Tu respuesta]

### Momento 2 - Error
**Que fallo y como lo resolviste?**

[Tu respuesta]

### Momento 3 - Aprendizaje
**Que aprendiste que NO sabias antes de empezar este bloque?**

[Tu respuesta]

### Prompt clave del Bloque B

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**El prompt que mas te ayudo en este bloque:**
```
[PEGA AQUI el texto EXACTO]
```

**Por que fue clave:** [Tu respuesta]

---

## Bloque C: Analisis y Visualizacion

### Momento 1 - Arranque
**Que fue lo primero que le pediste a la IA o buscaste en internet?**

[Tu respuesta]

### Momento 2 - Error
**Que fallo y como lo resolviste?**

[Tu respuesta]

### Momento 3 - Aprendizaje
**Que aprendiste que NO sabias antes de empezar este bloque?**

[Tu respuesta]

### Prompt clave del Bloque C

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**El prompt que mas te ayudo en este bloque:**
```
[PEGA AQUI el texto EXACTO]
```

**Por que fue clave:** [Tu respuesta]

---

## Captura de pantalla

Adjunta UNA captura de pantalla de tu conversacion con la IA mostrando
el prompt que consideras mas significativo de TODO el trabajo.
Si no usaste IA, captura del recurso web/video que mas te sirvio.

![Mi prompt mas importante](capturas/prompt_clave.png)

**De cual bloque es esta captura:** [A / B / C]

**Que estabas intentando resolver:** [1-2 oraciones]
