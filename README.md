# 🚀 Big Data con Python - De Cero a Producción

> **Aprende a procesar millones de registros de forma escalable y reproducible**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

### [**Visita el sitio web del curso**](https://todoeconometria.github.io/ejercicios-bigdata/) — Documentacion, dashboards interactivos y guias completas.

---

## 👨‍🏫 Autor y Metodología

**Profesor:** Juan Marcelo Gutierrez Miranda  
**Afiliación:** @TodoEconometria  
**Repositorio Oficial:** [github.com/TodoEconometria/ejercicios-bigdata](https://github.com/TodoEconometria/ejercicios-bigdata)

> Este curso sigue una metodología rigurosa basada en referencias académicas líderes en computación distribuida y ciencia de datos (Dean & Ghemawat, 2008; Zaharia et al., 2016).

---

## 🎯 Objetivo del Curso

Capacitar a estudiantes y profesionales en el manejo de grandes volúmenes de datos utilizando el ecosistema moderno de Python. El enfoque es **práctico ("Hands-on")** pero con fundamentos teóricos sólidos.

### ¿Qué aprenderás?

1. **Gestión de Datos:** SQL vs NoSQL, almacenamiento columnar (Parquet).
2. **Procesamiento Distribuido:** Dask y Apache Spark.
3. **Escalabilidad:** Pipeline ETL reproducibles.
4. **Calidad de Datos:** Limpieza y validación automática.

---

## 🏗️ Estructura del Repositorio

Este repositorio contiene **ejercicios diseñados para ser completados por el estudiante**.  
NO contiene soluciones directas en la rama principal.

```plaintext
ejercicios-bigdata/
├── ejercicios/                 # Enunciados y esqueletos de codigo
│   ├── 01_bases_de_datos/
│   ├── 02_limpieza_datos/
│   ├── 03_procesamiento_distribuido/
│   ├── 04_machine_learning/
│   ├── 05_nlp_text_mining/
│   ├── 06_análisis_datos_de_panel/
│   └── utils/                  # Herramientas auxiliares (Parquet, Spark)
│
├── datos/                      # Instrucciones y scripts de descarga
│   ├── qog/                    # Quality of Government (Panel Data)
│   └── descargar_datos.py      # Descarga automatica de datasets
│
├── entregas/                   # Zona de entregas por modulo
│   ├── 01_bases_de_datos/
│   ├── 02_limpieza_datos/
│   └── ...
│
├── trabajo_final/              # Proyecto integrador (Capstone)
│   └── plantilla/              # Plantilla numerada para el alumno
│
└── docs/                       # Documentacion web (MkDocs)
```

---

## 🚀 Inicio Rápido

Sigue estos pasos para configurar tu entorno de trabajo:

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
cd ejercicios-bigdata
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Infraestructura (Docker)
Este curso requiere PostgreSQL y pgAdmin. Consulta la guia de infraestructura:

> [Guia de Infraestructura](https://todoeconometria.github.io/ejercicios-bigdata/infraestructura/)

### 5. Descargar Datasets
```bash
# Descargar dataset NYC Taxi
python datos/descargar_datos.py
```
> Para el dataset QoG y otros, consulta las instrucciones en `datos/qog/README.md`.

---

## 📚 Referencias Académicas Principales

El diseño de estos ejercicios se basa en:

1. **Dean, J., & Ghemawat, S. (2008).** MapReduce: Simplified data processing on large clusters. *Communications of the ACM*.
2. **Zaharia, M., et al. (2016).** Apache Spark: A unified engine for big data processing. *Communications of the ACM*.
3. **McKinney, W. (2022).** *Python for Data Analysis*. O'Reilly Media.
4. **Kleppmann, M. (2017).** *Designing Data-Intensive Applications*. O'Reilly Media.

---

## 🤝 Contribuciones (Para Estudiantes)

1. Haz **Fork** de este repositorio.
2. Crea una rama para tu solución (`git checkout -b solucion-ejercicio-01`).
3. Resuelve el ejercicio completando los scripts.
4. Ejecuta los tests (si aplica).
5. Envía un **Pull Request** para revisión.

---

**© 2026 Juan Marcelo Gutierrez Miranda** - Material Educativo Abierto (MIT License)
