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

from sklearn.datasets import load_wine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ============================================================================
# K-MEANS - Ejemplo: Wine Dataset (Segmentación de vinos)
# ============================================================================

print("=" * 70)
print("K-MEANS - EJEMPLO: Wine Dataset")
print("Agrupamiento de vinos con validación de clusters")
print("=" * 70)

# Cargar dataset: 178 vinos de 3 cultivares con 13 características químicas
wine = load_wine()
X = wine.data
y_true = wine.target  # Etiquetas reales (solo para comparación)
feature_names = wine.feature_names
target_names = wine.target_names

print(f"\nDatos: {X.shape[0]} vinos")
print(f"Características: {len(feature_names)} propiedades químicas")
print(f"Cultivares reales: {', '.join(target_names)}")
print(f"Distribución real: {pd.Series(y_true).value_counts().sort_index().to_dict()}\n")

# Estandarizar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Método del Codo (Elbow Method) - Determinar número óptimo de clusters
print("Método del Codo: Buscando número óptimo de clusters...")
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans_temp.fit(X_scaled)
    inertias.append(kmeans_temp.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans_temp.labels_))

# Mostrar resultados
print("\nK  |  Inercia  |  Silhouette")
print("-" * 35)
for k, inercia, silhouette in zip(K_range, inertias, silhouette_scores):
    print(f"{k:2d} | {inercia:8.2f} | {silhouette:6.3f}")

# Entrenar K-Means con K=3 (sabemos que hay 3 cultivares)
best_k = 3
print(f"\nEntrenando K-Means con K={best_k}...")
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10, max_iter=300)
y_kmeans = kmeans.fit_predict(X_scaled)

# Métricas de evaluación
silhouette = silhouette_score(X_scaled, y_kmeans)
davies_bouldin = davies_bouldin_score(X_scaled, y_kmeans)
calinski = calinski_harabasz_score(X_scaled, y_kmeans)

print(f"\nMétricas de evaluación:")
print(f"  Inercia: {kmeans.inertia_:.2f}")
print(f"  Silhouette Score: {silhouette:.3f} (rango: -1 a 1, mejor cerca de 1)")
print(f"  Davies-Bouldin Index: {davies_bouldin:.3f} (menor es mejor)")
print(f"  Calinski-Harabasz Score: {calinski:.2f} (mayor es mejor)")

print(f"\nDistribución de clusters encontrados:")
cluster_counts = pd.Series(y_kmeans).value_counts().sort_index()
for cluster, count in cluster_counts.items():
    print(f"  Cluster {cluster}: {count} vinos")

# Comparar con etiquetas reales
print("\nMatriz de confusión (Clusters vs Cultivares reales):")
confusion = pd.crosstab(
    pd.Series(y_true, name='Cultivar Real'),
    pd.Series(y_kmeans, name='Cluster'),
    margins=True
)
print(confusion)

# Reducir a 2D con PCA para visualización
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualización
fig = plt.figure(figsize=(18, 12))

# Plot 1: Método del Codo
ax1 = plt.subplot(2, 3, 1)
ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.axvline(x=best_k, color='red', linestyle='--', label=f'K óptimo = {best_k}')
ax1.set_xlabel('Número de Clusters (K)')
ax1.set_ylabel('Inercia (WCSS)')
ax1.set_title('Método del Codo')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Silhouette Score
ax2 = plt.subplot(2, 3, 2)
ax2.plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
ax2.axvline(x=best_k, color='red', linestyle='--', label=f'K óptimo = {best_k}')
ax2.set_xlabel('Número de Clusters (K)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score vs K')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Clusters encontrados en 2D
ax3 = plt.subplot(2, 3, 3)
colores_clusters = ['red', 'green', 'blue']
for i in range(best_k):
    mask = y_kmeans == i
    ax3.scatter(X_pca[mask, 0], X_pca[mask, 1],
               label=f'Cluster {i}', c=colores_clusters[i],
               s=100, alpha=0.6, edgecolors='black')

# Plotear centroides
centroides_pca = pca.transform(kmeans.cluster_centers_)
ax3.scatter(centroides_pca[:, 0], centroides_pca[:, 1],
           c='yellow', marker='*', s=500, edgecolors='black',
           linewidths=2, label='Centroides')

ax3.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
ax3.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
ax3.set_title('Clusters K-Means en 2D (PCA)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Cultivares reales en 2D (para comparación)
ax4 = plt.subplot(2, 3, 4)
colores_cultivares = ['purple', 'orange', 'cyan']
for i, nombre in enumerate(target_names):
    mask = y_true == i
    ax4.scatter(X_pca[mask, 0], X_pca[mask, 1],
               label=nombre, c=colores_cultivares[i],
               s=100, alpha=0.6, edgecolors='black')

ax4.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
ax4.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
ax4.set_title('Cultivares Reales en 2D (para comparación)')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Plot 5: Top 6 características más importantes por cluster
ax5 = plt.subplot(2, 3, 5)
# Seleccionar las 6 características más importantes según varianza
feature_variance = np.var(X_scaled, axis=0)
top_6_indices = np.argsort(feature_variance)[-6:][::-1]
top_6_names = [feature_names[i].split('_')[0][:10] for i in top_6_indices]

cluster_means = []
for i in range(best_k):
    mask = y_kmeans == i
    cluster_means.append(X_scaled[mask][:, top_6_indices].mean(axis=0))

cluster_means = np.array(cluster_means)
x_pos = np.arange(len(top_6_names))
width = 0.25

for i in range(best_k):
    ax5.bar(x_pos + i * width, cluster_means[i],
           width, label=f'Cluster {i}', alpha=0.7,
           color=colores_clusters[i], edgecolor='black')

ax5.set_xticks(x_pos + width)
ax5.set_xticklabels(top_6_names, rotation=45, ha='right')
ax5.set_ylabel('Valor Medio (escalado)')
ax5.set_title('Top 6 Características por Cluster')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# Plot 6: Matriz de confusión (heatmap)
ax6 = plt.subplot(2, 3, 6)
confusion_matrix = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        confusion_matrix[i, j] = np.sum((y_true == i) & (y_kmeans == j))

im = ax6.imshow(confusion_matrix, cmap='Reds', aspect='auto')
ax6.set_xticks(range(3))
ax6.set_yticks(range(3))
ax6.set_xticklabels([f'Cluster {i}' for i in range(3)])
ax6.set_yticklabels(target_names)
ax6.set_xlabel('Cluster K-Means')
ax6.set_ylabel('Cultivar Real')
ax6.set_title('Matriz de Confusión: Real vs Clustering')

# Añadir valores en las celdas
for i in range(3):
    for j in range(3):
        text = ax6.text(j, i, int(confusion_matrix[i, j]),
                       ha="center", va="center",
                       color="white" if confusion_matrix[i, j] > 25 else "black",
                       fontsize=14, fontweight='bold')

plt.colorbar(im, ax=ax6, label='Número de vinos')

plt.suptitle('K-Means Clustering: Análisis del Dataset Wine',
            fontsize=14, y=0.995)
plt.tight_layout()
plt.show()

# Análisis de pureza de clusters
print("\n" + "=" * 70)
print("ANÁLISIS DE PUREZA DE CLUSTERS")
print("=" * 70)

for cluster in range(best_k):
    print(f"\nCluster {cluster}:")
    mask = y_kmeans == cluster
    cultivares_en_cluster = y_true[mask]
    for cultivar_idx, cultivar_nombre in enumerate(target_names):
        count = np.sum(cultivares_en_cluster == cultivar_idx)
        porcentaje = (count / len(cultivares_en_cluster)) * 100
        if count > 0:
            print(f"  {cultivar_nombre}: {count} vinos ({porcentaje:.1f}%)")

# Calcular pureza general
pureza_total = 0
for cluster in range(best_k):
    mask = y_kmeans == cluster
    cultivares_en_cluster = y_true[mask]
    cultivar_dominante = pd.Series(cultivares_en_cluster).mode()[0]
    pureza_cluster = np.sum(cultivares_en_cluster == cultivar_dominante) / len(cultivares_en_cluster)
    pureza_total += pureza_cluster * len(cultivares_en_cluster)

pureza_total /= len(y_true)
print(f"\nPureza total del clustering: {pureza_total:.2%}")
print("(Porcentaje de vinos asignados al cluster dominante de su cultivar)")

# Análisis adicional: características más discriminativas
print("\n" + "=" * 70)
print("CARACTERÍSTICAS MÁS DISCRIMINATIVAS")
print("=" * 70)
print("\nTop 5 características con mayor varianza entre clusters:")
cluster_centers = kmeans.cluster_centers_
feature_variance_between_clusters = np.var(cluster_centers, axis=0)
top_5_discriminative = np.argsort(feature_variance_between_clusters)[-5:][::-1]

for idx in top_5_discriminative:
    print(f"  {feature_names[idx]}: varianza = {feature_variance_between_clusters[idx]:.3f}")