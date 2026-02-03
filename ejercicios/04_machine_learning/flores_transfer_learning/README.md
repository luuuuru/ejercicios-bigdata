# Clasificacion de Flores con Transfer Learning

## Que es Transfer Learning?

**Transfer Learning** es una tecnica donde usamos un modelo pre-entrenado en millones de imagenes (ImageNet) y lo adaptamos a nuestro problema especifico.

```
ImageNet (14M imagenes)  -->  MobileNetV2  -->  Embeddings  -->  Clasificador Flores
      |                           |                |                    |
  1000 clases              Red neuronal      Vector 1280D          5 clases
```

### Por que funciona?

Las primeras capas de una CNN aprenden **patrones generales**:
- Bordes, texturas, formas basicas
- Combinaciones de colores
- Patrones geometricos

Estos patrones son **universales** - sirven para cualquier imagen.

## Pipeline del Ejercicio

```
1. DESCARGA          2. EMBEDDINGS         3. CLASIFICACION
   Flores              MobileNetV2            ML/DL
   3,670 imgs          1280 features          5 clases
      |                    |                     |
   [imagen] -------> [vector numerico] -----> [prediccion]
```

## Archivos

| Archivo | Descripcion |
|---------|-------------|
| `01_flores_transfer_learning.py` | Pipeline completo comentado |
| `requirements.txt` | Dependencias |

## Ejecucion

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python 01_flores_transfer_learning.py
```

El script descarga automaticamente el dataset y genera un dashboard HTML.

## Resultados Esperados

| Modelo | Accuracy |
|--------|----------|
| SVM | ~90% |
| Random Forest | ~86% |
| KNN | ~85% |

## Teoria: Embeddings vs Pixeles

**Sin Transfer Learning:**
- Imagen 224x224 = 150,528 pixeles
- Demasiadas dimensiones, poca informacion semantica

**Con Transfer Learning:**
- Imagen --> MobileNetV2 --> Vector de 1,280 dimensiones
- Cada dimension representa una caracteristica visual aprendida
- Flores similares = vectores similares (distancia coseno)

```python
# Ejemplo conceptual
rosa_1 = [0.2, 0.8, 0.1, ...]  # 1280 valores
rosa_2 = [0.21, 0.79, 0.12, ...]  # Similar!
girasol = [0.9, 0.1, 0.7, ...]  # Diferente
```

---
**Curso:** Big Data con Python - De Cero a Produccion
**Profesor:** Juan Marcelo Gutierrez Miranda | @TodoEconometria
**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c

**Referencias academicas:**
- Sandler, M., et al. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. CVPR.
- Yosinski, J., et al. (2014). How transferable are features in deep neural networks? NeurIPS.
- van der Maaten, L. & Hinton, G. (2008). Visualizing Data using t-SNE. JMLR.
