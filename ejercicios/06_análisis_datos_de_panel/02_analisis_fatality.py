"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA PRINCIPAL:
- Stock, J. H., & Watson, M. W. (2019). Introduction to Econometrics. Pearson.
- Rueben, K. (1997). The Impact of Alcohol Taxation on Traffic Fatalities.
-------------------------
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels import PanelOLS
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_datos_fatality():
    print("--- 1. INGESTA: DATASET FATALITY ---")
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/Fatalities.csv"
    try:
        df = pd.read_csv(url, index_col=0)
    except Exception as e:
        print(e)
        return None

    # Feature Engineering
    # Tasa de Fatalidad por 10,000 habitantes
    df['fatality_rate'] = (df['fatal'] / df['pop']) * 10000
    
    # MultiIndex
    df = df.set_index(['state', 'year'])
    print(f"Datos cargados. Shape: {df.shape}")
    return df

def modelado_bidireccional(df):
    print("\n--- 2. MODELADO: TWO-WAY FIXED EFFECTS ---")
    print("Objetivo: Aislar impacto de Impuesto Cerveza (beertax) en Muertes.")
    
    # Variables
    exog_vars = ['beertax', 'drinkage', 'unemp', 'income']
    exog = sm.add_constant(df[exog_vars])
    y = df['fatality_rate']
    
    # Modelo 1: Solo Efectos de Entidad (Entity FE)
    mod_ent = PanelOLS(y, exog, entity_effects=True)
    res_ent = mod_ent.fit(cov_type='clustered', cluster_entity=True)
    
    # Modelo 2: Efectos Bidireccionales (Entity + Time FE)
    # Controlamos por tendencias temporales (coches más seguros cada año)
    mod_two = PanelOLS(y, exog, entity_effects=True, time_effects=True)
    res_two = mod_two.fit(cov_type='clustered', cluster_entity=True)
    
    print("\n[A] Efectos Solo Entidad - Coeficiente 'beertax':")
    print(res_ent.summary.tables[1])
    
    print("\n[B] Efectos Bidireccionales (Entidad + Tiempo) - Coeficiente 'beertax':")
    print(res_two.summary.tables[1])
    
    return res_two

def interpretacion_negocio(res):
    print("\n--- 3. INSIGHT DE NEGOCIO ---")
    beta = res.params['beertax']
    p_val = res.pvalues['beertax']
    
    print(f"Sensibilidad al Impuesto (Beta): {beta:.4f}")
    
    if p_val < 0.05 and beta < 0:
        print("CONCLUSIÓN: El impuesto es EFECTIVO.")
        print("Existe evidencia estadística fuerte de que aumentar el impuesto a la cerveza")
        print("reduce la tasa de mortalidad en carreteras, controlando por")
        print("diferencias estatales y tendencias temporales.")
    else:
        print("CONCLUSIÓN: No concluyente.")
        print("No se encuentra evidencia robusta de que el impuesto reduzca muertes")
        print("bajo estas especificaciones del modelo.")

if __name__ == "__main__":
    df = cargar_datos_fatality()
    if df is not None:
        res = modelado_bidireccional(df)
        interpretacion_negocio(res)
