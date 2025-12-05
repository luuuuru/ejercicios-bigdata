# Ejercicios de Big Data para Certificación MCO

Bienvenido a esta serie de ejercicios prácticos diseñados para aprender los fundamentos de Big Data utilizando Python. Este material está pensado para alumnos que se están iniciando en la programación y el análisis de datos.

## Índice de Documentación

### Para Alumnos
- **[INSTRUCCIONES_ALUMNOS.md](INSTRUCCIONES_ALUMNOS.md)** - Guía de Git y PyCharm
- **[GUIA_ENTREGA_DASHBOARDS.md](GUIA_ENTREGA_DASHBOARDS.md)** - Cómo crear y entregar dashboards
- **[ENTENDIENDO_GIT_Y_RAMAS.md](ENTENDIENDO_GIT_Y_RAMAS.md)** - Explicación visual de Git y ramas

### Para Referencia
- **[ARQUITECTURA_Y_STACK.md](ARQUITECTURA_Y_STACK.md)** - Explicación del stack tecnológico
- **[ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)** - Buenas prácticas y organización

### Para Profesor (Solo Instructor)
- **[GUIA_PROFESOR.md](GUIA_PROFESOR.md)** - Gestión del proyecto colaborativo
- **[EJEMPLO_PRIMERA_TAREA.md](EJEMPLO_PRIMERA_TAREA.md)** - Ejemplo completo de asignación de tarea
- **[PROXIMOS_PASOS.md](PROXIMOS_PASOS.md)** - Setup inicial del repositorio

## ¿Qué vamos a aprender?
En estos ejercicios no solo ejecutaremos código, sino que entenderemos **qué** estamos haciendo y **por qué**. Cubriremos:

1.  **Obtención de datos**: Cómo descargar información real de internet usando código.
2.  **Almacenamiento**: Por qué guardamos los datos en bases de datos (SQLite) y formatos modernos (Parquet).
3.  **Limpieza**: Cómo preparar los datos "sucios" del mundo real para que sean útiles.
4.  **Procesamiento**: Cómo usar herramientas profesionales (Dask, PySpark) para manejar grandes volúmenes de información.

## Estructura del Proyecto
El proyecto está organizado en carpetas para mantener el orden, algo vital en proyectos profesionales:

```
ejercicios_bigdata/
├── __init__.py           # Archivo que indica a Python que esta carpeta es un "paquete"
├── requirements.txt      # Lista de "ingredientes" (librerías) que necesita nuestro proyecto
├── LEEME.md              # Este archivo de instrucciones
│
├── datos/                # Carpeta donde guardaremos los datos descargados
│   └── descargar_datos.py # Script (programa) para bajar los datos de internet
│
├── ejercicios/           # Carpeta con los ejercicios paso a paso
│   ├── 01_cargar_sqlite.py   # Ejercicio 1: Bases de datos SQL
│   ├── 02_limpieza_datos.py  # Ejercicio 2: Limpieza con Pandas
│   ├── 03_parquet_dask.py    # Ejercicio 3: Formatos Big Data y Dask
│   └── 04_pyspark_query.py   # Ejercicio 4: Introducción a Apache Spark
│
└── dashboards/           # Dashboards de visualización (Flask)
    └── nyc_taxi_eda/     # Ejemplo de dashboard con EDA
        ├── app.py
        ├── templates/
        └── README.md
```

## Conceptos Clave para Principiantes

### ¿Qué es una "Librería"?
Imagina que quieres construir una casa. Podrías fabricar tus propios ladrillos, cemento y herramientas, pero tardarías años. En programación, una **librería** es como ir a una ferretería y comprar herramientas ya hechas por expertos.
- **pandas**: Es como una hoja de cálculo de Excel superpotente pero sin interfaz gráfica.
- **requests**: Nos permite "navegar" por internet y descargar archivos usando código.
- **sqlalchemy**: Nos ayuda a hablar con bases de datos SQL.

### ¿Qué es un "Entorno Virtual"?
Es como tener una caja de herramientas separada para cada proyecto. Si en un proyecto necesitas un martillo grande y en otro uno pequeño, no quieres mezclarlos. El entorno virtual asegura que las versiones de las librerías de este proyecto no interfieran con otros.

## Configuración del Entorno (Paso a Paso)

1.  **Crear el entorno virtual**:
    Abre tu terminal en PyCharm y escribe:
    ```bash
    python -m venv venv
    ```
    Esto crea una carpeta `venv` con una copia aislada de Python.

2.  **Activar el entorno**:
    - En Windows: `venv\Scripts\activate`
    - Verás que aparece `(venv)` al principio de la línea de comandos.

3.  **Instalar las librerías**:
    Le decimos a Python que instale lo que hay en `requirements.txt`:
    ```bash
    pip install -r ejercicios_bigdata/requirements.txt
    ```

## Cómo realizar los ejercicios

Ejecuta los scripts en orden. Lee los comentarios dentro de cada archivo, ¡ahí está la explicación detallada de cada línea!

1.  **Descargar los datos**:
    ```bash
    python ejercicios_bigdata/datos/descargar_datos.py
    ```
2.  **Ejercicio 1 (Base de Datos)**:
    ```bash
    python ejercicios_bigdata/ejercicios/01_cargar_sqlite.py
    ```
3.  **Ejercicio 2 (Limpieza)**:
    ```bash
    python ejercicios_bigdata/ejercicios/02_limpieza_datos.py
    ```
4.  **Ejercicio 3 (Big Data con Dask)**:
    ```bash
    python ejercicios_bigdata/ejercicios/03_parquet_dask.py
    ```
5.  **Ejercicio 4 (Apache Spark)**:
    ```bash
    python ejercicios_bigdata/ejercicios/04_pyspark_query.py
    ```

¡Mucho éxito en tu aprendizaje!
