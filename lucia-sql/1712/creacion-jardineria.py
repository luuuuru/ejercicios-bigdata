import sqlite3

# Nombre del archivo de la base de datos (se creará si no existe)
DB_NAME = 'jardineria.db'

# Lee el script SQL desde el archivo
try:
    with open('creacion-jardineria.sql', 'r') as f:
        sql_script = f.read()
except FileNotFoundError:
    print("Error: El archivo 'creacion_jardineria.sql' no se encontró.")
    exit()

try:
    # Conectarse a la base de datos. Se crea si no existe.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ejecutar el script SQL completo
    # Nota: Para SQLite, es posible que debas asegurarte de que la sintaxis
    # 'NUMERIC(p,s)' y 'DATE' se ajusten a su tipo de afinidad.
    cursor.executescript(sql_script)

    # Confirmar los cambios
    conn.commit()
    print(f"Base de datos '{DB_NAME}' creada exitosamente con todas las tablas.")

except sqlite3.Error as e:
    print(f"Ocurrió un error al crear la base de datos: {e}")
    # En caso de error, puedes hacer un rollback
    if conn:
        conn.rollback()

finally:
    # Cerrar la conexión
    if conn:
        conn.close()