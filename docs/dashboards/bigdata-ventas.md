# Big Data y Analisis de Ventas

Dashboards construidos con D3.js que demuestran visualizacion de datos de ventas a gran escala.
Estos ejercicios conectan el procesamiento de Big Data con la presentacion ejecutiva de resultados.

---

## Dashboards interactivos

### Centro de Comando: Big Data Sales

Dashboard ejecutivo tipo "command center" con KPIs de ventas, tendencias temporales,
distribucion por categorias y metricas de rendimiento. Diseñado para escenarios de
monitoreo en tiempo real sobre datos particionados.

[Abrir Dashboard Big Data (interactivo)](dashboard_bigdata_d3.html){target="_blank" .md-button .md-button--primary}

**Tecnologias:** D3.js, JavaScript, CSS Grid

---

### Visualizacion D3.js: Scatter Plot Interactivo

Grafico de dispersion interactivo construido desde cero con D3.js.
Demuestra bindeo de datos, escalas, ejes, tooltips y transiciones animadas
sin depender de librerias de alto nivel.

[Abrir Visualizacion D3.js (interactivo)](visualizacion_d3.html){target="_blank" .md-button .md-button--primary}

**Tecnologias:** D3.js puro, SVG, JavaScript

---

## Contexto academico

El analisis de datos de ventas es uno de los casos de uso mas frecuentes en Big Data:

- **Volumen**: millones de transacciones diarias requieren procesamiento distribuido
- **Velocidad**: dashboards en tiempo real para toma de decisiones operativas
- **Variedad**: datos estructurados (transacciones) combinados con semi-estructurados (logs, clickstream)
- **Valor**: traduccion de patrones en acciones comerciales concretas

### Por que D3.js?

D3.js (Data-Driven Documents) es la libreria de referencia para visualizaciones web personalizadas:

- Control total sobre cada elemento visual (SVG, Canvas)
- Bindeo directo entre datos y elementos del DOM
- Transiciones y animaciones declarativas
- Escalabilidad para grandes volumenes de puntos de datos
- Estandar de la industria en periodismo de datos y dashboards ejecutivos

Estos dashboards ilustran como presentar resultados de pipelines de Big Data
en formatos comprensibles para audiencias no tecnicas.

---

## Codigo fuente

Los scripts y archivos HTML fueron generados como parte del modulo de procesamiento distribuido.
Utilizan datos sinteticos particionados (formato Parquet/CSV) procesados con Python y visualizados con D3.js.
