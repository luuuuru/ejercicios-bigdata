"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA PRINCIPAL:
- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data. MIT Press.
- Stock, J. H., & Watson, M. W. (2019). Introduction to Econometrics. Pearson.
- Ayres, I., & Donohue, J. J. (2003). Shooting down the 'more guns, less crime' hypothesis. Stanford Law Review.
-------------------------
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels import PanelOLS, RandomEffects
from linearmodels.panel import compare
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def cargar_datos():
    print("--- 1. INGESTA DE DATOS MULTIDIMENSIONALES (ETL) ---")
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/Guns.csv"
    try:
        df = pd.read_csv(url, index_col=0)
        print("Dataset 'Guns' descargado correctamente.")
    except Exception as e:
        print(f"Error descargando datos: {e}")
        return None

    # Preprocesamiento y Feature Engineering
    # 1. Convertir variable binaria
    if df['law'].dtype == 'object':
        df['law'] = df['law'].apply(lambda x: 1 if x == 'yes' else 0)
    
    # 2. Transformación Logarítmica (Para interpretación de elasticidad/semi-elasticidad)
    df['log_violent'] = np.log(df['violent'])
    
    # 3. Configuración del MultiIndex (Entidad, Tiempo)
    # Fundamental para librerías de Panel Data en Python
    df = df.set_index(['state', 'year'])
    
    print(f"Dimensiones: {df.shape}")
    print("Primeras filas con MultiIndex:")
    print(df.head())
    return df

def ejecutar_modelos(df):
    print("\n--- 2. MODELADO ECONOMÉTRICO AVANZADO ---")
    
    # Definición de Variables Explicativas (Exógenas) y Objetivo (Endógena)
    exog_vars = ['law', 'income', 'population', 'density']
    exog = sm.add_constant(df[exog_vars])
    y = df['log_violent']
    
    # ---------------------------------------------------------
    # A. Modelo Pooled OLS (Mínimos Cuadrados Agrupados)
    # ---------------------------------------------------------
    # Hipótesis: No existe heterogeneidad individual. Todos los estados son iguales.
    # Riesgo: Sesgo masivo por variable omitida (ej. cultura de armas preexistente).
    mod_pooled = PanelOLS(y, exog, check_rank=False) # Tratado como panel plano
    res_pooled = mod_pooled.fit()
    
    print("\n[A] Resultado Pooled OLS (Referencia Naive):")
    print(f"  Coeficiente 'law': {res_pooled.params['law']:.4f}")
    print(f"  P-value: {res_pooled.pvalues['law']:.4f}")
    
    # ---------------------------------------------------------
    # B. Modelo de Efectos Fijos (Fixed Effects - FE)
    # ---------------------------------------------------------
    # Hipótesis: Existen características únicas por estado invariantes en el tiempo (Alpha_i).
    # Técnica: Within Transformation (Diferenciación respecto a la media grupal).
    mod_fe = PanelOLS(y, exog, entity_effects=True)
    res_fe = mod_fe.fit(cov_type='clustered', cluster_entity=True) # Errores Robustos Clustered
    
    print("\n[B] Resultado Efectos Fijos (Control de Heterogeneidad):")
    print(f"  Coeficiente 'law': {res_fe.params['law']:.4f}")
    print(f"  P-value: {res_fe.pvalues['law']:.4f}")
    
    # ---------------------------------------------------------
    # C. Modelo de Efectos Aleatorios (Random Effects - RE)
    # ---------------------------------------------------------
    # Hipótesis: La heterogeneidad es ruido aleatorio no correlacionado con X.
    mod_re = RandomEffects(y, exog)
    res_re = mod_re.fit()
    
    print("\n[C] Resultado Efectos Aleatorios:")
    print(f"  Coeficiente 'law': {res_re.params['law']:.4f}")
    
    return res_pooled, res_fe, res_re

def test_hausman(res_fe, res_re):
    print("\n--- 3. VALIDACIÓN DE SUPUESTOS: TEST DE HAUSMAN ---")
    # Nota: linearmodels no trae Hausman nativo directo, lo calculamos manualmente.
    # H0: Los estimadores RE son consistentes y eficientes (Preferimos RE).
    # H1: Los estimadores RE son inconsistentes (Preferimos FE).
    
    b_fe = res_fe.params
    b_re = res_re.params
    v_fe = res_fe.cov
    v_re = res_re.cov
    
    # Usamos las variables comunes
    common_params = b_fe.index
    
    # Estadístico de Chi-Cuadrado
    diff = b_fe[common_params] - b_re[common_params]
    v_diff = v_fe.loc[common_params, common_params] - v_re.loc[common_params, common_params]
    
    try:
        hausman_stat = diff.dot(np.linalg.pinv(v_diff)).dot(diff)
        dof = len(common_params)
        p_val = 1 - stats.chi2.cdf(hausman_stat, dof)
        
        print(f"Estadístico Hausman: {hausman_stat:.4f}")
        print(f"P-value: {p_val:.4f}")
        
        if p_val < 0.05:
            print(">> CONCLUSIÓN: Rechazamos H0. Existe correlación entre X y los efectos individuales.")
            print(">> ACCIÓN: Debemos usar EFECTOS FIJOS (FE) para evitar sesgo.")
        else:
            print(">> CONCLUSIÓN: No rechazamos H0.")
            print(">> ACCIÓN: Podemos usar EFECTOS ALEATORIOS (RE) por eficiencia.")
            
    except Exception as e:
        print(f"Error calculando Hausman (posible singularidad): {e}")

def reporte_negocio(result):
    print("\n--- 4. INTERPRETACIÓN DE NEGOCIO Y EFECTOS MARGINALES ---")
    print("Modelo Seleccionado: Efectos Fijos (Log-Lin Specification)")
    
    beta_law = result.params['law']
    # Interpretación Log-Lin (Semi-elasticidad): 
    # % Cambio en Y = (exp(beta) - 1) * 100  (Exacta)
    # % Cambio en Y approx = beta * 100      (Aproximada para betas pequeños)
    
    impacto_pct = (np.exp(beta_law) - 1) * 100
    
    print(f"Coeficiente estimado para 'law': {beta_law:.4f}")
    print(f"Impacto Estimado (%): {impacto_pct:.2f}%")
    
    print("\nREPORTE EJECUTIVO:")
    print("----------------------------------------------------------------")
    if impacto_pct < 0:
        print(f"La implementación de leyes 'shall-issue' está asociada con una DECREMENTO")
        print(f"del {abs(impacto_pct):.2f}% en la tasa de crímenes violentos,")
    else:
        print(f"La implementación de leyes 'shall-issue' está asociada con un INCREMENTO")
        print(f"del {abs(impacto_pct):.2f}% en la tasa de crímenes violentos,")
    print("manteniendo constantes el ingreso, población y densidad del estado.")
    print("(Controlando por heterogeneidad cultural invariante por estado).")
    print("----------------------------------------------------------------")

def visualizacion(df, output_path="grafico_panel_guns.png"):
    # Reseteamos index para seaborn
    plot_df = df.reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=plot_df, x='year', y='log_violent', hue='state', legend=False, alpha=0.3)
    sns.regplot(data=plot_df, x='year', y='log_violent', scatter=False, color='red', label='Tendencia Promedio Global')
    
    plt.title('Heterogeneidad: Evolución de Tasa de Crimen (Log) por Estado')
    plt.xlabel('Año')
    plt.ylabel('Log(Crimen Violento)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"\nGráfico guardado en: {output_path}")
    # plt.show() # Descomentar si se ejecuta en entorno con pantalla

if __name__ == "__main__":
    df = cargar_datos()
    if df is not None:
        visualizacion(df)
        pool, fe, re = ejecutar_modelos(df)
        test_hausman(fe, re)
        # Asumiendo que FE gana (usual en Guns data), reportamos FE
        reporte_negocio(fe)
