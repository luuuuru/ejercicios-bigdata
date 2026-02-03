# Ejercicio 05: Procesamiento de Lenguaje Natural (NLP)

El texto es la fuente de datos más grande y desordenada del mundo (Big Data no estructurado). En este ejercicio aprenderás a transformar texto crudo en información matemática procesable.

---

## 🎯 Objetivos

1. **Preprocesamiento:** Limpieza de texto (stopwords, lematización, limpieza de signos).
2. **Análisis de Sentimiento:** Determinar si un texto es positivo o negativo usando Lexicones.
3. **Similitud:** Calcular qué tan parecidos son dos documentos (Jaccard).

---

## 📝 Tareas a Realizar

### Tarea 1: Limpieza de Texto
1. Revisa `02_limpieza_texto.py`.
2. **Reto:** Crea una función que limpie tweets (elimine `@usuarios`, `#hashtags` y URLs `http...`).

### Tarea 2: Matriz de Similitud (Jaccard)
1. Analiza `04_similitud_jaccard.py`.
2. Escribe un script que compare 3 frases diferentes y genere una matriz de similitud (quién se parece a quién).

### Tarea 3: Análisis de Sentimiento
1. Ejecuta `03_sentimiento_por_lexicon.py`.
2. **Reto:** Modifica el diccionario de palabras positivas/negativas (el "lexicon") para que detecte sarcasmo simple o modismos de tu país (ej. "brutal" puede ser bueno o malo).

---

## 📂 Entregables

Sube a `entregas/05_nlp_text_mining/TU_USUARIO/`:
1. Tu script de limpieza de tweets.
2. Tu script de comparación de frases (Jaccard).
3. (Opcional) Tu lexicon personalizado.

---

## 🆘 Referencias
- [NLTK Book](https://www.nltk.org/book/)
- [Jaccard Similarity Explanation](https://en.wikipedia.org/wiki/Jaccard_index)
