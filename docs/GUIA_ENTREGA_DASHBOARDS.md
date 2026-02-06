# Guia de Entrega de Dashboards

Esta guia explica como crear y entregar dashboards para el curso.

---

!!! danger "Sistema de Evaluacion por PROMPTS"
    **NO se usan Pull Requests.** El sistema evalua tu archivo `PROMPTS.md`
    directamente en tu fork. Solo necesitas hacer `git push`.

---

## Resumen del Flujo

```
1. Trabajas en TU fork (tu copia del repositorio)
2. Creas tu dashboard en la carpeta correcta
3. Documentas tus prompts de IA en PROMPTS.md
4. Subes con: git add . && git commit -m "mensaje" && git push
5. El sistema evalua automaticamente tu PROMPTS.md
```

---

## Estructura del Proyecto

```
dashboards/
├── nyc_taxi_eda/          # Ejemplo de referencia del profesor
│   ├── app.py
│   ├── templates/
│   └── README.md
└── tu-nombre-dashboard/   # Tu dashboard aqui
    ├── app.py
    ├── templates/
    ├── PROMPTS.md         # LO MAS IMPORTANTE - Tus prompts de IA
    └── README.md
```

---

## Pasos para Entregar tu Dashboard

### 1. Actualizar tu Fork

Antes de empezar, asegurate de tener la ultima version:

```bash
git fetch upstream
git merge upstream/main
```

---

### 2. Crear tu Carpeta de Dashboard

Crea una carpeta dentro de `dashboards/` con tu nombre:

```
dashboards/
└── tu-nombre-dashboard/
    ├── app.py              # Tu aplicacion Flask
    ├── templates/          # Tus archivos HTML
    │   └── index.html
    ├── static/             # CSS, JS, imagenes (opcional)
    ├── PROMPTS.md          # OBLIGATORIO - Tus prompts de IA
    └── README.md           # Documentacion de tu dashboard
```

**Ejemplos de nombre de carpeta:**
- `garcia-taxi-eda`
- `lopez-analisis-nyc`
- `martinez-dashboard`

---

### 3. El Archivo mas Importante: PROMPTS.md

!!! warning "PROMPTS.md es lo que se evalua"
    No el codigo, no el diseno. **Tus prompts de IA**.

Tu archivo `PROMPTS.md` debe contener:

```markdown
# Prompts de IA - Dashboard [Tu Nombre]

## Prompt A: [Titulo descriptivo]

**IA usada:** ChatGPT / Claude / Copilot / etc.

**Prompt exacto (copiado tal cual):**
> [Pega aqui tu prompt REAL, con errores y todo]

---

## Prompt B: [Titulo descriptivo]

[Mismo formato...]

---

## Prompt C: [Titulo descriptivo]

[Mismo formato...]

---

## Blueprint Final

[Al terminar, pide a tu IA que genere un resumen tecnico
de lo que construiste: stack, arquitectura, decisiones]
```

!!! danger "NO limpies tus prompts"
    Si escribiste "como ago q flask lea el csv" con errores,
    pega ESO. El sistema detecta si los prompts fueron "limpiados".

---

### 4. Requisitos Minimos del Dashboard

Tu dashboard debe incluir:

1. **Al menos 3 visualizaciones diferentes**
2. **Estadisticas descriptivas** (media, mediana, conteos)
3. **Analisis de calidad de datos** (nulos, tipos, outliers)
4. **README.md** explicando tu trabajo
5. **PROMPTS.md** con tus prompts de IA

---

### 5. Probar Localmente

Antes de subir, verifica que funciona:

```bash
cd dashboards/tu-nombre-dashboard/
python app.py
```

Abre http://localhost:5000 y verifica:

- El dashboard carga sin errores
- Las visualizaciones se muestran
- Los datos se cargan correctamente

---

### 6. Subir tu Trabajo

```bash
# Desde la raiz del repositorio
git add dashboards/tu-nombre-dashboard/
git commit -m "Dashboard EDA - [Tu Nombre]"
git push
```

!!! success "Listo!"
    No necesitas hacer nada mas. El sistema evalua tu PROMPTS.md
    automaticamente.

---

## Checklist de Entrega

Antes de hacer push, verifica:

- [ ] Mi carpeta esta en `dashboards/mi-nombre-dashboard/`
- [ ] Incluyo `PROMPTS.md` con mis prompts reales
- [ ] Incluyo `app.py` funcional
- [ ] Incluyo `README.md` documentando mi trabajo
- [ ] Mi dashboard tiene al menos 3 visualizaciones
- [ ] Probe localmente y funciona
- [ ] Hice `git push` a mi fork

---

## Que NO Subir

El `.gitignore` protege esto, pero recuerda:

- Archivos de datos (`.csv`, `.parquet`, `.db`)
- Entornos virtuales (`venv/`, `.venv/`)
- Archivos `__pycache__/`
- Credenciales (`.env`)

---

## Como se Evalua

| Aspecto | Peso | Que se evalua |
|---------|------|---------------|
| **PROMPTS.md** | 40% | Calidad y autenticidad de tus prompts |
| **Funcionalidad** | 30% | Dashboard carga y funciona |
| **Analisis** | 20% | Visualizaciones e interpretacion |
| **Documentacion** | 10% | README claro |

!!! info "El codigo NO se revisa linea por linea"
    Lo importante es tu proceso de aprendizaje documentado en PROMPTS.md.

---

## Ejemplo de Referencia

Puedes consultar el dashboard de ejemplo en `dashboards/nyc_taxi_eda/`.

**No copies el codigo.** Usalo como referencia para entender la estructura.

---

## Errores Comunes

### "No such file or directory: datos/nyc_taxi.csv"

```python
DATA_PATH = os.path.join('..', '..', 'datos', 'nyc_taxi.csv')
```

### "Port 5000 is already in use"

```python
app.run(debug=True, port=5001)  # Cambia el puerto
```

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

---

## Recursos

- [Flask Docs](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/docs/)
- [Plotly Python](https://plotly.com/python/)
- [Guia de Entregas General](entregas/guia-entregas.md)

---

**Ultima actualizacion:** 2026-02-04
