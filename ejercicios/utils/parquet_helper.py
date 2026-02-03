"""
═══════════════════════════════════════════════════════════════════════════════
HEADER ACADÉMICO - EJERCICIOS BIG DATA CON PYTHON
═══════════════════════════════════════════════════════════════════════════════

Autor/Instructor: Juan Marcelo Gutierrez Miranda
Afiliación: @TodoEconometria
Repositorio: https://github.com/TodoEconometria/ejercicios-bigdata
Hash ID Certificación: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c

METODOLOGÍA:
    Cursos Avanzados de Big Data, Ciencia de Datos,
    Desarrollo de Aplicaciones con IA & Econometría Aplicada

═══════════════════════════════════════════════════════════════════════════════
REFERENCIAS ACADÉMICAS PRINCIPALES (Formato APA 7ª Ed.)
═══════════════════════════════════════════════════════════════════════════════

Big Data & Distributed Computing:
    - Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified data processing 
      on large clusters. Communications of the ACM, 51(1), 107-113.
      https://doi.org/10.1145/1327452.1327492
    
    - Rocklin, M. (2015). Dask: Parallel computation with blocked algorithms 
      and task scheduling. In Proceedings of the 14th Python in Science 
      Conference (pp. 126-132). https://doi.org/10.25080/Majora-7b98e3ed-013

═══════════════════════════════════════════════════════════════════════════════
LICENCIA: MIT License - Material Educativo Abierto
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import dask.dataframe as dd
import pandas as pd
from pathlib import Path

def csv_a_parquet(input_path: str, output_path: str, compression: str = 'snappy'):
    """
    Convierte CSV a Parquet de manera eficiente usando Dask.
    
    Argumentos:
        input_path (str): Ruta al archivo CSV origen.
        output_path (str): Ruta al archivo Parquet destino (o directorio).
        compression (str): Algoritmo de compresión ('snappy', 'gzip', etc).
    
    Por qué usar Parquet:
    - Binario y Columnar: Lecturas selectivas mucho más rápidas.
    - Compresión: Reduce espacio en disco significativamente.
    - Tipos de datos: Mantiene el esquema (int, float, string) mejor que CSV.
    """
    
    source = Path(input_path)
    target = Path(output_path)
    
    if not source.exists():
        print(f"❌ Error: No encuentro el archivo origen: {source}")
        return False

    print(f"📖 Leyendo CSV limpio con Dask: {source}")
    # Dask funciona de manera 'lazy'. No lee todo el archivo a RAM.
    try:
        ddf = dd.read_csv(str(source))
        
        # Crear directorio padre si no existe
        target.parent.mkdir(parents=True, exist_ok=True)

        print(f"💾 Convirtiendo a formato Parquet: {target} ...")
        # Aquí es donde Dask realmente trabaja y paraleliza la escritura
        ddf.to_parquet(
            str(target), 
            engine='pyarrow', 
            write_index=False,
            compression=compression
        )
        print("✅ Conversión completada.")
        return True
        
    except Exception as e:
        print(f"❌ Error en la conversión: {e}")
        return False

def demo_analisis_dask(parquet_path: str):
    """
    Demostración de análisis distribuido con Dask sobre Parquet.
    """
    print("\n--- Análisis Distribuido con Dask ---")
    
    if not os.path.exists(parquet_path):
        print(f"❌ Archivo no encontrado: {parquet_path}")
        return

    print(f"📖 Leyendo Parquet desde: {parquet_path}")
    # Leer Parquet es instantáneo (solo lee metadatos)
    ddf = dd.read_parquet(parquet_path, engine='pyarrow')

    # Ejemplo 1: Conteo de registros (Count)
    # Ejemplo 2: Promedio por grupo (GroupBy + Mean)
    
    # Supongamos que tenemos columnas 'payment_type' y 'fare_amount' (Dataset Taxi)
    # Si no existen, mostramos las columnas disponibles
    
    cols = ddf.columns
    print(f"ℹ️ Columnas detectadas: {list(cols)}")
    
    if 'payment_type' in cols and 'fare_amount' in cols:
        print("🧠 Planificando cálculo: Promedio de 'fare_amount' por 'payment_type'...")
        calculo_perezoso = ddf.groupby('payment_type')['fare_amount'].mean()
        
        print("🚀 Ejecutando cálculo distribuido (compute)...")
        resultado = calculo_perezoso.compute()
        
        print("\n📊 Resultado:")
        print(resultado)
    else:
        print("⚠️ Las columnas de ejemplo no coinciden con este dataset.")
        print("   Mostrando primeras 5 filas:")
        print(ddf.head())

if __name__ == "__main__":
    # Bloque de prueba
    BASE_DIR = Path(__file__).parent.parent.parent
    INPUT_TEST = BASE_DIR / "datos" / "taxi_limpio.csv"
    OUTPUT_TEST = BASE_DIR / "datos" / "taxi.parquet"
    
    if INPUT_TEST.exists():
        csv_a_parquet(str(INPUT_TEST), str(OUTPUT_TEST))
        demo_analisis_dask(str(OUTPUT_TEST))
    else:
        print("⚠️ Ejecuta este script importándolo como módulo en tus ejercicios.")
