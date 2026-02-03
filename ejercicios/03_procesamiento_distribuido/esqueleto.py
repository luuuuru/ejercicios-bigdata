"""
═══════════════════════════════════════════════════════════════════════════════
HEADER ACADÉMICO - EJERCICIOS BIG DATA CON PYTHON
═══════════════════════════════════════════════════════════════════════════════
Alumno: __________________________
Ejercicio: 03 - Procesamiento Distribuido con Dask
═══════════════════════════════════════════════════════════════════════════════
"""

import time
import os
import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client, LocalCluster

# TODO: Configura aquí la ruta a tu archivo Parquet limpio (del ejercicio 2)
PARQUET_FILE = "../../datos/qog/processed/qog_limpio.parquet"

def procesamiento_dask():
    print("="*80)
    print("EJERCICIO 3: Dask Cluster Local")
    print("="*80)

    # 1. SETUP CLUSTER (TODO)
    # Configura un LocalCluster con 2 workers
    print("🚀 Iniciando Cluster...")
    # cluster = LocalCluster(n_workers=..., threads_per_worker=...)
    # client = Client(cluster)
    # print(client) # Muestra el link al dashboard

    # 2. LECTURA (TODO)
    # Lee el archivo Parquet
    print(f"📖 Leyendo: {PARQUET_FILE}")
    # ddf = ...

    # 3. TRANSFORMACION (TODO)
    # Calcula el promedio de 'indice_democracia' por año
    print("🧠 Calculando agregaciones...")
    # resultado = ddf.groupby(...)...

    # 4. COMPUTE (TODO)
    # Ejecuta el cálculo y muestra el tiempo
    start = time.time()
    # final = resultado.compute()
    end = time.time()
    
    print(f"⏱️ Tiempo: {end-start:.2f}s")
    # print(final)

if __name__ == "__main__":
    if os.path.exists(PARQUET_FILE):
        procesamiento_dask()
    else:
        print(f"❌ No encuentro el archivo: {PARQUET_FILE}")
        print("   Completa primero el Ejercicio 02.")
