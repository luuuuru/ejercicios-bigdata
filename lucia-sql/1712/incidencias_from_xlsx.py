import sqlite3
import pandas as pd
import os

# ============================================
# CONFIGURACIÓN
# ============================================

EXCEL_FILE = 'Ejercicio-de-Excel-resuelto-nivel-medio.xlsx'
DB_NAME = 'incidencias_completo.db'

# ============================================
# DATOS DE REFERENCIA
# ============================================

TIPO_INCIDENCIA_DATA = [
    ('Alto', 5),
    ('Medio', 15),
    ('Bajo', 30)
]

DEPARTAMENTO_DATA = [
    ('Dept1', 'Corbatas'),
    ('Dept2', 'Pañuelos'),
    ('Dept3', 'Camisas'),
    ('Dept4', 'Chaquetas'),
    ('Dept5', 'Pantalones'),
    ('Dept6', 'Chalecos')
]

# Meses del año
MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
         'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


# ============================================
# CREAR BASE DE DATOS
# ============================================

def create_database_from_excel(excel_path, db_path):
    """
    Crea una base de datos SQLite completa con TODAS las tablas del Excel
    """
    print("=" * 70)
    print("🚀 CREANDO BASE DE DATOS COMPLETA DE INCIDENCIAS")
    print("=" * 70)

    # Eliminar BD anterior
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✅ Base de datos anterior eliminada")
        except PermissionError:
            print(f"❌ ERROR: Cierra DB Browser o cualquier programa que use '{db_path}'")
            return

    # Conectar
    conn = sqlite3.connect(db_path, timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    print("✅ Conexión establecida")

    # ============================================
    # LEER EXCEL COMPLETO
    # ============================================

    print("\n📊 Leyendo Excel completo (columnas A-AN)...")

    try:
        # Leer TODO el Excel (columnas A a AN = 0 a 39)
        df_completo = pd.read_excel(
            excel_path,
            sheet_name='Datos',
            header=None  # Sin header automático
        )

        print(f"✅ Excel leído: {df_completo.shape[0]} filas x {df_completo.shape[1]} columnas")

    except Exception as e:
        print(f"❌ Error al leer Excel: {e}")
        conn.close()
        return

    # ============================================
    # 1. CREAR TABLAS DE CATÁLOGO
    # ============================================

    print("\n📋 Creando tablas de catálogo...")

    cursor.execute('''
        CREATE TABLE tipo_incidencia (
            id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            max_tiempo_respuesta INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE departamento (
            id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT
        )
    ''')

    # Insertar datos de referencia
    for tipo, tiempo in TIPO_INCIDENCIA_DATA:
        cursor.execute('INSERT INTO tipo_incidencia (nombre, max_tiempo_respuesta) VALUES (?, ?)',
                       (tipo, tiempo))

    for codigo, nombre in DEPARTAMENTO_DATA:
        cursor.execute('INSERT INTO departamento (codigo, nombre) VALUES (?, ?)',
                       (codigo, nombre))

    print("✅ Tablas de catálogo creadas")

    # ============================================
    # 2. TABLA DE INCIDENCIAS (Columnas A-K, Filas 1-1001)
    # ============================================

    print("\n💾 Extrayendo tabla de INCIDENCIAS (A-K, filas 1-1001)...")

    cursor.execute('''
        CREATE TABLE incidencia (
            numero_incidencia TEXT PRIMARY KEY,
            tipo_incidencia TEXT,
            fecha_llegada DATE,
            fecha_respuesta DATE,
            departamento TEXT,
            target DATE,
            on_time TEXT,
            anio_llegada INTEGER,
            mes_llegada INTEGER,
            tiempo_respuesta INTEGER,
            desviacion INTEGER
        )
    ''')

    # Extraer datos (filas 1 a 1001, columnas 0 a 10)
    df_incidencias = df_completo.iloc[1:1001, 0:11].copy()
    df_incidencias.columns = [
        'numero_incidencia', 'tipo_incidencia', 'fecha_llegada', 'fecha_respuesta',
        'departamento', 'target', 'on_time', 'anio_llegada', 'mes_llegada',
        'tiempo_respuesta', 'desviacion'
    ]

    # Limpiar y insertar
    df_incidencias = df_incidencias.dropna(subset=['numero_incidencia'])

    for _, row in df_incidencias.iterrows():
        try:
            cursor.execute('''
                INSERT INTO incidencia VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row))
        except:
            pass

    print(f"✅ {len(df_incidencias)} incidencias insertadas")

    # ============================================
    # 3. TABLA GENERAL (Columnas N-AN, Filas 5-12)
    # ============================================

    print("\n📈 Extrayendo tabla GENERAL (filas 5-12)...")

    cursor.execute('''
        CREATE TABLE tabla_general (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metrica TEXT,
            ene_2012 REAL, feb_2012 REAL, mar_2012 REAL, abr_2012 REAL, 
            may_2012 REAL, jun_2012 REAL, jul_2012 REAL, ago_2012 REAL,
            sep_2012 REAL, oct_2012 REAL, nov_2012 REAL, dic_2012 REAL,
            ene_2013 REAL, feb_2013 REAL, mar_2013 REAL, abr_2013 REAL,
            may_2013 REAL, jun_2013 REAL, jul_2013 REAL, ago_2013 REAL,
            sep_2013 REAL, oct_2013 REAL, nov_2013 REAL, dic_2013 REAL,
            total REAL
        )
    ''')

    # Extraer datos (filas 5-12, columnas 13 en adelante = N en adelante)
    df_general = df_completo.iloc[4:12, 13:].copy()

    # La primera columna (columna 13=N) contiene la métrica
    metricas = ['Total', 'Tiempo de respuesta', '% ON TIME']

    for i, metrica in enumerate(metricas):
        if i < len(df_general):
            valores = df_general.iloc[i].values.tolist()
            cursor.execute(f'''
                INSERT INTO tabla_general (metrica, {', '.join([f'{mes}_{anio}' for anio in [2012, 2013] for mes in MESES])}, total)
                VALUES (?, {', '.join(['?'] * 25)})
            ''', [metrica] + valores[:25])

    print("✅ Tabla GENERAL insertada")

    # ============================================
    # 4. TABLA DEPARTAMENTO (Filas 14-20)
    # ============================================

    print("\n🏢 Extrayendo tabla DEPARTAMENTO (filas 14-20)...")

    cursor.execute('''
        CREATE TABLE respuestas_departamento (
            departamento TEXT PRIMARY KEY,
            ene_2012 INTEGER, feb_2012 INTEGER, mar_2012 INTEGER, abr_2012 INTEGER,
            may_2012 INTEGER, jun_2012 INTEGER, jul_2012 INTEGER, ago_2012 INTEGER,
            sep_2012 INTEGER, oct_2012 INTEGER, nov_2012 INTEGER, dic_2012 INTEGER,
            ene_2013 INTEGER, feb_2013 INTEGER, mar_2013 INTEGER, abr_2013 INTEGER,
            may_2013 INTEGER, jun_2013 INTEGER, jul_2013 INTEGER, ago_2013 INTEGER,
            sep_2013 INTEGER, oct_2013 INTEGER, nov_2013 INTEGER, dic_2013 INTEGER,
            total INTEGER
        )
    ''')

    df_dept = df_completo.iloc[13:20, 13:].copy()

    for i, dept in enumerate(['Dept1', 'Dept2', 'Dept3', 'Dept4', 'Dept5', 'Dept6']):
        if i < len(df_dept):
            valores = df_dept.iloc[i].values.tolist()
            cursor.execute(f'''
                INSERT INTO respuestas_departamento VALUES (?, {', '.join(['?'] * 25)})
            ''', [dept] + valores[:25])

    print("✅ Tabla DEPARTAMENTO insertada")

    # ============================================
    # 5. TABLA TIPO DE INCIDENCIA (Filas 22-25)
    # ============================================

    print("\n📝 Extrayendo tabla TIPO DE INCIDENCIA (filas 22-25)...")

    cursor.execute('''
        CREATE TABLE respuestas_tipo_incidencia (
            tipo TEXT PRIMARY KEY,
            ene_2012 INTEGER, feb_2012 INTEGER, mar_2012 INTEGER, abr_2012 INTEGER,
            may_2012 INTEGER, jun_2012 INTEGER, jul_2012 INTEGER, ago_2012 INTEGER,
            sep_2012 INTEGER, oct_2012 INTEGER, nov_2012 INTEGER, dic_2012 INTEGER,
            ene_2013 INTEGER, feb_2013 INTEGER, mar_2013 INTEGER, abr_2013 INTEGER,
            may_2013 INTEGER, jun_2013 INTEGER, jul_2013 INTEGER, ago_2013 INTEGER,
            sep_2013 INTEGER, oct_2013 INTEGER, nov_2013 INTEGER, dic_2013 INTEGER,
            total INTEGER
        )
    ''')

    df_tipo = df_completo.iloc[21:25, 13:].copy()

    for i, tipo in enumerate(['Alto', 'Medio', 'Bajo']):
        if i < len(df_tipo):
            valores = df_tipo.iloc[i].values.tolist()
            cursor.execute(f'''
                INSERT INTO respuestas_tipo_incidencia VALUES (?, {', '.join(['?'] * 25)})
            ''', [tipo] + valores[:25])

    print("✅ Tabla TIPO DE INCIDENCIA insertada")

    # ============================================
    # 6. TABLA RESPUESTA ON TIME (Filas 27-43)
    # ============================================

    print("\n✅ Extrayendo tabla RESPUESTA ON TIME (filas 27-43)...")

    cursor.execute('''
        CREATE TABLE analisis_on_time (
            categoria TEXT PRIMARY KEY,
            ene_2012 TEXT, feb_2012 TEXT, mar_2012 TEXT, abr_2012 TEXT,
            may_2012 TEXT, jun_2012 TEXT, jul_2012 TEXT, ago_2012 TEXT,
            sep_2012 TEXT, oct_2012 TEXT, nov_2012 TEXT, dic_2012 TEXT,
            ene_2013 TEXT, feb_2013 TEXT, mar_2013 TEXT, abr_2013 TEXT,
            may_2013 TEXT, jun_2013 TEXT, jul_2013 TEXT, ago_2013 TEXT,
            sep_2013 TEXT, oct_2013 TEXT, nov_2013 TEXT, dic_2013 TEXT
        )
    ''')

    df_ontime = df_completo.iloc[26:43, 13:].copy()

    categorias = [
        'ON TIME', 'OUT OF TIME',
        'OT-Dept1', 'OT-Dept2', 'OT-Dept3', 'OT-Dept4', 'OT-Dept5', 'OT-Dept6',
        '% OT-Dept1', '% OT-Dept2', '% OT-Dept3', '% OT-Dept4', '% OT-Dept5', '% OT-Dept6'
    ]

    for i, cat in enumerate(categorias):
        if i < len(df_ontime):
            valores = df_ontime.iloc[i].values.tolist()
            cursor.execute(f'''
                INSERT INTO analisis_on_time VALUES (?, {', '.join(['?'] * 24)})
            ''', [cat] + [str(v) for v in valores[:24]])

    print("✅ Tabla RESPUESTA ON TIME insertada")

    # ============================================
    # 7. TABLA ANÁLISIS GLOBAL DESVIACIONES (Filas 46-54)
    # ============================================

    print("\n📊 Extrayendo tabla ANÁLISIS GLOBAL DESVIACIONES (filas 46-54)...")

    cursor.execute('''
        CREATE TABLE analisis_desviaciones (
            entidad TEXT PRIMARY KEY,
            target REAL,
            ene_2012 REAL, feb_2012 REAL, mar_2012 REAL, abr_2012 REAL,
            may_2012 REAL, jun_2012 REAL, jul_2012 REAL, ago_2012 REAL,
            sep_2012 REAL, oct_2012 REAL, nov_2012 REAL, dic_2012 REAL,
            ene_2013 REAL, feb_2013 REAL, mar_2013 REAL, abr_2013 REAL,
            may_2013 REAL, jun_2013 REAL, jul_2013 REAL, ago_2013 REAL,
            sep_2013 REAL, oct_2013 REAL, nov_2013 REAL, dic_2013 REAL,
            total REAL
        )
    ''')

    df_desv = df_completo.iloc[45:54, 13:].copy()

    entidades = ['Alto', 'Medio', 'Bajo', 'Dept1', 'Dept2', 'Dept3', 'Dept4', 'Dept5', 'Dept6']

    for i, entidad in enumerate(entidades):
        if i < len(df_desv):
            valores = df_desv.iloc[i].values.tolist()
            # La primera columna es target, luego 24 meses, luego total
            cursor.execute(f'''
                INSERT INTO analisis_desviaciones VALUES (?, ?, {', '.join(['?'] * 25)})
            ''', [entidad] + valores[:26])

    print("✅ Tabla ANÁLISIS DESVIACIONES insertada")

    conn.commit()

    # ============================================
    # RESUMEN
    # ============================================

    print("\n" + "=" * 70)
    print("📊 RESUMEN DE LA BASE DE DATOS")
    print("=" * 70)

    tablas = [
        'tipo_incidencia', 'departamento', 'incidencia', 'tabla_general',
        'respuestas_departamento', 'respuestas_tipo_incidencia',
        'analisis_on_time', 'analisis_desviaciones'
    ]

    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        print(f"✅ {tabla}: {count} registros")

    conn.close()

    print(f"\n✅ Base de datos creada: {db_path}")
    print("=" * 70)


# ============================================
# CONSULTAS DE EJEMPLO
# ============================================

def mostrar_consultas_ejemplo(db_path):
    """
    Muestra ejemplos de cada tabla
    """
    conn = sqlite3.connect(db_path)

    print("\n" + "=" * 70)
    print("🔍 EJEMPLOS DE CADA TABLA")
    print("=" * 70)

    # Incidencias
    print("\n1️⃣ INCIDENCIAS (primeras 5):")
    df = pd.read_sql_query("SELECT * FROM incidencia LIMIT 5", conn)
    print(df.to_string(index=False))

    # Tabla General
    print("\n2️⃣ TABLA GENERAL:")
    df = pd.read_sql_query("SELECT metrica, ene_2012, feb_2012, mar_2012, total FROM tabla_general", conn)
    print(df.to_string(index=False))

    # Respuestas por Departamento
    print("\n3️⃣ RESPUESTAS POR DEPARTAMENTO:")
    df = pd.read_sql_query("SELECT departamento, ene_2012, feb_2012, mar_2012, total FROM respuestas_departamento",
                           conn)
    print(df.to_string(index=False))

    # Análisis Desviaciones
    print("\n4️⃣ ANÁLISIS DE DESVIACIONES:")
    df = pd.read_sql_query("SELECT entidad, target, total FROM analisis_desviaciones", conn)
    print(df.to_string(index=False))

    conn.close()


# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    create_database_from_excel(EXCEL_FILE, DB_NAME)
    mostrar_consultas_ejemplo(DB_NAME)

    print("\n✅ ¡Proceso completado!")
    print(f"💡 Abre '{DB_NAME}' con DB Browser for SQLite para explorar")