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

# --- DOCUMENTACIÓN Y REFERENCIAS NLP ---
# 1. PROCESAMIENTO DE TEXTO (RE): https://docs.python.org/3/library/re.html
# 2. VISUALIZACIÓN (MATPLOTLIB): https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html
# 3. REFERENCIAS ACADÉMICAS:
#    - Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.
#    - Hutto, C. J., & Gilbert, E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis.
#    - Spanish Sentiment Lexicon (SEL): http://timmynlp.com/resources/SEL_Spanish/

# --- EJERCICIO 1: LA ANATOMÍA DEL TEXTO Y VISUALIZACIÓN DE FRECUENCIAS ---

# --- CONTEXTO ---
# Objetivo: Aprender el primer paso fundamental en cualquier tarea de NLP: convertir texto no estructurado
# en datos cuantitativos (frecuencias) y visualizar estos datos para obtener una primera impresión del contenido.
#
# Nuestra "Base de Datos":
# Ahora cargaremos un archivo de texto externo ('pistolon.txt') para analizar un texto más extenso y real.

# --- IMPORTACIONES --- 
# Importamos las herramientas que necesitaremos.

import re
import os
from collections import Counter
import matplotlib.pyplot as plt

# --- NUESTRO CORPUS (BASE DE DATOS DE TEXTO) ---

# CORPUS ANTERIOR (COMENTADO PARA REFERENCIA)
# corpus = ["""The wall on which the prophets wrote
# Is cracking at the seams
# Upon the instruments of death
# The sunlight brightly gleams
# When every man is torn apart
# With nightmares and with dreams
# Will no one lay the laurel wreath
# When silence drowns the screams
# Confusion will be my epitaph
# As I crawl a cracked and broken path
# If we make it we can all sit back and laugh
# But I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Between the iron gates of fate
# The seeds of time were sown
# And watered by the deeds of those
# Who know and who are known
# Knowledge is a deadly friend
# If no one sets the rules
# The fate of all mankind I see
# Is in the hands of fools
# The wall on which the prophets wrote
# Is cracking at the seams
# Upon the instruments of death
# The sunlight brightly gleams
# When every man is torn apart
# With nightmares and with dreams
# Will no one lay the laurel wreath
# When silence drowns the screams?
# Confusion will be my epitaph
# As I crawl a cracked and broken path
# If we make it we can all sit back and laugh
# But I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Crying
# Crying
# Yes, I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Yes, I fear tomorrow I'll be crying
# Crying"""]

# NUEVO CORPUS: Carga desde archivo 'pistolon.txt'
# Usamos os.path para asegurar que encuentra el archivo en la misma carpeta que este script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'pistolon.txt')

print(f"Intentando cargar archivo desde: {file_path}")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        texto_archivo = f.read()
        # Lo metemos en una lista para mantener la compatibilidad con el código original
        corpus = [texto_archivo]
    print("✓ Archivo cargado exitosamente.")
except FileNotFoundError:
    print("ERROR: No se encontró 'pistolon.txt'. Asegúrate de que el archivo esté en la misma carpeta.")
    corpus = [""] # Corpus vacío para evitar crash

# --- PROCESAMIENTO ---

# 1. Unificar todo el texto
# Para analizar la frecuencia en todo el corpus, primero unimos todas las frases en un único bloque de texto.
print("Paso 1: Unificando el corpus en un solo bloque de texto...")
all_text = ' '.join(corpus)
# Mostramos solo los primeros 100 caracteres para no saturar la consola
print(f"Texto completo (inicio): '{all_text[:100]}...'")

# 2. Normalización: Convertir a minúsculas
# Esto es crucial para que palabras como "Fantástico" y "fantástico" se cuenten como una sola.
print("\nPaso 2: Normalizando el texto a minúsculas...")
all_text_lower = all_text.lower()
print(f"Texto normalizado (inicio): '{all_text_lower[:100]}...'")

# 3. Tokenización: Dividir el texto en palabras (tokens)
# Usamos una expresión regular `\b\w+\b` que es más robusta que un simple `.split()`.
# `\b` asegura que solo cojamos palabras completas, ignorando signos de puntuación como comas o puntos.
print("\nPaso 3: Tokenizando el texto en palabras...")
words = re.findall(r'\b\w+\b', all_text_lower)
print(f"Primeras 20 palabras (tokens): {words[:20]}")

# 4. Conteo de Frecuencias
# `collections.Counter` es una herramienta de Python extremadamente eficiente para contar la frecuencia de elementos en una lista.
print("\nPaso 4: Contando la frecuencia de cada palabra...")
word_counts = Counter(words)

# `most_common(10)` nos da una lista de las 10 tuplas (palabra, frecuencia) más comunes.
top_10_words = word_counts.most_common(10)

# Calculamos estadísticas básicas
total_words = len(words)
unique_words = len(word_counts)

print("\n--- RESULTADOS DEL ANÁLISIS DE FRECUENCIA ---")
print(f"Total de palabras (tokens): {total_words}")
print(f"Vocabulario único: {unique_words}")
print("\nTop 10 palabras más frecuentes (antes de la limpieza):")
for word, count in top_10_words:
    print(f"- '{word}': {count} veces")

# --- VISUALIZACIÓN ---
# Un análisis no está completo si no podemos comunicarlo visualmente.

print("\nGenerando gráfico de barras... (una ventana nueva debería aparecer)")

if total_words > 0:
    # Desempaquetamos las palabras y sus conteos en dos listas separadas para el gráfico.
    words_for_plot, counts_for_plot = zip(*top_10_words)

    # Creamos la figura y los ejes para el gráfico.
    plt.figure(figsize=(12, 7))
    plt.bar(words_for_plot, counts_for_plot, color='skyblue')

    # Añadimos títulos y etiquetas para que el gráfico sea legible.
    plt.title(f'Top 10 Palabras Más Frecuentes (Total: {total_words} palabras)')
    plt.xlabel('Palabras')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45, ha="right") # Rotamos las etiquetas para que no se solapen
    plt.tight_layout() # Ajusta el gráfico para que todo quepa bien

    # Mostramos el gráfico. Esto abrirá una nueva ventana.
    plt.savefig('conteo_palabras_top10.png', dpi=300, bbox_inches='tight')
    plt.show()
else:
    print("No hay palabras para graficar.")

print("\n--- FIN DEL EJERCICIO 1 ---")
print("Observación: Nota cómo las palabras más frecuentes suelen ser artículos y preposiciones.")
print("Estas son 'stopwords' y no aportan mucho significado. ¡Esto es lo que solucionaremos en el siguiente ejercicio!")