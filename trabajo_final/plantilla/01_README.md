# Trabajo Final: [Tu Pregunta de Investigacion]

**Alumno:** [Nombre Apellido]
**Fecha:** [DD/MM/AAAA]

---

## Orden de trabajo

Completa los archivos en este orden. Cada numero indica la secuencia:

| Orden | Archivo | Que haces |
|-------|---------|-----------|
| **1** | `01_README.md` (este archivo) | Defines tu pregunta, paises y variables |
| **2** | `02_INFRAESTRUCTURA.md` | Construyes y explicas tu docker-compose.yml |
| **3** | `pipeline.py` | Escribes tu ETL + analisis con Spark |
| **4** | `03_RESULTADOS.md` | Presentas graficos e interpretas resultados |
| **5** | `04_REFLEXION_IA.md` | Documentas tu proceso y pegas tus prompts |
| **6** | `05_RESPUESTAS.md` | Respondes 4 preguntas de comprension |

Los archivos `docker-compose.yml`, `requirements.txt` y `.gitignore` los
completas conforme avanzas.

---

## Pregunta de investigacion

[Escribe aqui tu pregunta. Ejemplo: "Como ha evolucionado la calidad institucional
en los paises del Cono Sur comparado con el Sudeste Asiatico entre 2000-2023?"]

---

## Paises seleccionados (5)

| # | Pais | Codigo ISO | Por que lo elegiste |
|---|------|------------|---------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**IMPORTANTE:** No puedes usar los paises del ejemplo del profesor (KAZ, UZB, TKM, KGZ, TJK).

---

## Variables seleccionadas (5 numericas)

| # | Variable QoG | Que mide | Por que la elegiste |
|---|-------------|----------|---------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Tip:** Consulta el codebook de QoG para entender que mide cada variable:
https://www.gu.se/en/quality-government/qog-data

---

## Variable derivada

[Describe la variable que creaste a partir de las originales.
Ejemplo: "Cree un indice de gobernanza = (control_corrupcion + estado_derecho) / 2"]

---

## Tipo de analisis elegido

- [ ] Clustering (K-Means)
- [ ] Serie temporal (evolucion por pais)
- [ ] Comparacion (antes/despues de un evento)

---

## Como ejecutar mi pipeline

```bash
# Paso 1: Levantar infraestructura
docker compose up -d

# Paso 2: Verificar que todo funciona
docker ps

# Paso 3: Ejecutar pipeline
python pipeline.py
```

[Agrega cualquier instruccion adicional necesaria para reproducir tus resultados]
