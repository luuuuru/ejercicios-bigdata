"""
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
-------------------------

SERIE TEMPORAL COMPLETA - Metodologia Box-Jenkins (ARIMA / SARIMA)
Dataset: AirPassengers (Pasajeros de aerolineas mensuales, 1949-1960)

Este script implementa el flujo completo de analisis de series temporales:
  1. Carga y exploracion de datos
  2. Pruebas de estacionariedad (ADF, KPSS)
  3. Identificacion del modelo (ACF, PACF, auto_arima o busqueda manual)
  4. Estimacion del modelo SARIMA
  5. Diagnostico de residuos
  6. Pronostico con intervalos de confianza
  7. Comparacion con Prophet (opcional)
  8. Comparacion de metricas con grafico radar
  9. Grafico final consolidado
 10. Tablas de resultados y exportacion

Ejecucion:
    python serie_temporal_completa.py

Dependencias obligatorias: pandas, numpy, matplotlib, statsmodels, scipy
Dependencias opcionales:   pmdarima, prophet
"""

# ============================================================================
# CONFIGURACION INICIAL
# ============================================================================
import os
import sys
import warnings
import itertools

import numpy as np
import pandas as pd

# Renderizado sin interfaz grafica (headless) - DEBE ir antes de importar pyplot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

from scipy import stats as sp_stats

import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")

# Directorio de salida para graficos y tablas
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_SALIDA = os.path.join(DIRECTORIO_BASE, "output")
os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

# Estilo de graficos
plt.rcParams.update({
    "figure.figsize": (14, 7),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})

# Colores corporativos
COLOR_AZUL = "#1f77b4"
COLOR_NARANJA = "#ff7f0e"
COLOR_ROJO = "#d62728"
COLOR_VERDE = "#2ca02c"
COLOR_MORADO = "#9467bd"
COLOR_GRIS = "#7f7f7f"

# Verificacion de librerias opcionales
TIENE_PMDARIMA = False
TIENE_PROPHET = False

try:
    import pmdarima as pm
    TIENE_PMDARIMA = True
except ImportError:
    pass

try:
    from prophet import Prophet
    TIENE_PROPHET = True
except ImportError:
    pass


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def banner(titulo, ancho=78):
    """Imprime un banner decorativo para separar secciones."""
    linea = "=" * ancho
    print(f"\n{linea}")
    print(f"  {titulo.upper()}")
    print(f"{linea}\n")


def sub_banner(titulo, ancho=78):
    """Imprime un sub-banner para subsecciones."""
    print(f"\n{'-' * ancho}")
    print(f"  {titulo}")
    print(f"{'-' * ancho}\n")


def guardar_figura(nombre_archivo, fig=None):
    """Guarda la figura actual en el directorio de salida."""
    ruta = os.path.join(DIRECTORIO_SALIDA, nombre_archivo)
    if fig is not None:
        fig.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="white")
    else:
        plt.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close("all")
    print(f"  [GUARDADO] {ruta}")
    return ruta


def tabla_formateada(df, titulo=""):
    """Imprime una tabla pandas con formato legible."""
    if titulo:
        print(f"\n  {titulo}")
        print(f"  {'-' * len(titulo)}")
    print(df.to_string(index=True))
    print()


def calcular_metricas(y_real, y_pred, nombre="Modelo"):
    """Calcula metricas de error para evaluar un modelo de pronostico."""
    y_real = np.array(y_real).flatten()
    y_pred = np.array(y_pred).flatten()

    # Asegurar misma longitud
    n = min(len(y_real), len(y_pred))
    y_real = y_real[:n]
    y_pred = y_pred[:n]

    errores = y_real - y_pred
    rmse = np.sqrt(np.mean(errores ** 2))
    mae = np.mean(np.abs(errores))
    # MAPE: evitar division por cero
    mask = y_real != 0
    mape = np.mean(np.abs(errores[mask] / y_real[mask])) * 100
    # R-cuadrado
    ss_res = np.sum(errores ** 2)
    ss_tot = np.sum((y_real - np.mean(y_real)) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    return {
        "Modelo": nombre,
        "RMSE": round(rmse, 2),
        "MAE": round(mae, 2),
        "MAPE (%)": round(mape, 2),
        "R2": round(r2, 4),
    }


# ============================================================================
# DATOS DE RESPALDO (AirPassengers en linea)
# Se usan si la descarga desde GitHub falla.
# ============================================================================

DATOS_AIRPASSENGERS = {
    "Month": [
        "1949-01", "1949-02", "1949-03", "1949-04", "1949-05", "1949-06",
        "1949-07", "1949-08", "1949-09", "1949-10", "1949-11", "1949-12",
        "1950-01", "1950-02", "1950-03", "1950-04", "1950-05", "1950-06",
        "1950-07", "1950-08", "1950-09", "1950-10", "1950-11", "1950-12",
        "1951-01", "1951-02", "1951-03", "1951-04", "1951-05", "1951-06",
        "1951-07", "1951-08", "1951-09", "1951-10", "1951-11", "1951-12",
        "1952-01", "1952-02", "1952-03", "1952-04", "1952-05", "1952-06",
        "1952-07", "1952-08", "1952-09", "1952-10", "1952-11", "1952-12",
        "1953-01", "1953-02", "1953-03", "1953-04", "1953-05", "1953-06",
        "1953-07", "1953-08", "1953-09", "1953-10", "1953-11", "1953-12",
        "1954-01", "1954-02", "1954-03", "1954-04", "1954-05", "1954-06",
        "1954-07", "1954-08", "1954-09", "1954-10", "1954-11", "1954-12",
        "1955-01", "1955-02", "1955-03", "1955-04", "1955-05", "1955-06",
        "1955-07", "1955-08", "1955-09", "1955-10", "1955-11", "1955-12",
        "1956-01", "1956-02", "1956-03", "1956-04", "1956-05", "1956-06",
        "1956-07", "1956-08", "1956-09", "1956-10", "1956-11", "1956-12",
        "1957-01", "1957-02", "1957-03", "1957-04", "1957-05", "1957-06",
        "1957-07", "1957-08", "1957-09", "1957-10", "1957-11", "1957-12",
        "1958-01", "1958-02", "1958-03", "1958-04", "1958-05", "1958-06",
        "1958-07", "1958-08", "1958-09", "1958-10", "1958-11", "1958-12",
        "1959-01", "1959-02", "1959-03", "1959-04", "1959-05", "1959-06",
        "1959-07", "1959-08", "1959-09", "1959-10", "1959-11", "1959-12",
        "1960-01", "1960-02", "1960-03", "1960-04", "1960-05", "1960-06",
        "1960-07", "1960-08", "1960-09", "1960-10", "1960-11", "1960-12",
    ],
    "pasajeros": [
        112, 118, 132, 129, 121, 135, 148, 148, 136, 119, 104, 118,
        115, 126, 141, 135, 125, 149, 170, 170, 158, 133, 114, 140,
        145, 150, 178, 163, 172, 178, 199, 199, 184, 162, 146, 166,
        171, 180, 193, 181, 183, 218, 230, 242, 209, 191, 172, 194,
        196, 196, 236, 235, 229, 243, 264, 272, 237, 211, 180, 201,
        204, 188, 235, 227, 234, 264, 302, 293, 259, 229, 203, 229,
        242, 233, 267, 269, 270, 315, 364, 347, 312, 274, 237, 278,
        284, 277, 317, 313, 318, 374, 413, 405, 355, 306, 271, 306,
        315, 301, 356, 348, 355, 422, 465, 467, 404, 347, 305, 336,
        340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337,
        360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405,
        417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432,
    ],
}


# ############################################################################
#                        PROGRAMA PRINCIPAL
# ############################################################################

def main():
    """Funcion principal que ejecuta todo el analisis de series temporales."""

    archivos_generados = []  # Registro de archivos de salida

    print("\n" + "#" * 78)
    print("#" + " " * 76 + "#")
    print("#   ANALISIS COMPLETO DE SERIES TEMPORALES - METODOLOGIA BOX-JENKINS" +
          " " * 8 + "#")
    print("#   Dataset: AirPassengers (Pasajeros de aerolineas, 1949-1960)" +
          " " * 13 + "#")
    print("#   Profesor: Juan Marcelo Gutierrez Miranda (@TodoEconometria)" +
          " " * 14 + "#")
    print("#" + " " * 76 + "#")
    print("#" * 78)

    # Informacion del entorno
    print(f"\n  Python version:      {sys.version.split()[0]}")
    print(f"  NumPy version:       {np.__version__}")
    print(f"  Pandas version:      {pd.__version__}")
    print(f"  Statsmodels version: {sm.__version__}")
    print(f"  Matplotlib version:  {matplotlib.__version__}")
    print(f"  pmdarima disponible: {'SI' if TIENE_PMDARIMA else 'NO (se usara busqueda manual)'}")
    print(f"  Prophet disponible:  {'SI' if TIENE_PROPHET else 'NO (se omitira seccion Prophet)'}")
    print(f"  Directorio salida:   {DIRECTORIO_SALIDA}")

    # ========================================================================
    # PARTE 1: CARGA Y EXPLORACION DE DATOS
    # ========================================================================
    banner("PARTE 1: CARGA Y EXPLORACION DE DATOS")

    # Intentar descargar desde GitHub
    print("  Intentando descargar dataset AirPassengers desde GitHub...")
    try:
        url = ("https://raw.githubusercontent.com/jbrownlee/Datasets/"
               "master/airline-passengers.csv")
        df = pd.read_csv(url, parse_dates=["Month"], index_col="Month")
        df.columns = ["pasajeros"]
        print("  [OK] Datos descargados exitosamente desde GitHub.\n")
    except Exception as e:
        print(f"  [AVISO] No se pudo descargar: {e}")
        print("  Usando datos de respaldo incorporados en el script.\n")
        df = pd.DataFrame(DATOS_AIRPASSENGERS)
        df["Month"] = pd.to_datetime(df["Month"])
        df = df.set_index("Month")

    # Asegurar frecuencia mensual
    df.index.freq = "MS"
    serie = df["pasajeros"]

    # --- Estadisticas descriptivas ---
    sub_banner("1.1 Estadisticas Descriptivas")
    estadisticas = pd.DataFrame({
        "Estadistico": [
            "Numero de observaciones",
            "Valor minimo",
            "Valor maximo",
            "Media",
            "Mediana",
            "Desviacion estandar",
            "Coeficiente de variacion (%)",
            "Asimetria (skewness)",
            "Curtosis (kurtosis)",
            "Primer periodo",
            "Ultimo periodo",
        ],
        "Valor": [
            len(serie),
            serie.min(),
            serie.max(),
            round(serie.mean(), 2),
            round(serie.median(), 2),
            round(serie.std(), 2),
            round((serie.std() / serie.mean()) * 100, 2),
            round(serie.skew(), 4),
            round(serie.kurtosis(), 4),
            str(serie.index[0].date()),
            str(serie.index[-1].date()),
        ],
    })
    tabla_formateada(estadisticas, "TABLA DE ESTADISTICAS DESCRIPTIVAS")

    # --- Grafico de la serie original ---
    sub_banner("1.2 Grafico de la Serie Original")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(serie.index, serie.values, color=COLOR_AZUL, linewidth=1.5,
            label="Pasajeros mensuales")
    ax.set_title("Serie Temporal: Pasajeros de Aerolineas (1949-1960)",
                 fontweight="bold")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Numero de pasajeros (miles)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ruta = guardar_figura("01_serie_original.png", fig)
    archivos_generados.append(ruta)

    # --- Descomposicion estacional ---
    sub_banner("1.3 Descomposicion Estacional (Aditiva y Multiplicativa)")

    print("  La descomposicion separa la serie en tres componentes:")
    print("    - Tendencia: direccion general a largo plazo")
    print("    - Estacionalidad: patron repetitivo en un periodo fijo")
    print("    - Residuo: variacion aleatoria no explicada\n")

    # Descomposicion multiplicativa (apropiada cuando la amplitud estacional crece)
    descomposicion = seasonal_decompose(serie, model="multiplicative", period=12)

    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    descomposicion.observed.plot(ax=axes[0], color=COLOR_AZUL)
    axes[0].set_ylabel("Observado")
    axes[0].set_title("Descomposicion Multiplicativa de la Serie Temporal",
                      fontweight="bold")

    descomposicion.trend.plot(ax=axes[1], color=COLOR_NARANJA)
    axes[1].set_ylabel("Tendencia")

    descomposicion.seasonal.plot(ax=axes[2], color=COLOR_VERDE)
    axes[2].set_ylabel("Estacionalidad")

    descomposicion.resid.plot(ax=axes[3], color=COLOR_ROJO)
    axes[3].set_ylabel("Residuo")
    axes[3].set_xlabel("Fecha")

    fig.tight_layout()
    ruta = guardar_figura("02_descomposicion.png", fig)
    archivos_generados.append(ruta)

    print("  INTERPRETACION:")
    print("  - La tendencia muestra crecimiento sostenido de pasajeros.")
    print("  - La estacionalidad indica picos en meses de verano (julio-agosto).")
    print("  - La amplitud estacional crece con el nivel => modelo multiplicativo.")

    # ========================================================================
    # PARTE 2: PRUEBAS DE ESTACIONARIEDAD
    # ========================================================================
    banner("PARTE 2: PRUEBAS DE ESTACIONARIEDAD")

    print("  Una serie es estacionaria cuando sus propiedades estadisticas")
    print("  (media, varianza, autocorrelacion) no cambian con el tiempo.")
    print("  Los modelos ARIMA requieren series estacionarias.\n")

    # --- ACF y PACF de la serie original ---
    sub_banner("2.1 ACF y PACF de la Serie Original")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    plot_acf(serie, ax=axes[0], lags=40, title="ACF - Serie Original")
    plot_pacf(serie, ax=axes[1], lags=40, title="PACF - Serie Original",
              method="ywm")
    fig.suptitle("Funciones de Autocorrelacion - Serie Original",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    ruta = guardar_figura("03_acf_pacf_original.png", fig)
    archivos_generados.append(ruta)

    print("  La ACF decrece lentamente => indica no estacionariedad.")
    print("  Picos estacionales cada 12 lags => estacionalidad presente.\n")

    # --- Test ADF (Augmented Dickey-Fuller) ---
    sub_banner("2.2 Test ADF (Augmented Dickey-Fuller) - Serie Original")
    print("  Hipotesis nula (H0): La serie tiene raiz unitaria (NO estacionaria)")
    print("  Hipotesis alternativa (H1): La serie es estacionaria\n")

    resultado_adf = adfuller(serie, autolag="AIC")

    tabla_adf = pd.DataFrame({
        "Concepto": [
            "Estadistico ADF",
            "p-valor",
            "Lags utilizados",
            "Observaciones usadas",
            "Valor critico (1%)",
            "Valor critico (5%)",
            "Valor critico (10%)",
            "CONCLUSION",
        ],
        "Valor": [
            round(resultado_adf[0], 6),
            round(resultado_adf[1], 6),
            resultado_adf[2],
            resultado_adf[3],
            round(resultado_adf[4]["1%"], 6),
            round(resultado_adf[4]["5%"], 6),
            round(resultado_adf[4]["10%"], 6),
            "NO ESTACIONARIA (p > 0.05)" if resultado_adf[1] > 0.05
            else "ESTACIONARIA (p <= 0.05)",
        ],
    })
    tabla_formateada(tabla_adf, "RESULTADO DEL TEST ADF")

    # --- Test KPSS ---
    sub_banner("2.3 Test KPSS (Kwiatkowski-Phillips-Schmidt-Shin) - Serie Original")
    print("  Hipotesis nula (H0): La serie es estacionaria (en tendencia)")
    print("  Hipotesis alternativa (H1): La serie NO es estacionaria")
    print("  NOTA: La interpretacion es OPUESTA al test ADF.\n")

    resultado_kpss = kpss(serie, regression="ct", nlags="auto")

    tabla_kpss = pd.DataFrame({
        "Concepto": [
            "Estadistico KPSS",
            "p-valor",
            "Lags utilizados",
            "Valor critico (10%)",
            "Valor critico (5%)",
            "Valor critico (2.5%)",
            "Valor critico (1%)",
            "CONCLUSION",
        ],
        "Valor": [
            round(resultado_kpss[0], 6),
            round(resultado_kpss[1], 6),
            resultado_kpss[2],
            round(resultado_kpss[3]["10%"], 6),
            round(resultado_kpss[3]["5%"], 6),
            round(resultado_kpss[3]["2.5%"], 6),
            round(resultado_kpss[3]["1%"], 6),
            "NO ESTACIONARIA (rechazamos H0)" if resultado_kpss[1] < 0.05
            else "ESTACIONARIA (no rechazamos H0)",
        ],
    })
    tabla_formateada(tabla_kpss, "RESULTADO DEL TEST KPSS")

    # --- Aplicar diferenciacion ---
    sub_banner("2.4 Diferenciacion para lograr Estacionariedad")
    print("  Aplicamos transformaciones para eliminar tendencia y estacionalidad:")
    print("    1. Transformacion logaritmica (estabilizar varianza)")
    print("    2. Primera diferencia (d=1, eliminar tendencia)")
    print("    3. Diferencia estacional (D=1, periodo s=12)\n")

    # Transformacion log para estabilizar varianza
    serie_log = np.log(serie)

    # Primera diferencia
    serie_diff1 = serie_log.diff().dropna()

    # Diferencia estacional sobre la primera diferencia
    serie_diff1_12 = serie_diff1.diff(12).dropna()

    # Grafico de las transformaciones
    fig, axes = plt.subplots(4, 1, figsize=(14, 14), sharex=False)

    axes[0].plot(serie, color=COLOR_AZUL)
    axes[0].set_title("Serie Original", fontweight="bold")
    axes[0].set_ylabel("Pasajeros")

    axes[1].plot(serie_log, color=COLOR_NARANJA)
    axes[1].set_title("Serie con Transformacion Logaritmica", fontweight="bold")
    axes[1].set_ylabel("Log(Pasajeros)")

    axes[2].plot(serie_diff1, color=COLOR_VERDE)
    axes[2].set_title("Primera Diferencia de Log(Pasajeros) [d=1]",
                      fontweight="bold")
    axes[2].set_ylabel("Diferencia")
    axes[2].axhline(y=0, color="black", linestyle="--", alpha=0.5)

    axes[3].plot(serie_diff1_12, color=COLOR_ROJO)
    axes[3].set_title(
        "Primera Diferencia + Diferencia Estacional [d=1, D=1, s=12]",
        fontweight="bold")
    axes[3].set_ylabel("Diferencia")
    axes[3].set_xlabel("Fecha")
    axes[3].axhline(y=0, color="black", linestyle="--", alpha=0.5)

    fig.tight_layout()
    ruta = guardar_figura("04_diferenciacion.png", fig)
    archivos_generados.append(ruta)

    # Test ADF sobre serie diferenciada
    sub_banner("2.5 Test ADF sobre Serie Diferenciada (d=1, D=1)")
    resultado_adf_diff = adfuller(serie_diff1_12, autolag="AIC")

    tabla_adf_diff = pd.DataFrame({
        "Concepto": [
            "Estadistico ADF",
            "p-valor",
            "Lags utilizados",
            "CONCLUSION",
        ],
        "Valor": [
            round(resultado_adf_diff[0], 6),
            round(resultado_adf_diff[1], 6),
            resultado_adf_diff[2],
            "ESTACIONARIA (p <= 0.05)" if resultado_adf_diff[1] <= 0.05
            else "NO ESTACIONARIA (p > 0.05)",
        ],
    })
    tabla_formateada(tabla_adf_diff, "TEST ADF - SERIE DIFERENCIADA")

    # ACF y PACF de la serie diferenciada
    sub_banner("2.6 ACF y PACF de la Serie Diferenciada")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    plot_acf(serie_diff1_12, ax=axes[0], lags=36,
             title="ACF - Serie Diferenciada (d=1, D=1)")
    plot_pacf(serie_diff1_12, ax=axes[1], lags=36,
              title="PACF - Serie Diferenciada (d=1, D=1)", method="ywm")
    fig.suptitle("Funciones de Autocorrelacion - Serie Diferenciada",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    ruta = guardar_figura("05_acf_pacf_diferenciada.png", fig)
    archivos_generados.append(ruta)

    print("  LECTURA DE ACF Y PACF PARA IDENTIFICAR ORDENES:")
    print("  -------------------------------------------------")
    print("  Parte NO estacional (lags 1, 2, 3, ...):")
    print("    - ACF se corta en lag 1 => q = 1 (MA)")
    print("    - PACF se corta en lag 1 => p = 1 (AR)")
    print("  Parte ESTACIONAL (lags 12, 24, 36, ...):")
    print("    - ACF se corta en lag 12 => Q = 1 (SMA)")
    print("    - PACF se corta en lag 12 => P = 1 (SAR)")
    print("  Diferenciacion: d = 1, D = 1, s = 12")
    print("  => Modelo candidato: SARIMA(1,1,1)(1,1,1)[12]\n")

    # ========================================================================
    # PARTE 3: IDENTIFICACION DEL MODELO
    # ========================================================================
    banner("PARTE 3: IDENTIFICACION DEL MODELO")

    print("  Buscamos la combinacion optima de parametros (p,d,q)(P,D,Q)[s]")
    print("  que minimice el criterio de informacion AIC (Akaike) o BIC.\n")

    # Trabajamos con la serie en escala logaritmica para el modelo
    serie_modelo = serie_log.copy()
    serie_modelo.index.freq = "MS"

    mejor_modelo_auto = None
    orden_auto = None
    orden_estacional_auto = None

    if TIENE_PMDARIMA:
        sub_banner("3.1 Busqueda Automatica con pmdarima (auto_arima)")
        print("  pmdarima prueba multiples combinaciones automaticamente...\n")

        modelo_auto = pm.auto_arima(
            serie_modelo,
            seasonal=True,
            m=12,
            d=1,
            D=1,
            start_p=0, max_p=3,
            start_q=0, max_q=3,
            start_P=0, max_P=2,
            start_Q=0, max_Q=2,
            trace=True,
            error_action="ignore",
            suppress_warnings=True,
            stepwise=True,
            information_criterion="aic",
        )
        orden_auto = modelo_auto.order
        orden_estacional_auto = modelo_auto.seasonal_order
        print(f"\n  Mejor modelo (auto_arima): SARIMA{orden_auto}"
              f"{orden_estacional_auto}")
        print(f"  AIC: {round(modelo_auto.aic(), 2)}")
    else:
        sub_banner("3.1 pmdarima no disponible - Se omite busqueda automatica")
        print("  Para instalar: pip install pmdarima")
        print("  Se procedera con busqueda manual (grid search).\n")

    # --- Busqueda manual (grid search) siempre se ejecuta ---
    sub_banner("3.2 Busqueda Manual (Grid Search) de Parametros SARIMA")

    # Rangos de busqueda
    p_rango = range(0, 3)
    d_fijo = 1
    q_rango = range(0, 3)
    P_rango = range(0, 2)
    D_fijo = 1
    Q_rango = range(0, 2)
    s_fijo = 12

    resultados_busqueda = []
    total_combinaciones = (len(list(p_rango)) * len(list(q_rango)) *
                           len(list(P_rango)) * len(list(Q_rango)))
    print(f"  Evaluando {total_combinaciones} combinaciones de parametros...")
    print("  (Esto puede tomar unos minutos)\n")

    contador = 0
    for p in range(0, 3):
        for q in range(0, 3):
            for P in range(0, 2):
                for Q in range(0, 2):
                    contador += 1
                    orden = (p, d_fijo, q)
                    orden_estacional = (P, D_fijo, Q, s_fijo)
                    try:
                        modelo_temp = SARIMAX(
                            serie_modelo,
                            order=orden,
                            seasonal_order=orden_estacional,
                            enforce_stationarity=False,
                            enforce_invertibility=False,
                        )
                        resultado_temp = modelo_temp.fit(disp=False, maxiter=200)
                        resultados_busqueda.append({
                            "Orden (p,d,q)": str(orden),
                            "Estacional (P,D,Q,s)": str(orden_estacional),
                            "AIC": round(resultado_temp.aic, 2),
                            "BIC": round(resultado_temp.bic, 2),
                            "Log-Likelihood": round(resultado_temp.llf, 2),
                        })
                    except Exception:
                        pass  # Algunos modelos no convergen, se ignoran

    # Ordenar por AIC
    df_resultados = pd.DataFrame(resultados_busqueda).sort_values("AIC")
    df_top5 = df_resultados.head(5).reset_index(drop=True)
    df_top5.index = df_top5.index + 1
    df_top5.index.name = "Ranking"

    tabla_formateada(df_top5, "TOP 5 MODELOS CANDIDATOS (ordenados por AIC)")

    # Seleccionar mejor modelo
    mejor = df_resultados.iloc[0]
    mejor_orden = eval(mejor["Orden (p,d,q)"])
    mejor_estacional = eval(mejor["Estacional (P,D,Q,s)"])

    print(f"  MEJOR MODELO SELECCIONADO (Grid Search):")
    print(f"    SARIMA{mejor_orden}{mejor_estacional}")
    print(f"    AIC = {mejor['AIC']}  |  BIC = {mejor['BIC']}\n")

    # Si auto_arima dio un resultado diferente, mencionarlo
    if TIENE_PMDARIMA and orden_auto is not None:
        if orden_auto != mejor_orden or orden_estacional_auto != mejor_estacional:
            print(f"  NOTA: auto_arima sugirio SARIMA{orden_auto}"
                  f"{orden_estacional_auto}")
            print("  Usaremos el modelo con menor AIC de la busqueda manual.\n")

    # ========================================================================
    # PARTE 4: ESTIMACION DEL MODELO
    # ========================================================================
    banner("PARTE 4: ESTIMACION DEL MODELO SARIMA")

    print(f"  Ajustando SARIMA{mejor_orden}{mejor_estacional} "
          f"con s=12 (mensual)...\n")

    modelo_final = SARIMAX(
        serie_modelo,
        order=mejor_orden,
        seasonal_order=mejor_estacional,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    resultado_final = modelo_final.fit(disp=False, maxiter=500)

    # Resumen del modelo
    sub_banner("4.1 Resumen Completo del Modelo")
    print(resultado_final.summary())

    # Tabla de coeficientes
    sub_banner("4.2 Tabla de Coeficientes Estimados")
    coeficientes = pd.DataFrame({
        "Coeficiente": resultado_final.params.index,
        "Valor": resultado_final.params.values.round(6),
        "Error Estandar": resultado_final.bse.values.round(6),
        "z-Estadistico": resultado_final.zvalues.values.round(4),
        "p-valor": resultado_final.pvalues.values.round(6),
        "Significativo (5%)": [
            "SI" if p < 0.05 else "NO" for p in resultado_final.pvalues.values
        ],
    })
    tabla_formateada(coeficientes, "COEFICIENTES DEL MODELO")

    # ========================================================================
    # PARTE 5: DIAGNOSTICO DE RESIDUOS
    # ========================================================================
    banner("PARTE 5: DIAGNOSTICO DE RESIDUOS")

    print("  Un buen modelo debe tener residuos que se comporten como")
    print("  ruido blanco: sin autocorrelacion, media cero, varianza constante.\n")

    # --- Graficos de diagnostico ---
    sub_banner("5.1 Graficos de Diagnostico")
    fig = resultado_final.plot_diagnostics(figsize=(14, 10))
    fig.suptitle("Diagnostico de Residuos del Modelo SARIMA",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    ruta = guardar_figura("06_diagnostico_residuos.png", fig)
    archivos_generados.append(ruta)

    residuos = resultado_final.resid

    # --- Test de Ljung-Box ---
    sub_banner("5.2 Test de Ljung-Box (Autocorrelacion de Residuos)")
    print("  H0: Los residuos son independientes (no hay autocorrelacion)")
    print("  H1: Existe autocorrelacion en los residuos\n")

    lb_resultado = acorr_ljungbox(residuos, lags=[10, 20, 30], return_df=True)
    lb_resultado.index.name = "Lags"
    lb_resultado["Conclusion"] = [
        "Sin autocorrelacion (OK)" if p > 0.05 else "HAY autocorrelacion (PROBLEMA)"
        for p in lb_resultado["lb_pvalue"]
    ]
    lb_resultado.columns = ["Estadistico LB", "p-valor", "Conclusion"]
    tabla_formateada(lb_resultado, "TEST DE LJUNG-BOX")

    # --- Test de Jarque-Bera ---
    sub_banner("5.3 Test de Jarque-Bera (Normalidad de Residuos)")
    print("  H0: Los residuos siguen una distribucion normal")
    print("  H1: Los residuos NO son normales\n")

    residuos_limpios = residuos.dropna()
    jb_resultado = sp_stats.jarque_bera(residuos_limpios)
    jb_stat = float(jb_resultado.statistic)
    jb_pvalor = float(jb_resultado.pvalue)
    jb_skew = float(sp_stats.skew(residuos_limpios))
    jb_kurtosis = float(sp_stats.kurtosis(residuos_limpios, fisher=False))

    tabla_jb = pd.DataFrame({
        "Concepto": [
            "Estadistico Jarque-Bera",
            "p-valor",
            "Asimetria (Skewness)",
            "Curtosis (Kurtosis)",
            "CONCLUSION",
        ],
        "Valor": [
            round(jb_stat, 4),
            round(jb_pvalor, 6),
            round(jb_skew, 4),
            round(jb_kurtosis, 4),
            "Residuos NORMALES (p > 0.05)" if jb_pvalor > 0.05
            else "Residuos NO normales (p <= 0.05)",
        ],
    })
    tabla_formateada(tabla_jb, "TEST DE JARQUE-BERA")

    # --- Resumen de diagnosticos ---
    sub_banner("5.4 Resumen de Diagnostico")

    # Ljung-Box a lag 20
    lb_pval_20 = lb_resultado.iloc[1]["p-valor"]
    diag_resumen = pd.DataFrame({
        "Prueba": [
            "Ljung-Box (lag=20)",
            "Jarque-Bera",
            "Media de residuos",
        ],
        "Estadistico": [
            round(lb_resultado.iloc[1]["Estadistico LB"], 4),
            round(jb_stat, 4),
            round(residuos.mean(), 6),
        ],
        "p-valor": [
            round(lb_pval_20, 6),
            round(jb_pvalor, 6),
            "N/A",
        ],
        "Conclusion": [
            "OK" if lb_pval_20 > 0.05 else "REVISAR",
            "OK" if jb_pvalor > 0.05 else "REVISAR",
            "OK (cercana a 0)" if abs(residuos.mean()) < 0.05 else "REVISAR",
        ],
    })
    tabla_formateada(diag_resumen, "RESUMEN DE PRUEBAS DE DIAGNOSTICO")

    # ========================================================================
    # PARTE 6: PRONOSTICO CON SARIMA
    # ========================================================================
    banner("PARTE 6: PRONOSTICO CON SARIMA")

    # Division train/test: ultimos 12 meses como test
    n_test = 12
    serie_train = serie_modelo[:-n_test]
    serie_test = serie_modelo[-n_test:]
    fecha_corte = serie_test.index[0]

    print(f"  Conjunto de entrenamiento: {serie_train.index[0].date()} a "
          f"{serie_train.index[-1].date()} ({len(serie_train)} obs)")
    print(f"  Conjunto de prueba:        {serie_test.index[0].date()} a "
          f"{serie_test.index[-1].date()} ({len(serie_test)} obs)")
    print(f"  Fecha de corte:            {fecha_corte.date()}\n")

    # Reajustar modelo solo con datos de entrenamiento
    sub_banner("6.1 Reajuste del Modelo con Datos de Entrenamiento")

    modelo_train = SARIMAX(
        serie_train,
        order=mejor_orden,
        seasonal_order=mejor_estacional,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    resultado_train = modelo_train.fit(disp=False, maxiter=500)

    # Valores ajustados (in-sample)
    ajuste_insample = resultado_train.fittedvalues

    # Pronostico para periodo de test (12 meses)
    sub_banner("6.2 Pronostico sobre Periodo de Test (12 meses)")
    pronostico_test = resultado_train.get_forecast(steps=n_test)
    pronostico_test_media = pronostico_test.predicted_mean
    pronostico_test_ci = pronostico_test.conf_int(alpha=0.05)

    # Metricas SARIMA en escala log
    metricas_sarima_log = calcular_metricas(
        serie_test.values,
        pronostico_test_media.values,
        "SARIMA (log)"
    )

    # Convertir a escala original para metricas reales
    test_original = np.exp(serie_test.values)
    pronostico_original = np.exp(pronostico_test_media.values)
    metricas_sarima = calcular_metricas(
        test_original,
        pronostico_original,
        "SARIMA"
    )

    print("  METRICAS DE PRONOSTICO (escala original):")
    for k, v in metricas_sarima.items():
        if k != "Modelo":
            print(f"    {k}: {v}")

    # Pronostico futuro (12 meses mas alla del dataset)
    sub_banner("6.3 Pronostico Futuro (12 meses mas alla del dataset)")

    # Reajustar con todos los datos
    resultado_completo = SARIMAX(
        serie_modelo,
        order=mejor_orden,
        seasonal_order=mejor_estacional,
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False, maxiter=500)

    n_futuro = 12
    pronostico_futuro = resultado_completo.get_forecast(steps=n_futuro)
    pronostico_futuro_media = pronostico_futuro.predicted_mean
    pronostico_futuro_ci = pronostico_futuro.conf_int(alpha=0.05)

    # Convertir a escala original
    pronostico_futuro_orig = np.exp(pronostico_futuro_media)
    ci_futuro_inf = np.exp(pronostico_futuro_ci.iloc[:, 0])
    ci_futuro_sup = np.exp(pronostico_futuro_ci.iloc[:, 1])

    # Tabla de pronosticos futuros
    df_pronostico = pd.DataFrame({
        "Fecha": pronostico_futuro_orig.index.strftime("%Y-%m"),
        "Pronostico": pronostico_futuro_orig.values.round(0).astype(int),
        "Limite Inferior (95%)": ci_futuro_inf.values.round(0).astype(int),
        "Limite Superior (95%)": ci_futuro_sup.values.round(0).astype(int),
    })
    df_pronostico.index = range(1, n_futuro + 1)
    df_pronostico.index.name = "Mes"
    tabla_formateada(df_pronostico, "PRONOSTICO PARA LOS PROXIMOS 12 MESES")

    # ========================================================================
    # PARTE 7: COMPARACION CON PROPHET (OPCIONAL)
    # ========================================================================
    banner("PARTE 7: COMPARACION CON PROPHET (OPCIONAL)")

    metricas_prophet = None

    if TIENE_PROPHET:
        print("  Prophet esta disponible. Ajustando modelo Prophet...\n")

        try:
            # Prophet requiere columnas 'ds' y 'y'
            df_prophet = pd.DataFrame({
                "ds": serie.index,
                "y": serie.values,
            })

            # Division train/test
            df_prophet_train = df_prophet.iloc[:-n_test]
            df_prophet_test = df_prophet.iloc[-n_test:]

            # Ajustar Prophet (modo silencioso)
            modelo_prophet = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
            )
            modelo_prophet.fit(df_prophet_train)

            # Pronostico
            futuro_prophet = modelo_prophet.make_future_dataframe(
                periods=n_test, freq="MS"
            )
            pred_prophet = modelo_prophet.predict(futuro_prophet)

            # Extraer pronostico del periodo test
            pred_test_prophet = pred_prophet.iloc[-n_test:]

            metricas_prophet = calcular_metricas(
                df_prophet_test["y"].values,
                pred_test_prophet["yhat"].values,
                "Prophet"
            )

            print("  METRICAS DE PRONOSTICO PROPHET (escala original):")
            for k, v in metricas_prophet.items():
                if k != "Modelo":
                    print(f"    {k}: {v}")

            # Pronostico futuro con Prophet (12 meses despues del dataset)
            df_prophet_full = pd.DataFrame({
                "ds": serie.index,
                "y": serie.values,
            })
            modelo_prophet_full = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
            )
            modelo_prophet_full.fit(df_prophet_full)
            futuro_full = modelo_prophet_full.make_future_dataframe(
                periods=n_futuro, freq="MS"
            )
            pred_full = modelo_prophet_full.predict(futuro_full)

            print("\n  [OK] Prophet ajustado exitosamente.")

        except Exception as e:
            print(f"  [ERROR] Prophet fallo durante el ajuste: {e}")
            print("  Se continuara sin Prophet.\n")
            metricas_prophet = None

    else:
        print("  Prophet NO esta instalado.")
        print("  Para instalarlo: pip install prophet")
        print("  Se omite esta seccion. El analisis continua solo con SARIMA.\n")

    # ========================================================================
    # PARTE 8: COMPARACION DE MODELOS - GRAFICO RADAR
    # ========================================================================
    banner("PARTE 8: COMPARACION DE MODELOS - METRICAS Y GRAFICO RADAR")

    # Tabla comparativa
    sub_banner("8.1 Tabla Comparativa de Metricas")

    lista_metricas = [metricas_sarima]
    if metricas_prophet is not None:
        lista_metricas.append(metricas_prophet)

    df_comparacion = pd.DataFrame(lista_metricas)
    df_comparacion = df_comparacion.set_index("Modelo")
    tabla_formateada(df_comparacion, "COMPARACION DE MODELOS")

    if metricas_prophet is not None:
        # Determinar ganador por metrica
        print("  GANADOR POR METRICA:")
        for col in ["RMSE", "MAE", "MAPE (%)"]:
            ganador = df_comparacion[col].idxmin()
            print(f"    {col}: {ganador} ({df_comparacion.loc[ganador, col]})")
        ganador_r2 = df_comparacion["R2"].idxmax()
        print(f"    R2:      {ganador_r2} ({df_comparacion.loc[ganador_r2, 'R2']})")
    else:
        print("  Solo se evaluo SARIMA (Prophet no disponible).\n")

    # --- Grafico Radar ---
    sub_banner("8.2 Grafico Radar de Metricas")

    categorias = ["RMSE", "MAE", "MAPE (%)", "R2"]

    # Normalizar metricas para el radar (0-1 scale)
    # Para RMSE, MAE, MAPE: menor es mejor => invertir escala
    # Para R2: mayor es mejor

    def normalizar_para_radar(metricas_dict):
        """Normaliza metricas a escala 0-1 para el radar chart."""
        vals = []
        for cat in categorias:
            v = metricas_dict[cat]
            if cat == "R2":
                # R2 va de 0 a 1, ya esta en buena escala.
                # Clamp al rango [0, 1]
                vals.append(max(0, min(1, v)))
            elif cat == "MAPE (%)":
                # Invertir: 0% error => 1.0, 100% error => 0.0
                vals.append(max(0, 1 - v / 100))
            else:
                # Para RMSE y MAE usaremos el valor maximo observado como referencia
                vals.append(v)  # Se normalizara despues
        return vals

    valores_sarima = normalizar_para_radar(metricas_sarima)

    if metricas_prophet is not None:
        valores_prophet = normalizar_para_radar(metricas_prophet)

        # Normalizar RMSE y MAE usando el maximo de ambos
        for i, cat in enumerate(categorias):
            if cat in ["RMSE", "MAE"]:
                max_val = max(valores_sarima[i], valores_prophet[i])
                if max_val > 0:
                    valores_sarima[i] = 1 - valores_sarima[i] / (max_val * 1.2)
                    valores_prophet[i] = 1 - valores_prophet[i] / (max_val * 1.2)
                else:
                    valores_sarima[i] = 1.0
                    valores_prophet[i] = 1.0
    else:
        # Solo SARIMA: normalizar contra si mismo
        for i, cat in enumerate(categorias):
            if cat in ["RMSE", "MAE"]:
                if valores_sarima[i] > 0:
                    # Poner en escala relativa: 0.7 como referencia
                    valores_sarima[i] = 0.7
                else:
                    valores_sarima[i] = 1.0

    # Crear grafico radar
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]  # Cerrar el poligono

    valores_sarima_cerrado = valores_sarima + [valores_sarima[0]]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.plot(angulos, valores_sarima_cerrado, "o-", linewidth=2,
            color=COLOR_AZUL, label="SARIMA", markersize=8)
    ax.fill(angulos, valores_sarima_cerrado, alpha=0.15, color=COLOR_AZUL)

    if metricas_prophet is not None:
        valores_prophet_cerrado = valores_prophet + [valores_prophet[0]]
        ax.plot(angulos, valores_prophet_cerrado, "s-", linewidth=2,
                color=COLOR_ROJO, label="Prophet", markersize=8)
        ax.fill(angulos, valores_prophet_cerrado, alpha=0.15, color=COLOR_ROJO)

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, fontsize=12, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.set_title("Comparacion de Modelos - Grafico Radar\n"
                 "(Valores mas altos = mejor desempeno)",
                 fontweight="bold", pad=20, fontsize=13)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=11)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    ruta = guardar_figura("07_radar_comparacion.png", fig)
    archivos_generados.append(ruta)

    # ========================================================================
    # PARTE 9: GRAFICO FINAL CONSOLIDADO
    # ========================================================================
    banner("PARTE 9: GRAFICO FINAL CONSOLIDADO")

    print("  Generando grafico final con serie original, ajuste y pronostico...\n")

    # Valores ajustados (in-sample) en escala original
    ajuste_completo = resultado_completo.fittedvalues
    ajuste_completo_orig = np.exp(ajuste_completo)

    # Pronostico futuro en escala original
    pronostico_futuro_orig_serie = np.exp(pronostico_futuro_media)
    ci_inf = np.exp(pronostico_futuro_ci.iloc[:, 0])
    ci_sup = np.exp(pronostico_futuro_ci.iloc[:, 1])

    fig, ax = plt.subplots(figsize=(16, 8))

    # Serie original
    ax.plot(serie.index, serie.values, color=COLOR_AZUL, linewidth=1.8,
            label="Serie Original", zorder=3)

    # Ajuste in-sample
    ax.plot(ajuste_completo_orig.index, ajuste_completo_orig.values,
            color=COLOR_NARANJA, linewidth=1.2, linestyle="--",
            label="Ajuste SARIMA", alpha=0.8, zorder=2)

    # Pronostico futuro
    ax.plot(pronostico_futuro_orig_serie.index,
            pronostico_futuro_orig_serie.values,
            color=COLOR_ROJO, linewidth=2.5, label="Pronostico",
            marker="o", markersize=5, zorder=4)

    # Intervalo de confianza 95%
    ax.fill_between(ci_inf.index, ci_inf.values, ci_sup.values,
                    color=COLOR_ROJO, alpha=0.15,
                    label="Intervalo de Confianza 95%", zorder=1)

    # Linea vertical en el punto de corte (fin de datos originales)
    ax.axvline(x=serie.index[-1], color=COLOR_GRIS, linestyle="--",
               linewidth=1.5, alpha=0.7, label="Fin de datos historicos")

    # Anotacion
    ax.annotate(
        "Zona de\nPronostico",
        xy=(pronostico_futuro_orig_serie.index[3],
            pronostico_futuro_orig_serie.values[3]),
        xytext=(pronostico_futuro_orig_serie.index[0],
                pronostico_futuro_orig_serie.values.max() * 1.08),
        fontsize=10, fontweight="bold", color=COLOR_ROJO,
        arrowprops=dict(arrowstyle="->", color=COLOR_ROJO, lw=1.5),
    )

    ax.set_title(
        f"Serie Temporal: Pasajeros de Aerolineas - "
        f"Modelo SARIMA{mejor_orden}{mejor_estacional}\n"
        f"Pronostico a 12 meses con Intervalo de Confianza al 95%",
        fontweight="bold", fontsize=14
    )
    ax.set_xlabel("Fecha", fontsize=12)
    ax.set_ylabel("Numero de pasajeros (miles)", fontsize=12)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    # Texto informativo en la esquina
    texto_info = (f"RMSE = {metricas_sarima['RMSE']}  |  "
                  f"MAE = {metricas_sarima['MAE']}  |  "
                  f"MAPE = {metricas_sarima['MAPE (%)']}%  |  "
                  f"R2 = {metricas_sarima['R2']}")
    ax.text(0.5, -0.08, texto_info, transform=ax.transAxes,
            fontsize=10, ha="center", style="italic", color=COLOR_GRIS,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow",
                      alpha=0.8))

    fig.tight_layout()
    ruta = guardar_figura("08_grafico_final.png", fig)
    archivos_generados.append(ruta)

    # ========================================================================
    # PARTE 10: TABLA FINAL Y EXPORTACION
    # ========================================================================
    banner("PARTE 10: TABLA FINAL Y EXPORTACION DE RESULTADOS")

    # --- Tabla: ultimos 5 valores originales + proximos 5 pronosticados ---
    sub_banner("10.1 Comparacion de Valores Originales vs Pronosticados")

    ultimos_5 = serie.tail(5)
    primeros_5_pron = pronostico_futuro_orig_serie.head(5)

    # Construir tabla combinada
    filas_tabla_final = []
    for fecha, valor in ultimos_5.items():
        filas_tabla_final.append({
            "Fecha": fecha.strftime("%Y-%m"),
            "Valor Original": int(valor),
            "Valor Predicho": "--",
            "Tipo": "Historico",
        })
    for fecha, valor in primeros_5_pron.items():
        filas_tabla_final.append({
            "Fecha": fecha.strftime("%Y-%m"),
            "Valor Original": "--",
            "Valor Predicho": int(round(valor)),
            "Tipo": "Pronostico",
        })

    df_tabla_final = pd.DataFrame(filas_tabla_final)
    df_tabla_final.index = range(1, len(df_tabla_final) + 1)
    df_tabla_final.index.name = "#"
    tabla_formateada(df_tabla_final,
                     "ULTIMOS 5 VALORES HISTORICOS + PROXIMOS 5 PRONOSTICADOS")

    # --- Guardar resultados como CSV ---
    sub_banner("10.2 Exportacion a CSV")

    # CSV del pronostico completo
    ruta_csv_pronostico = os.path.join(DIRECTORIO_SALIDA,
                                       "pronostico_sarima.csv")
    df_pronostico_export = pd.DataFrame({
        "Fecha": pronostico_futuro_orig_serie.index,
        "Pronostico": pronostico_futuro_orig_serie.values.round(0),
        "Limite_Inferior_95": ci_futuro_inf.values.round(0),
        "Limite_Superior_95": ci_futuro_sup.values.round(0),
    })
    df_pronostico_export.to_csv(ruta_csv_pronostico, index=False)
    print(f"  [GUARDADO] {ruta_csv_pronostico}")
    archivos_generados.append(ruta_csv_pronostico)

    # CSV de la tabla comparativa
    ruta_csv_tabla = os.path.join(DIRECTORIO_SALIDA,
                                  "tabla_comparacion_final.csv")
    df_tabla_final.to_csv(ruta_csv_tabla)
    print(f"  [GUARDADO] {ruta_csv_tabla}")
    archivos_generados.append(ruta_csv_tabla)

    # CSV de metricas
    ruta_csv_metricas = os.path.join(DIRECTORIO_SALIDA,
                                     "metricas_modelos.csv")
    df_comparacion.to_csv(ruta_csv_metricas)
    print(f"  [GUARDADO] {ruta_csv_metricas}")
    archivos_generados.append(ruta_csv_metricas)

    # CSV del ranking de modelos
    ruta_csv_ranking = os.path.join(DIRECTORIO_SALIDA,
                                    "ranking_modelos_aic.csv")
    df_top5.to_csv(ruta_csv_ranking)
    print(f"  [GUARDADO] {ruta_csv_ranking}")
    archivos_generados.append(ruta_csv_ranking)

    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    banner("RESUMEN FINAL DE EJECUCION")

    print("  MODELO SELECCIONADO:")
    print(f"    SARIMA{mejor_orden}{mejor_estacional}")
    print(f"    AIC = {round(resultado_final.aic, 2)}  |  "
          f"BIC = {round(resultado_final.bic, 2)}")
    print()

    print("  METRICAS DE PRONOSTICO (sobre los ultimos 12 meses):")
    print(f"    RMSE:    {metricas_sarima['RMSE']}")
    print(f"    MAE:     {metricas_sarima['MAE']}")
    print(f"    MAPE:    {metricas_sarima['MAPE (%)']}%")
    print(f"    R2:      {metricas_sarima['R2']}")
    print()

    print("  ARCHIVOS GENERADOS:")
    print("  " + "-" * 70)
    for i, archivo in enumerate(archivos_generados, 1):
        nombre = os.path.basename(archivo)
        tipo = "PNG" if archivo.endswith(".png") else "CSV"
        print(f"    {i:2d}. [{tipo}] {nombre}")
        print(f"        Ruta: {archivo}")
    print("  " + "-" * 70)
    print(f"  Total: {len(archivos_generados)} archivos en '{DIRECTORIO_SALIDA}'")
    print()

    print("  CONCLUSION METODOLOGICA:")
    print("  " + "-" * 70)
    print("  La metodologia Box-Jenkins nos permitio:")
    print("    1. Identificar la no estacionariedad de la serie (ADF, KPSS)")
    print("    2. Determinar las diferenciaciones necesarias (d=1, D=1)")
    print("    3. Identificar los ordenes p, q, P, Q mediante ACF/PACF")
    print("    4. Estimar el modelo SARIMA optimo por criterio AIC")
    print("    5. Validar los supuestos del modelo (diagnostico de residuos)")
    print("    6. Generar pronosticos confiables con intervalos de confianza")
    print()
    print("  La serie AirPassengers presenta tendencia creciente y")
    print("  estacionalidad multiplicativa, patron tipico en datos de")
    print("  transporte y turismo. El modelo SARIMA captura adecuadamente")
    print("  ambos componentes tras la transformacion logaritmica.")
    print()

    print("=" * 78)
    print("  ANALISIS COMPLETADO EXITOSAMENTE")
    print("  @TodoEconometria - Prof. Juan Marcelo Gutierrez Miranda")
    print("=" * 78)
    print()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================
if __name__ == "__main__":
    main()


# -------------------------
# Autor original/Referencia: @TodoEconometria
# Profesor: Juan Marcelo Gutierrez Miranda
# Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
#              Desarrollo de aplicaciones con IA & Econometria Aplicada.
# Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
# Repositorio: https://github.com/TodoEconometria/certificaciones
#
# REFERENCIA ACADEMICA:
# - Box, G.E.P. & Jenkins, G.M. (1976). Time Series Analysis: Forecasting and Control. Holden-Day.
# - Hyndman, R.J. & Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3rd ed.). OTexts.
# - Taylor, S.J. & Letham, B. (2018). Forecasting at Scale. The American Statistician, 72(1), 37-45.
# - Hamilton, J.D. (1994). Time Series Analysis. Princeton University Press.
# -------------------------
