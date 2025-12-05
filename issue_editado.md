# 📊 Tarea 1: Dashboard EDA - NYC Taxi Dataset

## Objetivo
Crear un dashboard web interactivo usando Flask para analizar el dataset de taxis de NYC.

## ⚠️ IMPORTANTE: Descarga de Datos

**El archivo de datos NO está en el repositorio** (es muy grande para GitHub - 121 MB).

### Cómo obtener los datos:

**Opción 1 - Script automático (Recomendado):**
```bash
cd datos/
python descargar_datos.py
```

**Opción 2 - Descarga manual:**
Si el script falla, consulta `datos/README.md` para instrucciones de descarga manual.

**Verificación:**
Después de descargar, deberías tener el archivo: `datos/nyc_taxi.csv`

---

## Dataset
- **Archivo:** `datos/nyc_taxi.csv`
- **Ubicación:** Debes descargarlo (ver instrucciones arriba)
- **Tamaño:** ~121 MB
- **Contenido:** Viajes de taxi en Nueva York
- **Columnas principales:** `trip_distance`, `fare_amount`, `passenger_count`, etc.

## Lo Que Debes Entregar

### 1. Tu Carpeta Personal
Crea una carpeta con tu nombre:
```
dashboards/tu-nombre-apellido-dashboard/
├── app.py              (tu código Flask)
├── templates/
│   └── index.html      (tu página web)
└── README.md           (explicación de tu trabajo)
```

**Ejemplo de nombre:** Si te llamas Juan Pérez:
```
dashboards/juan-perez-dashboard/
```

### 2. Requisitos Mínimos

Tu dashboard DEBE tener:

#### ✅ Estadísticas (mínimo 5)
- Total de viajes
- Distancia promedio
- Tarifa promedio
- Más/menos pasajeros frecuentes
- Valores nulos

#### ✅ Visualizaciones (mínimo 3 gráficos)
- Gráfico 1: Distribución de distancias
- Gráfico 2: Distribución de tarifas
- Gráfico 3: Pasajeros por viaje

Puedes usar Chart.js, Plotly, o cualquier librería de gráficos.

#### ✅ README.md en tu carpeta
Debe incluir:
- Qué hace tu dashboard
- Cómo ejecutarlo
- 3-5 conclusiones de tu análisis

### 3. Ejemplo de Referencia

Puedes ver el ejemplo del profesor en:
```
dashboards/nyc_taxi_eda/
```

**Ver código:** [dashboards/nyc_taxi_eda/app.py](https://github.com/TodoEconometria/ejercicios-bigdata/blob/main/dashboards/nyc_taxi_eda/app.py)

**IMPORTANTE:**
- ✅ Úsalo como referencia para entender la estructura
- ❌ NO copies el código
- ✅ Implementa tu propia solución

---

## Cómo Entregar

Lee la guía completa: **[GUIA_ENTREGA_DASHBOARDS.md](GUIA_ENTREGA_DASHBOARDS.md)**

### ⚠️ PASO 0 (MUY IMPORTANTE): Limpiar tu Fork

**Si hiciste fork ANTES del 4 de diciembre de 2025**, primero debes limpiar archivos viejos.

**⚠️ HAZLO SOLO SI:**
- ✅ Aún NO empezaste a trabajar en tu dashboard
- ✅ NO has creado tu carpeta en `dashboards/`
- ❌ **NO lo hagas si ya tienes código sin subir a GitHub**

**Limpieza segura (4 pasos):**

```bash
# 1. Borrar archivos viejos uno por uno
git rm README.md GUIA_GIT_GITHUB.md GUIA_IA_ASISTENTE.md INSTRUCCIONES_CONFIGURACION.md PROGRESO.md 2>nul
git rm -r plantillas/ 2>nul

# 2. Guardar la limpieza
git commit -m "Limpiar archivos antiguos del repositorio"

# 3. Actualizar desde el profesor
git fetch upstream
git merge upstream/main

# 4. Subir a tu fork
git push origin main
```

**Verificar que está limpio:**
```bash
dir *.md
# Deberías ver SOLO: LEEME.md, ARQUITECTURA_Y_STACK.md, ESTRUCTURA_PROYECTO.md,
# GUIA_ENTREGA_DASHBOARDS.md, INSTRUCCIONES_ALUMNOS.md, ENTENDIENDO_GIT_Y_RAMAS.md
```

**📖 Detalles completos:** Ver **[GUIA_ENTREGA_DASHBOARDS.md - PASO 0](GUIA_ENTREGA_DASHBOARDS.md#paso-0-limpieza-inicial-solo-primera-vez)**

---

### Resumen rápido:

#### Paso 1: Actualizar tu fork
```bash
git fetch upstream
git merge upstream/main
```

#### Paso 2: Descargar los datos
```bash
cd datos/
python descargar_datos.py
# Verifica que existe: datos/nyc_taxi.csv
```

#### Paso 3: Crear tu rama
```bash
git checkout -b tu-nombre-dashboard-eda
```
Ejemplo: `git checkout -b juan-perez-dashboard-eda`

#### Paso 4: Crear tu carpeta y desarrollar
```bash
mkdir dashboards/tu-nombre-dashboard
cd dashboards/tu-nombre-dashboard
# Crear app.py, templates/, README.md
# Programar tu dashboard
```

#### Paso 5: Probar que funciona
```bash
python app.py
# Abrir http://localhost:5000
# Verificar que todo funciona
```

#### Paso 6: Hacer commit y push
```bash
git add dashboards/tu-nombre-dashboard/
git commit -m "Agregar dashboard EDA - [Tu Nombre]"
git push -u origin tu-nombre-dashboard-eda
```

#### Paso 7: Crear Pull Request
1. Ve a GitHub
2. Verás un botón "Compare & pull request"
3. Haz clic y crea el PR

---

## Fechas

- **📅 Fecha de entrega:** 20 de diciembre de 2025, 23:59
- **📅 Tiempo estimado:** 2 semanas

---

## Ayuda

Si tienes problemas:

1. **Lee la documentación:**
   - [GUIA_ENTREGA_DASHBOARDS.md](GUIA_ENTREGA_DASHBOARDS.md) - Guía paso a paso
   - [ENTENDIENDO_GIT_Y_RAMAS.md](ENTENDIENDO_GIT_Y_RAMAS.md) - Explicación de Git
   - [INSTRUCCIONES_ALUMNOS.md](INSTRUCCIONES_ALUMNOS.md) - Git con PyCharm

2. **Consulta el ejemplo:**
   - [dashboards/nyc_taxi_eda/](https://github.com/TodoEconometria/ejercicios-bigdata/tree/main/dashboards/nyc_taxi_eda)

3. **Pregunta:**
   - Crea un Issue con etiqueta `help wanted`
   - Describe tu problema específico con capturas si es posible

4. **Problemas comunes:**
   - **Error "FileNotFoundError: nyc_taxi.csv"** → No descargaste los datos
   - **Error "Port 5000 in use"** → Cambia el puerto en app.py
   - **Gráficos no se muestran** → Revisa la consola del navegador (F12)

---

## Evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Funcionalidad** | 40% | El dashboard funciona sin errores |
| **Análisis** | 30% | Estadísticas correctas, visualizaciones apropiadas |
| **Código** | 20% | Limpio, comentado, bien estructurado |
| **Documentación** | 10% | README completo con conclusiones |

### Rúbrica Detallada

**Funcionalidad (40 pts):**
- Dashboard carga sin errores
- Todas las visualizaciones funcionan
- Datos se procesan correctamente

**Análisis (30 pts):**
- Estadísticas descriptivas correctas
- Visualizaciones apropiadas para los datos
- Conclusiones basadas en el análisis

**Código (20 pts):**
- Código limpio y organizado
- Comentarios útiles
- Buenas prácticas (rutas relativas, nombres descriptivos)

**Documentación (10 pts):**
- README completo con instrucciones
- Descripción clara del análisis

---

## Puntos Extra (Opcional)

- **+5 pts:** Más de 5 visualizaciones
- **+5 pts:** Filtros interactivos
- **+5 pts:** Diseño excepcional (UX/UI)
- **+5 pts:** Análisis estadístico avanzado (correlaciones, outliers)
- **+5 pts:** Tests automatizados

---

## Dependencias

El proyecto usa estas librerías (ver `requirements.txt`):
- `flask` - Framework web
- `pandas` - Análisis de datos
- `plotly` o Chart.js - Visualizaciones

**Instalar dependencias:**
```bash
pip install -r requirements.txt
```

---

¡Éxito con tu dashboard! 🚀

**Recursos útiles:**
- Flask: https://flask.palletsprojects.com/
- Pandas: https://pandas.pydata.org/docs/
- Chart.js: https://www.chartjs.org/docs/
