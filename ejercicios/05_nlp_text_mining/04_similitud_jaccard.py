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
- Jaccard, P. (1912). The distribution of the flora in the alpine zone. New Phytologist, 11(2), 37-50.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.
- Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.
  (Disponible gratis: https://www.nltk.org/book/)
-------------------------
"""

# --- EJERCICIO 4: SIMILITUD DE TEXTO Y MAPAS DE CALOR ---

# --- CONTEXTO ---
# Objetivo: Aprender a cuantificar la similitud entre diferentes textos. Esto es fundamental para tareas
# como la detección de plagio, agrupación de documentos o sistemas de recomendación.
# Usaremos una métrica simple y muy intuitiva, la "Similitud de Jaccard", y visualizaremos
# nuestros resultados con un mapa de calor (heatmap) para una interpretación rápida.
#
# ¿Qué es la Similitud de Jaccard? Mide la similitud entre dos conjuntos (sets). Se define como
# el tamaño de la intersección dividido por el tamaño de la unión de los dos conjuntos.
# Jaccard = |A ∩ B| / |A ∪ B|. Un valor de 1 significa que los textos son idénticos (en términos de palabras únicas),
# y un valor de 0 significa que no tienen ninguna palabra en común.

# --- IMPORTACIONES ---
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- CORPUS Y STOPWORDS ---
# Corpus organizado por CATEGORÍAS TEMÁTICAS
# Esto permite observar patrones claros en el mapa de calor:
# - Documentos del mismo tema tendrán ALTA similitud (colores cálidos)
# - Documentos de temas diferentes tendrán BAJA similitud (colores fríos)

corpus = [
    # CATEGORÍA 1: FÚTBOL (índices 0-2)
    "El delantero anotó un gol espectacular en el partido de fútbol.",
    "El portero atajó el penalti y salvó al equipo de fútbol.",
    "El árbitro mostró tarjeta roja al defensa durante el partido.",

    # CATEGORÍA 2: TECNOLOGÍA (índices 3-5)
    "El procesador del computador tiene ocho núcleos de alto rendimiento.",
    "La memoria RAM del computador mejora el rendimiento del sistema.",
    "El disco duro almacena datos y programas en el computador.",

    # CATEGORÍA 3: COCINA (índices 6-8)
    "La receta de pasta italiana lleva tomate, albahaca y queso parmesano.",
    "Cocinar pasta requiere hervir agua con sal y aceite de oliva.",
    "El chef prepara pasta fresca con ingredientes naturales y frescos.",
]

# Etiquetas descriptivas para la visualización
etiquetas = [
    "Fútbol: Gol",
    "Fútbol: Portero",
    "Fútbol: Árbitro",
    "Tech: Procesador",
    "Tech: Memoria",
    "Tech: Disco",
    "Cocina: Receta",
    "Cocina: Hervir",
    "Cocina: Chef"
]

stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por',
    'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero',
    'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando',
    'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era',
    'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo',
    'qué', 'e', 'o', 'u', 'algunos', 'aspectos', 'tiene', 'lleva'
])

# --- PROCESAMIENTO ---

# 1. Preprocesamiento: Convertir cada frase en un conjunto de palabras limpias
def preprocess_to_set(frase, stopwords):
    """Limpia una frase y la convierte en un conjunto de palabras únicas."""
    frase_lower = frase.lower()
    words = re.findall(r'\b\w+\b', frase_lower)
    words_cleaned = [word for word in words if word not in stopwords]
    return set(words_cleaned)

print("Paso 1: Preprocesando cada documento del corpus en un conjunto de palabras...")
sets_de_palabras = [preprocess_to_set(frase, stopwords_es) for frase in corpus]

print("\n" + "-"*50)
print("CONJUNTOS DE PALABRAS POR CATEGORÍA:")
print("-"*50)
categorias = ["FÚTBOL", "TECNOLOGÍA", "COCINA"]
for cat_idx, categoria in enumerate(categorias):
    print(f"\n{categoria}:")
    for i in range(3):
        idx = cat_idx * 3 + i
        print(f"  Doc {idx} ({etiquetas[idx]}): {sets_de_palabras[idx]}")

# 2. Cálculo de la Similitud de Jaccard
def jaccard_similarity(set1, set2):
    """Calcula la similitud de Jaccard entre dos conjuntos."""
    interseccion = set1.intersection(set2)
    union = set1.union(set2)
    
    # Evitamos la división por cero si ambos conjuntos están vacíos
    if not union:
        return 1.0
    else:
        return len(interseccion) / len(union)

# 3. Creación de la Matriz de Similitud
# Esta matriz cuadrada nos dirá la similitud de cada frase con cada otra frase.
num_frases = len(corpus)
matriz_similitud = np.zeros((num_frases, num_frases))

print("\nPaso 2: Calculando la matriz de similitud... (Jaccard)")
for i in range(num_frases):
    for j in range(num_frases):
        similitud = jaccard_similarity(sets_de_palabras[i], sets_de_palabras[j])
        matriz_similitud[i, j] = similitud

print("Matriz de similitud calculada (primeras 5x5 filas/columnas):")
print(np.round(matriz_similitud[:5, :5], 2))

# --- VISUALIZACIÓN ---

print("\nGenerando visualizaciones...")

# Crear figura con múltiples subplots
fig = plt.figure(figsize=(16, 12))

# --- GRÁFICO 1: Mapa de calor triangular (matriz simétrica) ---
ax1 = fig.add_subplot(2, 2, 1)

# Crear máscara para mostrar solo el triángulo inferior
mask = np.triu(np.ones_like(matriz_similitud, dtype=bool), k=1)

sns.heatmap(matriz_similitud,
            mask=mask,
            annot=True,
            cmap='coolwarm',
            fmt=".2f",
            xticklabels=etiquetas,
            yticklabels=etiquetas,
            vmin=0, vmax=1,
            square=True,
            cbar_kws={'label': 'Similitud Jaccard'},
            ax=ax1)

ax1.set_title('Matriz de Similitud (Triangular)\nEvita redundancia por simetría', fontsize=11)
ax1.set_xticklabels(etiquetas, rotation=45, ha='right', fontsize=8)
ax1.set_yticklabels(etiquetas, rotation=0, fontsize=8)

# --- GRÁFICO 2: Similitud promedio por categoría (barras agrupadas) ---
ax2 = fig.add_subplot(2, 2, 2)

# Calcular similitud promedio intra-categoría y entre-categorías
categorias_nombres = ["Fútbol", "Tecnología", "Cocina"]
similitud_intra = []
similitud_inter = []

for cat_idx in range(3):
    inicio = cat_idx * 3
    fin = inicio + 3
    # Similitud dentro de la misma categoría (excluyendo diagonal)
    bloque = matriz_similitud[inicio:fin, inicio:fin]
    mask_diag = ~np.eye(3, dtype=bool)
    similitud_intra.append(bloque[mask_diag].mean())

    # Similitud con otras categorías
    otros_indices = [i for i in range(9) if i < inicio or i >= fin]
    similitud_inter.append(matriz_similitud[inicio:fin, otros_indices].mean())

x = np.arange(len(categorias_nombres))
width = 0.35

bars1 = ax2.bar(x - width/2, similitud_intra, width, label='Intra-categoría', color='#e74c3c')
bars2 = ax2.bar(x + width/2, similitud_inter, width, label='Inter-categoría', color='#3498db')

ax2.set_ylabel('Similitud Promedio')
ax2.set_title('Comparación: Similitud Intra vs Inter Categoría', fontsize=11)
ax2.set_xticks(x)
ax2.set_xticklabels(categorias_nombres)
ax2.legend()
ax2.set_ylim(0, 0.5)
ax2.axhline(y=np.mean(similitud_intra), color='#e74c3c', linestyle='--', alpha=0.5, label='Media intra')
ax2.axhline(y=np.mean(similitud_inter), color='#3498db', linestyle='--', alpha=0.5, label='Media inter')

# Agregar valores sobre las barras
for bar in bars1:
    ax2.annotate(f'{bar.get_height():.2f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax2.annotate(f'{bar.get_height():.2f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9)

# --- GRÁFICO 3: Distribución de similitudes (histograma) ---
ax3 = fig.add_subplot(2, 2, 3)

# Extraer valores del triángulo inferior (sin diagonal)
indices_tril = np.tril_indices(num_frases, k=-1)
similitudes_unicas = matriz_similitud[indices_tril]

# Separar similitudes intra e inter categoría
similitudes_intra_todas = []
similitudes_inter_todas = []

for i, j in zip(indices_tril[0], indices_tril[1]):
    cat_i = i // 3
    cat_j = j // 3
    if cat_i == cat_j:
        similitudes_intra_todas.append(matriz_similitud[i, j])
    else:
        similitudes_inter_todas.append(matriz_similitud[i, j])

ax3.hist(similitudes_intra_todas, bins=8, alpha=0.7, label='Misma categoría', color='#e74c3c', edgecolor='black')
ax3.hist(similitudes_inter_todas, bins=8, alpha=0.7, label='Diferente categoría', color='#3498db', edgecolor='black')
ax3.set_xlabel('Similitud de Jaccard')
ax3.set_ylabel('Frecuencia')
ax3.set_title('Distribución de Similitudes', fontsize=11)
ax3.legend()
ax3.axvline(x=np.mean(similitudes_intra_todas), color='#c0392b', linestyle='--', linewidth=2)
ax3.axvline(x=np.mean(similitudes_inter_todas), color='#2980b9', linestyle='--', linewidth=2)

# --- GRÁFICO 4: Clustermap / Dendrograma con mapa de calor ---
ax4 = fig.add_subplot(2, 2, 4)

# Mostrar las palabras compartidas entre documentos de alta similitud
# Encontrar los pares más similares (excluyendo diagonal)
pares_similitud = []
for i in range(num_frases):
    for j in range(i+1, num_frases):
        pares_similitud.append((i, j, matriz_similitud[i, j]))

pares_ordenados = sorted(pares_similitud, key=lambda x: x[2], reverse=True)[:6]

# Crear texto para mostrar
texto_pares = "TOP 6 PARES MÁS SIMILARES:\n" + "="*40 + "\n\n"
for idx, (i, j, sim) in enumerate(pares_ordenados, 1):
    palabras_comunes = sets_de_palabras[i].intersection(sets_de_palabras[j])
    texto_pares += f"{idx}. {etiquetas[i]} vs {etiquetas[j]}\n"
    texto_pares += f"   Similitud: {sim:.2f}\n"
    texto_pares += f"   Palabras comunes: {palabras_comunes if palabras_comunes else 'Ninguna'}\n\n"

ax4.text(0.05, 0.95, texto_pares, transform=ax4.transAxes, fontsize=9,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax4.axis('off')
ax4.set_title('Análisis de Pares con Mayor Similitud', fontsize=11)

# Guardar la figura principal
plt.suptitle('Análisis Completo de Similitud de Jaccard\n(Corpus temático: Fútbol, Tecnología, Cocina)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('analisis_jaccard_completo.png', dpi=300, bbox_inches='tight')
plt.show()

# --- GRÁFICO ADICIONAL: Clustermap con dendrograma ---
print("\nGenerando clustermap con dendrograma...")
g = sns.clustermap(matriz_similitud,
                   annot=True,
                   cmap='coolwarm',
                   fmt=".2f",
                   xticklabels=etiquetas,
                   yticklabels=etiquetas,
                   figsize=(10, 8),
                   dendrogram_ratio=0.15,
                   cbar_pos=(0.02, 0.8, 0.03, 0.15))
g.figure.suptitle('Clustermap: Agrupación Jerárquica por Similitud', fontsize=12, y=1.02)
plt.savefig('clustermap_ejercicio.png', dpi=300, bbox_inches='tight')
plt.show()

# --- ANÁLISIS DIDÁCTICO ---
print("\n--- FIN DEL EJERCICIO 4 ---")
print("\n" + "="*70)
print("ANÁLISIS DIDÁCTICO DEL CORPUS TEMÁTICO")
print("="*70)
print("""
ESTRUCTURA DEL CORPUS:
  - Documentos 0-2: FÚTBOL (partido, gol, portero, árbitro)
  - Documentos 3-5: TECNOLOGÍA (procesador, memoria, disco, computador)
  - Documentos 6-8: COCINA (pasta, receta, chef, ingredientes)

QUÉ OBSERVAR EN EL MAPA DE CALOR:
  1. BLOQUES DIAGONALES: Los cuadros 3x3 en la diagonal muestran
     mayor similitud (colores cálidos) porque pertenecen al mismo tema.

  2. FUERA DE LOS BLOQUES: Los valores son más bajos (colores fríos)
     porque documentos de diferentes temas comparten pocas palabras.

  3. DIAGONAL PRINCIPAL: Siempre es 1.0 (rojo intenso) porque cada
     documento es idéntico a sí mismo.

APLICACIONES PRÁCTICAS:
  - Agrupación automática de documentos (clustering)
  - Detección de plagio
  - Sistemas de recomendación de contenido
  - Clasificación de textos por tema
""")
