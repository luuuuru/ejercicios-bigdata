"""
═══════════════════════════════════════════════════════════════════════════════
HEADER ACADÉMICO - EJERCICIOS BIG DATA CON PYTHON
═══════════════════════════════════════════════════════════════════════════════
Alumno: __________________________ (Escribe tu nombre aquí)
Fecha:  __________________________
Ejercicio: 02 - Limpieza de Datos QoG
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import dask.dataframe as dd
import pandas as pd
from pathlib import Path

# Agregar directorio raíz al path para importar utils si fuera necesario
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# Configuración de Rutas
INPUT_FILE = BASE_DIR / "datos" / "qog" / "qog_std_ts_jan24.csv"
OUTPUT_DIR = BASE_DIR / "datos" / "qog" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "qog_limpio.parquet"

def clean_qog_dataset():
    """
    Función principal para limpiar el dataset Quality of Government.
    """
    
    # 1. VERIFICACIÓN
    if not INPUT_FILE.exists():
        print(f"❌ Error: No se encuentra el archivo {INPUT_FILE}")
        print("   Ejecuta: python scripts/download_datasets.py --dataset qog")
        return

    print(f"📖 Cargando dataset: {INPUT_FILE}")
    
    # 2. CARGA (TODO: Completa la carga con Dask)
    # Pista: dd.read_csv(str(INPUT_FILE))
    # df = ... 
    df = dd.read_csv(str(INPUT_FILE)) # <--- Descomenta y ajusta si es necesario

    # 3. SELECCIÓN Y RENOMBRADO (TODO)
    # Selecciona solo estas columnas: ccode, cname, year, vdem_polyarchy, wdi_gdppc
    # Renóbralas a: codigo_pais, nombre_pais, anio, indice_democracia, pib_per_capita
    
    selected_columns = {
        'ccode': 'codigo_pais',
        # ... TODO: Completa el diccionario ...
    }
    
    # df = df[list(selected_columns.keys())]
    # df = df.rename(columns=selected_columns)

    # 4. FILTRADO (TODO)
    # Quédate solo con años >= 2000
    # df = df[ ... ]

    # 5. LIMPIEZA DE NULOS (TODO)
    # Elimina filas donde 'nombre_pais' sea nulo (NaN)
    # df = df.dropna(subset=['nombre_pais'])

    # 6. CONVERSIÓN DE TIPOS (Opción Avanzada)
    # Asegura que 'anio' sea entero
    # df['anio'] = df['anio'].astype(int)

    # 7. GUARDADO
    print(f"💾 Guardando resultado en: {OUTPUT_FILE}")
    
    # Crear carpeta destino si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Guardar en Parquet (Usamos PyArrow)
    try:
        # TODO: Descomenta la línea siguiente para guardar
        # df.to_parquet(str(OUTPUT_FILE), engine='pyarrow', write_index=False, compression='snappy')
        print("✅ Proceso finalizado con éxito.")
        
        # Validación rápida (Esto se ejecutará realmente aquí al llamar a compute/head)
        print("\n📊 Vista previa de los datos procesados:")
        print(df.head())
        
    except Exception as e:
        print(f"❌ Error al guardar/procesar: {e}")

if __name__ == "__main__":
    clean_qog_dataset()
