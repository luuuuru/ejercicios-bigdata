# Guía de Análisis de Datos de Panel en Big Data

Esta guía acompaña los ejercicios prácticos de **Análisis de Datos Estructurados Multidimensionales** (Panel Data) en el contexto de Big Data y Data Science.

## 1. Introducción: Datos Longitud-Transversales en Data Science
En Big Data, es común encontrar estructuras de datos que no son simplemente una "foto" estática (cross-section) ni solo una serie temporal (time-series), sino una combinación de ambas.
Los **Datos de Panel** combinan una dimensión temporal ($T$) con una dimensión de entidad ($N$).

**Estructura del Dataset:**
- **Indexación Jerárquica (MultiIndex)**: Es fundamental en `pandas` y `dask`.
  - `Entity` (ID): Identificador único (ej. `state_id`, `user_id`, `device_id`).
  - `Time` (Timestamp): Periodo de observación (ej. `year`, `month`, `transaction_date`).
- **Features**: Variables observadas ($X_{it}, Y_{it}$).

### El Desafío del Sesgo por Heterogeneidad
En un entorno de Big Data, "más datos" no siempre significa "mejores modelos" si ignoramos la estructura subyacente.
Si entrenamos un modelo global ignorando que los datos provienen de distintas fuentes (estados, usuarios), corremos el riesgo de sufrir el **Sesgo de Variable Omitida**.
*Ejemplo*: Un algoritmo puede concluir equivocadamente que "más policía causa más crimen" si no controla por el hecho de que las ciudades peligrosas *siempre* tienen más policía (efecto fijo de la ciudad).

---

## 2. Algoritmos de Modelado en Python

El flujo de trabajo en Python (usando `linearmodels` y `statsmodels`) para mitigar estos sesgos es el siguiente:

### Algoritmo 1: Modelo Global Agrupado (Pooled OLS)
- **Definición**: Un único modelo de regresión lineal entrenado sobre todo el dataset apilado ("stacked").
- **Hipótesis de Datos**: Asume que todas las observaciones son i.i.d. (independientes e idénticamente distribuidas) y que el comportamiento es universal para todas las entidades.
- **Riesgo en Producción**: Alto riesgo de **Underfitting** de la estructura grupal.

### Algoritmo 2: Modelo de Efectos Fijos (Fixed Effects - FE)
- **Definición**: Un modelo que aprende un "intercepto" o "bias" único para cada entidad ($\alpha_i$).
- **Mecanismo**: $Y_{it} = (\alpha + \alpha_i) + \beta X_{it} + \epsilon_{it}$
  - El modelo "desvía" los datos restando la media de cada grupo (Within Transformation).
  - **Interpretación**: Analiza cómo cambios *dentro* de una entidad afectan el resultado, ignorando las diferencias estáticas entre entidades.
- **Uso en Big Data**: Crucial para A/B testing longitudinal o análisis de políticas donde características intrínsecas del usuario/región no cambian.

### Algoritmo 3: Modelo de Efectos Aleatorios (Random Effects - RE)
- **Definición**: Trata la variación entre entidades como ruido aleatorio estructurado en lugar de parámetros fijos a aprender.
- **Validación**: Se utiliza el **Test de Hausman** para determinar si el error del modelo está correlacionado con los features.
  - Si el test falla ($p < 0.05$), el modelo RE está sesgado -> Usar FE.

---

## 3. Datasets y Referencias Técnicas

### A. Dataset "Guns" (Crimen y Políticas Públicas)
**Fuente Técnica**: Ayres, I., & Donohue, J. J. (2003). *Shooting down the 'more guns, less crime' hypothesis*. Stanford Law Review.
- **Objetivo del Análisis**: Determinar el impacto causal de la feature binaria `law` (ley shall-issue) sobre el target continuo `violent` (tasa de crimen).
- **Reto de Datos**: Alta colinealidad temporal y heterogeneidad espacial.

### B. Dataset "Fatality" (Seguridad Vial)
**Fuente Técnica**: Stock, J. H., & Watson, M. W. (2003). *Introduction to Econometrics*. Addison Wesley.
- **Objetivo del Análisis**: Modelar la elasticidad de `fatality_rate` respecto a `beertax` (impuesto alcohol).
- **Técnica Avanzada**: **Two-Way Fixed Effects**. Controlar simultáneamente por:
  1. Heterogeneidad del Estado (cultura de conducción local).
  2. Efectos Temporales (mejoras tecnológicas en seguridad vehicular año tras año).

---

## 4. Pipeline de Implementación Python

### Transformación de Datos en Pandas
El pipeline de preprocesamiento requiere establecer explícitamente el índice multidimensional para habilitar las operaciones de panel algebraico.

```python
# Pipeline de transformación
df_panel = (
    df_raw
    .assign(log_target=lambda x: np.log(x['target_col'])) # Transformación Log-Normal
    .set_index(['entity_id', 'time_id'])                  # MultiIndex Pandas
)
```

### Visualización Analítica (Dashboarding)
Utilizamos `HoloViz` (`panel`, `hvplot`) para exploración interactiva, permitiendo al analista hacer "slicing" y "dicing" de la data a través de las dimensiones temporales y espaciales.

### Interpretación de Coeficientes para Negocio
Los coeficientes resultantes ($\beta$) no son simples multiplicadores, sino estimadores de elasticidad o semi-elasticidad en modelos log-lineales.
- **Feature Log / Target Log**: $\beta$ representa % de cambio en Y dado % de cambio en X (Elasticidad).
