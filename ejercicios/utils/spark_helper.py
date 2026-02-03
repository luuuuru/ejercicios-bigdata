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
    - Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., 
      ... & Stoica, I. (2016). Apache Spark: A unified engine for big data 
      processing. Communications of the ACM, 59(11), 56-65.
      https://doi.org/10.1145/2934664

Database Systems:
    - Kleppmann, M. (2017). Designing Data-Intensive Applications: The Big 
      Ideas Behind Reliable, Scalable, and Maintainable Systems. O'Reilly Media.

═══════════════════════════════════════════════════════════════════════════════
LICENCIA: MIT License - Material Educativo Abierto
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession

def get_spark_session(app_name="CursoBigData"):
    """
    Inicializa una SparkSession configurada para entorno Windows local.
    Maneja automáticamente las variables de entorno para Python.
    """
    
    # --- CORRECCIÓN PARA WINDOWS ---
    # Aseguramos que PySpark use el mismo Python que está ejecutando este script.
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    print(f"⚡ Iniciando SparkSession: {app_name}...")
    print("   (Si estás en Windows y ves advertencias sobre 'winutils', es normal en local)")

    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .config("spark.ui.showConsoleProgress", "false") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        # Reducir verbosidad de logs (ERROR instead of INFO/WARN)
        spark.sparkContext.setLogLevel("ERROR")
        
        return spark
        
    except Exception as e:
        print("\n❌ Error crítico al iniciar Spark.")
        print("Posible causa: Problema con Java o variables de entorno.")
        print(f"Detalle: {e}")
        return None

def ejecutar_consulta_sql(spark, parquet_path, query, view_name="tabla_datos"):
    """
    Ejecuta una consulta SQL sobre un archivo Parquet.
    """
    if not os.path.exists(parquet_path):
        print(f"❌ Error: Archivo no encontrado: {parquet_path}")
        return None

    try:
        print(f"📖 Leyendo Parquet: {parquet_path}")
        df = spark.read.parquet(parquet_path)
        
        # Crear vista temporal para SQL
        df.createOrReplaceTempView(view_name)
        
        print(f"🧠 Ejecutando SQL...")
        print(f"   Query: {query.strip().splitlines()[0]}...") # Mostrar primera línea
        
        resultado = spark.sql(query)
        return resultado
        
    except Exception as e:
        print(f"❌ Error durante la consulta: {e}")
        return None

if __name__ == "__main__":
    # Test rápido
    spark = get_spark_session("TestUtils")
    if spark:
        print("✅ Spark iniciado correctamente.")
        spark.stop()
