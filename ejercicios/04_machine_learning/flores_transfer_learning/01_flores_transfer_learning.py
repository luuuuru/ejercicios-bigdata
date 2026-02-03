"""
CLASIFICACION DE FLORES CON TRANSFER LEARNING
=============================================
Pipeline completo de Computer Vision para clasificar 5 tipos de flores
usando Transfer Learning con MobileNetV2.

QUE ES TRANSFER LEARNING?
------------------------
En lugar de entrenar una red neuronal desde cero (necesitariamos millones
de imagenes), usamos una red ya entrenada en ImageNet y la adaptamos:

    ImageNet (14M imgs) --> MobileNetV2 --> Embeddings --> Nuestro clasificador
                               |                |
                        Ya sabe "ver"     Vector de 1280
                                          caracteristicas

Las primeras capas de la CNN ya aprendieron a detectar:
- Bordes y texturas
- Formas y patrones
- Combinaciones de colores

Esto es UNIVERSAL - sirve para cualquier imagen!

PIPELINE
--------
1. Descargar dataset de flores (TensorFlow Flowers)
2. Extraer embeddings con MobileNetV2 (sin entrenar, solo usar)
3. Entrenar clasificadores ML sobre los embeddings
4. Visualizar con t-SNE y generar dashboard

Ejecutar:
    python 01_flores_transfer_learning.py

Autor: Juan Marcelo Gutierrez Miranda | @TodoEconometria
"""
import os
import sys
import json
import warnings
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

warnings.filterwarnings("ignore")

# =====================================================================
# CONFIGURACION
# =====================================================================
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

FLOWERS_URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

FLOWER_CLASSES = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]
CLASS_NAMES_ES = {
    "daisy": "Margarita",
    "dandelion": "Diente de Leon",
    "roses": "Rosa",
    "sunflowers": "Girasol",
    "tulips": "Tulipan",
}

COLORS = {
    "daisy": "#FFD700",
    "dandelion": "#FFA500",
    "roses": "#FF1744",
    "sunflowers": "#FFEB3B",
    "tulips": "#E91E63",
}


# =====================================================================
# PASO 1: DESCARGA DE DATOS
# =====================================================================
def download_flowers():
    """Descarga el dataset de flores de TensorFlow."""
    print("\n[1/5] DESCARGA DE DATOS")
    print("-" * 40)

    data_dir = OUTPUT_DIR / "flower_photos"

    if data_dir.exists() and len(list(data_dir.glob("*/*.jpg"))) > 3000:
        print(f"  Dataset ya existe: {data_dir}")
        return data_dir

    tgz_path = OUTPUT_DIR / "flower_photos.tgz"

    print(f"  Descargando desde: {FLOWERS_URL}")
    print("  (Esto puede tardar unos minutos...)")

    urllib.request.urlretrieve(FLOWERS_URL, tgz_path)

    print("  Extrayendo archivos...")
    with tarfile.open(tgz_path, "r:gz") as tar:
        tar.extractall(OUTPUT_DIR)

    tgz_path.unlink()  # Eliminar archivo comprimido

    # Contar imagenes
    n_images = len(list(data_dir.glob("*/*.jpg")))
    print(f"  [OK] Dataset listo: {n_images} imagenes")

    return data_dir


def prepare_metadata(data_dir):
    """Crea metadata con rutas y clases."""
    print("\n  Preparando metadata...")

    records = []
    for class_dir in data_dir.iterdir():
        if class_dir.is_dir() and class_dir.name in FLOWER_CLASSES:
            for img_path in class_dir.glob("*.jpg"):
                records.append({
                    "path": str(img_path),
                    "filename": img_path.name,
                    "class_name": class_dir.name,
                    "class_name_es": CLASS_NAMES_ES[class_dir.name],
                })

    df = pd.DataFrame(records)
    print(f"  Total imagenes: {len(df)}")
    for cls in FLOWER_CLASSES:
        n = len(df[df["class_name"] == cls])
        print(f"    {CLASS_NAMES_ES[cls]}: {n}")

    return df


# =====================================================================
# PASO 2: EXTRACCION DE EMBEDDINGS (Transfer Learning)
# =====================================================================
def check_tensorflow():
    """Verifica si TensorFlow esta disponible."""
    try:
        import tensorflow as tf
        print(f"  TensorFlow: {tf.__version__}")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"  GPU: {gpus[0].name}")
        else:
            print("  GPU: No disponible (usando CPU)")
        return True
    except ImportError:
        return False


def extract_embeddings(df):
    """
    TRANSFER LEARNING: Extraer embeddings con MobileNetV2

    MobileNetV2 fue entrenado en ImageNet (14 millones de imagenes, 1000 clases).
    Usamos la red SIN la capa final de clasificacion - obtenemos un vector
    de 1280 dimensiones que representa las "caracteristicas visuales" de cada imagen.

    Estos embeddings capturan:
    - Formas y contornos
    - Texturas y patrones
    - Colores y gradientes
    - Relaciones espaciales

    Flores similares tendran embeddings similares (distancia coseno pequena).
    """
    print("\n[2/5] EXTRACCION DE EMBEDDINGS (Transfer Learning)")
    print("-" * 40)

    if not check_tensorflow():
        print("\n  [ERROR] TensorFlow no esta instalado.")
        print("  Instalar con: pip install tensorflow")
        print("  O en WSL2: source ~/tf-gpu-env/bin/activate")
        return None

    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    print("\n  Cargando MobileNetV2 pre-entrenado...")
    print("  - Pesos: ImageNet (1000 clases, 14M imagenes)")
    print("  - Output: Vector de 1280 dimensiones por imagen")

    # Cargar modelo SIN la capa de clasificacion
    model = MobileNetV2(
        weights="imagenet",
        include_top=False,  # Sin capa de clasificacion
        pooling="avg",      # Global average pooling
        input_shape=(*IMG_SIZE, 3)
    )
    model.trainable = False  # No entrenar, solo usar

    print(f"  Parametros del modelo: {model.count_params():,}")

    # Extraer embeddings
    print(f"\n  Procesando {len(df)} imagenes...")

    embeddings = []
    for i, row in df.iterrows():
        # Cargar y preprocesar imagen
        img = tf.keras.preprocessing.image.load_img(row["path"], target_size=IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Extraer embedding
        embedding = model.predict(img_array, verbose=0)
        embeddings.append(embedding[0])

        if (i + 1) % 500 == 0:
            print(f"    Procesadas: {i + 1}/{len(df)}")

    embeddings = np.array(embeddings)
    print(f"  [OK] Embeddings extraidos: {embeddings.shape}")

    return embeddings


# =====================================================================
# PASO 3: CLASIFICACION CON ML TRADICIONAL
# =====================================================================
def train_classifiers(df, embeddings):
    """
    Entrenar clasificadores ML sobre los embeddings.

    Como los embeddings ya capturan la "esencia" de cada imagen,
    podemos usar clasificadores simples como KNN, SVM o Random Forest.

    Esto es mucho mas rapido que entrenar una CNN desde cero!
    """
    print("\n[3/5] CLASIFICACION CON ML TRADICIONAL")
    print("-" * 40)

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

    # Preparar datos
    le = LabelEncoder()
    y = le.fit_transform(df["class_name"])

    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, y, test_size=0.2, random_state=42, stratify=y
    )

    # Escalar (importante para SVM y KNN)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    # Modelos a entrenar
    models = {
        "KNN": KNeighborsClassifier(n_neighbors=5, metric="cosine"),
        "SVM": SVC(kernel="rbf", C=10.0),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42),
    }

    results = {}
    best_model = None
    best_acc = 0

    for name, model in models.items():
        print(f"\n  Entrenando {name}...")
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="macro")
        cm = confusion_matrix(y_test, y_pred)

        results[name] = {
            "accuracy": acc,
            "f1_macro": f1,
            "confusion_matrix": cm.tolist(),
        }

        print(f"    Accuracy: {acc:.1%} | F1: {f1:.1%}")

        if acc > best_acc:
            best_acc = acc
            best_model = name

    print(f"\n  [OK] Mejor modelo: {best_model} ({best_acc:.1%})")

    return results, scaler


# =====================================================================
# PASO 4: REDUCCION DE DIMENSIONALIDAD
# =====================================================================
def reduce_dimensions(embeddings):
    """
    Reducir 1280 dimensiones a 2 para visualizacion con t-SNE.

    t-SNE preserva las relaciones de vecindad:
    - Flores similares quedan cerca en el grafico 2D
    - Flores diferentes quedan lejos
    """
    print("\n[4/5] REDUCCION DE DIMENSIONALIDAD (t-SNE)")
    print("-" * 40)

    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE

    # PCA primero (1280 -> 50) para acelerar t-SNE
    print("  PCA: 1280 -> 50 dimensiones...")
    pca = PCA(n_components=50, random_state=42)
    embeddings_pca = pca.fit_transform(embeddings)
    print(f"    Varianza explicada: {pca.explained_variance_ratio_.sum():.1%}")

    # t-SNE (50 -> 2)
    print("  t-SNE: 50 -> 2 dimensiones (puede tardar)...")
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings_pca)

    print("  [OK] Reduccion completada")

    return embeddings_2d


# =====================================================================
# PASO 5: VISUALIZACION
# =====================================================================
def image_to_base64(img_path, size=(100, 100)):
    """Convierte imagen a base64 para embeber en HTML."""
    import base64
    import io
    try:
        img = Image.open(img_path)
        img.thumbnail(size)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=75)
        return base64.b64encode(buffer.getvalue()).decode()
    except:
        return None


def get_sample_images(df, n_per_class=4):
    """Obtiene imagenes de muestra por clase."""
    samples = {}
    for flower_class in FLOWER_CLASSES:
        class_df = df[df["class_name"] == flower_class].sample(n=min(n_per_class, len(df[df["class_name"] == flower_class])), random_state=42)
        samples[flower_class] = []
        for _, row in class_df.iterrows():
            b64 = image_to_base64(row["path"])
            if b64:
                samples[flower_class].append({"b64": b64, "name": row["filename"]})
    return samples


def build_gallery_html(samples):
    """Construye HTML de galeria de imagenes."""
    html = '<div style="display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;padding:1rem;">'
    for flower_class, images in samples.items():
        if not images:
            continue
        class_name_es = CLASS_NAMES_ES.get(flower_class, flower_class)
        color = COLORS.get(flower_class, "#888")
        html += f'''
        <div style="background:#161b22;border-radius:12px;padding:1rem;border:2px solid {color};min-width:200px;">
            <h4 style="color:{color};text-align:center;margin-bottom:0.5rem;">{class_name_es}</h4>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;justify-content:center;">
        '''
        for img in images:
            html += f'''
                <img src="data:image/jpeg;base64,{img["b64"]}"
                     alt="{img["name"]}" title="{img["name"]}"
                     style="width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid #30363d;">
            '''
        html += '</div></div>'
    html += '</div>'
    return html


def create_dashboard(df, results, embeddings_2d):
    """Genera dashboard HTML con visualizaciones."""
    print("\n[5/5] GENERACION DE DASHBOARD")
    print("-" * 40)

    import plotly.express as px
    import plotly.graph_objects as go

    # Agregar coordenadas t-SNE al dataframe
    df = df.copy()
    df["tsne_x"] = embeddings_2d[:, 0]
    df["tsne_y"] = embeddings_2d[:, 1]

    # 0. Galeria de imagenes
    print("  Creando galeria de imagenes...")
    samples = get_sample_images(df, n_per_class=4)
    gallery_html = build_gallery_html(samples)

    # 1. Scatter t-SNE
    print("  Creando visualizacion t-SNE...")
    fig_tsne = px.scatter(
        df, x="tsne_x", y="tsne_y",
        color="class_name_es",
        hover_data=["filename"],
        color_discrete_map={CLASS_NAMES_ES[c]: COLORS[c] for c in FLOWER_CLASSES},
        title="Embeddings t-SNE: Agrupacion Natural por Tipo de Flor",
    )
    fig_tsne.update_traces(marker=dict(size=6, opacity=0.7))
    fig_tsne.update_layout(height=600, template="plotly_dark")

    # 2. Comparativa de modelos
    print("  Creando comparativa de modelos...")
    models = list(results.keys())
    accuracies = [results[m]["accuracy"] for m in models]

    fig_compare = go.Figure(data=[
        go.Bar(x=models, y=accuracies, marker_color=["#2196F3", "#FF5722", "#4CAF50"],
               text=[f"{a:.1%}" for a in accuracies], textposition="outside")
    ])
    fig_compare.update_layout(
        title="Comparativa de Modelos ML",
        yaxis_title="Accuracy", yaxis_range=[0, 1.1],
        height=400, template="plotly_dark"
    )

    # 3. Matriz de confusion (mejor modelo)
    print("  Creando matriz de confusion...")
    best = max(results.items(), key=lambda x: x[1]["accuracy"])
    cm = np.array(best[1]["confusion_matrix"])
    cm_percent = cm.astype(float) / cm.sum(axis=1, keepdims=True) * 100
    class_labels = [CLASS_NAMES_ES[c] for c in FLOWER_CLASSES]

    fig_cm = go.Figure(data=go.Heatmap(
        z=cm_percent, x=class_labels, y=class_labels,
        colorscale="Blues",
        text=[[f"{cm_percent[i,j]:.0f}%" for j in range(5)] for i in range(5)],
        texttemplate="%{text}",
    ))
    fig_cm.update_layout(
        title=f"Matriz de Confusion - {best[0]} (Acc: {best[1]['accuracy']:.1%})",
        xaxis_title="Predicho", yaxis_title="Real",
        height=500, template="plotly_dark"
    )

    # 4. Distribucion radar
    print("  Creando distribucion radar...")
    counts = df["class_name_es"].value_counts()
    values = [counts.get(CLASS_NAMES_ES[c], 0) for c in FLOWER_CLASSES]

    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=class_labels + [class_labels[0]],
        fill='toself', fillcolor='rgba(76, 175, 80, 0.3)',
        line=dict(color='#4CAF50', width=2),
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Distribucion del Dataset",
        height=450, template="plotly_dark"
    )

    # Construir HTML
    print("  Construyendo HTML...")
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Clasificacion de Flores - Transfer Learning</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; }}
        .header {{ background: linear-gradient(135deg, #1a472a, #3d7a4d); padding: 2rem; text-align: center; }}
        .header h1 {{ color: #81C784; margin: 0; }}
        .tabs {{ display: flex; gap: 4px; padding: 1rem; background: #161b22; flex-wrap: wrap; }}
        .tab-btn {{ padding: 0.8rem 1.2rem; background: #21262d; color: #8b949e; border: 1px solid #30363d;
                   cursor: pointer; border-radius: 8px 8px 0 0; font-size: 0.9rem; }}
        .tab-btn:hover {{ background: #30363d; }}
        .tab-btn.active {{ background: #4CAF50; color: white; }}
        .content {{ padding: 1rem 2rem; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .ref {{ background: #161b22; padding: 1.5rem; margin: 1rem 2rem; border-radius: 12px; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Clasificacion de Flores con Transfer Learning</h1>
        <p>MobileNetV2 + ML Tradicional | TensorFlow + scikit-learn</p>
    </div>
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab(0)">Galeria</button>
        <button class="tab-btn" onclick="showTab(1)">t-SNE</button>
        <button class="tab-btn" onclick="showTab(2)">Comparativa</button>
        <button class="tab-btn" onclick="showTab(3)">Confusion Matrix</button>
        <button class="tab-btn" onclick="showTab(4)">Distribucion</button>
    </div>
    <div class="content">
        <div class="tab-content active" id="tab-0">
            <h3 style="text-align:center;color:#4CAF50;margin:1rem 0;">Muestra del Dataset: Flores Reales</h3>
            {gallery_html}
        </div>
        <div class="tab-content" id="tab-1">{fig_tsne.to_html(full_html=False, include_plotlyjs=True)}</div>
        <div class="tab-content" id="tab-2">{fig_compare.to_html(full_html=False, include_plotlyjs=False)}</div>
        <div class="tab-content" id="tab-3">{fig_cm.to_html(full_html=False, include_plotlyjs=False)}</div>
        <div class="tab-content" id="tab-4">{fig_radar.to_html(full_html=False, include_plotlyjs=False)}</div>
    </div>
    <div class="ref">
        <strong>Curso:</strong> Big Data con Python - De Cero a Produccion<br>
        <strong>Profesor:</strong> Juan Marcelo Gutierrez Miranda | @TodoEconometria<br>
        <strong>Hash ID:</strong> 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c<br><br>
        <strong>Referencias:</strong><br>
        - Sandler, M., et al. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. CVPR.<br>
        - van der Maaten, L. & Hinton, G. (2008). Visualizing Data using t-SNE. JMLR.
    </div>
    <script>
    function showTab(idx) {{
        document.querySelectorAll('.tab-content').forEach((el, i) => {{
            el.classList.toggle('active', i === idx);
        }});
        document.querySelectorAll('.tab-btn').forEach((el, i) => {{
            el.classList.toggle('active', i === idx);
        }});
        window.dispatchEvent(new Event('resize'));
    }}
    </script>
</body>
</html>"""

    output_path = OUTPUT_DIR / "dashboard_flores.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"  [OK] Dashboard: {output_path}")
    return str(output_path)


# =====================================================================
# MAIN
# =====================================================================
def main():
    """Pipeline completo de Transfer Learning."""
    print("=" * 60)
    print("CLASIFICACION DE FLORES CON TRANSFER LEARNING")
    print("=" * 60)

    # 1. Descargar datos
    data_dir = download_flowers()
    df = prepare_metadata(data_dir)

    # 2. Extraer embeddings
    embeddings = extract_embeddings(df)
    if embeddings is None:
        return

    # 3. Entrenar clasificadores
    results, scaler = train_classifiers(df, embeddings)

    # 4. Reducir dimensiones para visualizacion
    embeddings_2d = reduce_dimensions(embeddings)

    # 5. Crear dashboard
    dashboard_path = create_dashboard(df, results, embeddings_2d)

    # Resumen
    print("\n" + "=" * 60)
    print("[OK] PIPELINE COMPLETADO")
    print("=" * 60)
    print(f"\nResultados:")
    for name, res in sorted(results.items(), key=lambda x: -x[1]["accuracy"]):
        print(f"  {name}: {res['accuracy']:.1%}")
    print(f"\nDashboard: {dashboard_path}")
    print("\nAbre el archivo HTML en tu navegador para ver las visualizaciones.")


if __name__ == "__main__":
    main()
