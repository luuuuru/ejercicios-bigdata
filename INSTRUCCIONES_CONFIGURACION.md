# Instrucciones de Configuración Inicial

> Sigue estos pasos ANTES de comenzar con los ejercicios.

## Paso 1: Verifica que Hiciste Fork/Template

Asegúrate de que estás trabajando en TU copia del repositorio:
- La URL debe ser: `https://github.com/TU_USUARIO/ejercicios-bigdata`
- NO debe ser: `https://github.com/TodoEconometria/ejercicios-bigdata` (ese es el original)

## Paso 2: Clona TU Repositorio

```bash
# Reemplaza TU_USUARIO con tu usuario de GitHub
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
cd ejercicios-bigdata
```

## Paso 3: Crea las Carpetas de Trabajo

Estas carpetas NO están en el repositorio. Debes crearlas:

```bash
# En Windows (PowerShell o CMD):
mkdir datos
mkdir ejercicios

# En Mac/Linux:
mkdir datos ejercicios
```

## Paso 4: Copia las Plantillas

Ahora copia los archivos desde `plantillas/` a tus carpetas de trabajo:

### En Windows (PowerShell):
```powershell
# Copiar script de descarga de datos
copy plantillas\datos\descargar_datos.py datos\

# Copiar ejercicios
copy plantillas\ejercicios\*.py ejercicios\
```

### En Windows (Command Prompt/CMD):
```cmd
# Copiar script de descarga de datos
copy plantillas\datos\descargar_datos.py datos\

# Copiar ejercicios
copy plantillas\ejercicios\*.py ejercicios\
```

### En Mac/Linux:
```bash
# Copiar script de descarga de datos
cp plantillas/datos/descargar_datos.py datos/

# Copiar ejercicios
cp plantillas/ejercicios/*.py ejercicios/
```

## Paso 5: Verifica la Estructura

Tu proyecto debe verse así:

```
ejercicios-bigdata/
├── README.md
├── GUIA_GIT_GITHUB.md
├── GUIA_IA_ASISTENTE.md
├── PROGRESO.md
├── requirements.txt
├── plantillas/          ← Plantillas originales (NO modificar)
│   ├── datos/
│   └── ejercicios/
├── datos/               ← TU carpeta de trabajo (nueva)
│   └── descargar_datos.py
└── ejercicios/          ← TU carpeta de trabajo (nueva)
    ├── 01_cargar_sqlite.py
    ├── 02_limpieza_datos.py
    ├── 03_parquet_dask.py
    └── 04_pyspark_query.py
```

Verifica con:
```bash
# En Windows:
dir datos
dir ejercicios

# En Mac/Linux:
ls datos
ls ejercicios
```

Deberías ver los archivos .py en cada carpeta.

## Paso 6: Crea el Entorno Virtual de Python

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno
# En Windows:
.venv\Scripts\activate

# En Mac/Linux:
source .venv/bin/activate
```

Verás `(.venv)` al inicio de tu línea de comandos cuando esté activado.

## Paso 7: Instala las Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará: pandas, dask, pyspark, matplotlib, seaborn, etc.

## Paso 8: Descarga los Datos

```bash
python datos/descargar_datos.py
```

Esto descargará la base de datos de taxis (~158 MB).

## Paso 9: Verifica que Todo Funciona

Prueba ejecutar el primer ejercicio:

```bash
python ejercicios/01_cargar_sqlite.py
```

Si ves resultados y no errores, ¡todo está listo! 🎉

## Paso 10: Haz tu Primer Commit

```bash
# NO hagas commit de datos/ ni ejercicios/ (están en .gitignore)
# Solo actualiza tu PROGRESO.md

git add PROGRESO.md
git commit -m "Configuración inicial completada"
git push origin main
```

## Problemas Comunes

### "No such file or directory: datos/descargar_datos.py"
**Solución**: No copiaste las plantillas. Vuelve al Paso 4.

### "python: command not found"
**Solución**: Python no está instalado o no está en el PATH. Descárgalo de [python.org](https://www.python.org/downloads/)

### "pip: command not found"
**Solución**: Asegúrate de haber activado el entorno virtual (Paso 6).

### Los archivos no se copian en Windows
**Solución**: Usa PowerShell en lugar de CMD, o copia manualmente los archivos desde el explorador de archivos.

## ¿Por qué No se Suben datos/ y ejercicios/ a GitHub?

- **datos/**: Contiene archivos muy grandes (158 MB). GitHub tiene límites de tamaño.
- **ejercicios/**: Es TU código de trabajo. Cada estudiante tendrá su propia versión.
- **plantillas/**: Son las versiones originales que SÍ están en GitHub como referencia.

Cuando hagas cambios en tus ejercicios, Git NO los subirá automáticamente (están en `.gitignore`).

## Siguiente Paso

Lee **LEEME.md** para comenzar con los ejercicios.

---

**¿Problemas?** Consulta la **GUIA_GIT_GITHUB.md** o abre un Issue en tu repositorio.
