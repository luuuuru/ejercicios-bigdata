# Guía del Alumno: Flujo de Trabajo con PyCharm

Sigue estos pasos para descargar los ejercicios, trabajar en ellos y enviarlos. Usaremos **PyCharm** para casi todo.

## 1. Preparación Inicial (Solo la primera vez)

### Paso 1: Fork en GitHub (Web)
1.  Ve al repositorio del profesor: [https://github.com/TodoEconometria/ejercicios-bigdata](https://github.com/TodoEconometria/ejercicios-bigdata)
2.  Haz clic en el botón **Fork** (arriba a la derecha).
3.  Esto crea una copia en TU cuenta.

### Paso 2: Clonar en PyCharm
1.  Abre PyCharm.
2.  Si estás en la pantalla de bienvenida, haz clic en **Get from VCS**.
    *   *Si ya tienes un proyecto abierto, ve a `Git` > `Clone...`*
3.  En la barra lateral izquierda, selecciona **GitHub**.
4.  Busca tu repositorio `ejercicios-bigdata` (el que está en tu cuenta) y selecciónalo.
5.  Haz clic en **Clone**.

### Paso 3: Conectar con el Profesor (Upstream)
Para recibir nuevos ejercicios, necesitas conectar tu PyCharm al repositorio original.

1.  Ve al menú superior: **Git** > **Manage Remotes...**
2.  Verás uno llamado `origin` (ese es el tuyo).
3.  Haz clic en el botón **+** para añadir uno nuevo.
4.  **Name**: `upstream`
5.  **URL**: `https://github.com/TodoEconometria/ejercicios-bigdata.git`
6.  Haz clic en **OK** y cierra la ventana.

---

## 2. Cómo Hacer un Ejercicio (Rutina Diaria)

Cada vez que vayas a hacer una tarea nueva, repite estos pasos:

### Paso A: Actualizar tu Proyecto
Asegúrate de tener lo último que haya subido el profesor.

1.  Ve al menú **Git** > **Fetch**. (Esto descarga la info, pero no cambia tus archivos aún).
2.  Ve al menú **Git** > **Merge...**
3.  En la lista, busca `upstream/main` (o `upstream/master`).
4.  Selecciónalo y dale a **Merge**.
    *   *Ahora tu rama `main` local está igual que la del profesor.*

### Paso B: Crear una Rama (Branch)
**NUNCA trabajes en `main`**. Crea una rama para cada tarea.

1.  Ve al menú **Git** > **New Branch...**
2.  Ponle un nombre descriptivo (ej. `juan-ejercicio-1`).
3.  Asegúrate de que "Checkout branch" esté marcado.
4.  Haz clic en **Create**.

### Paso C: Trabajar y Guardar (Commit)
1.  Haz tus ejercicios, crea archivos, edita código, etc.
2.  Cuando termines, abre la pestaña **Commit** (normalmente a la izquierda, icono de un "check" ✔️).
3.  Verás tus archivos en "Changes". Selecciónalos.
4.  Escribe un mensaje claro en el cuadro de texto (ej. "Solución ejercicio 1").
5.  Haz clic en **Commit**.

### Paso D: Subir a GitHub (Push)
1.  Ve al menú **Git** > **Push...**
2.  Verás que vas a subir tu rama `juan-ejercicio-1` a `origin`.
3.  Haz clic en **Push**.

---

## 3. Entregar la Tarea (Pull Request)

1.  Al hacer el Push, PyCharm suele mostrar una notificación abajo a la derecha con un enlace para crear el Pull Request. Si lo ves, haz clic ahí.
2.  Si no, ve a **tu** repositorio en GitHub (en el navegador).
3.  Verás un aviso amarillo "Compare & pull request". Haz clic.
4.  Comprueba que la flecha va de **tu rama** -> **repositorio del profesor**.
5.  Escribe un título y dale a **Create pull request**.

¡Listo!
