import pandas as pd
import sqlite3

# Conectar a una base temporal
conn = sqlite3.connect(':memory:')

# Leer el archivo SQL y extraer solo los INSERT
with open("C:/Users/lucia/Downloads/Modelo_HR.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Filtrar solo los CREATE TABLE e INSERT
import re
creates = re.findall(r'CREATE TABLE.*?;', sql_script, re.DOTALL | re.IGNORECASE)
inserts = re.findall(r'INSERT INTO.*?;', sql_script, re.DOTALL | re.IGNORECASE)

# Ejecutar solo CREATE e INSERT
for create in creates:
    try:
        conn.execute(create)
    except:
        pass

for insert in inserts:
    try:
        conn.execute(insert)
    except:
        pass

# Listar tablas
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("📋 Tablas encontradas:")
for tabla in tablas:
    print(f"  - {tabla[0]}")
    df = pd.read_sql_query(f"SELECT * FROM {tabla[0]} LIMIT 5", conn)
    print(df)
    print()

###

for tabla in tablas:
    print(f"\n📋 Tabla: {tabla[0]}")
    df = pd.read_sql_query(f"SELECT * FROM {tabla[0]} LIMIT 5", conn)

    # Mostrar información detallada
    print(df.info())  # ← Tipos de datos, valores nulos
    print(df)

conn.close()
