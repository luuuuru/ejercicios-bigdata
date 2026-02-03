# Paso 2: Infraestructura Docker

**Alumno:** [Nombre Apellido]

---

## 2.1 Mi docker-compose.yml explicado

Explica **cada seccion** de tu archivo YAML con tus propias palabras.
No copies definiciones de internet; demuestra que entiendes lo que escribiste.

### Servicio: PostgreSQL

```yaml
# Pega aqui la seccion de PostgreSQL de tu YAML
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

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**Tu prompt exacto:**
```
[PEGA AQUI EL TEXTO COMPLETO de lo que le escribiste a la IA.
No lo resumas. No lo edites. Pega el texto tal cual.]
```

**Que te devolvio (resumen en 2-3 lineas):**

[Resumen breve de la respuesta]

**Que tuviste que cambiar de esa respuesta y por que:**

[Que partes NO funcionaron o tuviste que adaptar.
Si funciono todo a la primera, explicalo tambien.]

---

### Prompt 2 (si iteraste o pediste correccion):

**Herramienta:** [ChatGPT / Claude / Copilot / otra]

**Tu prompt exacto:**
```
[PEGA AQUI]
```

**Que te devolvio y que cambiaste:**

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
