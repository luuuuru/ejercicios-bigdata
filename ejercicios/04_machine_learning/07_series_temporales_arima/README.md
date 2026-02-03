# 7. Series Temporales: ARIMA, SARIMA y Metodologia Box-Jenkins

> **Modulo 04 - Machine Learning | Ejercicio 07**
> Curso Avanzado de Big Data y Ciencia de Datos
> Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

---

Este documento es una guia teorica completa sobre el analisis de series temporales
utilizando modelos ARIMA/SARIMA y la metodologia clasica de Box-Jenkins.
Al finalizar, el estudiante debera comprender los fundamentos estadisticos,
saber identificar los parametros de un modelo y diagnosticar su calidad.

---

## Indice

- [7.1 Que es una serie temporal](#71-que-es-una-serie-temporal)
- [7.2 Estacionariedad](#72-estacionariedad)
- [7.3 ACF y PACF](#73-acf-y-pacf)
- [7.4 Modelos ARIMA](#74-modelos-arima)
- [7.5 Modelos SARIMA](#75-modelos-sarima)
- [7.6 Procedimiento Box-Jenkins](#76-procedimiento-box-jenkins)
- [7.7 Criterios de seleccion](#77-criterios-de-seleccion)
- [7.8 Diagnostico de residuos](#78-diagnostico-de-residuos)
- [7.9 Prophet (alternativa moderna)](#79-prophet-alternativa-moderna)
- [7.10 Redes neuronales para series temporales](#710-redes-neuronales-para-series-temporales)
- [7.11 Ejercicio practico](#711-ejercicio-practico)

---

## 7.1 Que es una serie temporal

Una **serie temporal** (o serie de tiempo) es una secuencia de observaciones
registradas en intervalos regulares a lo largo del tiempo. A diferencia de los
datos de corte transversal, aqui el **orden importa**: cada observacion depende
potencialmente de las anteriores.

### Componentes de una serie temporal

Toda serie temporal puede descomponerse conceptualmente en cuatro componentes:

| Componente       | Descripcion                                                    | Ejemplo                          |
|------------------|----------------------------------------------------------------|----------------------------------|
| **Tendencia**    | Movimiento de largo plazo (creciente, decreciente o estable)   | PIB que crece ano tras ano       |
| **Estacionalidad** | Patron que se repite en periodos fijos (semanal, mensual, anual) | Ventas altas en Navidad cada ano |
| **Ciclo**        | Fluctuaciones de largo plazo sin periodo fijo                  | Ciclos economicos de expansion   |
| **Ruido**        | Variacion aleatoria e impredecible (componente irregular)      | Fluctuaciones diarias aleatorias |

### Descomposicion visual (modelo aditivo)

```
Serie Original = Tendencia + Estacionalidad + Ciclo + Ruido

       Serie Original           Tendencia            Estacionalidad         Ruido
    |     *                 |         ___/        |   /\  /\  /\        |  * *
    |   *   *   *           |       _/            |  /  \/  \/  \       | *  * *
    |  *     * * *          |     _/              | /              \     |*    * *
    | *       *   * *       |   _/                |/                \   /|  *    *
    |*             * *      |  /                  |                  \/  | *  * *
    |               *       | /                   |                     |*  *  *
    +----------tiempo-->    +----------->         +----------->         +--------->
```

### Ejemplos reales de series temporales

- **Ventas mensuales** de una cadena de supermercados (tendencia + estacionalidad fuerte)
- **Temperatura diaria** de una ciudad (estacionalidad anual marcada)
- **PIB trimestral** de un pais (tendencia de largo plazo + ciclos economicos)
- **Pasajeros aereos internacionales** (dataset clasico de Box-Jenkins, 1949-1960)
- **Precio diario de acciones** en bolsa (ruido dominante, dificil de predecir)
- **Consumo electrico por hora** (estacionalidad diaria y semanal)

> **Nota importante:** En Big Data es comun trabajar con series de alta frecuencia
> (datos por segundo, por minuto). Los principios son los mismos, pero la escala
> computacional cambia significativamente.

---

## 7.2 Estacionariedad

### Que es y por que importa

Una serie es **estacionaria** cuando sus propiedades estadisticas (media, varianza,
autocorrelacion) no cambian a lo largo del tiempo. Esto es un **requisito fundamental**
para aplicar modelos ARIMA, ya que las ecuaciones del modelo asumen que la estructura
estadistica de la serie permanece constante.

En terminos simples: si cortas la serie en dos mitades, ambas deberian "verse"
estadisticamente similares.

### Estacionariedad fuerte vs debil

| Tipo                       | Definicion                                                          |
|----------------------------|---------------------------------------------------------------------|
| **Fuerte (estricta)**      | La distribucion conjunta de cualquier subconjunto de observaciones  |
|                            | no depende del tiempo. Muy restrictiva, rara vez se verifica.       |
| **Debil (de segundo orden)** | Solo se requiere que la media, varianza y autocovarianza sean      |
|                            | constantes en el tiempo. Esta es la que usamos en la practica.      |

### Como detectar estacionariedad visualmente

```
  Serie NO estacionaria             Serie ESTACIONARIA
  (tendencia creciente)             (fluctua alrededor de media constante)

  |            ___/                 |     *  *     *
  |         __/                     |  *    *  * *   *
  |       _/ *                      | * *      *  *    *
  |     _/ *                        |    *  *       * *
  |   _/*                           |  *   *  * *     *
  |  / *                            | *  *       *  *
  +--------tiempo-->                +--------tiempo-->
```

**Senales de NO estacionariedad:**
- La media cambia con el tiempo (tendencia visible)
- La varianza aumenta o disminuye (forma de "embudo")
- Hay patrones estacionales que no se han removido

### Tests formales de estacionariedad

#### Test ADF (Augmented Dickey-Fuller)

Es el test mas utilizado. Plantea como hipotesis:

- **H0 (hipotesis nula):** La serie tiene raiz unitaria (NO es estacionaria)
- **H1 (hipotesis alternativa):** La serie ES estacionaria

**Interpretacion:**
- Si el **p-valor < 0.05** --> Rechazamos H0 --> La serie ES estacionaria
- Si el **p-valor >= 0.05** --> No rechazamos H0 --> La serie NO es estacionaria

```python
from statsmodels.tsa.stattools import adfuller
resultado = adfuller(serie)
print(f"Estadistico ADF: {resultado[0]}")
print(f"p-valor: {resultado[1]}")
```

#### Test KPSS (Kwiatkowski-Phillips-Schmidt-Shin)

Complementario al ADF. Tiene las hipotesis **invertidas**:

- **H0:** La serie ES estacionaria
- **H1:** La serie NO es estacionaria

**Interpretacion:**
- Si el **p-valor < 0.05** --> Rechazamos H0 --> La serie NO es estacionaria
- Si el **p-valor >= 0.05** --> No rechazamos H0 --> La serie ES estacionaria

> **Buena practica:** Usar ambos tests juntos. Si ADF dice "estacionaria" Y KPSS
> dice "estacionaria", tenemos mayor confianza en el resultado.

### Como transformar una serie a estacionaria

| Tecnica                    | Cuando usarla                               | Ejemplo en Python              |
|----------------------------|---------------------------------------------|--------------------------------|
| **Diferenciacion (d=1)**   | Para remover tendencia lineal               | `serie.diff(1).dropna()`       |
| **Diferenciacion (d=2)**   | Para tendencia cuadratica (raro)            | `serie.diff(1).diff(1)`        |
| **Log-transform**          | Cuando la varianza crece con el nivel       | `np.log(serie)`                |
| **Diferenciacion estacional** | Para remover estacionalidad              | `serie.diff(12)` (mensual)     |
| **Log + Diferenciacion**   | Varianza no constante + tendencia           | `np.log(serie).diff(1)`        |

---

## 7.3 ACF y PACF

Las funciones de autocorrelacion son las herramientas principales para
**identificar** el tipo y orden del modelo ARIMA.

### Que es la Autocorrelacion (ACF)

La **ACF (Autocorrelation Function)** mide la correlacion entre una observacion
y sus valores pasados (lags). Por ejemplo, ACF en lag 3 mide cuanto se
correlaciona `Y(t)` con `Y(t-3)`.

La ACF incluye correlaciones **directas e indirectas**. Es decir, la correlacion
en lag 3 puede estar "contaminada" por las correlaciones en lag 1 y lag 2.

### Que es la Autocorrelacion Parcial (PACF)

La **PACF (Partial Autocorrelation Function)** mide la correlacion entre `Y(t)`
y `Y(t-k)` **despues de remover** el efecto de los lags intermedios.
Es la correlacion "pura" o "directa" en cada lag.

### Como leer los graficos ACF y PACF

```
  Grafico ACF tipico                    Grafico PACF tipico

  1.0 |#                                1.0 |#
      |#                                    |#
  0.5 |##                               0.5 |##
      | ##                                  |
  0.0 |---##-----banda---              0.0 |------banda---------
      |     ###  confianza                  |  #   confianza
 -0.5 |        ##                      -0.5 |
      |                                     |
      +--1--2--3--4--5--lag-->              +--1--2--3--4--5--lag-->
```

**Reglas de lectura:**
- Las barras que **sobresalen** de la banda de confianza (zona azul sombreada)
  son estadisticamente significativas
- La banda de confianza suele estar en +/- 1.96 / sqrt(n)
- El lag 0 siempre es 1.0 (una observacion correlaciona perfectamente consigo misma)

### Patrones tipicos de ACF y PACF

```
  Proceso AR(1):                        Proceso MA(1):
  ACF: decae exponencialmente           ACF: corte abrupto despues de lag 1
  PACF: corte abrupto despues lag 1     PACF: decae exponencialmente

  ACF del AR(1):          PACF del AR(1):        ACF del MA(1):         PACF del MA(1):
  |####                   |####                   |####                   |####
  | ###                   |                       |                       | ###
  |  ##                   | (dentro               | (dentro               |  ##
  |   #                   |  de banda)             |  de banda)            |   #
  |    #                  |                       |                       |    #
  +--lags-->              +--lags-->              +--lags-->              +--lags-->
   decae gradual           corte en lag 1          corte en lag 1          decae gradual
```

### Tabla de identificacion de modelos

Esta tabla es **fundamental** para la etapa de identificacion en Box-Jenkins:

| ACF muestra...                | PACF muestra...               | Modelo sugerido |
|-------------------------------|-------------------------------|-----------------|
| Decae exponencial/sinusoidal  | Corte abrupto en lag p        | **AR(p)**       |
| Corte abrupto en lag q        | Decae exponencial/sinusoidal  | **MA(q)**       |
| Decae exponencialmente        | Decae exponencialmente        | **ARMA(p,q)**   |
| No decae (persiste)           | Primer lag muy alto           | Serie no estacionaria (diferenciar) |

> **Tip practico:** Si la ACF decae MUY lentamente, es casi seguro que la serie
> no es estacionaria y necesita diferenciacion antes de modelar.

---

## 7.4 Modelos ARIMA

### AR(p): Modelo Autoregresivo

El modelo AR(p) predice el valor actual como una combinacion lineal de los
**p valores pasados** mas un termino de error.

**Ecuacion:**

```
Y(t) = c + phi_1 * Y(t-1) + phi_2 * Y(t-2) + ... + phi_p * Y(t-p) + epsilon(t)
```

Donde:
- `c` es una constante
- `phi_1, ..., phi_p` son los coeficientes autoregresivos
- `epsilon(t)` es ruido blanco (error aleatorio)
- `p` es el **orden** del modelo (numero de lags)

**Cuando usar:** Cuando la PACF muestra un corte abrupto en lag p.

**Ejemplo intuitivo:** Las ventas de hoy dependen de las ventas de ayer y anteayer.

### MA(q): Modelo de Media Movil

El modelo MA(q) predice el valor actual como una combinacion lineal de los
**q errores pasados**.

**Ecuacion:**

```
Y(t) = mu + epsilon(t) + theta_1 * epsilon(t-1) + theta_2 * epsilon(t-2) + ... + theta_q * epsilon(t-q)
```

Donde:
- `mu` es la media de la serie
- `theta_1, ..., theta_q` son los coeficientes de media movil
- `epsilon(t), epsilon(t-1), ...` son los terminos de error
- `q` es el **orden** del modelo

**Cuando usar:** Cuando la ACF muestra un corte abrupto en lag q.

**Ejemplo intuitivo:** El valor de hoy depende de los "shocks" o sorpresas recientes.

### ARMA(p,q): Combinacion

Combina ambos componentes. Util cuando tanto la ACF como la PACF decaen
gradualmente (sin cortes abruptos claros).

**Ecuacion:**

```
Y(t) = c + phi_1*Y(t-1) + ... + phi_p*Y(t-p) + epsilon(t) + theta_1*epsilon(t-1) + ... + theta_q*epsilon(t-q)
```

### ARIMA(p,d,q): La "I" de Integrado

El modelo ARIMA agrega la **diferenciacion** al ARMA, permitiendo trabajar con
series no estacionarias. La "I" significa "Integrado" (la operacion inversa
de diferenciar).

**Parametros:**
- `p` = orden autoregresivo (cuantos lags de Y usar)
- `d` = orden de diferenciacion (cuantas veces diferenciar para lograr estacionariedad)
- `q` = orden de media movil (cuantos lags de error usar)

**Casos especiales comunes:**

| Modelo         | Descripcion                                         |
|----------------|-----------------------------------------------------|
| ARIMA(0,0,0)   | Ruido blanco (sin estructura)                       |
| ARIMA(1,0,0)   | AR(1) puro                                          |
| ARIMA(0,0,1)   | MA(1) puro                                          |
| ARIMA(0,1,0)   | Caminata aleatoria (random walk)                    |
| ARIMA(0,1,1)   | Suavizado exponencial simple                        |
| ARIMA(1,1,1)   | Modelo mixto con una diferenciacion                 |

> **Regla practica:** En la mayoria de aplicaciones reales, `d` es 0 o 1.
> Valores de `d >= 2` son muy raros e indican posibles problemas con los datos.

---

## 7.5 Modelos SARIMA

### Extension estacional

Cuando una serie tiene **patron estacional** (por ejemplo, ventas que suben
cada diciembre), el modelo ARIMA simple no es suficiente. SARIMA agrega
componentes estacionales.

### Notacion: SARIMA(p,d,q)(P,D,Q)[s]

```
SARIMA(p, d, q)(P, D, Q)[s]
       -------  ---------  -
       parte     parte      periodo
       no        estacional estacional
       estacional
```

| Parametro | Significado                                            |
|-----------|--------------------------------------------------------|
| `p`       | Orden AR no estacional                                 |
| `d`       | Diferenciacion no estacional                           |
| `q`       | Orden MA no estacional                                 |
| `P`       | Orden AR estacional                                    |
| `D`       | Diferenciacion estacional                              |
| `Q`       | Orden MA estacional                                    |
| `s`       | Periodo estacional (12=mensual, 4=trimestral, 7=diario semanal) |

### Estacionalidad aditiva vs multiplicativa

- **Aditiva:** La amplitud de la estacionalidad es **constante** en el tiempo.
  La serie se modela como: `Y = Tendencia + Estacionalidad + Error`

- **Multiplicativa:** La amplitud de la estacionalidad **crece** con el nivel
  de la serie. Se modela como: `Y = Tendencia x Estacionalidad x Error`

```
  Estacionalidad ADITIVA:            Estacionalidad MULTIPLICATIVA:

  |    /\    /\    /\                |              /\
  |   /  \  /  \  /  \              |           /\/ \
  |  /    \/    \/    \             |        /\/     \
  | /                  \            |     /\/         \
  |/                    \           |  /\/             \
  +--------tiempo-->                +--------tiempo-->
  (amplitud constante)              (amplitud crece con la tendencia)
```

> **Tip:** Si la estacionalidad es multiplicativa, aplicar `log()` a la serie
> la convierte en aditiva, lo que facilita el modelado SARIMA.

### Ejemplo: SARIMA(1,1,1)(1,1,1)[12]

Este es uno de los modelos mas comunes para datos mensuales:

- **(1,1,1):** Un lag AR, una diferenciacion, un lag MA (parte no estacional)
- **(1,1,1)[12]:** Un lag AR estacional, una diferenciacion estacional,
  un lag MA estacional, con periodo de 12 meses

En Python:

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

modelo = SARIMAX(serie,
                 order=(1, 1, 1),
                 seasonal_order=(1, 1, 1, 12))
resultado = modelo.fit()
```

---

## 7.6 Procedimiento Box-Jenkins

La **metodologia Box-Jenkins** (1976) es el procedimiento sistematico clasico
para construir modelos ARIMA/SARIMA. Es un proceso **iterativo** de cuatro etapas.

### Diagrama de flujo del procedimiento

```
+========================+
|   DATOS ORIGINALES     |
|   (serie temporal)     |
+========================+
           |
           v
+---------------------------+
| PASO 1: IDENTIFICACION    |
| - Graficar la serie       |
| - Test ADF/KPSS           |
| - Diferenciar si es       |       +---------------------------+
|   necesario (d, D)        | <---- | Si diagnostico FALLA:     |
| - Analizar ACF y PACF     |       | volver a identificar con  |
| - Proponer p, q, P, Q     |       | otros ordenes (p, q)      |
+---------------------------+       +---------------------------+
           |                                     ^
           v                                     |
+---------------------------+                    |
| PASO 2: ESTIMACION        |                    |
| - Ajustar modelo SARIMA   |                    |
| - Maxima verosimilitud     |                    |
| - Verificar que los       |                    |
|   coeficientes sean       |                    |
|   significativos           |                    |
+---------------------------+                    |
           |                                     |
           v                                     |
+---------------------------+                    |
| PASO 3: DIAGNOSTICO       |                    |
| - Residuos = ruido blanco?|                    |
| - Test Ljung-Box          |-----> NO ------->--+
| - Test Jarque-Bera        |
| - ACF de residuos         |
| - Q-Q plot                |
+---------------------------+
           |
           | SI (residuos OK)
           v
+---------------------------+
| PASO 4: PRONOSTICO        |
| - Generar forecast        |
| - Intervalos de confianza |
| - Validar con datos       |
|   de prueba (backtest)    |
+---------------------------+
           |
           v
     [MODELO FINAL]
```

### Paso 1: Identificacion (detalle)

1. **Graficar** la serie original y observar tendencia, estacionalidad, varianza.
2. **Aplicar tests** ADF y KPSS para determinar si es estacionaria.
3. Si no es estacionaria:
   - Aplicar `log()` si la varianza no es constante.
   - Diferenciar una vez (`d=1`). Repetir test.
   - Si hay estacionalidad, diferenciar estacionalmente (`D=1`).
4. **Graficar ACF y PACF** de la serie transformada.
5. Usar la tabla de la Seccion 7.3 para proponer valores de `p` y `q`.
6. Si hay picos estacionales en ACF/PACF (en lags 12, 24, 36...), proponer `P` y `Q`.

### Paso 2: Estimacion (detalle)

- Se ajusta el modelo por **Maxima Verosimilitud (MLE)**.
- Se verifican los coeficientes: cada uno debe ser **estadisticamente significativo**
  (p-valor < 0.05).
- Si un coeficiente no es significativo, considerar eliminarlo (reducir el orden).

### Paso 3: Diagnostico (detalle)

Ver Seccion 7.8 para un tratamiento completo del diagnostico de residuos.

### Paso 4: Pronostico (detalle)

- Solo si el diagnostico es satisfactorio se procede a hacer predicciones.
- Siempre reportar **intervalos de confianza** (generalmente al 95%).
- Los intervalos se ensanchan a medida que el horizonte de prediccion aumenta.
- Validar con un conjunto de datos de prueba reservado (train/test split temporal).

> **Regla de oro:** Un modelo ARIMA solo debe pronosticar a corto/mediano plazo.
> Para horizontes muy largos, los intervalos de confianza se vuelven tan amplios
> que la prediccion pierde utilidad practica.

---

## 7.7 Criterios de seleccion

Cuando hay varios modelos candidatos (por ejemplo, ARIMA(1,1,1) vs ARIMA(2,1,1)),
necesitamos criterios objetivos para elegir el mejor.

### AIC (Criterio de Informacion de Akaike)

```
AIC = -2 * log(L) + 2 * k
```

Donde `L` es la verosimilitud del modelo y `k` es el numero de parametros.
**Se elige el modelo con MENOR AIC.**

### BIC (Criterio de Informacion Bayesiano)

```
BIC = -2 * log(L) + k * log(n)
```

Donde `n` es el numero de observaciones. El BIC penaliza **mas fuertemente**
los modelos con muchos parametros. **Se elige el modelo con MENOR BIC.**

### Comparacion AIC vs BIC

| Criterio | Penalizacion por complejidad | Tendencia                        |
|----------|------------------------------|----------------------------------|
| AIC      | Moderada (2*k)               | Puede seleccionar modelos mas complejos |
| BIC      | Fuerte (k*log(n))            | Prefiere modelos mas simples      |

### Principio de parsimonia

> "Entre dos modelos que explican igualmente bien los datos,
> preferir siempre el mas simple." -- Navaja de Occam

Un modelo con menos parametros es:
- Mas facil de interpretar
- Menos propenso al sobreajuste (overfitting)
- Mas robusto ante datos nuevos
- Mas rapido de calcular

### Grid Search vs auto_arima

**Grid search manual:** Probar sistematicamente combinaciones de (p,d,q)(P,D,Q)
y comparar AIC/BIC. Es lento pero da control total.

**auto_arima (pmdarima):** Automatiza la busqueda del mejor modelo. Implementa
una version optimizada del procedimiento Box-Jenkins.

```python
from pmdarima import auto_arima

modelo = auto_arima(serie,
                    seasonal=True, m=12,
                    stepwise=True,
                    trace=True)  # muestra la busqueda en consola
print(modelo.summary())
```

> **Recomendacion:** Usar `auto_arima` como punto de partida, pero siempre
> verificar manualmente los residuos y comparar con modelos alternativos.

---

## 7.8 Diagnostico de residuos

### Que son los residuos

Los **residuos** son la diferencia entre los valores observados y los valores
ajustados por el modelo:

```
residuo(t) = Y_observado(t) - Y_ajustado(t)
```

Si el modelo es bueno, los residuos deben comportarse como **ruido blanco**:
sin patron, sin autocorrelacion, con media cero y varianza constante.

### Test de Ljung-Box (autocorrelacion residual)

Verifica si hay autocorrelacion significativa en los residuos.

- **H0:** Los residuos son independientes (no hay autocorrelacion)
- **H1:** Existe autocorrelacion en los residuos

**Interpretacion:**
- p-valor > 0.05 --> No se rechaza H0 --> Los residuos son independientes (BIEN)
- p-valor < 0.05 --> Se rechaza H0 --> Hay autocorrelacion residual (MAL)

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
resultado = acorr_ljungbox(residuos, lags=[10, 20, 30])
print(resultado)
```

### Test de Jarque-Bera (normalidad)

Verifica si los residuos siguen una distribucion normal.

- **H0:** Los residuos son normales
- **H1:** Los residuos no son normales

**Interpretacion:**
- p-valor > 0.05 --> Residuos normales (BIEN)
- p-valor < 0.05 --> Residuos no normales (revisar, pero no siempre es critico)

### Herramientas graficas de diagnostico

```
  1. ACF de residuos         2. Histograma             3. Q-Q Plot
  (no debe haber barras      (debe parecerse a         (puntos deben seguir
   significativas)            campana de Gauss)          la linea diagonal)

  |                           |    __                   |          **/
  | (dentro de banda)         |   /  \                  |        **/
  | # # # # # # #            |  /    \                 |      **/
  +--1--2--3--4--lag-->       | /      \                |   **/
                              |/        \___            | **/
                              +--valores-->             +--cuantiles teoricos-->
```

### Que hacer si el diagnostico falla

| Problema detectado                  | Accion correctiva                               |
|-------------------------------------|--------------------------------------------------|
| Autocorrelacion en residuos          | Ajustar p o q (agregar mas lags)                |
| Residuos no normales                | Considerar transformacion log o Box-Cox          |
| Varianza no constante (heterocedasticidad) | Aplicar log-transform, considerar GARCH    |
| Patron estacional en residuos       | Agregar componente estacional (P, D, Q)          |
| Outliers extremos                   | Investigar causas, considerar modelos robustos   |

> **Importante:** El diagnostico no es un paso que se hace una sola vez. Es un
> proceso iterativo: si falla, se vuelve al Paso 1 (Identificacion) con nuevos
> parametros y se repite el ciclo.

---

## 7.9 Prophet (alternativa moderna)

### Que es Prophet

**Prophet** es una herramienta de pronostico de series temporales desarrollada
por Meta (Facebook) y publicada en 2018 por Sean Taylor y Ben Letham.
Fue disenada para ser accesible a analistas que no son especialistas en
series temporales.

### Modelo aditivo de Prophet

```
y(t) = g(t) + s(t) + h(t) + epsilon(t)
```

| Componente    | Significado                                              |
|---------------|----------------------------------------------------------|
| `g(t)`        | Tendencia (lineal o logistica, con puntos de cambio)     |
| `s(t)`        | Estacionalidad (Fourier series: anual, semanal, diaria)  |
| `h(t)`        | Efecto de dias festivos y eventos especiales              |
| `epsilon(t)`  | Error (ruido)                                            |

### Ventajas de Prophet

- **Automatico:** Detecta tendencia, estacionalidad y puntos de cambio sin intervencion.
- **Robusto a datos faltantes:** No requiere que la serie sea completa ni regular.
- **Detecta cambios de tendencia:** Identifica automaticamente "changepoints".
- **Incorpora dias festivos:** Permite modelar efectos de Navidad, feriados, etc.
- **Facil de usar:** API simple, pocos hiperparametros que ajustar.
- **Incertidumbre:** Genera intervalos de confianza automaticamente.

### Desventajas de Prophet

- **Menos control fino** que SARIMA: no permite especificar ordenes AR/MA exactos.
- **Caja negra parcial:** Los componentes internos son menos transparentes.
- **No modela autocorrelacion directamente:** No usa la estructura AR/MA.
- **Puede fallar con series muy cortas** (necesita al menos 1-2 anos de datos).
- **Rendimiento variable:** No siempre supera a SARIMA bien calibrado.

### Cuando usar cada uno

| Criterio                          | SARIMA                        | Prophet                       |
|-----------------------------------|-------------------------------|-------------------------------|
| Conocimiento estadistico          | Requiere experiencia          | Accesible para principiantes  |
| Series cortas (< 2 anos)         | Funciona bien                 | Puede tener problemas         |
| Multiples estacionalidades        | Complejo de modelar           | Lo maneja nativamente         |
| Datos con muchos faltantes        | Problematico                  | Lo maneja bien                |
| Interpretabilidad del modelo      | Alta (coeficientes claros)    | Media (componentes separados) |
| Datos de negocio con feriados     | Manual                        | Integrado                     |
| Control sobre parametros          | Total                         | Limitado                      |
| Velocidad de implementacion       | Lenta (iterativo)             | Rapida                        |

```python
# Ejemplo basico con Prophet
from prophet import Prophet
import pandas as pd

df = pd.DataFrame({'ds': fechas, 'y': valores})  # formato requerido
modelo = Prophet(yearly_seasonality=True)
modelo.fit(df)

futuro = modelo.make_future_dataframe(periods=30)
pronostico = modelo.predict(futuro)
modelo.plot(pronostico)
```

---

## 7.10 Redes neuronales para series temporales (vista general)

### LSTM (Long Short-Term Memory)

Las redes **LSTM** son un tipo de red neuronal recurrente (RNN) disenada
especificamente para aprender dependencias de largo plazo en secuencias.
Son la arquitectura clasica de deep learning para series temporales.

**Ventajas:**
- Capturan **patrones no lineales** que ARIMA no puede modelar.
- Pueden manejar multiples variables de entrada (series multivariantes).
- Aprenden automaticamente las representaciones relevantes.

**Desventajas:**
- Requieren **grandes cantidades de datos** para entrenarse bien.
- Alto costo computacional (GPU recomendada).
- Dificiles de interpretar ("caja negra").
- Muchos hiperparametros que ajustar (capas, neuronas, learning rate, etc.).

### NeuralProphet

**NeuralProphet** combina la filosofia de Prophet con redes neuronales.
Mantiene la descomposicion en componentes interpretables pero agrega la
capacidad de modelar relaciones no lineales.

**Caracteristicas principales:**
- Descomposicion aditiva (como Prophet) + componentes autoregresivos neuronales.
- Soporte para covariables (variables exogenas).
- Mas flexible que Prophet clasico.
- Mas interpretable que LSTM puro.

### Resumen comparativo

```
  Interpretabilidad vs Complejidad:

  ARIMA/SARIMA  ------>  Prophet  ------>  NeuralProphet  ------>  LSTM
  |                                                                   |
  Alta interpretabilidad                          Alta capacidad de
  Baja complejidad                                modelar no linealidades
  Pocos datos necesarios                          Muchos datos necesarios
```

> **Nota:** El uso de redes neuronales para series temporales se cubre en
> un ejercicio separado dentro del modulo. Aqui solo se presenta una vision general
> para que el estudiante comprenda el panorama completo de herramientas disponibles.

---

## 7.11 Ejercicio practico

### Script principal

El ejercicio practico se implementa en el archivo **`serie_temporal_completa.py`**,
que contiene un pipeline completo del procedimiento Box-Jenkins aplicado
a un dataset real.

### Como ejecutar

```bash
# Desde la raiz del proyecto
cd ejercicios/04_machine_learning/07_series_temporales_arima/
python serie_temporal_completa.py
```

### Que outputs genera

El script produce:
1. **Graficos de la serie original** y su descomposicion.
2. **Tests de estacionariedad** (ADF y KPSS) con interpretacion automatica.
3. **Graficos ACF y PACF** para identificar ordenes del modelo.
4. **Ajuste del modelo SARIMA** con resumen estadistico.
5. **Diagnostico de residuos** (Ljung-Box, Jarque-Bera, graficos).
6. **Pronostico** con intervalos de confianza al 95%.
7. **Comparacion** entre SARIMA y Prophet (si esta instalado).

### Dependencias

```
pandas
numpy
matplotlib
statsmodels
pmdarima
prophet        # opcional, para la comparacion
scikit-learn   # para metricas de error
```

Instalacion:

```bash
pip install pandas numpy matplotlib statsmodels pmdarima
pip install prophet  # opcional
```

### Tareas para el estudiante

1. **Ejecutar** el script y analizar cada grafico generado.
2. **Modificar** los ordenes (p,d,q) manualmente y observar como cambian el AIC y los residuos.
3. **Comparar** los resultados de `auto_arima` con el modelo que el estudiante identifique
   usando ACF/PACF.
4. **Reflexionar:** En que casos SARIMA funciona mejor que Prophet y viceversa?

---

## Referencias y recursos adicionales

Para profundizar en los temas cubiertos en esta guia:

- **Libro clasico:** Box, Jenkins & Reinsel - "Time Series Analysis: Forecasting and Control"
- **Libro moderno (gratuito):** Hyndman & Athanasopoulos - "Forecasting: Principles and Practice"
  disponible en https://otexts.com/fpp3/
- **Documentacion statsmodels:** https://www.statsmodels.org/stable/tsa.html
- **Documentacion pmdarima:** https://alkaline-ml.com/pmdarima/
- **Documentacion Prophet:** https://facebook.github.io/prophet/

---

```
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA:
- Box, G.E.P. & Jenkins, G.M. (1976). Time Series Analysis: Forecasting and Control. Holden-Day.
- Hyndman, R.J. & Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3rd ed.). OTexts.
- Taylor, S.J. & Letham, B. (2018). Forecasting at Scale. The American Statistician, 72(1), 37-45.
- Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
- Brockwell, P.J. & Davis, R.A. (2016). Introduction to Time Series and Forecasting (3rd ed.). Springer.
-------------------------
```
