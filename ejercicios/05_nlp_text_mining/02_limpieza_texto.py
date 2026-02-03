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

# --- EJERCICIO 2: LIMPIEZA DE RUIDO Y EL IMPACTO VISUAL ---

# --- CONTEXTO ---
# Objetivo: Aprender a limpiar texto eliminando "stopwords" (palabras comunes sin significado semántico)
# y visualizar de forma impactante cómo esta limpieza cambia el análisis de frecuencia, haciendo que
# las palabras verdaderamente importantes emerjan.
#
# ¿Qué son las Stopwords? Son palabras como 'el', 'y', 'o', 'de', que son extremadamente frecuentes
# pero no nos dicen nada sobre el tema o el sentimiento de un texto. Son el "ruido" del lenguaje.

# --- IMPORTACIONES ---
import re
from collections import Counter
import matplotlib.pyplot as plt

# --- CORPUS Y STOPWORDS ---
corpus = [
    "Me encanta este producto, es fantástico y muy útil.",
    "El servicio al cliente fue terrible, muy decepcionante.",
    "El precio es adecuado, ni caro ni barato.",
    "No volvería a comprar, la calidad es pésima.",
    "Una experiencia increíble, lo recomiendo totalmente.",
    "El envío tardó más de lo esperado.",
    "Fantástico, simplemente fantástico.",
    "No está mal, pero podría mejorar en algunos aspectos.",
    "La batería dura poquísimo, un desastre."
]

# Lista de stopwords comunes en español. En proyectos reales, se usan listas más exhaustivas de librerías como NLTK o spaCy.
stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

# --- PROCESAMIENTO ---

# Función para procesar y limpiar texto
def procesar_y_contar(text, stopwords=None):
    """Toma un bloque de texto, lo normaliza, tokeniza y opcionalmente elimina stopwords."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    if stopwords:
        words = [word for word in words if word not in stopwords]
    return Counter(words)

# 1. Análisis SIN limpieza (Repetimos el paso del ejercicio 1 para comparar)
print("Paso 1: Analizando frecuencias SIN limpiar el texto...")
all_text = ' '.join(corpus)
word_counts_sin_limpieza = procesar_y_contar(all_text)
top_10_sin_limpieza = word_counts_sin_limpieza.most_common(10)
print("Top 10 palabras (sin limpieza):", top_10_sin_limpieza)

# 2. Análisis CON limpieza
print("\nPaso 2: Analizando frecuencias CON limpieza de stopwords...")
word_counts_con_limpieza = procesar_y_contar(all_text, stopwords=stopwords_es)
top_10_con_limpieza = word_counts_con_limpieza.most_common(10)
print("Top 10 palabras (con limpieza):", top_10_con_limpieza)


# --- VISUALIZACIÓN COMPARATIVA ---

print("\nGenerando gráficos comparativos...")

# Desempaquetamos los resultados para ambos gráficos
words_sin, counts_sin = zip(*top_10_sin_limpieza)
words_con, counts_con = zip(*top_10_con_limpieza)

# Creamos una figura con dos subplots (uno al lado del otro)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Gráfico 1: Sin Limpieza
ax1.bar(words_sin, counts_sin, color='#ff9999')
ax1.set_title('Frecuencias ANTES de la Limpieza', fontsize=16)
ax1.set_xlabel('Palabras')
ax1.set_ylabel('Frecuencia')
ax1.tick_params(axis='x', rotation=45)

# Gráfico 2: Con Limpieza
ax2.bar(words_con, counts_con, color='#99ff99')
ax2.set_title('Frecuencias DESPUÉS de la Limpieza', fontsize=16)
ax2.set_xlabel('Palabras')
ax2.tick_params(axis='x', rotation=45)

# Título general para toda la figura
fig.suptitle('Impacto de la Eliminación de Stopwords', fontsize=20)

# Ajustamos el layout y mostramos
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajuste para el supertítulo
plt.savefig('limpieza_stopwords_comparativa.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n--- FIN DEL EJERCICIO 2 ---")
print("Observación: ¡El cambio es drástico! El gráfico de la derecha revela las palabras que realmente aportan significado:")
print("'fantástico', 'producto', 'calidad', 'terrible'. Ahora sí podemos empezar a pensar en el sentimiento.")
