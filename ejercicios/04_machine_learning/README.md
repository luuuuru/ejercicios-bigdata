# Ejercicio 04: Machine Learning y Clustering

En este módulo aprenderás a aplicar técnicas de **Aprendizaje No Supervisado** (Clustering y reducción de dimensionalidad) sobre datasets complejos. No nos limitaremos a `scikit-learn` básico; buscaremos optimizar los flujos de trabajo.

---

## 🎯 Objetivos

1. **Reducción de Dimensionalidad:** Entender y aplicar **PCA** (Principal Component Analysis) para visualizar datos de alta dimensionalidad.
2. **Clustering:** Agrupar datos similares usando **K-Means**.
3. **Interpretación:** Analizar qué significan los grupos encontrados (profiling).

---

## 📝 Tareas a Realizar

### Tarea 1: PCA con Iris (Intro)
1. Ejecuta el script `01_PCA_iris.py` para entender cómo reducir 4 dimensiones a 2.
2. **Reto:** Modifica el script para usar el dataset `Wine` de scikit-learn en lugar de Iris. ¿Qué observas?

### Tarea 2: Clustering de Vinos (K-Means)
1. Analiza `06_kmeans_wine.py`.
2. Observa cómo usamos el "Método del Codo" (Elbow Method) para decidir el número de clusters.
3. **Reto:** Implementa el cálculo del **Silhouette Score** para validar si el número de clusters elegido es óptimo.

### Tarea 3: Pipeline Completo (Opcional - Avanzado)
1. Revisa `05_vectorizacion_y_clustering.py`.
2. Intenta aplicar este pipeline de vectorización + clustering a un texto propio (ej. descripciones breves de productos).

---

## 📂 Entregables

Sube a `entregas/04_machine_learning/TU_USUARIO/`:
1. El script modificado de la **Tarea 1** (`pca_wine.py`).
2. El script modificado de la **Tarea 2** con Silhouette Score.
3. Una breve reflexión (en `README.md` o comentarios) sobre los resultados.

---

## 🆘 Referencias
- [Scikit-Learn Clustering Guide](https://scikit-learn.org/stable/modules/clustering.html)
- [PCA Explained](https://setosa.io/ev/principal-component-analysis/)
