import panel as pn
import numpy as np
import pandas as pd
import altair as alt

pn.extension('vega')

def generate_and_plot(slope_within=(-1.0), intercept_gap=5.0, noise_level=1.0):
    """
    Genera datos sintéticos para demostrar cómo Pooled OLS falla comparado con Efectos Fijos.
    
    Escenario:
    Tenemos 3 'Ciudades' (Entidades).
    Dentro de cada ciudad, aumentar policía (X) reduce el crimen (Y) -> Pendiente Negativa (Correcto).
    Pero las ciudades con más policía son intrínsecamente más peligrosas (Intercepto más alto).
    
    Si ignoramos el panel (Pooled OLS), veremos una correlación POSITIVA (Incorrecto).
    """
    
    # Configuración de 3 Entidades (Grupos)
    n_points = 20
    groups = ['Ciudad A (Segura)', 'Ciudad B (Media)', 'Ciudad C (Peligrosa)']
    
    # Bases de X (Policía) para cada ciudad.
    # Ciudad A tiene poca policía, C tiene mucha.
    x_centers = [2, 5, 8]
    
    # Interceptos Reales (Heterogeneidad No Observada)
    # Ciudad C tiene mucho más crimen base que A.
    alphas = [2, 2 + intercept_gap, 2 + (intercept_gap * 2)] 
    
    data_list = []
    
    for i, group in enumerate(groups):
        # Generar X alrededor del centro del grupo
        x = np.random.normal(x_centers[i], 0.5, n_points)
        
        # Generar Y = Alpha_i + Beta * X + Error
        # Beta (slope_within) es el efecto REAL de la política.
        y = alphas[i] + slope_within * x + np.random.normal(0, noise_level, n_points)
        
        data_list.append(pd.DataFrame({'Policía (X)': x, 'Crimen (Y)': y, 'Entidad': group}))
        
    df = pd.concat(data_list)
    
    # 1. Ajuste Pooled (Incorrecto)
    # Regresión simple de Y sobre X ignorando grupos
    coef_pooled = np.polyfit(df['Policía (X)'], df['Crimen (Y)'], 1)
    line_pooled = pd.DataFrame({
        'Policía (X)': np.linspace(df['Policía (X)'].min(), df['Policía (X)'].max(), 100),
        'Entidad': 'Modelo Global (Pooled OLS)'
    })
    line_pooled['Crimen (Y)'] = coef_pooled[1] + coef_pooled[0] * line_pooled['Policía (X)']
    
    # 2. Ajuste Efectos Fijos (Correcto)
    # Una linea por grupo, misma pendiente (slope_within teórica aprox, o estimada)
    # Para visualización simple usaremos la pendiente real generadora para mostrar el ideal
    lines_fe_list = []
    for i, group in enumerate(groups):
        # Usamos la pendiente real para ilustrar "Fixed Effects" visualmente perfecto
        # En la práctica, el modelo estimaría esto.
        x_range = np.linspace(df[df['Entidad']==group]['Policía (X)'].min(), 
                              df[df['Entidad']==group]['Policía (X)'].max(), 10)
        y_pred = alphas[i] + slope_within * x_range # Usamos slope generadora para claridad didáctica
        
        lines_fe_list.append(pd.DataFrame({
            'Policía (X)': x_range,
            'Crimen (Y)': y_pred,
            'Entidad': group # Usamos el mismo color del grupo
        }))
    df_fe_lines = pd.concat(lines_fe_list)

    # Gráfico Altair
    
    # Puntos de datos
    points = alt.Chart(df).mark_circle(size=60).encode(
        x='Policía (X)',
        y='Crimen (Y)',
        color='Entidad',
        tooltip=['Entidad', 'Policía (X)', 'Crimen (Y)']
    )
    
    # Línea Pooled (Mala Interpretación)
    line_plot_pooled = alt.Chart(line_pooled).mark_line(strokeDash=[5, 5], color='red', size=3).encode(
        x='Policía (X)',
        y='Crimen (Y)'
    )
    
    # Texto explicando la línea pooled
    text_pooled = alt.Chart(pd.DataFrame({'x': [5], 'y': [line_pooled['Crimen (Y)'].mean() + 2], 't': ['Efecto Percibido (Falso)']})).mark_text(color='red').encode(
        x='x', y='y', text='t'
    )

    # Líneas Fixed Effects (Interpretación Correcta)
    lines_fe_plot = alt.Chart(df_fe_lines).mark_line(size=3).encode(
        x='Policía (X)',
        y='Crimen (Y)',
        color='Entidad'
    )
    
    return (points + line_plot_pooled + lines_fe_plot + text_pooled).properties(
        width=700, height=400,
        title=f"Paradoja de Simpson en Panel Data: Pendiente Global {coef_pooled[0]:.2f} (Roja) vs Real {slope_within} (Grupos)"
    )

# Widgets
slope_slider = pn.widgets.FloatSlider(name='Efecto Real de la Política (Pendiente)', start=-3.0, end=1.0, value=-1.0, step=0.5)
gap_slider = pn.widgets.FloatSlider(name='Heterogeneidad (Diferencia entre Interceptos)', start=0.0, end=10.0, value=5.0)

# Layout
text_intro = """
# Visualizador Didáctico: El Problema de la Heterogeneidad No Observada

### ¿Por qué necesitamos "Efectos Fijos"?

En este simulador controlas la realidad:
1. **Efecto Real**: Aumentar X reduce Y (Pendiente negativa).
2. **Heterogeneidad**: Grupos con ALTO X también tienen ALTO Y basal (por razones externas).

Observa la **Línea Roja Punteada** (Pooled OLS). ¿Ves cómo sube aunque el efecto real sea bajar?
Eso es el **Sesgo**. El modelo cree que X causa Y, pero en realidad **X está correlacionado con la Entidad**.
"""

dashboard = pn.Column(
    text_intro,
    pn.Row(slope_slider, gap_slider),
    pn.bind(generate_and_plot, slope_within=slope_slider, intercept_gap=gap_slider)
)

# Servir (para correr localmente se usaria .show() o panel serve)
if __name__ == '__main__':
    dashboard.show()
