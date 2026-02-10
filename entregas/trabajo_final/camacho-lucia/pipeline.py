import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, isnan
from pyspark.sql.types import FloatType, DoubleType

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def aplicar_transformaciones_neuro_adni(pdf):
    """
    Aplica transformaciones estándar según la literatura:
    - TA (Thickness): Z-Score.
    - SA (Area): Ratio / ICV (Intracranial Volume).
    """
    df_t = pdf.copy()

    # Buscamos la columna de ICV
    icv_col = 'Intracranial_Vol'
    
    # Identificar columnas
    cols_ta = [c for c in df_t.columns if c.endswith('TA')]
    cols_sa = [c for c in df_t.columns if c.endswith('SA')]

    print(f"🧠 Aplicando transformaciones científicas:")

    # 1. Transformación para AREA (SA) -> Ratio / ICV
    if cols_sa and icv_col in df_t.columns:
        print(f"   -> Normalizando {len(cols_sa)} variables de Área (SA) por {icv_col}")
        for col_name in cols_sa:
            # Evitamos división por cero o nulos en ICV
            df_t[col_name] = df_t[col_name] / df_t[icv_col]

    # 2. Transformación para THICKNESS (TA) -> Z-Score
    if cols_ta:
        print(f"   -> Escalando {len(cols_ta)} variables de Grosor (TA) mediante Z-Score")
        scaler = StandardScaler()
        # Solo escalamos si hay datos
        df_t[cols_ta] = scaler.fit_transform(df_t[cols_ta])

    return df_t

def descubrir_features_mas_importantes(pdf, n_top=10):
    """
    Random Forest para selección de variables.
    """
    print("\n" + "🔥" * 20)
    print(" SELECCIÓN DE VARIABLES (RANDOM FOREST) ")
    print("🔥" * 20)

    # 1. Copia de trabajo
    data = pdf.copy()

    # 2. Filtros de seguridad
    cols_a_borrar = [
        'PTID', 'RID', 'SITEID', 'VISCODE', 'EXAMDATE', 'DX_bl',
        'EXAMDATE_bl', 'PTGENDER', 'PTEDUCAT', 'PTETHCAT', 'PTRACCAT',
        'PTMARRY', 'update_stamp', 'PHASE', 'VISCODE2', 'IMAGEUID', # ID interno de la imagen (no biológico)
    'FIELD_STRENGTH', # Potencia del escáner (metadato técnico)
    'EXAMDATE',       # Fecha (el modelo no procesa fechas crudas bien)
    'RUNDATE',        # Fecha de ejecución del software
    'STATUS',         # Estado del procesamiento
    'FSVER'           # Versión de FreeSurfer (metadato técnico)
    ]
    cols_a_borrar = [c for c in cols_a_borrar if c in data.columns]
    data.drop(columns=cols_a_borrar, inplace=True)

    # 3. Preparar Objetivo (Y) y Variables (X)
    if 'DIAGNOSIS' not in data.columns:
        print("❌ Error: No se encuentra la columna DIAGNOSIS")
        return []
    # Limpiar filas sin diagnóstico
    data = data.dropna(subset=['DIAGNOSIS'])
    # Variable dependiente del analisis (target)
    y_full = data['DIAGNOSIS'] # Lo llamamos full porque tiene todos los datos

    # 4. Seleccionar solo columnas numéricas (Biomarcadores, Volúmenes, Scores)
    X = data.drop(columns=['DIAGNOSIS']).select_dtypes(include=[np.number])

    # 5. Limpieza agresiva para RF
    # Borramos columnas que tengan más del 40% de nulos (thresh = 60% de datos reales)
    umbral = int(0.6 * len(X))
    X = X.dropna(axis=1, thresh=umbral)

    # Borramos cualquier paciente que tenga un hueco en las variables que quedan
    n_antes = len(X)

    X = X.dropna(axis=0, how='any')
    # Recortamos la 'y' para que tenga EXACTAMENTE las mismas filas que sobrevivieron en 'X'
    y = y_full.loc[X.index]
    n_despues = len(X)
    print(f"📉 Limpieza de Nulos: {n_antes} -> {n_despues} filas válidas para entrenamiento.")

    print("⚖️ Escalando variables (StandardScaler)...")
    scaler = StandardScaler()
    # Es vital volver a crear el DataFrame para conservar X.columns y X.index
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    print(f"-> Analizando {X.shape[1]} variables candidatas...")

    # 5. Entrenar Random Forest "Detector"
    rf = RandomForestClassifier(n_estimators=100,
                                max_features='sqrt',  # ← CRÍTICO: √350 ≈ 19 variables por árbol
                                max_depth=20,  # ← Evitar overfitting con muchas variables
                                min_samples_split=10,  # ← Mínimo 10 muestras para dividir
                                min_samples_leaf=5,  # ← Mínimo 5 muestras por hoja
                                n_jobs=-1,  # ← Usar todos los procesadores
                                random_state=42,
                                oob_score=True,  # ← Para validación automática
                                verbose=1  # ← Ver progreso
                                )
    rf.fit(X, y)

    # 6. Extraer importancias
    importancias = pd.Series(rf.feature_importances_, index=X.columns)
    top_features = importancias.sort_values(ascending=False).head(n_top)

    print(f"\n✅ LAS {n_top} VARIABLES MÁS IMPORTANTES DETECTADAS SON:")
    print(top_features)

    # 5. Guardar Gráfico (En Docker no podemos usar .show())
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_features.values, y=top_features.index, palette='magma')
    plt.title(f'Top {n_top} Variables (Gini)')
    plt.tight_layout()
    # Guardamos la imagen en la carpeta compartida
    plt.savefig("/opt/spark-data/importancia_variables.png", bbox_inches='tight')
    print(f"📊 Gráfico de importancia guardado en: /opt/spark-data/importancia_variables.png")
    plt.close()

    return top_features.index.tolist()


def ejecutar_eda_completo(df, cols_num, cols_cat):
    # Barras categoricas
    print("   -> Generando gráficos categóricos...")
    # Filtramos solo las categorías que nos interesan para graficar
    cats_plot = [c for c in cols_cat if c in ['DIAGNOSIS', 'PTGENDER', 'APOE4', 'VISCODE']]

    if cats_plot:
        fig, axes = plt.subplots(1, len(cats_plot), figsize=(18, 5))
        # Si solo hay 1 variable, convertimos axes en lista para que el índice [i] funcione
        if len(cats_plot) == 1:
            axes = [axes]
        elif isinstance(axes, np.ndarray) == False:
            axes = [axes]  # Seguridad extra

        for i, col in enumerate(cats_plot):
            if col in df.columns:
                sns.countplot(x=col, data=df, ax=axes.flatten()[i], hue=col, legend=False, palette='viridis',
                              order=df[col].value_counts().index)
                axes.flatten()[i].set_title(f'Frecuencia: {col}')
                axes.flatten()[i].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig("/opt/spark-data/eda_categorias.png")
        plt.close()

    # Histogramas
    plt.rcParams.update({'font.size': 14})
    fig, axes = plt.subplots(max(1, len(cols_num) // 3 + 1), 3, figsize=(18, 12))
    for i, col in enumerate(cols_num):
        sns.histplot(df[col], kde=True, ax=axes.flatten()[i], color='skyblue')
        # Eliminar subplots vacíos si los hay
    for i in range(len(cols_num), len(axes.flatten())):
        fig.delaxes(axes.flatten()[i])

    plt.tight_layout()
    plt.savefig("/opt/spark-data/eda_histogramas.png")

    # Correlación
    plt.figure(figsize=(14, 12))
    ax = sns.heatmap(
        df[cols_num].corr(),
        annot=True,  # Mostrar números
        fmt=".2f",  # Solo 2 decimales
        cmap='coolwarm',  # Color: Rojo (alto) a Azul (bajo)
        linewidths=0.5,  # Líneas blancas separadoras
        square=True,  # Forzar que sean cuadrados perfectos
        cbar_kws={"shrink": 0.8},  # Barra de color un poco más pequeña
        annot_kws={"size": 10}  # Tamaño de la fuente de los números internos
    )
    # Etiquetas
    plt.xticks(rotation=45, ha='right', fontsize=12)  # Rotar eje X 45 grados
    plt.yticks(rotation=0, fontsize=12)  # Eje Y recto

    # Guardado (bbox_inches='tight' es clave para no cortar texto)
    plt.tight_layout()
    plt.savefig("/opt/spark-data/eda_correlacion.png", bbox_inches='tight', dpi=150)
    plt.close()

def ejecutar_metodo_codo(df, features_cols):
    """
    ### NUEVO ###
    Calcula la inercia para k=1 a k=10 y genera el gráfico del codo.
    """
    print("\n💪 Ejecutando Técnica del Codo...")

    # Preparar datos
    X = df[features_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []
    K_range = range(1, 11)  # Probamos de 1 a 10 clusters

    # Línea 218-220:
    for k in K_range:
        # n_init=10 para asegurar estabilidad
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, 'bo-', markersize=8, linewidth=2)
    plt.xlabel('Número de Clusters (k)')
    plt.ylabel('Inercia (WCSS)')
    plt.title('Técnica del Codo para determinar k óptimo')
    plt.grid(True)

    # Guardar
    ruta_img = "/opt/spark-data/metodo_codo.png"
    plt.savefig(ruta_img)
    plt.close()

    print(f"✅ Gráfico del codo guardado en: {ruta_img}")
    print(f"   Valores de inercia: {[round(x, 2) for x in inertias]}")


def ejecutar_clustering_grid(df, features_cols):
    """
    Grid Search para clustering: evalúa múltiples algoritmos y k.
    Calcula Silhouette Score y Davies-Bouldin Index para cada configuración.
    """
    from sklearn.metrics import silhouette_score, davies_bouldin_score
    from sklearn.mixture import GaussianMixture

    print("\n🔬 GRID SEARCH: Evaluando algoritmos de clustering...")

    # Preparar datos
    X = df[features_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    resultados = []

    # Configuraciones a probar
    configs = [
                  ('KMeans', k) for k in range(2, 6)
              ] + [
                  ('GMM', k) for k in range(2, 6)
              ]

    for algoritmo, k in configs:
        try:
            if algoritmo == 'KMeans':
                model = KMeans(n_clusters=k, random_state=42, n_init=10)
            else:  # GMM
                model = GaussianMixture(n_components=k, random_state=42, n_init=10)

            labels = model.fit_predict(X_scaled)

            # Métricas
            sil = silhouette_score(X_scaled, labels)
            dbi = davies_bouldin_score(X_scaled, labels)

            resultados.append({
                'Algoritmo': algoritmo,
                'k': k,
                'Silhouette': round(sil, 3),
                'Davies-Bouldin': round(dbi, 3)
            })

            print(f"   ✓ {algoritmo} k={k} | Silhouette={sil:.3f} | DBI={dbi:.3f}")

        except Exception as e:
            print(f"   ✗ {algoritmo} k={k} falló: {e}")

    # Mostrar mejores configuraciones
    df_res = pd.DataFrame(resultados)
    print("\n🏆 TOP 3 CONFIGURACIONES (por Silhouette):")
    print(df_res.nlargest(3, 'Silhouette'))

    # Guardar resultados
    ruta_grid = "/opt/spark-data/clustering_grid_results.csv"
    df_res.to_csv(ruta_grid, index=False)
    print(f"\n📊 Resultados completos guardados en: {ruta_grid}")
    # Crear matriz pivotada para heatmap
    pivot_sil = df_res.pivot(index='Algoritmo', columns='k', values='Silhouette')

    plt.figure(figsize=(10, 4))
    sns.heatmap(pivot_sil, annot=True, fmt='.3f', cmap='RdYlGn',
                cbar_kws={'label': 'Silhouette Score'},
                linewidths=1, linecolor='black')
    plt.title('Mapa de Calidad: Algoritmo vs Número de Clusters',
              fontsize=14, fontweight='bold')
    plt.xlabel('Número de Clusters (k)', fontsize=12)
    plt.ylabel('Algoritmo', fontsize=12)
    plt.tight_layout()
    plt.savefig("/opt/spark-data/clustering_heatmap.png", dpi=150)
    plt.close()

    print(f"🔥 Heatmap guardado en: /opt/spark-data/clustering_heatmap.png")

    return df_res

# ML (CLUSTERING)
def ejecutar_clustering_pipeline(df, features_X):
    print("\n🤖 INICIANDO CLUSTERING NO SUPERVISADO...")

    cols_meta = ['PTID', 'DIAGNOSIS']
    df_ml = df[features_X + cols_meta].dropna()

    X = df_ml[features_X]
    X_scaled = StandardScaler().fit_transform(X)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # KMeans
    # k=3 justificado clínicamente (CN, MCI, AD)
    print("⚠️ Usando k=3 fijo (conocimiento clínico previo)")
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = model.fit_predict(X_scaled)

    df_res = df_ml.copy()
    df_res['PC1'] = X_pca[:, 0]
    df_res['PC2'] = X_pca[:, 1]
    df_res['Cluster'] = clusters
    df_res['Cluster_KMeans'] = clusters

    # 1. Crear un diccionario para mapear los números a nombres reales
    # Basado en tu imagen visual:
    mapeo_auto = df_ml.groupby(clusters)['DIAGNOSIS'].mean().sort_values()
    cluster_map = {
        mapeo_auto.index[0]: 'CN (Control)',
        mapeo_auto.index[1]: 'MCI (Deterioro Leve)',
        mapeo_auto.index[2]: 'AD (Alzheimer)'
    }
    print(f"🔄 Mapeo automático: {cluster_map}")
    diagnosis_map = {1.0: 'CN (Control)', 2.0: 'MCI (Deterioro Leve)', 3.0: 'AD (Alzheimer)'}

    # 2. Aplicar el mapeo a nuevas columnas (para no romper los datos originales)
    df_ml_plot = df_ml.copy()  # Copia para graficar
    df_ml_plot['Cluster_Label'] = [cluster_map[c] for c in
                                   clusters]  # Asumiendo que 'clusters' es tu array de predicción
    df_ml_plot['Diagnosis_Label'] = df_ml_plot['DIAGNOSIS'].map(diagnosis_map)

    # 3. Configurar la figura
    plt.figure(figsize=(16, 6))

    # --- GRÁFICA 1: CLUSTERS DETECTADOS ---
    plt.subplot(1, 2, 1)
    # Usamos 'hue_order' para asegurar que los colores coincidan lógica (Sano -> Enfermo)
    order = ['CN (Control)', 'MCI (Deterioro Leve)', 'AD (Alzheimer)']
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1],
                    hue=df_ml_plot['Cluster_Label'],
                    hue_order=order,
                    palette='viridis', s=60, alpha=0.8)
    plt.title("Clusters Detectados (K-Means)", fontsize=14, fontweight='bold')
    plt.xlabel("Componente Principal 1 (Gravedad)", fontsize=12)
    plt.ylabel("Componente Principal 2", fontsize=12)
    plt.legend(title='Grupo Identificado')

    # --- GRÁFICA 2: DIAGNÓSTICO REAL ---
    plt.subplot(1, 2, 2)
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1],
                    hue=df_ml_plot['Diagnosis_Label'],
                    hue_order=order,
                    palette='coolwarm', s=60, alpha=0.8)
    plt.title("Diagnóstico Clínico Real", fontsize=14, fontweight='bold')
    plt.xlabel("Componente Principal 1 (Gravedad)", fontsize=12)
    plt.ylabel("Componente Principal 2", fontsize=12)
    plt.legend(title='Diagnóstico Médico')

    plt.tight_layout()
    plt.savefig("/opt/spark-data/ml_clustering.png", dpi=150, bbox_inches='tight')
    plt.close()  # Liberar memoria
    print("📊 Gráfico guardado en: /opt/spark-data/ml_clustering.png")

    return df_res
# ==========================================
#      MAIN
# ==========================================
def main():
    print("--- INICIANDO CONEXIÓN AL CLUSTER ---")
    # ---------------------------------------------------------
    # INICIO: Configuración Spark
    # ---------------------------------------------------------
    spark = SparkSession.builder \
        .appName("ADNI_ETL_Cluster") \
        .master("spark://spark-master:7077") \
        .config("spark.executor.memory", "2g") \
        .config("spark.executor.cores", "2") \
        .config("spark.driver.memory", "1g") \
        .config("spark.sql.caseSensitive", "True") \
        .getOrCreate()
    # Nota: He quitado .config("spark.jars", ...) porque para CSV/Parquet no hace falta.
    # Solo se pone si conectas a bases de datos SQL (PostgreSQL, MySQL, etc).

    print(f"✅ Conectado al Master: {spark.sparkContext.master}")
    base_path = "/opt/spark-data"

    print(f"📂 Buscando archivos en: {base_path}")

    # Función auxiliar para leer CSVs de forma segura
    def read_adni_csv(filename):
        full_path = os.path.join(base_path, filename)
        # Verificamos si existe antes de leer (opcional, ayuda a depurar)
        print(f"   -> Leyendo: {filename} ...")
        return spark.read.csv(full_path, header=True, inferSchema=True, nullValue="")

    # ---------------------------------------------------------
    # BLOQUE B: ETL CON SPARK (Extract, Transform, Load)
    # ---------------------------------------------------------
    print("--- Cargando datos ---")
    # 1. Ingesta
    df_adni3 = read_adni_csv('UCSFFSX7_25Jan2026.csv')
    # FILTRO: Solo fase ADNI3
    df_adni3 = df_adni3.filter(col('PHASE') == 'ADNI3')
    print(f"Registros iniciales ADNI3 tras filtro: {df_adni3.count()}")
    df_dx = read_adni_csv('DXSUM_25Jan2026.csv')
    df_adnimerge = read_adni_csv('ADNIMERGE_05Feb2026.csv')
    df_MMSE = read_adni_csv('MMSE_25Jan2026.csv')
    df_FAQ = read_adni_csv('FAQ_25Jan2026.csv')
    print(f"Registros iniciales ADNI3: {df_adni3.count()}")

    # 2. MERGE (Joins)
    print("\n" + "🔍" * 20)
    print("PRUEBA")
    count_pre = df_adni3.count()
    # 2.1 DX (Join por PTID y PHASE)
    cols_dx = ['PTID', 'PHASE', 'DIAGNOSIS']
    # Verificamos que existan las columnas antes de seleccionar
    valid_cols_dx = [c for c in cols_dx if c in df_dx.columns]
    df_adni3 = df_adni3.join(df_dx.select(valid_cols_dx), on=['PTID', 'PHASE'], how='left')

    # 2.2 MMSE (Join por PTID, PHASE, VISCODE)
    cols_mmse = ['PTID', 'PHASE', 'VISCODE', 'MMSCORE']
    valid_cols_mmse = [c for c in cols_mmse if c in df_MMSE.columns]
    df_adni3 = df_adni3.join(df_MMSE.select(valid_cols_mmse), on=['PTID', 'PHASE', 'VISCODE'], how='left')

    # 2.3 FAQ
    cols_faq = ['PTID', 'PHASE', 'VISCODE', 'FAQTOTAL']
    valid_cols_faq = [c for c in cols_faq if c in df_FAQ.columns]
    df_adni3 = df_adni3.join(df_FAQ.select(valid_cols_faq), on=['PTID', 'PHASE', 'VISCODE'], how='left')

    # 2.4 ADNIMERGE
    print("-> Uniendo Genero, Edad, APOE...")
    cols_static = ['PTID', 'PTGENDER', 'PTEDUCAT', 'PTMARRY', 'APOE4', 'AGE']
    cols_drop = [c for c in cols_static if c in df_adni3.columns and c != 'PTID']
    if cols_drop:
        df_adni3 = df_adni3.drop(*cols_drop)
    df_static = df_adnimerge.select(cols_static).dropDuplicates(['PTID'])
    df_adni3 = df_adni3.join(df_static, on='PTID', how='left')


    # 2.5. Reemplazar 'sc' e 'init' por 'y0' usando sintaxis Spark (Más eficiente antes de convertir a Pandas)
    df_adni3 = df_adni3.withColumn(
        'VISCODE',
        when(col('VISCODE').isin(['sc', 'init']), 'y0')  # Si es sc o init -> y0
        .otherwise(col('VISCODE'))  # Si no, dejar como está
    )

    # 3. PRE-PROCESAMIENTO Y LIMPIEZA
    # 3.1 Eliminar columnas donde TODOS los valores son nulos
    print("--- Buscando y eliminando columnas vacías ---")
    # Lista para guardar las expresiones de conteo
    expresiones_conteo = []
    for c in df_adni3.columns:
        # Obtenemos el tipo de dato de la columna actual
        tipo = df_adni3.schema[c].dataType
        # LOGICA SEGURA:
        # Si es número decimal (Float/Double), hay que cuidar los NaNs
        if isinstance(tipo, (FloatType, DoubleType)):
            # Contamos cuántos valores NO son nulos y NO son NaN
            expresiones_conteo.append(count(when(~isnan(col(c)) & col(c).isNotNull(), c)).alias(c))
        else:
            # Para fechas (DateType), texto o enteros, 'count' funciona directo ignorando nulos
            expresiones_conteo.append(count(col(c)).alias(c))
    # Ejecutamos la consulta (esto devuelve una sola fila con los conteos)
    # .first() obtiene el resultado en python local
    conteo_row = df_adni3.select(expresiones_conteo).first()
    # Si el conteo es 0, significa que la columna está vacía
    cols_a_borrar = [c for c in df_adni3.columns if conteo_row[c] == 0]

    # Borramos las columnas identificadas
    if cols_a_borrar:
        print(f"Eliminando {len(cols_a_borrar)} columnas totalmente vacías.")
        df_adni3 = df_adni3.drop(*cols_a_borrar)
    else:
        print("No se encontraron columnas totalmente vacías.")

    # 3.2 RENOMBRAR VARIABLES
    print("--- Renombrando variables ---")
    mapping_nombres = {
        # --- HIPOCAMPO Y ENTORRINAL (Zona Cero) ---
        'ST29SV': 'Hippocampus_Left', 'ST88SV': 'Hippocampus_Right',
        'ST24CV': 'Entorhinal_Left_CortVol', 'ST83CV': 'Entorhinal_Right_CortVol',
        'ST24TA': 'Entorhinal_Left_Thick', 'ST83TA': 'Entorhinal_Right_Thick',

        # --- PARAHIPOCAMPO Y FUSIFORME ---
        'ST42SV': 'Parahippocampal_Left', 'ST101SV': 'Parahippocampal_Right',
        'ST26CV': 'Fusiform_Left_CortVol', 'ST85CV': 'Fusiform_Right_CortVol',
        'ST26TA': 'Fusiform_Left_Thick', 'ST85TA': 'Fusiform_Right_Thick',

        # --- TEMPORAL (Medio e Inferior) ---
        'ST40CV': 'MidTemp_Left_CortVol', 'ST99CV': 'MidTemp_Right_CortVol',
        'ST40TA': 'MidTemp_Left_Thick', 'ST99TA': 'MidTemp_Right_Thick',
        'ST32CV': 'InfTemp_Left_CortVol', 'ST91CV': 'InfTemp_Right_CortVol',

        # --- AMÍGDALA, ÍNSULA Y PARIETAL ---
        'ST15CV': 'Amygdala_Left_CortVol', 'ST74CV': 'Amygdala_Right_CortVol',
        'ST35CV': 'Insula_Left_CortVol', 'ST94CV': 'Insula_Right_CortVol',
        'ST50CV': 'Precuneus_Left_CortVol', 'ST109CV': 'Precuneus_Right_CortVol',
        'ST50TA': 'Precuneus_Left_Thick', 'ST109TA': 'Precuneus_Right_Thick',
        'ST31CV': 'InfParietal_Left_CortVol', 'ST90CV': 'InfParietal_Right_CortVol',

        # --- FRONTAL ---
        'ST54CV': 'SupFrontal_Left_CortVol', 'ST113CV': 'SupFrontal_Right_CortVol',

        # --- VENTRÍCULOS Y GLOBALES ---
        'ST12SV': 'Ventricle_Lat_Left', 'ST71SV': 'Ventricle_Lat_Right',
        'ST64SV': 'Ventricle_Inf_Left', 'ST123SV': 'Ventricle_Inf_Right',
        'ST1SV': 'WholeBrain_Vol', 'ICV': 'Intracranial_Vol',

        # --- DUPLICADOS GESTIONADOS ---
        'ST24SV': 'Entorhinal_Left', 'ST83SV': 'Entorhinal_Right',
        'ST26SV': 'Fusiform_Left', 'ST85SV': 'Fusiform_Right',
        'ST40SV': 'MidTemp_Left', 'ST99SV': 'MidTemp_Right',
        'ST32SV': 'InfTemp_Left', 'ST91SV': 'InfTemp_Right',
        'ST15SV': 'Amygdala_Left', 'ST74SV': 'Amygdala_Right',
        'ST50SV': 'Precuneus_Left', 'ST109SV': 'Precuneus_Right',
        'ST31SV': 'InfParietal_Left', 'ST90SV': 'InfParietal_Right',
        'ST54SV': 'SupFrontal_Left', 'ST113SV': 'SupFrontal_Right',
        'ST35SV': 'Insula_Left', 'ST94SV': 'Insula_Right',

        # Temporal Superior
        'ST56SV': 'SupTemp_Left', 'ST115SV': 'SupTemp_Right',

        # Cingulado
        'ST16SV': 'CaudalAntCingulate_Left', 'ST75SV': 'CaudalAntCingulate_Right',
        'ST52SV': 'RostralAntCingulate_Left', 'ST111SV': 'RostralAntCingulate_Right',
        'ST44SV': 'PostCingulate_Left', 'ST103SV': 'PostCingulate_Right',
        'ST30SV': 'IsthmusCingulate_Left', 'ST89SV': 'IsthmusCingulate_Right',
        'ST93TA': 'IsthmusCingulate_Right_TA',
        'ST74TS': 'CaudalMiddleFrontal_Right_TS',
        'ST55SA': 'RostralMiddleFrontal_Left_SA',

        # Frontal
        'ST51SV': 'RostralMidFrontal_Left', 'ST110SV': 'RostralMidFrontal_Right',
        'ST17SV': 'CaudalMidFrontal_Left', 'ST76SV': 'CaudalMidFrontal_Right',
        'ST33SV': 'LatOrbitofrontal_Left', 'ST92SV': 'LatOrbitofrontal_Right',
        'ST36SV': 'MedOrbitofrontal_Left', 'ST95SV': 'MedOrbitofrontal_Right',
        'ST38SV': 'ParsOpercularis_Left', 'ST97SV': 'ParsOpercularis_Right',
        'ST39SV': 'ParsTriangularis_Left', 'ST98SV': 'ParsTriangularis_Right',

        # Parietal
        'ST55SV': 'SupParietal_Left', 'ST114SV': 'SupParietal_Right',

        # Occipital
        'ST34SV': 'LatOccipital_Left', 'ST93SV': 'LatOccipital_Right',
        'ST28SV': 'Lingual_Left', 'ST87SV': 'Lingual_Right',
        'ST23SV': 'Cuneus_Left', 'ST82SV': 'Cuneus_Right',
        'ST43SV': 'Pericalcarine_Left', 'ST102SV': 'Pericalcarine_Right',

        # Global Extra
        'ST10CV': 'ICV_Alt'
    }

    # Aplicar renombrado en bucle
    for old_name, new_name in mapping_nombres.items():
        if old_name in df_adni3.columns:
            df_adni3 = df_adni3.withColumnRenamed(old_name, new_name)

    # 4. VARIABLE DERIVADA (Requisito Bloque B)
    # Creamos un Ratio de Hipocampo total normalizado por Volumen Intracraneal (ICV)
    if 'Hippocampus_Left' in df_adni3.columns and 'ICV' in df_adni3.columns:
        df_adni3 = df_adni3.withColumn(
            "Hippocampal_Total_Ratio",
            (col("Hippocampus_Left") + col("Hippocampus_Right")) / col("ICV")
        )
        print("✅ Variable derivada 'Hippocampal_Total_Ratio' creada.")

    # ---------------------------------------------------------
    # REPORTE DE CALIDAD DE DATOS (BLOQUE B - ETL)
    # ---------------------------------------------------------
    print("\n--- Generando reporte de calidad de datos ---")
    # 5.1 Reporte de Nulos SEGURO
    final_rows = df_adni3.count()

    expresiones_reporte = []
    for c in df_adni3.columns:
        tipo = df_adni3.schema[c].dataType
        if isinstance(tipo, (FloatType, DoubleType)):
            expresiones_reporte.append(count(when(isnan(c) | col(c).isNull(), c)).alias(c))
        else:
            expresiones_reporte.append(count(when(col(c).isNull(), c)).alias(c))

    # Obtenemos los conteos de nulos (lo que contamos son los NO nulos, así que restamos)
    # Un momento: count(when(isNull)) cuenta los NULOS directamente.
    # Ajustamos la lógica para contar NULOS:

    lista_nulos = []
    row_nulos = df_adni3.select([
        count(when(col(c).isNull(), c)).alias(c)
        if not isinstance(df_adni3.schema[c].dataType, (FloatType, DoubleType))
        else count(when(isnan(col(c)) | col(c).isNull(), c)).alias(c)
        for c in df_adni3.columns
    ]).first()

    null_dict = row_nulos.asDict()
    sorted_nulls = sorted(null_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"\n--- TOP 10 VARIABLES CON VALORES PERDIDOS (Total filas: {final_rows}) ---")
    print(f"{'Variable':<30} | {'Nulos':<10} | {'%'}")
    print("-" * 50)
    for col_name, val in sorted_nulls:
        pct = round((val / final_rows) * 100, 2)
        print(f"{col_name:<30} | {val:<10} | {pct}%")

    # 5.2 Conteos de Categorías
    print("\n--- Conteos ---")
    df_adni3.groupBy("PHASE").count().show()
    df_adni3.groupBy("VISCODE").count().show()

    # 5.3 Tipo de datos ?

    # ---------------------------------------------------------
    # TRANSICIÓN: CONVERSIÓN A PANDAS
    # ---------------------------------------------------------
    print("\n" + "💾" * 20)
    # Optimización Arrow
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    try:
        # Convertimos de Spark (Distribuido) a Pandas (Local en memoria)
        print("🔄 Convirtiendo a Pandas para selección de variables...")
        pdf_adni = df_adni3.toPandas()
        print(f"✅ Conversión exitosa. Filas en memoria: {len(pdf_adni)}")

        if not pdf_adni.empty:
            # Aplicamos transformaciones AHORA para que la selección de variables
            # y el clustering usen los datos corregidos.
            pdf_adni = aplicar_transformaciones_neuro_adni(pdf_adni)

            # SELECCIÓN DE VARIABLES (Machine Learning)
            # Ejecutamos (randomForest) -> seleccion de variables
            top_cols = descubrir_features_mas_importantes(pdf_adni, n_top=10)
            
            # ---------------------------------------------------------
            # BLOQUE C: ANÁLISIS Y VISUALIZACIÓN
            # ---------------------------------------------------------
            print("\n" + "="*50)
            print(" BLOQUE C: ANÁLISIS Y VISUALIZACIÓN")
            print("="*50)

            # 1. EDA
            eda_cats = ['DIAGNOSIS', 'PTGENDER', 'VISCODE', 'APOE4']
            ejecutar_eda_completo(pdf_adni, top_cols, eda_cats)
            ejecutar_metodo_codo(pdf_adni, top_cols)
            ejecutar_clustering_grid(pdf_adni, top_cols)
            
            # 2. CLUSTERING SOBRE TOP FEATURES
            df_ml_results = ejecutar_clustering_pipeline(pdf_adni, top_cols)
            print("\n--- Perfil Medio de los Clusters ---")
            print(df_ml_results.groupby('Cluster_KMeans')[top_cols].mean().T)
            print("\n📝 Preparando archivo de salida...")

            # Define las columnas de resultados del modelo
            cols_resultado = ['Cluster_KMeans', 'PC1', 'PC2']
            cols_exportar = list(dict.fromkeys(cols_resultado))
            cols_finales = [c for c in cols_exportar if c in df_ml_results.columns]

            # Guardar CSV
            nombre_fichero = "resultados_clustering_adni.csv"
            df_ml_results[cols_finales].to_csv(nombre_fichero, index=False)
            print(f"✅ Archivo guardado: {nombre_fichero}")
            print(f"   -> Dimensiones: {len(df_ml_results)} filas x {len(cols_finales)} columnas")
            print(f"   -> Columnas incluidas: {cols_finales[:5]} ...")

            # ---------------------------------------------------------
            # FILTRADO FINAL Y GUARDADO
            # ---------------------------------------------------------
            print("\n" + "💾" * 20)

            cols_meta = ['PTID', 'DIAGNOSIS', 'VISCODE', 'PTGENDER', 'APOE4']
            # Filtramos el DataFrame final: Top Variables + Metadatos
            columnas_finales = [c for c in top_cols + cols_meta if c in pdf_adni.columns]

            pdf_adni = pdf_adni[columnas_finales]
            print(f"📦 Dataset con seleccion de variables: {pdf_adni.shape} (Filas, Columnas)")

            # IMPORTANTE: base_path debe ser tu ruta montada (/opt/spark-data)
            ruta_csv = os.path.join(base_path, "adni_seleccionado.csv")
            ruta_parquet = os.path.join(base_path, "adni_seleccionado.parquet")

            print(f"📄 Guardando CSV con variables seleccionadas en: {ruta_csv}")
            try:
                pdf_adni.to_csv(ruta_csv, index=False, sep=",", encoding='utf-8')
                print("🎉 ¡ÉXITO! Archivo CSV guardado.")
            except Exception as e:
                print(f"❌ Error escribiendo CSV: {e}")

            # Guardar Parquet
            print(f"📦 Escribiendo Parquet directo en: {ruta_parquet}")
            try:
                pdf_adni.to_parquet(ruta_parquet, index=False)
                print("🎉 ¡ÉXITO! Archivo Parquet guardado.")
            except Exception as e:
                print(f"⚠️ Aviso: No se generó el Parquet (probablemente falta la librería pyarrow).")

        else:
            print("❌ ERROR CRÍTICO: El DataFrame está vacío antes de guardar.")

    except Exception as e:
        print(f"❌ Error: {e}")
        pdf_adni = None

    print("💾" * 20 + "\n")

    spark.stop()

if __name__ == "__main__":
    main()
