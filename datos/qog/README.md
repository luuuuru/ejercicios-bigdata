# 📊 Quality of Government Dataset

## Descripción

Panel data longitudinal con más de 1,000 variables sobre calidad gubernamental, democracia, corrupción y desarrollo económico.

- **Países:** 200+
- **Período temporal:** 1946-2023
- **Frecuencia:** Anual
- **Variables:** Democracia, corrupción, desarrollo, recursos naturales, instituciones

## 🔗 Fuente Oficial

**Quality of Government Institute**  
University of Gothenburg, Sweden

- **Website:** https://www.qogdata.pol.gu.se/
- **Versión:** Standard Time-Series (January 2024)
- **Licencia:** Creative Commons Attribution 4.0 International

## 📥 Descarga

### Opción 1: Script Automático (Recomendado)

```bash
python scripts/download_datasets.py --dataset qog
```

### Opción 2: Descarga Manual

1. Visita: https://www.qogdata.pol.gu.se/data/qog_std_ts_jan24.csv
2. Descarga el archivo CSV (~45MB)
3. Guárdalo en: `datos/qog/qog_std_ts_jan24.csv`

## 📖 Documentación

### Codebook Completo
- **PDF:** https://www.qogdata.pol.gu.se/data/codebook_std_jan24.pdf
- **Excel:** https://www.qogdata.pol.gu.se/data/codebook_std_jan24.xlsx

### Variables Principales

| Variable | Descripción | Fuente |
|----------|-------------|--------|
| `vdem_polyarchy` | Índice de democracia (0-1) | V-Dem |
| `polity2` | Régimen político (-10 a +10) | Polity V |
| `ti_cpi` | Índice de percepción de corrupción | Transparency International |
| `wbgi_cce` | Control de corrupción | World Bank |
| `wdi_gdppc` | PIB per cápita (USD constantes) | World Bank |
| `ross_oil_value` | Valor producción petróleo per cápita | Ross |
| `ross_gas_value` | Valor producción gas per cápita | Ross |
| `wdi_water` | Acceso a agua potable (% población) | World Bank |
| `wdi_sanit` | Acceso a saneamiento (% población) | World Bank |

Ver codebook completo para las 1,000+ variables disponibles.

## 🎓 Uso en el Curso

Este dataset se utiliza en:

- **Ejercicio 02:** Limpieza de datos y análisis exploratorio
- **Ejercicio 03:** Conversión a Parquet y procesamiento con Dask
- **Ejercicio 04:** Queries SQL con Apache Spark
- **Proyecto Final:** Análisis de panel data

## 📊 Estructura de Datos

### Formato Panel Data

```
| ccode | cname       | year | vdem_polyarchy | ti_cpi | wdi_gdppc |
|-------|-------------|------|----------------|--------|-----------|
| 4     | Afghanistan | 2000 | 0.15           | 18     | 450       |
| 4     | Afghanistan | 2001 | 0.14           | 17     | 420       |
| ...   | ...         | ...  | ...            | ...    | ...       |
| 724   | Spain       | 2022 | 0.85           | 60     | 30,500    |
| 724   | Spain       | 2023 | 0.86           | 61     | 31,200    |
```

### Identificadores

- **ccode:** Código numérico del país (Correlates of War)
- **cname:** Nombre del país
- **year:** Año de observación

## 📚 Cómo Citar

### Formato APA 7ª Edición

```
Teorell, J., Sundström, A., Holmberg, S., Rothstein, B., Pachon, N. A., 
Dalli, C. M., & Svensson, R. (2024). The Quality of Government Standard 
Dataset, version Jan24. University of Gothenburg: The Quality of Government 
Institute. https://www.gu.se/en/quality-government
```

### BibTeX

```bibtex
@misc{qog2024,
  author = {Teorell, Jan and Sundström, Aksel and Holmberg, Sören and 
            Rothstein, Bo and Pachon, Natalia Alvarado and Dalli, Cem Mert 
            and Svensson, Richard},
  title = {The Quality of Government Standard Dataset, version Jan24},
  year = {2024},
  publisher = {University of Gothenburg: The Quality of Government Institute},
  url = {https://www.gu.se/en/quality-government}
}
```

## 🔍 Ejemplos de Investigación

### Temas Comunes

1. **Democracia y Desarrollo**
   - Relación entre instituciones democráticas y crecimiento económico
   - Transiciones políticas post-autoritarias

2. **Corrupción y Gobernanza**
   - Efectos de la corrupción en el desarrollo
   - Calidad institucional y confianza ciudadana

3. **Recursos Naturales**
   - "Maldición de los recursos" (resource curse)
   - Petróleo, gas y desarrollo institucional

4. **Análisis Regional**
   - Asia Central post-soviética
   - América Latina
   - África Subsahariana

## 💡 Tips para Análisis

### Datos Faltantes

- Muchas variables tienen valores faltantes (NA)
- Verificar disponibilidad temporal por variable
- Considerar imputación o análisis con datos completos

### Regresiones de Panel

El dataset es ideal para:
- **Fixed Effects (FE):** Controlar heterogeneidad no observada por país
- **Random Effects (RE):** Si asumes no correlación con regresores
- **Difference-in-Differences (DiD):** Efectos causales de intervenciones

### Herramientas Recomendadas

**Python:**
```python
import pandas as pd
import dask.dataframe as dd
from linearmodels import PanelOLS

# Leer con Dask (para archivos grandes)
df = dd.read_csv('datos/qog/qog_std_ts_jan24.csv')

# Convertir a panel
df = df.set_index(['ccode', 'year'])
```

**R:**
```r
library(plm)
library(haven)

# Leer datos
qog <- read.csv("datos/qog/qog_std_ts_jan24.csv")

# Crear panel data
pdata <- pdata.frame(qog, index = c("ccode", "year"))
```

## 📞 Soporte

- **Preguntas sobre el dataset:** qog@pol.gu.se
- **Preguntas sobre el curso:** Ver README principal del repositorio

## 📄 Licencia

El dataset QoG está bajo licencia **CC BY 4.0**.  
Puedes usar, compartir y adaptar los datos con atribución apropiada.

---

**Última actualización:** Enero 2024  
**Próxima versión esperada:** Julio 2024
