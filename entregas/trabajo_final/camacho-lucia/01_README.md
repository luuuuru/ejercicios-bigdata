# Trabajo Final: [Detección de patrones asociadas con Deterioro cognitivo leve (MCI) y Enfermedad de alzheimer (AD) mediante machine learning no supervisado]

**Alumno:** [Lucia Camacho]
**Fecha:** [07/02/2026]
**Curso:** Especialista en Big Data
**Profesor:** Juan Marcelo Gutierrez Miranda
TodoEconometria [Repositorio de GitHub]. GitHub. Disponible en: https://github.com/TodoEconometria

---

## Orden de trabajo

Este proyecto sigue una estructura secuencial. Cada número indica el orden de ejecución y lectura:

| Orden | Archivo | Que haces                                                                    |
|-------|---------|------------------------------------------------------------------------------|
| **1** | `01_README.md` (este archivo) | Definición de la pregunta, variables y metodología.                          |
| **2** | `02_INFRAESTRUCTURA.md` | Explicación de la arquitectura Docker y `docker-compose.yml`.                |
| **3** | `pipeline.py` | Script principal: ETL con PySpark, Selección de Variables (RF) y Clustering. |
| **4** | `03_RESULTADOS.md` | Visualización de gráficos e interpretación clínica de los clusters.          |
| **5** | `04_REFLEXION_IA.md` | Documentación del proceso de desarrollo asistido por IA.                     |
| **6** | `05_RESPUESTAS.md` | Respuestas a las preguntas de evaluación del curso.                          |

---
## 🔬 Pregunta de investigación
> **¿Existen subtipos o patrones latentes identificables mediante aprendizaje no supervisado en pacientes de la cohorte ADNI3, basándose en biomarcadores de neuroimagen (MRI) y evaluaciones neuropsicológicas?**
> 
Este proyecto tiene como objetivo identificar patrones característicos diferenciando entre individuos sanos (**CN**), con deterioro cognitivo leve (**MCI**) y enfermedad de Alzheimer (**AD**), utilizando un pipeline híbrido de Big Data (Spark) y Machine Learning (Scikit-Learn).

## Adquisición de Datos

### 1. Registro y acceso
Los datos provienen de la **Alzheimer's Disease Neuroimaging Initiative (ADNI)**.
1. Registro en LONI IDA: [https://ida.loni.usc.edu/](https://ida.loni.usc.edu/).
2. Solicitud de acceso aprobada.

### 2. Datasets Utilizados
Se utilizan archivos CSV pre-procesados por el equipo de UCSF (FreeSurfer 6.0, Cross-Sectional, versión 7/6.0) y datos clínicos:
* **`UCSFFSX7.csv`**: Volúmenes corticales, grosor y áreas (Neuroimagen).
* **`ADNIMERGE.csv`**: Datos demográficos (Edad, Género, Educación, APOE4).
* **`DXSUM_25Jan2026.csv`**: Diagnóstico clínico actualizado.
* **`MMSE.csv`**: Puntuación del Mini-Mental State Examination.
* **`FAQ.csv`**: Puntuación del Functional Activities Questionnaire.

**Tip:** Consulta el codebook de ADNI para entender que mide cada variable:
https://adni.loni.usc.edu/help-faqs/adni-data-user-guide/

---

## Variables categoricas 
1.  **DIAGNOSIS:** Variable objetivo para validación cruzada (no entra al clustering). Categorías: CN, MCI, AD.
2.  **VISCODE:** Se ha normalizado la nomenclatura temporal.
    * *Originales:* `init`, `sc`, `y1`, `y2`, etc.
    * *Transformación:* `sc` e `init` se han unificado como **`y0`** (Línea base).

A este csv se merge las siguientes variables Edad, Género, nivel educativo, Estado civil, APOE4,
así como variables clinicas/neuropsicologicas: puntuacion total del MMSE, MOCA y FAQ.
Para este estudio centrado en la fase **ADNI3**, se han aplicado los siguientes filtros:
En este estudio se trabaja con la base de datos ADNI, las variables categoricas de interés son DIAGNOSIS, incluyendo 
controles sanos (CN), deterioro cognitivo leve (MCI), y enfermedad de Alzheimer (AD). 
La segunda es VISCODE que inicialmente tiene los siguientes valores init (n= 887), sc (n= 2234), y1 (n= 1500)
 y2 (n= 1770), y3 (n= 495), y4 (n= 870), y5 (n=133). 
La variable VISCODE, para la consecucion de objetivos se filtra de la siguiente forma: 
- Objetivo 1: análisis transversal, se filtra visita inicial o screening (creandose un nuevo valor etiquetado como y0). 
- Objetivo 2: análisis longitudinal, se filtra y0 y el primer año (y1).

| # | Variable  | Por que lo elegiste                                             |
|---|-----------|-----------------------------------------------------------------|
| 1 | DIAGNOSIS | Variable independiente del análisis diferencia CN, MCI y AD     |
| 2 | VISCODE   | Permite filtrar el momento del análisis (Transversal en `y0`).  |

---

## Variables dependientes seleccionadas (5 numericas)
Se utilizó un algoritmo de **Random Forest** para selección de características (Feature Selection), reduciendo la dimensionalidad de >300 variables a las más relevantes.

**Top 5 Variables Detectadas:**

| # | Variable | Qué mide                                                       | 
|---|----------|----------------------------------------------------------------|
| 1 | **FAQTOTAL** | *Functional Activities Questionnaire*. Evalúa la funcionalidad | 
| 2 | **MMSCORE** | *Mini-Mental State Exam*. Score cognitivo global (0-30).       | 
| 3 | **Hippocampus_Left** | Volumen del hipocampo izquierdo ($mm^3$).                      | 
| 4 | **Entorhinal_Left_Thick** | Grosor de la corteza entorrinal izquierda (mm).                |
| 5 | **IsthmusCingulate_Right_TA** | Grosor del istmo del giro cingulado.                           | 

---

## Variable derivada
Se han creado y transformado variables:
### 1. Normalización (Función `aplicar_transformaciones_neuro_adni`)
* **Volumen ($mm^3$):** Se usa tal cual o ajustado por regresión en estudios avanzados.
* **Área (SA):** Se normaliza por el Volumen Intracraneal Total (ICV) para corregir por tamaño de cabeza.
    $$Area_{adj} = \frac{Area_{raw}}{ICV}$$
* **Grosor (Thickness - TA):** Se aplica **Z-Score** para centrar la anatomía respecto a la media poblacional.
    $$z = \frac{x - \mu}{\sigma}$$
* 
### 2. Variable Derivada Creada
* **`Hippocampus_Total_Ratio`**: Se creó una variable  sumando ambos hemisferios del hipocampo y normalizándolo por el volumen craneal total, permitiendo una medida relativa de atrofia.
    ```python
    (Hippocampus_Left + Hippocampus_Right) / ICV
    ```

---

## Tipo de analisis elegido
- [X] Clustering (K-Means)
* Técnica no supervisada para agrupar pacientes.
    * Se utilizó la **Técnica del Codo** para determinar el número óptimo de clusters ($k=3$).
    * Se validó visualmente mediante reducción de dimensionalidad **PCA** (Principal Component Analysis).
  
---

## 🚀 Cómo ejecutar el pipeline
El proyecto está contenerizado con Docker
```bash
# Paso 1: Levantar infraestructura
docker compose up -d

# Paso 2: Verificar que todo funciona
docker ps

# Paso 3 instalar requerimientos
docker exec -u 0 spark-master pip install -r /opt/spark-apps/requirements.txt
docker exec -u 0 spark-worker-1 pip install -r /opt/spark-apps/requirements.txt

# Paso 3: Ejecutar pipeline
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark-apps/pipeline.py

python pipeline.py
```

## Requerimientos
pandas
numpy
matplotlib
seaborn
scikit-learn
pyspark
pyarrow

## Referencias

1) Mueller, S. G., et al. (2005) [Dataset]. The Alzheimer's disease neuroimaging initiative. Neuroimaging Clinics of North America, 15(4), 869-877.
2) TodoEconometria [Repositorio de GitHub]. GitHub. Disponible en: https://github.com/TodoEconometria
3) scikit-learn developers. RandomForestClassifier — scikit-learn documentation [Documentación]. scikit-learn. Disponible en: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
4) Sahu, ADNI clustering [Repositorio de GitHub]. GitHub. Disponible en: https://github.com/adarshsahu460/ADNI_CLUSTERING/blob/main/README.md

### Referencias academicas 
Sönmez, T. F., Harvey, D. J., Beckett, L. A., & for the Alzheimer’s Disease Neuroimaging Initiative. (2025). An unsupervised learning approach for clustering joint trajectories of Alzheimer’s disease biomarkers: An application to ADNI Data. Alzheimer’s & Dementia, 21(2), e14524. https://doi.org/10.1002/alz.14524
Venkataraman, A. V., Bai, W., Whittington, A., Myers, J. F., Rabiner, E. A., Lingford-Hughes, A., Matthews, P. M., & for the Alzheimer’s Disease Neuroimaging Initiative. (2021). Boosting the diagnostic power of amyloid-β PET using a data-driven spatially informed classifier for decision support. Alzheimer’s Research & Therapy, 13(1), 185. https://doi.org/10.1186/s13195-021-00910-8
for the Alzheimer’s Disease Neuroimaging Initiative, Escudero, J., Ifeachor, E., & Zajicek, J. P. (2012). Bioprofile Analysis: A New Approach for the Analysis of Biomedical Data in Alzheimer’s Disease. Journal of Alzheimer’s Disease, 32(4), 997-1010. https://doi.org/10.3233/JAD-2012-121024

