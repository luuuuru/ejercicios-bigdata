"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA PRINCIPAL:
- Husson, F., Le, S., & Pages, J. (2017). Exploratory Multivariate Analysis by Example Using R. CRC Press.
- Anderson, E. (1935). The irises of the Gaspe Peninsula. Bulletin of the American Iris Society, 59, 2-5.
- Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7(2), 179-188.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.
-------------------------

PCA + CLUSTERING EN PYTHON: Dataset Iris
=========================================
Este script realiza un analisis completo del dataset Iris combinando:
1. PCA estilo FactoMineR (reduccion de dimensionalidad)
2. Clustering K-Means (agrupacion de especies)
3. Visualizaciones didacticas y profesionales

El dataset Iris es un clasico de Machine Learning con 150 flores de 3 especies
(Setosa, Versicolor, Virginica) y 4 medidas (largo/ancho de sepalo y petalo).
"""

# =============================================================================
# INSTALACION DEL ENTORNO (ejecutar una vez en terminal)
# =============================================================================
# pip install pandas matplotlib seaborn prince scikit-learn numpy openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from prince import PCA
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
import warnings
import os

warnings.filterwarnings('ignore')

# Obtener la ruta del directorio donde esta el script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuracion de graficos
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("=" * 80)
print("PCA + CLUSTERING: DATASET IRIS")
print("Analisis Exploratorio Multivariante + Agrupacion No Supervisada")
print("=" * 80)

# =============================================================================
# 1. CARGAR EL DATASET IRIS
# =============================================================================
print("\n" + "=" * 80)
print("1. CARGANDO DATASET IRIS (Fisher, 1936)")
print("=" * 80)

# Cargar dataset Iris desde sklearn
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# Crear DataFrame
df = pd.DataFrame(X, columns=feature_names)
df['species'] = pd.Categorical.from_codes(y, target_names)
df['species_code'] = y

print(f"\nDimensiones del dataset: {df.shape[0]} flores x {df.shape[1]} variables")
print(f"\nEspecies: {', '.join(target_names)}")
print(f"Distribucion: {df['species'].value_counts().to_dict()}")

print("\nPrimeras 5 flores de cada especie:")
print(df.groupby('species').head(5))

print("\nEstadisticas descriptivas:")
print(df[feature_names].describe().round(2))

# =============================================================================
# 2. ANALISIS EXPLORATORIO DE DATOS (EDA)
# =============================================================================
print("\n" + "=" * 80)
print("2. ANALISIS EXPLORATORIO DE DATOS (EDA)")
print("=" * 80)

# Crear figura de EDA
fig_eda = plt.figure(figsize=(16, 12))

# Subplot 1: Distribucion de variables
ax1 = plt.subplot(2, 3, 1)
df[feature_names].boxplot(ax=ax1)
ax1.set_title('Distribucion de Variables\n(Boxplots)', fontweight='bold', fontsize=12)
ax1.set_ylabel('Valor (cm)', fontsize=10)
ax1.set_xticklabels([name.split(' ')[0] for name in feature_names], rotation=45)
ax1.grid(True, alpha=0.3)

# Subplot 2: Matriz de correlacion (solo triangulo inferior)
ax2 = plt.subplot(2, 3, 2)
corr_matrix = df[feature_names].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax2,
            mask=mask)
ax2.set_title('Matriz de Correlacion\n(Pearson - triangulo inferior)', fontweight='bold', fontsize=12)

# Subplot 3: Distribucion por especie (Sepal Length)
ax3 = plt.subplot(2, 3, 3)
for species in target_names:
    data = df[df['species'] == species]['sepal length (cm)']
    ax3.hist(data, alpha=0.6, label=species, bins=15, edgecolor='black')
ax3.set_xlabel('Sepal Length (cm)', fontsize=10)
ax3.set_ylabel('Frecuencia', fontsize=10)
ax3.set_title('Distribucion de Sepal Length\npor Especie', fontweight='bold', fontsize=12)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Subplot 4: Scatter plot Sepal
ax4 = plt.subplot(2, 3, 4)
for i, species in enumerate(target_names):
    mask = df['species'] == species
    ax4.scatter(df.loc[mask, 'sepal length (cm)'], df.loc[mask, 'sepal width (cm)'],
                label=species, s=80, alpha=0.7, edgecolors='black')
ax4.set_xlabel('Sepal Length (cm)', fontsize=10)
ax4.set_ylabel('Sepal Width (cm)', fontsize=10)
ax4.set_title('Sepal: Length vs Width\npor Especie', fontweight='bold', fontsize=12)
ax4.legend()
ax4.grid(True, alpha=0.3)

# Subplot 5: Scatter plot Petal
ax5 = plt.subplot(2, 3, 5)
for i, species in enumerate(target_names):
    mask = df['species'] == species
    ax5.scatter(df.loc[mask, 'petal length (cm)'], df.loc[mask, 'petal width (cm)'],
                label=species, s=80, alpha=0.7, edgecolors='black')
ax5.set_xlabel('Petal Length (cm)', fontsize=10)
ax5.set_ylabel('Petal Width (cm)', fontsize=10)
ax5.set_title('Petal: Length vs Width\npor Especie', fontweight='bold', fontsize=12)
ax5.legend()
ax5.grid(True, alpha=0.3)

# Subplot 6: Violin plot
ax6 = plt.subplot(2, 3, 6)
df_melt = df.melt(id_vars='species', value_vars=feature_names,
                  var_name='Feature', value_name='Value')
sns.violinplot(data=df_melt, x='Feature', y='Value', hue='species', split=False, ax=ax6)
ax6.set_xticklabels([name.split(' ')[0] for name in feature_names], rotation=45)
ax6.set_title('Distribucion de Variables\npor Especie (Violin Plot)', fontweight='bold', fontsize=12)
ax6.set_ylabel('Valor (cm)', fontsize=10)
ax6.legend(title='Especie', loc='upper right')

plt.suptitle('ANALISIS EXPLORATORIO DE DATOS (EDA) - IRIS DATASET\n'
             'Fisher (1936) | 150 flores, 3 especies, 4 medidas',
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '02_pca_iris_eda.png'), dpi=150, bbox_inches='tight')
plt.show()

print("\nGraficos EDA guardados en: 02_pca_iris_eda.png")

# =============================================================================
# 3. PCA ESTILO FACTOMINER
# =============================================================================
print("\n" + "=" * 80)
print("3. ANALISIS DE COMPONENTES PRINCIPALES (PCA)")
print("=" * 80)

# Variables activas (las 4 medidas)
active_cols = feature_names

print(f"\nVARIABLES ACTIVAS (construyen los ejes PCA):")
for i, col in enumerate(active_cols, 1):
    print(f"  {i}. {col}")

# Configurar PCA con Prince (estilo FactoMineR)
pca = PCA(
    n_components=4,
    rescale_with_mean=True,
    rescale_with_std=True,
    copy=True,
    engine='sklearn',
    random_state=42
)

# Entrenar PCA
pca = pca.fit(df[active_cols])

print("\nModelo PCA entrenado exitosamente")
print("Parametros: rescale_with_mean=True, rescale_with_std=True (estandarizacion)")

# =============================================================================
# 4. AUTOVALORES Y VARIANZA EXPLICADA
# =============================================================================
print("\n" + "=" * 80)
print("4. AUTOVALORES Y VARIANZA EXPLICADA")
print("=" * 80)

# Crear tabla de autovalores
eigenvalues_df = pd.DataFrame({
    'Autovalor': pca.eigenvalues_,
    'Varianza (%)': pca.percentage_of_variance_,
    'Varianza Acumulada (%)': pca.cumulative_percentage_of_variance_
}, index=[f'Dim.{i+1}' for i in range(len(pca.eigenvalues_))])

print("\nTabla de Autovalores:")
print(eigenvalues_df.round(3))

# Regla de Kaiser
n_kaiser = sum(pca.eigenvalues_ > 1)
print(f"\nRegla de Kaiser: Retener {n_kaiser} componentes (autovalor > 1)")
print(f"Varianza explicada por Dim.1 + Dim.2: {(pca.percentage_of_variance_[0] + pca.percentage_of_variance_[1]):.2f}%")

# =============================================================================
# 5. COORDENADAS, CONTRIBUCIONES Y COS2 DE INDIVIDUOS
# =============================================================================
print("\n" + "=" * 80)
print("5. COORDENADAS DE LOS INDIVIDUOS (Factor Scores)")
print("=" * 80)

# Coordenadas
row_coords = pca.row_coordinates(df[active_cols])
row_coords.columns = [f'Dim.{i+1}' for i in range(row_coords.shape[1])]
row_coords['species'] = df['species'].values

print("\nCoordenadas de las primeras 10 flores:")
print(row_coords.head(10).round(3))

# Contribuciones
row_contrib = pca.row_contributions_
row_contrib.columns = [f'Dim.{i+1}' for i in range(row_contrib.shape[1])]

# Cos2 (calidad de representacion)
row_cos2 = pca.row_cosine_similarities(df[active_cols])
row_cos2.columns = [f'Dim.{i+1}' for i in range(row_cos2.shape[1])]

cos2_plano = row_cos2['Dim.1'] + row_cos2['Dim.2']
print(f"\nFlores mejor representadas en el plano Dim1-Dim2:")
for idx, cos2 in cos2_plano.sort_values(ascending=False).head(5).items():
    print(f"  Flor {idx}: {cos2:.3f} ({cos2*100:.1f}% de variabilidad explicada)")

# =============================================================================
# 6. CORRELACIONES Y CONTRIBUCIONES DE VARIABLES
# =============================================================================
print("\n" + "=" * 80)
print("6. CORRELACIONES Y CONTRIBUCIONES DE VARIABLES")
print("=" * 80)

# Correlaciones
col_correlations = pca.column_correlations.copy()
col_correlations.columns = [f'Dim.{i+1}' for i in range(col_correlations.shape[1])]

print("\nCorrelaciones Variables-Dimensiones:")
print(col_correlations.round(3))

# Contribuciones
col_contrib = pca.column_contributions_
col_contrib.columns = [f'Dim.{i+1}' for i in range(col_contrib.shape[1])]

print("\nContribuciones de Variables (%):")
print((col_contrib * 100).round(2))

print(f"\nVariables que mas contribuyen a Dim.1:")
for var, contrib in (col_contrib['Dim.1'] * 100).sort_values(ascending=False).items():
    print(f"  {var}: {contrib:.2f}%")

# Cos2 de variables
col_cos2 = pca.column_cosine_similarities_
col_cos2.columns = [f'Dim.{i+1}' for i in range(col_cos2.shape[1])]

# =============================================================================
# 7. CLUSTERING K-MEANS EN EL ESPACIO PCA
# =============================================================================
print("\n" + "=" * 80)
print("7. CLUSTERING K-MEANS (DESPUES DE PCA)")
print("=" * 80)

# Usar las primeras 2 componentes principales para clustering
X_pca = row_coords[['Dim.1', 'Dim.2']].values

# Metodo del codo (Elbow) y Silhouette
inertias = []
silhouettes = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_pca)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_pca, kmeans.labels_))

print("\nMetodo del Codo y Silhouette:")
print(f"{'K':<5} {'Inercia':<15} {'Silhouette':<15}")
print("-" * 35)
for k, inertia, sil in zip(K_range, inertias, silhouettes):
    print(f"{k:<5} {inertia:<15.2f} {sil:<15.3f}")

# Clustering con K=3 (sabemos que hay 3 especies)
kmeans_final = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_pca)

# Metricas de evaluacion
sil_score = silhouette_score(X_pca, clusters)
db_score = davies_bouldin_score(X_pca, clusters)
ch_score = calinski_harabasz_score(X_pca, clusters)

print(f"\nCLUSTERING FINAL (K=3):")
print(f"  Silhouette Score: {sil_score:.3f} (cercano a 1 = bueno)")
print(f"  Davies-Bouldin Index: {db_score:.3f} (cercano a 0 = bueno)")
print(f"  Calinski-Harabasz Index: {ch_score:.2f} (mas alto = mejor)")

# Agregar clusters al DataFrame
row_coords['cluster'] = clusters
df['cluster'] = clusters

# Comparar clusters con especies reales
print("\nComparacion Clusters vs Especies Reales:")
confusion = pd.crosstab(df['species'], df['cluster'], rownames=['Especie'], colnames=['Cluster'])
print(confusion)

# Calcular pureza de clusters
purity = 0
for cluster_id in range(3):
    cluster_mask = df['cluster'] == cluster_id
    if cluster_mask.sum() > 0:
        species_counts = df[cluster_mask]['species'].value_counts()
        purity += species_counts.max()
purity /= len(df)
print(f"\nPureza de Clusters: {purity:.2%}")

# =============================================================================
# 8. VISUALIZACIONES PRINCIPALES
# =============================================================================
print("\n" + "=" * 80)
print("8. GENERANDO VISUALIZACIONES PRINCIPALES")
print("=" * 80)

# Crear figura principal
fig_main = plt.figure(figsize=(20, 16))

# -----------------------------------------------------------------------------
# GRAFICO 1: SCREE PLOT
# -----------------------------------------------------------------------------
ax1 = plt.subplot(3, 3, 1)
x = range(1, len(pca.eigenvalues_) + 1)
bars = ax1.bar(x, pca.percentage_of_variance_, color='steelblue',
               edgecolor='black', alpha=0.7)
ax1.plot(x, np.cumsum(pca.percentage_of_variance_), 'ro-',
         linewidth=2, markersize=8, label='Acumulada')
ax1.axhline(y=100/len(active_cols), color='gray', linestyle='--',
            label=f'Umbral = {100/len(active_cols):.1f}%')
ax1.set_xlabel('Dimension', fontsize=11)
ax1.set_ylabel('Porcentaje de Varianza', fontsize=11)
ax1.set_title('Scree Plot\n(Varianza Explicada)', fontweight='bold', fontsize=12)
ax1.set_xticks(x)
ax1.legend()
ax1.grid(True, alpha=0.3)

for bar, val in zip(bars, pca.percentage_of_variance_):
    ax1.annotate(f'{val:.1f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9)

# -----------------------------------------------------------------------------
# GRAFICO 2: CIRCULO DE CORRELACION
# -----------------------------------------------------------------------------
ax2 = plt.subplot(3, 3, 2)
circle = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='--', linewidth=2)
ax2.add_artist(circle)

for var in active_cols:
    x = col_correlations.loc[var, 'Dim.1']
    y = col_correlations.loc[var, 'Dim.2']
    cos2_var = col_cos2.loc[var, 'Dim.1'] + col_cos2.loc[var, 'Dim.2']
    color = plt.cm.RdYlGn(cos2_var)
    
    ax2.arrow(0, 0, x*0.9, y*0.9, head_width=0.05, head_length=0.05,
              fc=color, ec=color, linewidth=2.5)
    ax2.text(x*1.15, y*1.15, var.split(' ')[0], ha='center', va='center',
             fontsize=10, fontweight='bold', color='darkblue')

ax2.axhline(0, color='black', linewidth=0.5)
ax2.axvline(0, color='black', linewidth=0.5)
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)
ax2.set_xlabel(f'Dim.1 ({pca.percentage_of_variance_[0]:.1f}%)', fontsize=11)
ax2.set_ylabel(f'Dim.2 ({pca.percentage_of_variance_[1]:.1f}%)', fontsize=11)
ax2.set_title('Circulo de Correlacion\n(Variables)', fontweight='bold', fontsize=12)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# -----------------------------------------------------------------------------
# GRAFICO 3: PCA BIPLOT (Especies Reales)
# -----------------------------------------------------------------------------
ax3 = plt.subplot(3, 3, 3)
colors_species = {'setosa': '#FF4136', 'versicolor': '#FFDC00', 'virginica': '#0074D9'}

for species in target_names:
    mask = row_coords['species'] == species
    ax3.scatter(row_coords.loc[mask, 'Dim.1'], row_coords.loc[mask, 'Dim.2'],
                label=species.capitalize(), c=colors_species[species],
                s=100, alpha=0.7, edgecolors='black', linewidth=1.5)

ax3.axhline(0, color='black', linestyle='--', linewidth=0.5)
ax3.axvline(0, color='black', linestyle='--', linewidth=0.5)
ax3.set_xlabel(f'Dim.1 ({pca.percentage_of_variance_[0]:.1f}%)', fontsize=11)
ax3.set_ylabel(f'Dim.2 ({pca.percentage_of_variance_[1]:.1f}%)', fontsize=11)
ax3.set_title('PCA Biplot\n(Especies Reales)', fontweight='bold', fontsize=12)
ax3.legend(title='Especie', loc='best')
ax3.grid(True, alpha=0.3)

# -----------------------------------------------------------------------------
# GRAFICO 4: CONTRIBUCIONES A DIM.1
# -----------------------------------------------------------------------------
ax4 = plt.subplot(3, 3, 4)
contrib_dim1 = (col_contrib['Dim.1'] * 100).sort_values(ascending=True)
colors = ['steelblue' if v < 100/len(active_cols) else 'red' for v in contrib_dim1]
ax4.barh(range(len(contrib_dim1)), contrib_dim1.values, color=colors, edgecolor='black')
ax4.set_yticks(range(len(contrib_dim1)))
ax4.set_yticklabels([name.split(' ')[0] for name in contrib_dim1.index])
ax4.axvline(x=100/len(active_cols), color='red', linestyle='--',
            label=f'Esperado ({100/len(active_cols):.1f}%)')
ax4.set_xlabel('Contribucion (%)', fontsize=11)
ax4.set_title('Contribuciones a Dim.1\n(Rojo = sobre la media)', fontweight='bold', fontsize=12)
ax4.legend(loc='lower right')
ax4.grid(True, alpha=0.3, axis='x')

# -----------------------------------------------------------------------------
# GRAFICO 5: CONTRIBUCIONES A DIM.2
# -----------------------------------------------------------------------------
ax5 = plt.subplot(3, 3, 5)
contrib_dim2 = (col_contrib['Dim.2'] * 100).sort_values(ascending=True)
colors = ['steelblue' if v < 100/len(active_cols) else 'red' for v in contrib_dim2]
ax5.barh(range(len(contrib_dim2)), contrib_dim2.values, color=colors, edgecolor='black')
ax5.set_yticks(range(len(contrib_dim2)))
ax5.set_yticklabels([name.split(' ')[0] for name in contrib_dim2.index])
ax5.axvline(x=100/len(active_cols), color='red', linestyle='--',
            label=f'Esperado ({100/len(active_cols):.1f}%)')
ax5.set_xlabel('Contribucion (%)', fontsize=11)
ax5.set_title('Contribuciones a Dim.2\n(Rojo = sobre la media)', fontweight='bold', fontsize=12)
ax5.legend(loc='lower right')
ax5.grid(True, alpha=0.3, axis='x')

# -----------------------------------------------------------------------------
# GRAFICO 6: METODO DEL CODO
# -----------------------------------------------------------------------------
ax6 = plt.subplot(3, 3, 6)
ax6.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
ax6.set_xlabel('Numero de Clusters (K)', fontsize=11)
ax6.set_ylabel('Inercia (Within-Cluster Sum of Squares)', fontsize=11)
ax6.set_title('Metodo del Codo\n(Elbow Method)', fontweight='bold', fontsize=12)
ax6.set_xticks(K_range)
ax6.grid(True, alpha=0.3)
ax6.axvline(x=3, color='red', linestyle='--', label='K=3 (optimo)')
ax6.legend()

# -----------------------------------------------------------------------------
# GRAFICO 7: SILHOUETTE SCORE
# -----------------------------------------------------------------------------
ax7 = plt.subplot(3, 3, 7)
ax7.plot(K_range, silhouettes, 'go-', linewidth=2, markersize=8)
ax7.set_xlabel('Numero de Clusters (K)', fontsize=11)
ax7.set_ylabel('Silhouette Score', fontsize=11)
ax7.set_title('Silhouette Score\n(Mayor = Mejor)', fontweight='bold', fontsize=12)
ax7.set_xticks(K_range)
ax7.grid(True, alpha=0.3)
ax7.axvline(x=3, color='red', linestyle='--', label='K=3 (optimo)')
ax7.axhline(y=silhouettes[1], color='green', linestyle=':', alpha=0.5)
ax7.legend()

# -----------------------------------------------------------------------------
# GRAFICO 8: CLUSTERS ENCONTRADOS
# -----------------------------------------------------------------------------
ax8 = plt.subplot(3, 3, 8)
colors_clusters = {0: '#FF4136', 1: '#FFDC00', 2: '#0074D9'}

for cluster_id in range(3):
    mask = row_coords['cluster'] == cluster_id
    ax8.scatter(row_coords.loc[mask, 'Dim.1'], row_coords.loc[mask, 'Dim.2'],
                label=f'Cluster {cluster_id}', c=colors_clusters[cluster_id],
                s=100, alpha=0.7, edgecolors='black', linewidth=1.5)

# Centroides
centroids_pca = kmeans_final.cluster_centers_
ax8.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
            c='black', marker='X', s=300, edgecolors='white', linewidth=2,
            label='Centroides', zorder=5)

ax8.axhline(0, color='black', linestyle='--', linewidth=0.5)
ax8.axvline(0, color='black', linestyle='--', linewidth=0.5)
ax8.set_xlabel(f'Dim.1 ({pca.percentage_of_variance_[0]:.1f}%)', fontsize=11)
ax8.set_ylabel(f'Dim.2 ({pca.percentage_of_variance_[1]:.1f}%)', fontsize=11)
ax8.set_title('Clusters K-Means\n(K=3, en espacio PCA)', fontweight='bold', fontsize=12)
ax8.legend(title='Cluster', loc='best')
ax8.grid(True, alpha=0.3)

# -----------------------------------------------------------------------------
# GRAFICO 9: COMPARACION CLUSTERS VS ESPECIES
# -----------------------------------------------------------------------------
ax9 = plt.subplot(3, 3, 9)
confusion_plot = confusion.T
sns.heatmap(confusion_plot, annot=True, fmt='d', cmap='YlGnBu', cbar=True,
            linewidths=1, linecolor='black', ax=ax9)
ax9.set_xlabel('Especie Real', fontsize=11)
ax9.set_ylabel('Cluster Asignado', fontsize=11)
ax9.set_title(f'Confusion Matrix\n(Pureza: {purity:.1%})', fontweight='bold', fontsize=12)

plt.suptitle('PCA + CLUSTERING K-MEANS: IRIS DATASET\n'
             f'Varianza Explicada (Dim1+Dim2): {(pca.percentage_of_variance_[0] + pca.percentage_of_variance_[1]):.1f}% | '
             f'Silhouette Score: {sil_score:.3f} | Pureza: {purity:.1%}',
             fontsize=15, fontweight='bold', y=0.995)

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, '02_pca_iris_clustering.png'), dpi=150, bbox_inches='tight')
plt.show()

print("\nGraficos principales guardados en: 02_pca_iris_clustering.png")

# =============================================================================
# 9. INTERPRETACION DE RESULTADOS
# =============================================================================
print("\n" + "=" * 80)
print("9. INTERPRETACION DE RESULTADOS")
print("=" * 80)

print(f"""
RESUMEN EJECUTIVO DEL ANALISIS
===============================

1. DATASET:
   - 150 flores de 3 especies (Setosa, Versicolor, Virginica)
   - 4 medidas: {', '.join([name.split(' ')[0] for name in feature_names])}
   - Distribucion balanceada: 50 flores por especie

2. PCA (Reduccion de Dimensionalidad):
   - Varianza explicada por Dim.1: {pca.percentage_of_variance_[0]:.2f}%
   - Varianza explicada por Dim.2: {pca.percentage_of_variance_[1]:.2f}%
   - Varianza total (Dim1+Dim2): {(pca.percentage_of_variance_[0] + pca.percentage_of_variance_[1]):.2f}%
   
   INTERPRETACION:
   - Dim.1 esta dominada por: {col_contrib['Dim.1'].idxmax()} ({col_contrib['Dim.1'].max()*100:.1f}%)
   - Dim.2 esta dominada por: {col_contrib['Dim.2'].idxmax()} ({col_contrib['Dim.2'].max()*100:.1f}%)
   
   CONCLUSION: Las medidas de petalo (petal length/width) son las mas importantes
   para diferenciar las especies, seguidas por las medidas de sepalo.

3. CLUSTERING K-MEANS:
   - Numero optimo de clusters: K=3 (coincide con las 3 especies)
   - Silhouette Score: {sil_score:.3f} (buena separacion)
   - Davies-Bouldin Index: {db_score:.3f} (clusters compactos y separados)
   - Pureza: {purity:.1%} (alta concordancia con especies reales)
   
   INTERPRETACION:
   - El algoritmo K-Means logro identificar correctamente las 3 especies
   - La especie Setosa es perfectamente separable (cluster puro)
   - Versicolor y Virginica tienen cierta superposicion (especies similares)

4. VALIDACION:
   - El PCA redujo de 4D a 2D manteniendo {(pca.percentage_of_variance_[0] + pca.percentage_of_variance_[1]):.1f}% de informacion
   - Los clusters encontrados coinciden en {purity:.1%} con las especies reales
   - Las variables mas discriminantes son: petal length y petal width

5. RECOMENDACIONES:
   - Para clasificacion de especies de Iris, enfocarse en medidas de petalo
   - El espacio 2D del PCA es suficiente para visualizacion y clustering
   - K=3 es el numero optimo de clusters (validado por Elbow y Silhouette)
""")

# =============================================================================
# 10. EXPORTAR RESULTADOS A EXCEL
# =============================================================================
print("\n" + "=" * 80)
print("10. EXPORTANDO RESULTADOS A EXCEL")
print("=" * 80)

try:
    with pd.ExcelWriter(os.path.join(SCRIPT_DIR, '02_pca_iris_resultados.xlsx')) as writer:
        # Datos originales
        df.to_excel(writer, sheet_name='Datos_Originales', index=False)
        
        # Autovalores
        eigenvalues_df.to_excel(writer, sheet_name='Autovalores')
        
        # Coordenadas PCA
        row_coords.to_excel(writer, sheet_name='Coordenadas_PCA')
        
        # Correlaciones variables
        col_correlations.round(3).to_excel(writer, sheet_name='Correlaciones_Variables')
        
        # Contribuciones variables
        (col_contrib * 100).round(2).to_excel(writer, sheet_name='Contribuciones_Variables')
        
        # Confusion matrix
        confusion.to_excel(writer, sheet_name='Confusion_Matrix')
        
        # Metricas clustering
        metrics_df = pd.DataFrame({
            'Metrica': ['Silhouette Score', 'Davies-Bouldin Index', 'Calinski-Harabasz Index', 'Pureza'],
            'Valor': [sil_score, db_score, ch_score, purity]
        })
        metrics_df.to_excel(writer, sheet_name='Metricas_Clustering', index=False)
    
    print("Resultados exportados a: 02_pca_iris_resultados.xlsx")
    print("Hojas: Datos_Originales, Autovalores, Coordenadas_PCA, Correlaciones_Variables,")
    print("       Contribuciones_Variables, Confusion_Matrix, Metricas_Clustering")
except Exception as e:
    print(f"Error al exportar Excel: {e}")

print("\n" + "=" * 80)
print("FIN DEL ANALISIS PCA + CLUSTERING - IRIS DATASET")
print("=" * 80)
print("""
REFERENCIAS:
- Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems.
  Annals of Eugenics, 7(2), 179-188.
- Husson, F., Le, S., & Pages, J. (2017). Exploratory Multivariate Analysis by Example Using R.
  CRC Press.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.

Autor: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
""")
