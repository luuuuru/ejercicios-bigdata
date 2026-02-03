# 🎓 Guía Formativa: Vectorización y Clustering de Documentos

## 🚀 Análisis de Tópicos con Inteligencia Artificial (NLP & Machine Learning)

---

> ### 📝 Información de Certificación y Referencia
>
> **Autor original/Referencia:** @TodoEconometria  
> **Profesor:** Juan Marcelo Gutierrez Miranda  
> **Metodología:** Cursos Avanzados de Big Data, Ciencia de Datos, Desarrollo de aplicaciones con IA & Econometría Aplicada.  
> **Hash ID de Certificación:** `4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c`  
> **Repositorio:** [https://github.com/TodoEconometria/certificaciones](https://github.com/TodoEconometria/certificaciones)  
>
> **REFERENCIA ACADÉMICA:**
>
> - McKinney, W. (2012). Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython. O'Reilly Media.
> - Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.
> - Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.

---

## 🏛️ 1. Introducción al Laboratorio

En el mundo del **Big Data**, la mayor parte de la información es **no estructurada** (textos, correos, noticias). El reto fundamental es: *¿Cómo puede una computadora entender que dos documentos hablan de lo mismo sin leerlos?*

Este ejercicio implementa un pipeline completo de Ciencia de Datos para agrupar automáticamente **1,200 documentos** en español, utilizando una combinación de técnicas matemáticas avanzadas para transformar el lenguaje humano en estructuras que las máquinas pueden procesar.

---

## 🧠 2. Fundamentos Teóricos (¿Qué usamos y por qué?)

### A. Vectorización: El Puente entre Texto y Matemáticas

Las computadoras no entienden palabras, solo números. Usamos **TF-IDF (Term Frequency - Inverse Document Frequency)** por su capacidad de discernir la relevancia.

- **¿Qué es?**: Un valor estadístico que busca medir qué tan importante es una palabra para un documento dentro de una colección (corpus).
- **¿Cómo funciona?**:
    $$TF(t, d) = \frac{\text{Conteo de la palabra } t \text{ en documento } d}{\text{Total de palabras en } d}$$
    $$IDF(t) = \log\left(\frac{\text{Total de documentos}}{\text{Documentos que contienen la palabra } t}\right)$$
- **¿Por qué lo usamos?**: A diferencia del simple conteo (Bak-of-Words), el TF-IDF penaliza palabras que aparecen en todos lados (como "el", "que", "es") y premia palabras temáticas ("procesador", "inversión", "vacuna").

### B. K-Means: El Cerebro del Agrupamiento

Para el **Aprendizaje No Supervisado**, el algoritmo de **K-Means** es el estándar de oro para encontrar patrones sin etiquetas previas.

- **El Proceso**:
    1. Define $k$ puntos aleatorios (centroides).
    2. Asigna cada documento al centroide más cercano (usando distancia euclidiana en el espacio vectorial).
    3. Recalcula el centro del grupo y repite hasta que los grupos se estabilizan.
- **Por qué lo usamos**: Es extremadamente eficiente para grandes volúmenes de datos y nos permite segmentar el mercado, noticias o documentos legales de forma automática.

### C. PCA: Visualizando el Hiperespacio

Nuestra matriz TF-IDF tiene cientos de dimensiones (una por cada palabra única). El ser humano solo puede ver en 2D o 3D.

- **¿Qué significa?**: **Principal Component Analysis** "comprime" la información. Busca las direcciones (componentes) donde los datos varían más y proyecta todo sobre ellas.
- **Utilidad Didáctica**: Sin PCA, el clustering sería una lista de números abstractos. Con PCA, podemos "ver" la separación de conceptos en una gráfica.

---

## 📊 3. Interpretación de lo que estamos viendo

Al ejecutar el código, se genera la visualización `05_visualizacion_clustering.png`.

![Clustering de Documentos](05_visualizacion_clustering.png)

### ¿Cómo leer este gráfico?

1. **Cercanía es Similitud**: Dos puntos que están pegados significan documentos que comparten palabras clave y, por lo tanto, temas.
2. **Dispersión de Clusters**:
    - Si los grupos están muy separados, el algoritmo ha tenido éxito total identificando temas únicos.
    - Si hay solapamiento, indica que hay documentos que comparten vocabulario de varios temas (ej. un artículo sobre "Tecnología en la Salud").
3. **Los Ejes (PCA)**: El Eje X (Componente 1) suele capturar la diferencia más grande entre los temas (ej. términos médicos vs términos financieros).

---

## 👨‍🏫 4. Guía Didáctica: Paso a Paso

### Paso 1: Generación del Corpus

Creamos 1,200 documentos sintéticos. En una formación real, esto simula la ingesta de datos de una API o una base de datos SQL.

### Paso 2: Limpieza y Tokenización

Aunque el script es directo, en NLP real eliminaríamos puntuación, convertiríamos a minúsculas y quitaríamos *Stop Words* (palabras vacías) para que el modelo no se distraiga con ruido.

### Paso 3: Entrenamiento del Modelo

El comando `kmeans.fit(tfidf_matrix)` es donde ocurre la "magia". El modelo "aprende" la estructura latente de los datos sin ayuda humana.

---

## 📚 Referencias y Citas Académicas

Para profundizar en la metodología, se recomienda la consulta de las siguientes fuentes fundamentales:

- **McKinney, W. (2012).** *Python for Data Analysis*. O'Reilly Media. (Referencia para manipulación de matrices).
- **Pedregosa, F., et al. (2011).** *Scikit-learn: Machine Learning in Python*. JMLR. (Documentación oficial del framework utilizado).
- **Manning, C. D., et al. (2008).** *Introduction to Information Retrieval*. Cambridge University Press. (Teoría base de TF-IDF).

---

## 🎓 Información Institucional

**Autor/Referencia:** @TodoEconometria  
**Profesor:** Juan Marcelo Gutierrez Miranda  
**Área:** Big Data, Ciencia de Datos & Econometría Aplicada.  

**Hash ID de Certificación:**  
`4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c`
