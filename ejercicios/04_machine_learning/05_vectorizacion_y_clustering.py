"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodología: Cursos Avanzados de Big Data, Ciencia de Datos, 
             Desarrollo de aplicaciones con IA & Econometría Aplicada.
Hash ID de Certificación: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADÉMICA:
- McKinney, W. (2012). Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython. O'Reilly Media.
- Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.
-------------------------
"""

# --- EJERCICIO 5: VECTORIZACIÓN Y CLUSTERING DE DOCUMENTOS (DATASET SINTÉTICO MASIVO) ---

# --- CONTEXTO ---
# Objetivo: Demostrar clustering con un volumen considerable de datos.
# Generaremos un corpus sintético de 1200 documentos en español distribuidos en 4 temas 
# para asegurar que el algoritmo de Clustering tenga material suficiente para trabajar.

import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# --- 1. GENERACIÓN DE BIG DATA SINTÉTICO ---
print("Paso 1: Generando dataset sintético de 1200 documentos...")

temas = {
    "Tecnología": ["procesador", "software", "algoritmo", "nube", "datos", "inteligencia artificial", "python", "hardware", "sistema", "redes"],
    "Finanzas": ["mercado", "inversión", "bolsa", "acciones", "economía", "banco", "interés", "crédito", "ahorro", "finanzas"],
    "Salud": ["paciente", "hospital", "médico", "tratamiento", "enfermedad", "diagnóstico", "salud", "vacuna", "terapia", "clínica"],
    "Viajes": ["turismo", "hotel", "vuelo", "playa", "montaña", "vacaciones", "pasaporte", "maleta", "guía", "aventura"]
}

corpus = []
labels_reales = []

for i, (tema, palabras) in enumerate(temas.items()):
    for _ in range(300): # 300 documentos por tema = 1200 total
        # Creamos una "frase" aleatoria usando palabras del tema
        n_palabras = random.randint(5, 15)
        frase = " ".join(random.choices(palabras, k=n_palabras))
        corpus.append(frase)
        labels_reales.append(i)

print(f"Dataset generado con {len(corpus)} documentos.")

# --- 2. VECTORIZACIÓN (TF-IDF) ---
print("\nPaso 2: Vectorizando con TF-IDF...")
# Usamos stop_words=None porque ya son solo palabras clave, pero en un caso real usaríamos 'spanish'
vectorizer = TfidfVectorizer(max_features=500)
tfidf_matrix = vectorizer.fit_transform(corpus)

print(f"Dimensiones de la matriz TF-IDF: {tfidf_matrix.shape}")

# --- 3. CLUSTERING (K-MEANS) ---
num_clusters = 4
print(f"\nPaso 3: Aplicando K-Means (k={num_clusters})...")
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
kmeans.fit(tfidf_matrix)
clusters = kmeans.labels_

# --- 4. REDUCCIÓN DE DIMENSIONALIDAD (PCA) ---
print("\nPaso 4: Reduciendo a 2D para visualización...")
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(tfidf_matrix.toarray())

# --- 5. VISUALIZACIÓN ---
print("\nPaso 5: Generando gráfico premium...")

plt.figure(figsize=(12, 8))
# Usamos una paleta de colores vibrante
scatter = plt.scatter(coords[:, 0], coords[:, 1], c=clusters, cmap='Spectral', alpha=0.7, s=30, edgecolors='k', linewidth=0.5)

plt.colorbar(scatter, label='ID del Cluster')
plt.title('Clustering de Documentos: Análisis de Tópicos Automático\n(1200 documentos en Español)', fontsize=16, fontweight='bold')
plt.xlabel('Componente Principal 1 (PCA)', fontsize=12)
plt.ylabel('Componente Principal 2 (PCA)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Guardar la imagen
save_path = "05_visualizacion_clustering.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Gráfico guardado en: {save_path}")

plt.show()

# --- 5B. GRÁFICO DEL MÉTODO DEL CODO (ELBOW METHOD) ---
print("\nPaso 5B: Generando gráfico del Método del Codo...")

# Calculamos la inercia para diferentes valores de k
rango_k = range(2, 11)
inercias = []
silhouette_scores = []

for k in rango_k:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(tfidf_matrix)
    inercias.append(km.inertia_)
    silhouette_scores.append(silhouette_score(tfidf_matrix, km.labels_))

plt.figure(figsize=(14, 5))

# Subplot 1: Método del Codo
plt.subplot(1, 2, 1)
plt.plot(rango_k, inercias, 'bo-', linewidth=2, markersize=8)
plt.axvline(x=4, color='r', linestyle='--', label='k óptimo = 4')
plt.fill_between(rango_k, inercias, alpha=0.2)
plt.xlabel('Número de Clusters (k)', fontsize=12)
plt.ylabel('Inercia (Suma de distancias al cuadrado)', fontsize=12)
plt.title('Método del Codo (Elbow Method)\nPara determinar k óptimo', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Subplot 2: Silhouette Score
plt.subplot(1, 2, 2)
plt.plot(rango_k, silhouette_scores, 'go-', linewidth=2, markersize=8)
plt.axvline(x=4, color='r', linestyle='--', label='k óptimo = 4')
plt.fill_between(rango_k, silhouette_scores, alpha=0.2, color='green')
plt.xlabel('Número de Clusters (k)', fontsize=12)
plt.ylabel('Silhouette Score', fontsize=12)
plt.title('Coeficiente de Silueta por k\n(Mayor = Mejor separación)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
save_path_elbow = "05_elbow_silhouette.png"
plt.savefig(save_path_elbow, dpi=300, bbox_inches='tight')
print(f"Gráfico Elbow/Silhouette guardado en: {save_path_elbow}")
plt.show()

# --- 5C. SCATTER PLOT ESTILO IRIS: CLUSTERS CON PALABRAS DOMINANTES ---
print("\nPaso 5C: Generando scatter plot con palabras dominantes por cluster...")

# Obtener palabras dominantes por cluster (top 3)
indices_centros = kmeans.cluster_centers_.argsort()[:, ::-1]
nombres_palabras = vectorizer.get_feature_names_out()

etiquetas_clusters = []
for i in range(num_clusters):
    top_3 = [nombres_palabras[idx] for idx in indices_centros[i, :3]]
    etiquetas_clusters.append(", ".join(top_3))

# Calcular centroides en espacio PCA
centroides_pca = pca.transform(kmeans.cluster_centers_.toarray() if hasattr(kmeans.cluster_centers_, 'toarray') else kmeans.cluster_centers_)

# Crear figura
fig, ax = plt.subplots(figsize=(14, 10))

# Colores distintivos para cada cluster
colores = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
marcadores = ['o', 's', '^', 'D']

# Graficar puntos por cluster con leyenda descriptiva
for i in range(num_clusters):
    mask = clusters == i
    ax.scatter(coords[mask, 0], coords[mask, 1],
               c=colores[i], marker=marcadores[i],
               s=50, alpha=0.6, edgecolors='white', linewidth=0.5,
               label=f'Cluster {i}: {etiquetas_clusters[i]}')

# Graficar centroides
ax.scatter(centroides_pca[:, 0], centroides_pca[:, 1],
           c='black', marker='X', s=300, edgecolors='white', linewidth=2,
           label='Centroides', zorder=5)

# Anotar centroides con las palabras dominantes
for i, (x, y) in enumerate(centroides_pca):
    ax.annotate(f'C{i}\n{etiquetas_clusters[i]}',
                xy=(x, y), xytext=(10, 10),
                textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=colores[i], alpha=0.8, edgecolor='black'),
                color='white')

ax.set_xlabel('Componente Principal 1', fontsize=12)
ax.set_ylabel('Componente Principal 2', fontsize=12)
ax.set_title('Clustering de Documentos con Palabras Dominantes\n(Estilo Dataset Iris - Visualización de Grupos Semánticos)',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
save_path_iris = "05_clustering_palabras_dominantes.png"
plt.savefig(save_path_iris, dpi=300, bbox_inches='tight')
print(f"Gráfico estilo Iris guardado en: {save_path_iris}")
plt.show()

# --- 6. TOP PALABRAS POR CLUSTER ---
print("\n--- PALABRAS DOMINANTES POR CLUSTER ---")
indices_centros = kmeans.cluster_centers_.argsort()[:, ::-1]
nombres_palabras = vectorizer.get_feature_names_out()

for i in range(num_clusters):
    top_10 = [nombres_palabras[idx] for idx in indices_centros[i, :10]]
    print(f"Cluster {i}: {', '.join(top_10)}")

print("\n--- FIN DEL EJERCICIO 5 ---")
