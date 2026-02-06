# Registro de Prompts - Trabajo Final

**Alumno:** [Tu Nombre Apellido]
**Fecha:** [DD/MM/YYYY]
**IA utilizada:** [ChatGPT / Claude / Copilot / Gemini / otra]

---

## COMO USAR ESTE ARCHIVO

Este archivo tiene **DOS PARTES** muy diferentes:

| Parte | Que es | Como debe verse |
|-------|--------|-----------------|
| **PARTE 1** | Tus 3 prompts reales | Lenguaje NATURAL, con errores, informal |
| **PARTE 2** | Blueprint generado por IA | Perfecto, profesional, estructurado |

### REGLA IMPORTANTE

> **Los prompts de la Parte 1 deben ser COPIA EXACTA de lo que escribiste.**
>
> NO los pases por la IA para "mejorarlos". NO corrijas errores.
> Si escribiste "como ago para que sparck lea el csv" con errores,
> eso es lo que debes pegar.
>
> **El sistema detecta automaticamente si los prompts fueron "limpiados".**
> Prompts perfectos en la Parte 1 = SOSPECHOSO.

---

# PARTE 1: Mis Prompts Reales (3 minimo)

> Copia y pega EXACTAMENTE lo que le escribiste a la IA.
> Incluye errores, lenguaje informal, todo. Eso demuestra autenticidad.

---

## Prompt A: Infraestructura Docker

**Contexto:** [Que estabas intentando hacer?]

**Mi prompt exacto (copiado tal cual):**
```
[PEGA AQUI tu prompt real, con errores y todo]
```

**Que paso:** [ ] Funciono  [ ] Funciono parcial  [ ] No funciono

**Que aprendi:** [1-2 oraciones con tus palabras]

---

## Prompt B: Pipeline ETL / Spark

**Contexto:** [Que estabas intentando hacer?]

**Mi prompt exacto (copiado tal cual):**
```
[PEGA AQUI tu prompt real]
```

**Que paso:** [ ] Funciono  [ ] Funciono parcial  [ ] No funciono

**Que aprendi:** [1-2 oraciones]

---

## Prompt C: Analisis / Graficos

**Contexto:** [Que estabas intentando hacer?]

**Mi prompt exacto (copiado tal cual):**
```
[PEGA AQUI tu prompt real]
```

**Que paso:** [ ] Funciono  [ ] Funciono parcial  [ ] No funciono

**Que aprendi:** [1-2 oraciones]

---

# PARTE 2: Blueprint Replicable (generado por IA)

> **Instrucciones:** Cuando termines tu proyecto, pidele a tu IA:
>
> *"Genera un prompt profesional tipo blueprint que describa exactamente
> lo que logramos: stack, tecnologias, arquitectura, datos y pasos.
> Debe ser tan detallado que si se lo paso a otra IA o a un desarrollador
> senior, pueda replicar el proyecto completo sin ver mi codigo."*
>
> Pega la respuesta completa aqui abajo.

---

## Mi Blueprint

**Prompt que use para generar esto:**
```
[Pega el prompt que usaste para pedir el blueprint]
```

**Blueprint generado por la IA:**

```
[PEGA AQUI TODO el blueprint que genero la IA]

Ejemplo de como deberia verse:
─────────────────────────────────────────────────────────────────
PROYECTO: Pipeline Big Data - Analisis de [tu tema]

INFRAESTRUCTURA:
- Docker Compose con X servicios:
  * PostgreSQL [version] (puerto XXXX, healthcheck)
  * Spark Master [version] (puerto XXXX)
  * Spark Worker (X GB RAM, X cores)
- Red: [nombre]
- Volumenes: [descripcion]

DATOS:
- Dataset: [nombre y fuente]
- Paises: [lista de codigos ISO]
- Variables: [lista]
- Periodo: [años]

PIPELINE ETL:
1. [Paso 1]
2. [Paso 2]
3. [Paso N]

ANALISIS:
- [Tipo de analisis]
- [Graficos generados]

TECNOLOGIAS:
- [Lista completa con versiones]

COMANDO PARA EJECUTAR:
docker compose up -d && python pipeline.py
─────────────────────────────────────────────────────────────────
```

---

## Verificacion de Coherencia

Responde estas preguntas para verificar que tu blueprint coincide con tu codigo:

| Pregunta | Tu respuesta |
|----------|--------------|
| La version de Spark en el blueprint coincide con tu docker-compose.yml? | [Si/No] |
| Los paises del blueprint son los mismos que filtra tu pipeline.py? | [Si/No] |
| Las variables del blueprint estan en tu codigo? | [Si/No] |
| El tipo de analisis del blueprint coincide con tus graficos? | [Si/No] |

**Si alguna respuesta es "No", corrige el blueprint o el codigo.**

---

## Estadisticas Finales

| Metrica | Valor |
|---------|-------|
| Total de interacciones con IA (aprox) | [numero] |
| Prompts que funcionaron a la primera | [numero] |
| Errores que tuve que resolver | [numero] |
| Horas totales de trabajo | [numero] |

---

## Declaracion

[ ] Confirmo que los prompts de la PARTE 1 son reales y no fueron
    modificados ni pasados por IA para corregirlos.

[ ] Confirmo que el blueprint de la PARTE 2 fue generado por IA
    basandose en mi proyecto real.

[ ] Entiendo que inconsistencias entre el blueprint y mi codigo
    seran investigadas.

**Nombre:** [Tu nombre completo]
**Fecha:** [DD/MM/YYYY]
