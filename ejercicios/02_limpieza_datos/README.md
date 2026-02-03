"""
═══════════════════════════════════════════════════════════════════════════════
EJERCICIO 02: LIMPIEZA DE DATOS (QoG)
═══════════════════════════════════════════════════════════════════════════════

Autor: Juan Marcelo Gutierrez Miranda (@TodoEconometria)
"""

# 🧹 Ejercicio 02: Limpieza de Datos (Quality of Government)

En este ejercicio aprenderás a procesar un dataset real utilizando **Dask**. El objetivo es simular un entorno de Big Data donde los datos no caben en la memoria RAM, aunque usaremos un dataset mediano para facilitar el aprendizaje.

---

## 🎯 Objetivos de Aprendizaje

1. **Cargar datos** de forma perezosa (*lazy*) con Dask.
2. **Estandarizar nombres** de columnas.
3. **Manejar valores nulos** de forma profesional.
4. **Exportar** resultados a formato eficiente (**Parquet**).

---

## 📝 Instrucciones Paso a Paso

### 1. Preparación
Asegúrate de tener el dataset descargado. Si no lo has hecho:
```bash
python scripts/download_datasets.py --dataset qog
```
Esto descargará `qog_std_ts_jan24.csv` en `datos/qog/`.

### 2. Tu Misión
Debes completar el script `solucion.py` que hemos preparado para ti. El script tiene huecos marcados con `TODO` que debes rellenar.

**Requisitos Específicos:**

1. **Carga:** Lee el CSV usando `dask.dataframe`.
2. **Columnas:** Selecciona SOLO estas columnas y renómbralas:
   - `ccode` → `codigo_pais` (Indice numérico)
   - `cname` → `nombre_pais`
   - `year`  → `anio`
   - `vdem_polyarchy` → `indice_democracia`
   - `wdi_gdppc` → `pib_per_capita`
3. **Tipos:** Asegúrate que `anio` sea entero (`int`).
4. **Nulos:** El dataset usa valores raros para nulos? Investiga. Si no, asegúrate de eliminar filas donde `nombre_pais` esté vacío.
5. **Filtrado:** Quédate solo con datos desde el año **2000 en adelante**.
6. **Guardado:** Guarda el resultado como `datos/qog/processed/qog_limpio.parquet`.

---

## 📂 Formato de Entrega

1. Copia el archivo `esqueleto.py` a `solucion.py`.
2. Completa el código.
3. Sigue las instrucciones de entrega en `entregas/README.md`:
   - Crea tu carpeta: `entregas/02_limpieza_datos/TU_USUARIO/`
   - Sube ahí tu `solucion.py` y una captura de pantalla de la ejecución exitosa.

---

## 🆘 Ayuda

- **Documentación Dask:** [docs.dask.org](https://docs.dask.org/)
- **Cheat Sheet:** Recuerda que Dask es muy similar a Pandas, pero requiere `.compute()` para ver resultados.

---

¡Buena suerte! 🚀
