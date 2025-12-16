# ⚙️ Configuración Inicial del Repositorio

## 🛡️ Paso 1: Proteger la Branch Main

**IMPORTANTE:** Esto evita que alguien (incluido tú) pueda pushear directo a `main` sin PR.

### Instrucciones:

1. **Ve a tu repositorio en GitHub:**
   - https://github.com/TodoEconometria/ejercicios-bigdata

2. **Settings → Branches:**
   - Clic en pestaña "Settings"
   - En el menú lateral: "Branches"

3. **Add branch protection rule:**
   - Clic en "Add rule" o "Add branch protection rule"

4. **Configuración:**

   **Branch name pattern:**
   ```
   main
   ```

   **Marca estas opciones:**
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: `1`
     - ✅ Dismiss stale pull request approvals when new commits are pushed

   - ✅ **Require conversation resolution before merging**

   - ✅ **Do not allow bypassing the above settings**
     - Esto hace que NI TÚ puedas saltarte las reglas

   - ✅ **Include administrators**
     - MUY IMPORTANTE: Marca esto

   **NO marques (por ahora):**
   - ❌ Require status checks (no tienes CI/CD aún)
   - ❌ Require signed commits (opcional)
   - ❌ Require linear history (opcional)

5. **Save changes:**
   - Clic en "Create" o "Save changes"

### ✅ Verificación:

Después de configurar, intenta pushear directo a main:

```bash
# Esto debería FALLAR
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
```

**Resultado esperado:**
```
remote: error: GH006: Protected branch update failed for refs/heads/main.
```

Si ves ese error, ¡perfecto! La protección funciona.

---

## 🔧 PASO 2: Instalar GitHub CLI (Recomendado)

GitHub CLI te permite automatizar TODO desde el script `profe.bat`.

### Windows:

**Opción A: Con winget**
```bash
winget install GitHub.cli
```

**Opción B: Descarga manual**
1. Ve a: https://cli.github.com/
2. Descarga el instalador para Windows
3. Ejecuta y sigue las instrucciones

### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install gh
```

### Mac:

```bash
brew install gh
```

### Configurar (Una sola vez):

```bash
gh auth login
```

Selecciona:
1. **GitHub.com**
2. **HTTPS**
3. **Login with a web browser**
4. Copia el código y pégalo en el navegador
5. Autoriza GitHub CLI

### ✅ Verificación:

```bash
gh auth status
```

Deberías ver:
```
✓ Logged in to github.com as [tu-usuario]
```

---

## 🌱 PASO 3: Crear Primera Branch de Entregas

Crea la branch para tu primer curso:

```bash
# Desde main
git checkout main

# Crear branch de entregas
git checkout -b entregas-2025-01

# Pushear a GitHub
git push -u origin entregas-2025-01

# Volver a main
git checkout main
```

**O usa el script:**
```bash
.\scripts\profe.bat
# Opción 7: Crear nueva branch de curso
# Nombre: 2025-01
```

### ✅ Verificación:

```bash
git branch -r | grep entregas
```

Deberías ver:
```
origin/entregas-2025-01
```

---

## 📋 PASO 4: Probar el Sistema

### Prueba 1: Script Maestro

```bash
.\scripts\profe.bat
```

Deberías ver el menú interactivo.

### Prueba 2: Flujo Completo (Con PR de prueba)

**Desde otra cuenta o pide a un amigo:**

1. Fork del repo
2. Crear rama `test-dashboard`
3. Crear carpeta `dashboards/test-dashboard/`
4. Agregar `app.py` y `README.md` básicos
5. Push y crear PR

**Tú como profesor:**

```bash
.\scripts\profe.bat
# Opción 5: Flujo completo
# Sigue las instrucciones
```

---

## ✅ Checklist de Configuración

Marca cuando completes cada paso:

- [ ] Protección de `main` configurada en GitHub
- [ ] GitHub CLI instalado y autenticado
- [ ] Branch `entregas-2025-01` creada
- [ ] Script `profe.bat` probado
- [ ] Flujo completo testeado con PR de prueba

---

## 🎓 ¡Sistema Listo!

Ahora puedes:
- Recibir PRs de alumnos
- Revisar desde PyCharm con el script
- Aprobar y mergear automáticamente
- Destacar los mejores trabajos
- Escalar a cientos de alumnos

---

## 📞 Soporte

Si tienes problemas:
- Revisa [scripts/README.md](../scripts/README.md)
- Crea un [Issue](../../issues) describiendo el problema
- Email para consultoría: cursos@todoeconometria.com

---

<p align="center">
  <strong>¡Todo listo para enseñar Big Data!</strong> 🚀
</p>
