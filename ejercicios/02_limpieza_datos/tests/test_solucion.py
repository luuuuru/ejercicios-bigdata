import pytest
import shutil
from pathlib import Path
import dask.dataframe as dd

# Intentar importar la solución del alumno (debe llamarse solucion.py para que pase el test)
# Si están desarrollando, pueden renombrar esqueleto.py a solucion.py
try:
    sys.path.append(str(Path(__file__).parent.parent))
    from solucion import clean_qog_dataset
except ImportError:
    clean_qog_dataset = None

OUTPUT_FILE = Path(__file__).parent.parent.parent.parent / "datos/qog/processed/qog_limpio.parquet"

def test_archivo_existe():
    """Valida que el alumno generó el archivo Parquet"""
    if clean_qog_dataset:
        clean_qog_dataset() # Ejecutar código del alumno
    
    assert OUTPUT_FILE.exists(), "❌ El archivo Parquet no se generó."

def test_columnas_correctas():
    """Valida que las columnas se renombraron bien"""
    if not OUTPUT_FILE.exists():
        pytest.skip("No existe archivo de salida")
    
    df = dd.read_parquet(str(OUTPUT_FILE))
    cols = df.columns
    
    esperadas = ['codigo_pais', 'nombre_pais', 'anio', 'indice_democracia', 'pib_per_capita']
    for col in esperadas:
        assert col in cols, f"❌ Falta la columna: {col}"

def test_filtro_anio():
    """Valida que no haya años anteriores a 2000"""
    if not OUTPUT_FILE.exists():
        pytest.skip("No existe archivo de salida")
    
    df = dd.read_parquet(str(OUTPUT_FILE))
    min_year = df['anio'].min().compute()
    
    assert min_year >= 2000, f"❌ Se encontraron años menores a 2000 (Mínimo: {min_year})"
