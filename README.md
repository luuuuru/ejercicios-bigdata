# 🎓 Ejercicios Big Data con Python

> Repositorio educativo para aprender Big Data con Python, Pandas, Dask, PySpark y visualización de datos.

[![Disponible para Consultoría](https://img.shields.io/badge/Consultoría-Disponible-brightgreen)](mailto:cursos@todoeconometria.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-blue)](https://www.linkedin.com/in/juangutierrezconsultor/)
[![Web](https://img.shields.io/badge/Web-TodoEconometria-orange)](https://www.todoeconometria.com)

---

## 🚀 Inicio Rápido

**👨‍🎓 ¿Eres alumno?** → Lee **[PARA_ALUMNOS.md](PARA_ALUMNOS.md)**

**👀 ¿Solo curioseas?** → Explora los **[ejemplos destacados](dashboards/ejemplos-destacados/)**

**🤝 ¿Quieres contribuir?** → Crea un [Issue](../../issues) o [Pull Request](../../pulls)

---

## 📚 ¿Qué aprenderás?

Este repositorio contiene ejercicios prácticos y dashboards interactivos para dominar:

### 🔧 Tecnologías Big Data
- **SQLite** - Bases de datos relacionales
- **Pandas** - Análisis de datos en Python
- **Dask** - Procesamiento paralelo de datos
- **PySpark** - Big Data distribuido
- **Parquet** - Formatos optimizados de almacenamiento

### 📊 Visualización de Datos
- **Flask** - Aplicaciones web interactivas
- **Chart.js** - Gráficos JavaScript
- **Plotly** - Visualizaciones avanzadas
- **Dashboards EDA** - Análisis exploratorio de datos

---

## 🗂️ Estructura del Proyecto

```
ejercicios_bigdata/
├── datos/                          # Datasets (NYC Taxi)
├── ejercicios/                     # Ejercicios de aprendizaje
│   ├── 01_cargar_sqlite.py
│   ├── 02_limpieza_datos.py
│   ├── 03_parquet_dask.py
│   └── 04_pyspark_query.py
├── dashboards/                     # Dashboards de visualización
│   ├── nyc_taxi_eda/              # Dashboard de ejemplo
│   └── ejemplos-destacados/        # Los mejores trabajos
└── scripts/                        # Scripts de automatización
```

---

## 🌟 Trabajos Destacados

Los mejores proyectos de la comunidad:

### 🏆 Hall of Fame

> Próximamente - Los mejores trabajos de todos los tiempos

### 📅 Top 3 del Mes

> Actualizándose mensualmente con los mejores trabajos de alumnos

[Ver todos los trabajos destacados →](dashboards/ejemplos-destacados/)

---

## 🎯 Para Alumnos

### Cómo Empezar

1. **Haz Fork** de este repositorio
2. **Clona** tu fork localmente
3. **Sigue** la guía completa en [PARA_ALUMNOS.md](PARA_ALUMNOS.md)
4. **Desarrolla** tu dashboard
5. **Crea** un Pull Request

### Requisitos del Dashboard

- ✅ Mínimo 3 visualizaciones diferentes
- ✅ Estadísticas descriptivas completas
- ✅ Análisis de calidad de datos
- ✅ README.md con documentación
- ✅ Código limpio y comentado

[Ver guía completa para alumnos →](PARA_ALUMNOS.md)

---

## 🤝 Contribuir

Este es un proyecto educativo **open source**. Las contribuciones son bienvenidas:

- 🐛 Reporta bugs creando un [Issue](../../issues)
- 💡 Propón mejoras o nuevos ejercicios
- 📝 Mejora la documentación
- ⭐ Dale una estrella si te gusta el proyecto

### Tipos de Contribución

1. **Mejoras al código base** - PRs a `main` (ejercicios, scripts, docs)
2. **Dashboards educativos** - Comparte tu trabajo
3. **Datasets adicionales** - Propón nuevos datasets para ejercicios

**Nota:** Si tienes dudas sobre cómo contribuir, crea un [Issue](../../issues) preguntando.

---

## 💼 Servicios Profesionales

Este repositorio es mi **portafolio educativo**. Si necesitas servicios profesionales:

### 🎯 Ofrezco

- ✅ **Consultoría en Big Data** - Arquitectura y optimización
- ✅ **Desarrollo de Pipelines** - ETL/ELT con Python y Spark
- ✅ **Capacitación Empresarial** - Entrenamientos personalizados
- ✅ **Análisis de Datos** - Insights accionables para tu negocio
- ✅ **Automatización** - Scripts y workflows de datos

### 📞 Contacto Profesional

- 📧 **Email:** [cursos@todoeconometria.com](mailto:cursos@todoeconometria.com)
- 💼 **LinkedIn:** [Juan Gutiérrez](https://www.linkedin.com/in/juangutierrezconsultor/)
- 🌐 **Web:** [www.todoeconometria.com](https://www.todoeconometria.com)
- 📅 **Agendar reunión:** Escríbeme para coordinar

### 💰 Servicios

- **Consultoría por hora** - Sesiones de asesoría técnica
- **Capacitación empresarial** - Programas desde nivel básico a avanzado
- **Desarrollo de proyectos** - Cotización personalizada según alcance

---

## ❓ Soporte y Ayuda

### Para Dudas del Curso (Gratis)

- 📖 Lee el [FAQ](docs/FAQ.md)
- 🔍 Busca en [Issues cerrados](../../issues?q=is%3Aissue+is%3Aclosed)
- 💬 Crea un [Issue](../../issues) con label `question`

### Para Servicios Profesionales

- 📧 Contacto directo: [cursos@todoeconometria.com](mailto:cursos@todoeconometria.com)

---

## 📖 Documentación Completa

- **[PARA_ALUMNOS.md](PARA_ALUMNOS.md)** - Guía completa para estudiantes
- **[Ejemplos Destacados](dashboards/ejemplos-destacados/)** - Los mejores trabajos
- **[Guía de Scripts](scripts/README.md)** - Herramientas de automatización

---

## 🛠️ Instalación Rápida

```bash
# 1. Clona el repositorio
git clone https://github.com/TodoEconometria/ejercicios-bigdata.git
cd ejercicios-bigdata

# 2. Crea entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Descarga los datos
cd datos
python descargar_datos.py

# 5. Prueba un ejercicio
cd ../ejercicios
python 01_cargar_sqlite.py

# 6. Ejecuta el dashboard de ejemplo
cd ../dashboards/nyc_taxi_eda
python app.py
# Abre http://localhost:5000
```

---

## 📊 Datasets

### NYC Taxi Dataset

Dataset principal para los ejercicios:
- **Registros:** ~100,000 viajes
- **Periodo:** Enero 2024
- **Tamaño:** ~15 MB
- **Variables:** 19 columnas (distancia, tarifa, pasajeros, etc.)

[Más info sobre los datos →](datos/README.md)

---

## 📜 Licencia

Este proyecto es **educativo** y está disponible bajo licencia MIT.

Úsalo libremente para:
- ✅ Aprender y enseñar
- ✅ Proyectos personales
- ✅ Proyectos comerciales (con atribución)

---

## 🙏 Agradecimientos

Gracias a todos los alumnos que han contribuido con sus dashboards y a la comunidad open source.

---

## ⭐ ¿Te gustó?

Si este repositorio te fue útil:
- Dale una ⭐ estrella en GitHub
- Compártelo con otros estudiantes
- Contribuye con mejoras
- Sígueme en [LinkedIn](https://www.linkedin.com/in/juangutierrezconsultor/)

---

<p align="center">
  <strong>Hecho con 💙 para la comunidad de Data Science</strong><br>
  <a href="https://www.todoeconometria.com">www.todoeconometria.com</a>
</p>
