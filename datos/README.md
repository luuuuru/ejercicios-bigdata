# Datos del Proyecto

Esta carpeta contiene los datasets utilizados en los ejercicios del curso.

## ⚠️ Archivos NO Incluidos en Git

Los archivos de datos **NO están en el repositorio** debido a su tamaño (>100MB).

## 📥 Cómo Obtener los Datos

### Opción 1: Script Automático (Recomendado)

```bash
cd datos/
python descargar_datos.py
```

Este script descargará automáticamente el dataset NYC Taxi.

### Opción 2: Descarga Manual

Si el script no funciona, descarga manualmente:

1. **NYC Taxi Dataset**
   - Fuente: [Especificar fuente oficial]
   - Tamaño: ~121 MB
   - Guardar como: `datos/nyc_taxi.csv`

## 📁 Archivos Esperados

Después de descargar, deberías tener:

```
datos/
├── descargar_datos.py       ✅ (en git)
├── README.md                ✅ (en git)
├── nyc_taxi.csv             ❌ (NO en git, debes descargar)
└── [otros archivos generados por ejercicios]
```

## 🔒 ¿Por Qué No Están en Git?

- GitHub tiene límite de **100 MB por archivo**
- `nyc_taxi.csv` es **121 MB**
- Solución: Cada alumno descarga los datos localmente

## ❓ Problemas Comunes

### Error: "FileNotFoundError: nyc_taxi.csv"

**Causa:** No descargaste los datos

**Solución:**
```bash
cd datos/
python descargar_datos.py
```

### Error al ejecutar descargar_datos.py

**Solución alternativa:** Descarga manual del dataset y colócalo en esta carpeta.

---

**Nota:** Los archivos `.csv`, `.parquet`, `.db` están en `.gitignore` y no se subirán a GitHub.
