# Instrucciones para el Profesor

> Estas instrucciones son para ti como profesor. Los estudiantes NO necesitan leer este archivo.

## Cómo Subir este Repositorio a GitHub

### Opción 1: Crear Repositorio desde GitHub (Recomendado)

1. Ve a [GitHub.com](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `ejercicios-bigdata` (o el nombre que prefieras)
   - **Description**: "Ejercicios prácticos de Big Data con Python para estudiantes"
   - **Visibility**:
     - **Public** ✅ (recomendado para que todos puedan hacer fork)
     - Private (solo si quieres control de acceso)
   - **NO marques** "Initialize with README" (ya tenemos uno)
4. Haz clic en **"Create repository"**
5. GitHub te mostrará instrucciones. Usa estas (desde la carpeta del proyecto):

```bash
# Ya hicimos git init y el primer commit, solo falta conectar con GitHub
git remote add origin https://github.com/TodoEconometria/ejercicios-bigdata.git
git branch -M main
git push -u origin main
```

### Opción 2: Usar GitHub CLI (gh)

Si tienes GitHub CLI instalado:

```bash
gh repo create ejercicios-bigdata --public --source=. --remote=origin --push
```

## Cómo Configurarlo como Template Repository

Para que los estudiantes puedan usar este repo como template:

1. Ve a tu repositorio en GitHub
2. Click en **Settings** (pestaña superior)
3. En la sección "General", marca la casilla **"Template repository"**
4. Guarda los cambios

Ahora cuando compartas el link, los estudiantes verán un botón **"Use this template"** en lugar de Fork.

## Diferencia: Template vs Fork

### Template Repository (Recomendado para este caso)
- Los estudiantes hacen clic en **"Use this template"**
- Crea una copia completamente independiente
- NO mantiene conexión con el original
- Cada estudiante tiene su propio repo sin historial compartido

### Fork Tradicional
- Los estudiantes hacen clic en **"Fork"**
- Mantiene conexión con el original
- Puedes ver fácilmente todos los forks
- Ideal si planeas hacer actualizaciones que los estudiantes deben sincronizar

**Recomendación**: Usa **Template** si los estudiantes trabajan independientemente. Usa **Fork** si planeas actualizar el repo durante el curso.

## Cómo Ver el Progreso de los Estudiantes

### Si usaste Template:
1. Pide a cada estudiante que te comparta el link de su repositorio
2. Guarda los links en una hoja de cálculo
3. Visita cada repo para ver commits y progreso

### Si usaste Fork:
1. Ve a tu repositorio en GitHub
2. Haz clic en **"Forks"** (debajo del título del repo)
3. Verás lista de todos los forks
4. Haz clic en cada uno para ver su progreso

## Estructura de Archivos que Subiste

```
ejercicios_bigdata/
├── README.md                      # Guía principal (lo primero que ven los estudiantes)
├── GUIA_GIT_GITHUB.md            # Tutorial de Git para principiantes
├── GUIA_IA_ASISTENTE.md          # Guía de uso de IA (Claude, Copilot, etc.)
├── PROGRESO.md                   # Checklist de avance para estudiantes
├── INSTRUCCIONES_PROFESOR.md     # Este archivo (solo para ti)
├── LEEME.md                      # Instrucciones técnicas de ejercicios
├── ARQUITECTURA_Y_STACK.md       # Conceptos avanzados
├── .gitignore                    # Ignora .venv, datos, __pycache__, etc.
├── requirements.txt              # Dependencias Python
├── __init__.py                   # Marca el proyecto como paquete Python
├── datos/
│   ├── .gitkeep                  # Mantiene la carpeta en git
│   └── descargar_datos.py        # Script para descargar datos
└── ejercicios/
    ├── 01_cargar_sqlite.py       # Ejercicio 1: SQLite
    ├── 02_limpieza_datos.py      # Ejercicio 2: Pandas
    ├── 03_parquet_dask.py        # Ejercicio 3: Dask
    └── 04_pyspark_query.py       # Ejercicio 4: Spark
```

## Instrucciones para los Estudiantes (Resumen)

Una vez que subas el repo a GitHub, comparte estas instrucciones:

---

### Para Estudiantes: Cómo Empezar

1. **Haz Fork/Template** del repositorio: https://github.com/TodoEconometria/ejercicios-bigdata
2. **Clona TU copia** a tu computadora:
   ```bash
   git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
   cd ejercicios-bigdata
   ```
3. **Lee el README.md** - Ahí está todo explicado paso a paso
4. **Sigue la GUIA_GIT_GITHUB.md** si es tu primera vez con Git
5. **Usa PROGRESO.md** para marcar tu avance
6. **Haz commits frecuentes** y push regularmente

---

## Cómo Actualizar el Repo Durante el Curso

Si necesitas agregar contenido o corregir errores:

1. Haz los cambios en tu repositorio local
2. Commit y push:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push origin main
   ```

3. Notifica a los estudiantes que actualicen:
   ```bash
   # Estudiantes ejecutan en su fork/template:
   git remote add upstream https://github.com/TodoEconometria/ejercicios-bigdata.git
   git fetch upstream
   git merge upstream/main
   ```

## Evaluación del Progreso

Revisa en cada repositorio de estudiante:

1. **Commits**: Frecuencia y calidad de mensajes
2. **PROGRESO.md**: Si están marcando su avance
3. **Código**: Cambios en los archivos de ejercicios
4. **Issues**: Si están documentando problemas

## Preguntas Frecuentes

### ¿Los datos (taxi.db) se suben a GitHub?
**No**. El `.gitignore` excluye archivos `.db`, `.csv`, `.parquet` para evitar subir datos grandes. Los estudiantes descargan los datos ejecutando `datos/descargar_datos.py`.

### ¿Las dependencias de Python se suben?
**No**. La carpeta `.venv` está en `.gitignore`. Solo se sube `requirements.txt`. Los estudiantes crean su propio entorno virtual e instalan con `pip install -r requirements.txt`.

### ¿Puedo agregar más ejercicios después?
**Sí**. Solo crea nuevos archivos `.py` en la carpeta `ejercicios/`, haz commit, push, y notifica a los estudiantes para que actualicen.

### ¿Cómo manejo ejercicios opcionales?
Crea una carpeta `ejercicios_opcionales/` y actualiza el README.md con la lista de opcionales.

## Recursos de Apoyo

- [Markdown Guide](https://www.markdownguide.org/) - Para editar archivos .md
- [GitHub Docs](https://docs.github.com/es) - Documentación oficial
- [Git Book Español](https://git-scm.com/book/es/v2) - Libro completo de Git

## Próximos Pasos

- [ ] Crear repositorio en GitHub
- [ ] Marcar como Template (si aplica)
- [ ] Compartir link con estudiantes
- [ ] Crear hoja de seguimiento con links de repos de estudiantes
- [ ] Programar revisiones semanales de progreso

---

**¡Listo!** Tu repositorio template está configurado y listo para usar.

Si tienes preguntas, consulta la [documentación de GitHub](https://docs.github.com) o abre un issue en GitHub Community.
