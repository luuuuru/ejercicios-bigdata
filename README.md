# Big Data con Python - De Cero a Producción

<div align="center">

**El curso más completo de Big Data en español**
*Desde tu primera query SQL hasta dashboards en tiempo real con Kafka y AWS*

[![GitHub Stars](https://img.shields.io/github/stars/TodoEconometria/ejercicios-bigdata?style=for-the-badge&logo=github)](https://github.com/TodoEconometria/ejercicios-bigdata/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/TodoEconometria/ejercicios-bigdata?style=for-the-badge&logo=github)](https://github.com/TodoEconometria/ejercicios-bigdata/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)

### [**Ver Sitio Web del Curso**](https://todoeconometria.github.io/ejercicios-bigdata/)

</div>

---

## Demos en Vivo

| Observatorio Sísmico Global | ISS Tracker |
|:---------------------------:|:-----------:|
| Sismos en tiempo real desde USGS API | Rastrea la Estación Espacial Internacional |
| [**Ver Demo**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_sismos_global.html) | [**Ver Demo**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_iss_tracker.html) |

*Dashboards con datos reales de APIs públicas, actualizados automáticamente*

---

## El Curso en Números

| 230 Horas | 6 Módulos | 25+ Ejercicios | 12+ Dashboards | 30+ Tecnologías |
|:---------:|:---------:|:--------------:|:--------------:|:---------------:|
| de contenido | completos | prácticos | interactivos | profesionales |

---

## Stack Tecnológico Completo

### Bases de Datos

| Tecnología | Nivel | Qué Aprenderás |
|------------|-------|----------------|
| **SQLite** | Básico | Queries SQL, índices, optimización |
| **PostgreSQL** | Intermedio | Joins complejos, Window Functions, CTEs |
| **Oracle** | Avanzado | PL/SQL, procedimientos almacenados |
| **DynamoDB** | Avanzado | NoSQL, key-value, serverless |

### Procesamiento de Datos

| Tecnología | Cuándo Usarla | Escala |
|------------|---------------|--------|
| **Pandas** | Análisis exploratorio | < 5 GB |
| **Dask** | Datasets grandes, 1 máquina | 5-100 GB |
| **Apache Spark** | Clusters, producción | > 100 GB |
| **Spark Streaming** | Datos en tiempo real | Ilimitado |

### Streaming y Cloud

| Tecnología | Propósito |
|------------|-----------|
| **Apache Kafka** | Streaming distribuido (KRaft mode) |
| **Spark Structured Streaming** | Procesamiento de streams |
| **LocalStack** | Simulación AWS local (gratis) |
| **Terraform** | Infraestructura como Código |
| **AWS S3/Lambda** | Almacenamiento y funciones serverless |

### Machine Learning e IA

| Tecnología | Aplicación |
|------------|------------|
| **Scikit-learn** | ML clásico, clustering, clasificación |
| **TensorFlow** | Deep Learning, redes neuronales |
| **MobileNetV2** | Transfer Learning, Computer Vision |
| **ARIMA/SARIMA** | Series temporales, forecasting |

### NLP y Visualización

| Tecnología | Uso |
|------------|-----|
| **NLTK** | Procesamiento de lenguaje natural |
| **TF-IDF** | Vectorización de texto |
| **Plotly** | Dashboards interactivos |
| **Leaflet.js** | Mapas interactivos |

### Econometría

| Tecnología | Aplicación |
|------------|------------|
| **linearmodels** | Datos de panel |
| **Panel OLS** | Efectos fijos y aleatorios |
| **Hausman Test** | Selección de modelo |

---

## Módulos del Curso

### Módulo 1: Bases de Datos
> SQLite, PostgreSQL, Oracle, migraciones

Desde tu primera query SELECT hasta procedimientos almacenados en Oracle.

### Módulo 2: Big Data y ETL
> Pipelines ETL, Dask, Parquet, QoG Dataset

Pipelines profesionales que procesan millones de registros.

### Módulo 3: Analítica Avanzada
> Machine Learning, Deep Learning, NLP, Series Temporales

PCA, K-Means, Transfer Learning con TensorFlow, ARIMA/SARIMA.

### Módulo 4: Econometría de Panel
> Efectos Fijos, Efectos Aleatorios, Hausman Test

Análisis longitudinal con datos país x año.

### Módulo 5: Streaming e Infraestructura Cloud
> Kafka, Spark Streaming, LocalStack, Terraform, AWS

Streaming en tiempo real y simulación de AWS sin costos.

### Trabajo Final
> Docker + Spark + PostgreSQL + Análisis Completo

Proyecto integrador de principio a fin.

---

## Inicio Rápido

```bash
# 1. Clona tu fork
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
cd ejercicios-bigdata

# 2. Crea entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instala dependencias
pip install -r requirements.txt
```

**Siguiente paso:** [Ver documentación completa](https://todoeconometria.github.io/ejercicios-bigdata/)

---

## Estructura del Repositorio

```
ejercicios-bigdata/
├── ejercicios/                 # Código por módulo
│   ├── 01_bases_de_datos/
│   ├── 02_limpieza_datos/
│   ├── 03_procesamiento_distribuido/
│   ├── 04_machine_learning/
│   ├── 05_nlp_text_mining/
│   └── 06_análisis_datos_de_panel/
│
├── entregas/                   # Zona de entregas del alumno
├── trabajo_final/              # Proyecto integrador
└── docs/                       # Sitio web (MkDocs)
```

---

## Galería de Dashboards

| Dashboard | Tecnologías |
|-----------|-------------|
| [**ARIMA PRO**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_arima_pro.html) | Series temporales estilo Bloomberg |
| [**PCA + K-Means**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/02_pca_iris_dashboard.html) | Clustering y reducción dimensional |
| [**Transfer Learning Flores**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_flores.html) | CNN + Computer Vision |
| [**Panel Data QoG**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/06_analisis_panel_qog.html) | Spark + PostgreSQL + ML |
| [**Sismos Global**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_sismos_global.html) | Kafka + Tiempo Real |
| [**ISS Tracker**](https://todoeconometria.github.io/ejercicios-bigdata/dashboards/dashboard_iss_tracker.html) | LocalStack + AWS |

---

## Instructor

**Juan Marcelo Gutierrez Miranda** — [@TodoEconometria](https://www.linkedin.com/in/juangutierrezconsultor/)

10+ años en análisis de datos y Big Data. Formador de profesionales en toda Latinoamérica y España.

**Contacto:**
- Email: cursos@todoeconometria.com
- LinkedIn: [Juan Gutierrez](https://www.linkedin.com/in/juangutierrezconsultor/)
- Web: [todoeconometria.com](https://www.todoeconometria.com)

---

## Referencias Académicas

1. **Dean, J., & Ghemawat, S. (2008).** MapReduce: Simplified data processing on large clusters. *Communications of the ACM*.
2. **Zaharia, M., et al. (2016).** Apache Spark: A unified engine for big data processing. *Communications of the ACM*.
3. **McKinney, W. (2022).** *Python for Data Analysis*. O'Reilly Media.
4. **Kleppmann, M. (2017).** *Designing Data-Intensive Applications*. O'Reilly Media.

---

<div align="center">

**© 2026 Juan Marcelo Gutierrez Miranda** — Material Educativo Abierto (MIT License)

**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c

</div>
