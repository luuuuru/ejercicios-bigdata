# Estructura del Proyecto - Buenas Prácticas

Este documento explica cómo está organizado el proyecto y las buenas prácticas para mantenerlo escalable y profesional.

---

## Estructura Actual

```
ejercicios_bigdata/
│
├── .git/                           # Control de versiones Git
├── .gitignore                      # Archivos ignorados por Git
├── .venv/                          # Entorno virtual Python (no versionado)
│
├── requirements.txt                # Dependencias del proyecto
├── __init__.py                     # Marca como paquete Python
│
├── LEEME.md                        # Documentación general
├── INSTRUCCIONES_ALUMNOS.md        # Guía de Git/PyCharm para alumnos
├── GUIA_ENTREGA_DASHBOARDS.md      # Guía de entrega de dashboards
├── GUIA_PROFESOR.md                # Guía de gestión para profesor
├── ARQUITECTURA_Y_STACK.md         # Explicación del stack tecnológico
├── ESTRUCTURA_PROYECTO.md          # Este archivo
│
├── datos/                          # Datasets del proyecto
│   ├── descargar_datos.py          # Script de descarga
│   ├── nyc_taxi.csv                # Dataset principal
│   ├── taxi_limpio.csv             # Dataset procesado
│   ├── distribucion_distancia.png  # Gráficos generados
│   └── taxi.parquet/               # Datos en formato Parquet
│       ├── part.0.parquet
│       └── part.1.parquet
│
├── ejercicios/                     # Ejercicios de aprendizaje
│   ├── 01_cargar_sqlite.py         # Ejercicio 1: SQLite
│   ├── 02_limpieza_datos.py        # Ejercicio 2: Pandas
│   ├── 03_parquet_dask.py          # Ejercicio 3: Dask
│   └── 04_pyspark_query.py         # Ejercicio 4: PySpark
│
└── dashboards/                     # Dashboards de visualización
    ├── nyc_taxi_eda/               # Dashboard ejemplo (profesor)
    │   ├── app.py                  # Aplicación Flask
    │   ├── templates/              # Templates HTML
    │   │   └── index.html
    │   ├── static/                 # Archivos estáticos (opcional)
    │   │   ├── css/
    │   │   ├── js/
    │   │   └── img/
    │   └── README.md               # Documentación del dashboard
    │
    └── [alumno-nombre-dashboard]/  # Dashboards de alumnos
        └── ...
```

---

## Principios de Organización

### 1. Separación de Responsabilidades

Cada carpeta tiene un propósito específico:

- **`datos/`**: Solo datos y scripts de descarga/preparación
- **`ejercicios/`**: Scripts de ejercicios de aprendizaje
- **`dashboards/`**: Aplicaciones web de visualización
- **Raíz**: Configuración y documentación

### 2. Autocontenido

Cada dashboard debe ser **autocontenido**:

```
alumno-dashboard/
├── app.py              # Todo el código necesario
├── templates/          # Templates propios
├── static/             # Assets propios (si los hay)
└── README.md           # Documentación completa
```

No debe depender de archivos de otros dashboards.

### 3. Rutas Relativas

Siempre usa rutas relativas para acceder a datos:

```python
# ✅ Correcto
import os
DATA_PATH = os.path.join('..', '..', 'datos', 'nyc_taxi.csv')

# ❌ Incorrecto
DATA_PATH = 'C:\\Users\\alumno\\Documents\\datos\\nyc_taxi.csv'
```

### 4. Nomenclatura Consistente

**Archivos Python:**
- Usa snake_case: `cargar_datos.py`, `procesar_taxi.py`

**Carpetas:**
- Minúsculas con guiones: `nyc-taxi-eda`, `juan-dashboard`

**Variables:**
- Descriptivas: `trip_distance`, `fare_amount`
- Evita: `x`, `temp`, `data1`

---

## Escalabilidad

### Cuando el Proyecto Crezca

Si agregas más tipos de contenido:

```
ejercicios_bigdata/
├── datos/
├── ejercicios/
├── dashboards/
├── notebooks/              # Nueva: Jupyter notebooks
│   ├── exploracion.ipynb
│   └── modelos.ipynb
├── scripts/                # Nueva: Scripts utilitarios
│   ├── backup_datos.py
│   └── generar_reportes.py
├── tests/                  # Nueva: Tests automatizados
│   ├── test_ejercicios.py
│   └── test_dashboards.py
└── docs/                   # Nueva: Documentación adicional
    ├── guias/
    └── referencias/
```

### Cuando Tengas Muchos Dashboards

Organiza por categoría:

```
dashboards/
├── ejemplo-profesor/
│   └── nyc_taxi_eda/
├── entregas-clase-2024/
│   ├── juan-dashboard/
│   ├── maria-dashboard/
│   └── pedro-dashboard/
└── entregas-clase-2025/
    └── ...
```

---

## Buenas Prácticas por Tipo de Archivo

### Ejercicios (`ejercicios/*.py`)

```python
"""
Ejercicio X: Descripción breve

Este ejercicio enseña [concepto].
Requisitos: [librerías]
"""

import pandas as pd

# Constantes al inicio
DATA_PATH = '../datos/nyc_taxi.csv'

def funcion_principal():
    """Descripción de qué hace"""
    # código
    pass

if __name__ == '__main__':
    # Solo se ejecuta si se corre directamente
    funcion_principal()
```

### Dashboards (`dashboards/*/app.py`)

```python
"""
Dashboard: [Nombre]
Autor: [Tu nombre]
Descripción: [Qué visualiza]
"""

from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Configuración
DATA_PATH = os.path.join('..', '..', 'datos', 'nyc_taxi.csv')

# Funciones auxiliares
def cargar_datos():
    """Carga y retorna el dataset"""
    pass

# Rutas
@app.route('/')
def index():
    """Página principal"""
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### README de Dashboard

```markdown
# Dashboard [Nombre]

Breve descripción del dashboard.

## Autor
[Tu nombre]

## Características
- Visualización 1
- Visualización 2
- Estadística X

## Cómo ejecutar
[instrucciones]

## Dependencias
[librerías adicionales si las hay]

## Conclusiones
[Qué aprendiste del análisis]
```

---

## Gestión de Datos

### Versionamiento de Datos

**NO versionar:**
- Archivos grandes (>100MB)
- Archivos generados automáticamente
- Datos temporales

**SÍ versionar:**
- Datasets pequeños de ejemplo (<10MB)
- Scripts de descarga/generación
- Metadata y descripciones

**En `.gitignore`:**
```
# Datos grandes
datos/*.csv
datos/*.parquet

# Excepciones: archivos pequeños
!datos/ejemplo.csv
```

### Organización de Datos

```
datos/
├── raw/                    # Datos originales (no tocar)
│   └── nyc_taxi.csv
├── processed/              # Datos procesados
│   ├── taxi_limpio.csv
│   └── taxi.parquet/
├── interim/                # Datos intermedios (opcional)
└── external/               # Datos de fuentes externas
```

---

## Testing en Proyectos Educativos

### Tests Básicos

Crea `tests/test_basico.py`:

```python
"""Tests básicos para verificar que los ejercicios funcionan"""

def test_import_ejercicio_1():
    """Verifica que el ejercicio 1 se puede importar"""
    try:
        import ejercicios.ejercicio_01_cargar_sqlite as ex1
        assert True
    except Exception as e:
        assert False, f"Error al importar: {e}"

def test_dashboard_carga():
    """Verifica que el dashboard carga sin errores"""
    from dashboards.nyc_taxi_eda import app
    client = app.app.test_client()
    response = client.get('/')
    assert response.status_code == 200
```

### Ejecutar Tests

```bash
pip install pytest
pytest tests/
```

---

## Documentación

### Niveles de Documentación

1. **README principal (LEEME.md)**
   - Visión general del proyecto
   - Instalación básica
   - Links a otras guías

2. **Guías específicas**
   - INSTRUCCIONES_ALUMNOS.md
   - GUIA_ENTREGA_DASHBOARDS.md
   - GUIA_PROFESOR.md

3. **Documentación de código**
   - Docstrings en funciones
   - Comentarios en lógica compleja

4. **READMEs de dashboards**
   - Cómo ejecutar
   - Qué hace
   - Conclusiones

### Template de README para Dashboard

```markdown
# [Nombre del Dashboard]

## Descripción
[1-2 párrafos explicando qué hace]

## Características
- Feature 1
- Feature 2

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```bash
cd dashboards/mi-dashboard
python app.py
```

Luego abre: http://localhost:5000

## Estructura
```
mi-dashboard/
├── app.py
├── templates/
└── README.md
```

## Tecnologías
- Flask
- Pandas
- Chart.js

## Capturas
[Opcional: screenshots]

## Autor
[Tu nombre]

## Licencia
Educativo
```

---

## Control de Versiones

### Estrategia de Branches

**Main/Master:**
- Código estable y revisado
- Solo merge desde PRs aprobados

**Feature branches:**
- `feature/ejercicio-5`
- `feature/nuevo-dataset`

**Student branches:**
- `alumno-nombre-dashboard`
- `alumno-nombre-ejercicio-X`

### Commits Significativos

```bash
# ✅ Buenos commits
git commit -m "Agregar ejercicio 5: análisis con PySpark MLlib"
git commit -m "Corregir error de división por cero en ejercicio 2"
git commit -m "Actualizar README con instrucciones de instalación"

# ❌ Malos commits
git commit -m "cambios"
git commit -m "fix"
git commit -m "asdfasdf"
```

### Anatomía de un Buen Commit

```
Título corto (50 caracteres o menos)

Descripción detallada opcional:
- Qué cambiaste
- Por qué lo cambiaste
- Impacto de los cambios

Fixes #123 (si aplica)
```

---

## Seguridad

### Nunca Versionar

```
# En .gitignore
.env
.env.local
secrets.json
credentials.json
*.key
*.pem
```

### Si Usas APIs

```python
# ✅ Correcto
import os
API_KEY = os.environ.get('API_KEY')

# ❌ Incorrecto
API_KEY = 'abc123xyz456'
```

---

## Performance

### Carga de Datos en Dashboards

```python
# ❌ Malo: Carga datos en cada request
@app.route('/')
def index():
    df = pd.read_csv('datos.csv')  # Lento
    return render_template('index.html', data=df)

# ✅ Mejor: Carga una vez al inicio
df_global = None

def cargar_datos():
    global df_global
    if df_global is None:
        df_global = pd.read_csv('datos.csv')
    return df_global

@app.route('/')
def index():
    df = cargar_datos()  # Rápido
    return render_template('index.html', data=df)
```

### Archivos Grandes

```python
# Para datasets grandes, usa Dask o chunks
import dask.dataframe as dd

df = dd.read_csv('datos_grandes.csv')
# Procesa en paralelo automáticamente
```

---

## Recursos Adicionales

**Estructura de Proyectos:**
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)

**Git Best Practices:**
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)

**Flask Structure:**
- [Flask Application Factory](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/2.3.x/tutorial/)

---

Este documento es una guía viva. Actualízalo conforme el proyecto evolucione.
