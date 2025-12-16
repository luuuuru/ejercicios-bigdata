# Guía de Entrega de Dashboards

Esta guía explica cómo los alumnos deben crear, desarrollar y entregar sus dashboards para revisión del curso.

---

## Estructura del Proyecto

El proyecto tiene la siguiente estructura para dashboards:

```
ejercicios_bigdata/
├── dashboards/
│   ├── nyc_taxi_eda/          # Ejemplo de referencia del profesor
│   │   ├── app.py
│   │   ├── templates/
│   │   └── README.md
│   ├── tu-nombre-dashboard/    # Tu dashboard aquí
│   │   ├── app.py
│   │   ├── templates/
│   │   └── README.md
```

---

## Pasos para Crear y Entregar tu Dashboard

### PASO 0: Limpieza Inicial (Solo Primera Vez)

**⚠️ IMPORTANTE:** Si hiciste fork antes del 4 de diciembre de 2025, es posible que tengas archivos antiguos que ya no necesitas. Vamos a limpiarlos.

#### 🖥️ ¿Dónde ejecutar estos comandos?

Tienes 3 opciones:

**Opción A - Terminal de PyCharm (Recomendado):**
1. Abre PyCharm con tu proyecto
2. En el menú inferior, haz clic en **Terminal** (o `Alt + F12`)
3. La terminal se abre en la carpeta correcta automáticamente
4. Ejecuta los comandos directamente

**Opción B - CMD de Windows:**
1. `Win + R` → escribe `cmd` → Enter
2. Navega a tu proyecto:
   ```cmd
   cd C:\ruta\a\tu\ejercicios_bigdata
   ```
3. Ejecuta los comandos (reemplaza `/` por `\` si es necesario)

**Opción C - PowerShell:**
1. Busca "PowerShell" en el menú inicio
2. Navega: `cd C:\ruta\a\tu\ejercicios-bigdata`
3. Ejecuta los comandos

**💡 Tip:** En PyCharm la terminal ya está en la carpeta correcta, es lo más fácil.

---

#### Verificar si necesitas limpiar:

**En PyCharm Terminal o CMD:**
```bash
dir *.md
```

**En PowerShell o Git Bash:**
```bash
ls *.md
```

**Busca estos archivos (NO deberían estar):**
- `README.md` (viejo, debe ser `LEEME.md`)
- `GUIA_GIT_GITHUB.md`
- `GUIA_IA_ASISTENTE.md`
- `INSTRUCCIONES_CONFIGURACION.md`
- `PROGRESO.md`
- Carpeta `plantillas/`

#### ⚠️ ANTES DE LIMPIAR - IMPORTANTE:

**¿Cuándo hacer esta limpieza?**
- ✅ Si hiciste fork ANTES del 4 de diciembre de 2025
- ✅ ANTES de empezar a trabajar en tu dashboard
- ✅ Si aún NO has creado tu carpeta en `dashboards/`
- ❌ **NO hagas esto si ya tienes trabajo sin subir a GitHub**

**Archivos que están seguros (NO se borran):**
- ✅ Tus datos descargados (`datos/nyc_taxi.csv`) - Están en `.gitignore`
- ✅ Tu entorno virtual (`venv/`) - Está en `.gitignore`
- ✅ Bases de datos (`*.db`, `*.sqlite`) - Están en `.gitignore`
- ✅ Otros proyectos fuera de esta carpeta

**Archivos que SÍ se borrarían:**
- ❌ Tu dashboard si ya lo creaste (en `dashboards/tu-nombre/`)
- ❌ Cualquier código que hayas escrito y NO subido a GitHub

---

#### Limpieza SEGURA (Paso a Paso):

**PASO 1: Eliminar archivos viejos UNO POR UNO**

**En PyCharm Terminal o CMD:**
```bash
git rm README.md 2>nul
git rm GUIA_GIT_GITHUB.md 2>nul
git rm GUIA_IA_ASISTENTE.md 2>nul
git rm INSTRUCCIONES_CONFIGURACION.md 2>nul
git rm PROGRESO.md 2>nul
git rm -r plantillas/ 2>nul
```

**En PowerShell o Git Bash:**
```bash
git rm README.md 2>/dev/null
git rm GUIA_GIT_GITHUB.md 2>/dev/null
git rm GUIA_IA_ASISTENTE.md 2>/dev/null
git rm INSTRUCCIONES_CONFIGURACION.md 2>/dev/null
git rm PROGRESO.md 2>/dev/null
git rm -r plantillas/ 2>/dev/null
```

**PASO 2: Guardar la limpieza**
```bash
git commit -m "Limpiar archivos antiguos del repositorio"
```

**PASO 3: Actualizar desde el repositorio del profesor**
```bash
git fetch upstream
git merge upstream/main
```

**PASO 4: Subir los cambios a tu fork en GitHub**
```bash
git push origin main
```

**Verificar que quedó limpio:**

**En PyCharm Terminal o CMD:**
```bash
dir *.md
```

**En PowerShell o Git Bash:**
```bash
ls *.md
```

**Resultado esperado (deberías ver SOLO estos archivos):**
```
LEEME.md
ARQUITECTURA_Y_STACK.md
ENTENDIENDO_GIT_Y_RAMAS.md
ESTRUCTURA_PROYECTO.md
GUIA_ENTREGA_DASHBOARDS.md
INSTRUCCIONES_ALUMNOS.md
```

Si ves otros archivos como `README.md` o `PROGRESO.md`, la limpieza no funcionó. Intenta la Opción 2 (manual).

---

### 1. Actualizar tu Fork

Antes de empezar, asegúrate de tener la última versión del repositorio:

**En PyCharm:**
1. Ve a **Git** > **Fetch**
2. Ve a **Git** > **Merge...**
3. Selecciona `upstream/main` y dale a **Merge**

**En terminal:**
```bash
git fetch upstream
git merge upstream/main
```

---

### 2. Crear una Rama Nueva

**IMPORTANTE:** Nunca trabajes directamente en `main`.

**Nombre de la rama:** `nombre-dashboard-eda`

**Ejemplo:** Si tu nombre es Juan y estás creando un dashboard de EDA:
```bash
git checkout -b juan-dashboard-eda
```

**En PyCharm:**
1. Ve a **Git** > **New Branch...**
2. Escribe: `tu-nombre-dashboard-eda`
3. Haz clic en **Create**

---

### 3. Crear tu Carpeta de Dashboard

Crea una carpeta dentro de `dashboards/` con la siguiente estructura:

```
dashboards/
└── tu-nombre-dashboard/
    ├── app.py              # Tu aplicación Flask
    ├── templates/          # Tus archivos HTML
    │   └── index.html
    ├── static/             # CSS, JS, imágenes (opcional)
    │   ├── css/
    │   ├── js/
    │   └── img/
    └── README.md           # Documentación de tu dashboard
```

**Ejemplo de nombre de carpeta:**
- `juan-taxi-eda`
- `maria-analisis-taxi`
- `pedro-dashboard-nyc`

---

### 4. Desarrollar tu Dashboard

#### Requisitos Mínimos

Tu dashboard debe incluir:

1. **Al menos 3 visualizaciones diferentes:**
   - Gráficos de barras, líneas, dispersión, etc.
   - Pueden ser con Chart.js, Plotly, o Matplotlib

2. **Estadísticas descriptivas:**
   - Media, mediana, moda
   - Desviación estándar
   - Valores mínimos y máximos
   - Conteo de registros

3. **Análisis de calidad de datos:**
   - Valores nulos
   - Tipos de datos
   - Valores atípicos (outliers)

4. **README.md en tu carpeta:**
   - Explicación de qué hace tu dashboard
   - Cómo ejecutarlo
   - Qué visualizaciones incluye
   - Conclusiones del análisis

#### Buenas Prácticas

- **Código comentado:** Explica qué hace cada función
- **Nombres descriptivos:** Variables y funciones con nombres claros
- **Validación de datos:** Maneja errores cuando el archivo no existe
- **Diseño limpio:** Usa CSS para que se vea profesional
- **Responsive:** Que funcione en diferentes tamaños de pantalla

---

### 5. Probar tu Dashboard Localmente

Antes de hacer commit, prueba que todo funciona:

```bash
# Navega a tu carpeta
cd dashboards/tu-nombre-dashboard/

# Ejecuta el dashboard
python app.py
```

Abre tu navegador en: http://localhost:5000

**Verifica:**
- ✅ El dashboard carga sin errores
- ✅ Las visualizaciones se muestran correctamente
- ✅ Los datos se cargan desde `datos/nyc_taxi.csv`
- ✅ Las estadísticas son correctas

---

### 6. Hacer Commit de tus Cambios

Una vez que todo funciona:

**En PyCharm:**
1. Abre la pestaña **Commit** (icono ✔️)
2. Selecciona todos tus archivos nuevos
3. Escribe un mensaje descriptivo:
   ```
   Agregar dashboard EDA de NYC Taxi - [Tu Nombre]

   - Implementar visualizaciones de distancia, tarifa y pasajeros
   - Añadir estadísticas descriptivas
   - Crear interfaz responsive
   ```
4. Haz clic en **Commit**

**En terminal:**
```bash
git add dashboards/tu-nombre-dashboard/
git commit -m "Agregar dashboard EDA de NYC Taxi - [Tu Nombre]"
```

---

### 7. Subir a tu Fork (Push)

**En PyCharm:**
1. Ve a **Git** > **Push...**
2. Verifica que estás subiendo tu rama `tu-nombre-dashboard-eda` a `origin`
3. Haz clic en **Push**

**En terminal:**
```bash
git push -u origin tu-nombre-dashboard-eda
```

---

### 8. Crear Pull Request

**Opción 1: Desde PyCharm**
- Después del push, verás una notificación abajo a la derecha
- Haz clic en el enlace para crear el Pull Request

**Opción 2: Desde GitHub**
1. Ve a tu repositorio en GitHub
2. Verás un banner amarillo: **"Compare & pull request"**
3. Haz clic en el botón

**Configurar el Pull Request:**

- **Base repository:** `TodoEconometria/ejercicios-bigdata`
- **Base branch:** `main`
- **Head repository:** `tu-usuario/ejercicios-bigdata`
- **Compare branch:** `tu-nombre-dashboard-eda`

**Título del PR:**
```
Dashboard EDA NYC Taxi - [Tu Nombre]
```

**Descripción del PR:**
```markdown
## Resumen
Dashboard interactivo para análisis exploratorio del dataset NYC Taxi.

## Características
- 3 visualizaciones interactivas (especifica cuáles)
- Estadísticas descriptivas completas
- Análisis de calidad de datos
- Interfaz responsive

## Tecnologías
- Flask
- Chart.js / Plotly
- Pandas
- HTML/CSS/JavaScript

## Cómo probar
1. `cd dashboards/tu-nombre-dashboard/`
2. `python app.py`
3. Abrir http://localhost:5000

## Capturas de pantalla
(Opcional: agrega capturas de tu dashboard)

## Conclusiones
(Breve resumen de tus hallazgos del análisis)
```

4. Haz clic en **Create pull request**

---

### 9. Comunicación con el Profesor

#### Después de crear el PR:

1. **Esperar revisión:** El profesor recibirá una notificación automática

2. **Responder a comentarios:** Si el profesor deja comentarios en tu código:
   - Lee cada comentario cuidadosamente
   - Haz los cambios solicitados en tu rama local
   - Haz commit de los cambios
   - Push a tu rama (el PR se actualiza automáticamente)

3. **Marcar como resuelto:** Cuando hayas hecho un cambio solicitado:
   - Ve al comentario en GitHub
   - Haz clic en **Resolve conversation**

#### Si necesitas ayuda:

**En el PR:**
- Deja un comentario con tu pregunta
- Menciona al profesor: `@TodoEconometria`

**Por otros canales:**
- Envía el link de tu PR al profesor
- Especifica qué necesitas ayuda

---

## Checklist de Entrega

Antes de crear tu Pull Request, verifica:

- [ ] Creé una rama nueva (no estoy en `main`)
- [ ] Mi carpeta está en `dashboards/mi-nombre-dashboard/`
- [ ] Incluí `app.py` funcional
- [ ] Incluí al menos `templates/index.html`
- [ ] Incluí `README.md` documentando mi trabajo
- [ ] Mi dashboard tiene al menos 3 visualizaciones
- [ ] Mi dashboard muestra estadísticas descriptivas
- [ ] Probé mi dashboard localmente y funciona
- [ ] Mi código está comentado
- [ ] Hice commit con mensaje descriptivo
- [ ] Hice push a mi fork
- [ ] Creé el Pull Request con descripción completa
- [ ] Incluí conclusiones del análisis

---

## Ejemplo de Referencia

Puedes consultar el dashboard de ejemplo en:
```
dashboards/nyc_taxi_eda/
```

Este dashboard incluye:
- Estructura básica de Flask
- 3 tipos de visualizaciones (barras, líneas, dona)
- API endpoints
- Diseño responsive
- Código comentado

**No copies el código directamente.** Úsalo como referencia para entender la estructura y crear tu propia implementación.

---

## Errores Comunes

### Error: "No such file or directory: datos/nyc_taxi.csv"

**Solución:** Asegúrate de que la ruta al archivo sea relativa desde tu carpeta de dashboard:
```python
DATA_PATH = os.path.join('..', '..', 'datos', 'nyc_taxi.csv')
```

### Error: "Port 5000 is already in use"

**Solución:** Otro proceso está usando el puerto. Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Mi gráfico no se muestra

**Solución:**
- Abre la consola del navegador (F12)
- Revisa si hay errores de JavaScript
- Verifica que los datos lleguen correctamente desde el backend

---

## Criterios de Evaluación

Tu dashboard será evaluado en:

1. **Funcionalidad (40%)**
   - El dashboard carga sin errores
   - Las visualizaciones se muestran correctamente
   - Los datos se procesan adecuadamente

2. **Análisis (30%)**
   - Estadísticas relevantes y correctas
   - Visualizaciones apropiadas para los datos
   - Conclusiones basadas en el análisis

3. **Código (20%)**
   - Código limpio y comentado
   - Buenas prácticas de programación
   - Estructura organizada

4. **Documentación (10%)**
   - README completo
   - Descripción clara del PR
   - Instrucciones de uso

---

## Recursos Adicionales

- **Chart.js:** https://www.chartjs.org/docs/latest/
- **Flask Docs:** https://flask.palletsprojects.com/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Plotly:** https://plotly.com/python/

---

## Preguntas Frecuentes

**¿Puedo usar librerías adicionales?**
Sí, pero debes agregarlas a `requirements.txt` en tu PR.

**¿Puedo trabajar en equipo?**
Consulta con el profesor. Si es sí, ambos deben figurar en el README y commits.

**¿Qué pasa si encuentro un error en los datos?**
Documéntalo en tu README y explica cómo lo manejaste.

**¿Puedo usar otro framework en lugar de Flask?**
Consulta con el profesor primero. Flask es el estándar para este curso.

**¿Debo incluir los datos en mi PR?**
NO. Los datos ya están en `datos/`. Solo sube tu código.

---

## Contacto

Si tienes dudas que no están cubiertas en esta guía:
1. Revisa el dashboard de ejemplo
2. Consulta las instrucciones de alumnos
3. Pregunta en el PR
4. Contacta al profesor
