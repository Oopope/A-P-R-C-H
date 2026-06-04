# Implementación de Interfaz Gráfica (Dashboard A-P-R-C-H) con PyQt5

El objetivo es construir una interfaz gráfica moderna utilizando `PyQt5`, basándonos en el diseño de panel de administración (dashboard) proporcionado en la imagen, y conectándola con la lógica de negocio existente en `src/logic.py` (`GestorAgua` y `ContenedorHidrico`).

## User Review Required

> [!IMPORTANT]
> **Diseño vs. Lógica actual:** El diseño de la imagen está pensado para gestión de tareas (Project Management). He adaptado los componentes visuales para que tengan sentido con nuestra gestión de agua. Revisa la sección de "Mapeo de Componentes" para asegurarte de que estás de acuerdo con esta adaptación.

> [!WARNING]
> **Gráficos:** El diseño original incluye una gráfica de líneas curva suave. Para mantener las dependencias simples y el rendimiento alto, propongo dibujar un gráfico de barras o líneas simplificado nativo usando `QPainter` de PyQt5, o alternativamente instalar `matplotlib` o `PyQtChart`. Por defecto, planeo crear un widget personalizado nativo de PyQt5 para no agregar más dependencias pesadas. ¿Estás de acuerdo?

## Open Questions

1. **Colores y Tema:** El diseño tiene un tema claro (Light Mode) con acentos oscuros. ¿Deseas mantener este esquema de colores exacto o prefieres un modo oscuro (Dark Mode)?
2. **Navegación:** La barra lateral izquierda tiene varios botones. En esta primera versión, ¿quieres que la barra lateral sea solo visual/decorativa y toda la acción ocurra en la pantalla principal (Dashboard), o planeas tener múltiples pantallas reales desde el principio?

## Proposed Changes

### 1. Estructura del Proyecto

Se creará una nueva carpeta `ui` dentro de `src` para separar la interfaz de la lógica.

#### [NEW] `src/ui/__init__.py`
#### [NEW] `src/ui/main_window.py`
Contendrá la ventana principal y la estructura del dashboard (Sidebar, Header, Main Content).

#### [NEW] `src/ui/styles.py`
Archivo dedicado para almacenar las hojas de estilo (QSS - Qt Style Sheets) para darle el aspecto moderno y limpio al estilo de la imagen de referencia.

#### [NEW] `src/main.py`
Punto de entrada de la aplicación. Instanciará el `GestorAgua` (con datos simulados iniciales o leyendo de un archivo en el futuro) y lanzará la ventana de PyQt5.

---

### 2. Mapeo de Componentes Visuales a la Lógica A-P-R-C-H

Basado en la imagen, adaptaremos las secciones:

*   **Sidebar (Barra Lateral):**
    *   Logo: "A-P-R-C-H"
    *   Menú: "Dashboard" (activo), "Contenedores", "Actividades", "Ajustes".
*   **Header (Encabezado):**
    *   Barra de búsqueda (visual).
    *   Fecha actual.
*   **Sección "Last Tasks" (Centro Superior) -> "Estado de Contenedores":**
    *   Una tabla o lista elegante mostrando cada `ContenedorHidrico`: Nombre, Tipo, Capacidad, Nivel Actual (barra de progreso).
*   **Sección "Productivity" (Abajo Izquierda) -> "Historial de Consumo":**
    *   Un gráfico mostrando el historial de consumo de los últimos días vs. el Límite Diario Ideal.
*   **Sección "Projects in progress" (Abajo Derecha) -> "Panel de Control / Acciones":**
    *   Aquí colocaremos los controles principales:
        *   Indicador del **Semaforo** (Verde, Amarillo, Rojo).
        *   **Probabilidad de Supervivencia** (%).
        *   Botones para "Registrar Actividad" (ej. Baño, Lavar) que descontarán agua usando `gestor.registrar_actividad()`.
        *   Selector de "Modo de Operación" (Normal, Ahorro, Extremo) usando `gestor.cambiar_modo()`.

## Verification Plan

### Manual Verification
1. Ejecutar el nuevo `src/main.py`.
2. Verificar que la ventana de PyQt5 se abre con el estilo (QSS) moderno aproximado al diseño.
3. Interactuar con el panel:
    *   Registrar una actividad (ej. "Baño").
    *   Verificar que la barra de progreso de los contenedores disminuya.
    *   Verificar que el "Semáforo" y la "Probabilidad de supervivencia" se actualicen dinámicamente.
    *   Cambiar el modo de operación y ver si el límite diario ideal se ajusta.
