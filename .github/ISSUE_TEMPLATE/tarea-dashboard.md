---
name: Tarea - Dashboard
about: Template para asignar tarea de dashboard a un alumno
title: 'Dashboard [NOMBRE-ALUMNO] - [TEMA]'
labels: 'tarea, dashboard'
assignees: ''
---

# 📊 Tarea: Dashboard de [TEMA]

## 👨‍🎓 Alumno Asignado

@[usuario-github]

---

## 🎯 Objetivo

Crear un dashboard interactivo con Flask que muestre un análisis exploratorio de datos (EDA) del dataset: **[NOMBRE DEL DATASET]**

---

## 📋 Requisitos Mínimos

### Visualizaciones (Mínimo 3)
- [ ] Gráfico de barras o histograma
- [ ] Gráfico de líneas o series temporales
- [ ] Gráfico de dispersión o correlaciones
- [ ] Otras visualizaciones relevantes

### Estadísticas (Mínimo 5)
- [ ] Media, mediana, desviación estándar
- [ ] Valores máximos y mínimos
- [ ] Conteo de categorías
- [ ] Porcentajes o proporciones
- [ ] Otras métricas relevantes

### Análisis de Calidad de Datos
- [ ] Valores nulos o faltantes
- [ ] Valores duplicados
- [ ] Rango de valores (outliers)
- [ ] Tipos de datos

### Documentación
- [ ] README.md completo con:
  - Descripción del dashboard
  - Instrucciones de instalación
  - Instrucciones de ejecución
  - Tecnologías utilizadas
  - 3-5 conclusiones principales del análisis

---

## 📁 Estructura Esperada

```
dashboards/[nombre-alumno]-dashboard/
├── app.py                    # Aplicación Flask
├── templates/
│   └── index.html           # Template HTML
├── static/                  # CSS, JS, imágenes (opcional)
├── README.md                # Documentación
└── requirements.txt         # Dependencias (opcional)
```

---

## 🚀 Flujo de Trabajo

### 1. Fork del Repositorio
- Ir a: https://github.com/TodoEconometria/ejercicios-bigdata
- Click en "Fork" (esquina superior derecha)
- Ahora tienes tu propia copia del repositorio

### 2. Clonar TU Fork (no el original)
```bash
git clone https://github.com/TU-USUARIO/ejercicios-bigdata.git
cd ejercicios-bigdata
```

### 3. Crear Rama de Trabajo
```bash
git checkout -b alumno/tu-nombre-apellido
```

### 4. Trabajar en el Dashboard
- Crear tu carpeta en `dashboards/`
- Desarrollar el dashboard
- Hacer commits regularmente:
```bash
git add .
git commit -m "Mensaje descriptivo"
```

### 5. Subir a TU Fork
```bash
git push origin alumno/tu-nombre-apellido
```

### 6. Abrir Pull Request
- Ir a TU fork en GitHub
- Verás un botón "Compare & pull request"
- Asegúrate de que el PR va desde:
  - **Base repository**: `TodoEconometria/ejercicios-bigdata` (base: `main`)
  - **Head repository**: `TU-USUARIO/ejercicios-bigdata` (compare: `alumno/tu-nombre-apellido`)
- Llenar el template de PR
- Enviar

---

## 📖 Recursos

- [Guía completa para alumnos](../PARA_ALUMNOS.md)
- [Instrucciones detalladas con PyCharm](../docs/INSTRUCCIONES_ALUMNOS.md)
- [Guía de entrega de dashboards](../docs/GUIA_ENTREGA_DASHBOARDS.md)
- [Template de dashboard de ejemplo](../dashboards/nyc_taxi_eda/)
- [Ejemplos destacados](../dashboards/ejemplos-destacados/)

---

## 🗓️ Fecha de Entrega

**[FECHA]**

---

## ✅ Criterios de Evaluación

- **Funcionalidad (40%)**: El dashboard funciona sin errores
- **Visualizaciones (30%)**: Calidad y relevancia de los gráficos
- **Análisis (20%)**: Profundidad del análisis de datos
- **Documentación (10%)**: Claridad del README y comentarios en código

---

## 💬 Preguntas o Dudas

Si tienes preguntas, comenta en este issue o contacta al profesor.

---

**¡Éxito con tu dashboard! 🚀**
