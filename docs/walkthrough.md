# Resumen del Rediseño de Aquli e Implementación de Secciones

Se ha completado con éxito la transformación del sistema inteligente hídrico **Aquli**, mejorando la elegancia de la interfaz y facilitando la comprensión del usuario al traducir litros a minutos restantes por cada actividad doméstica.

## Cambios Clave Realizados

### 1. Interfaz Multipestaña e Interactiva

- **Barra Lateral de Navegación (Sidebar):** Implementada con un diseño moderno de botones redondeados que responden visualmente a los estados de cursor (hover) y selección.
- **Nombre/Logo Elegante:** El nombre **Aquli** ahora se muestra en la parte superior izquierda utilizando una tipografía serif elegante basada en el estilo solicitado (Times New Roman, negrita y cursiva).
- **QStackedWidget para las 4 Secciones:**
  1.  **Sistema:** Vista resumida diaria con tarjetas estadísticas (días restantes, litros de reserva, consumo de hoy), indicador bayesiano de supervivencia con colores dinámicos (verde/amarillo/rojo) y nivel gráfico de contenedores.
  2.  **Administrador:** Panel de control para recargar tanques al 100%, reportar fugas, alternar el factor del modo de operación, y agregar o eliminar contenedores.
  3.  **Usuario:** Una vista simplificada de las actividades domésticas ("Ducha", "Lavar Platos", "Lavadora", "Cocinar", etc.) con tarjetas individuales que informan al usuario cuántos **minutos restantes** tiene disponibles para cada actividad según la reserva total de agua en lugar de un confuso porcentaje. Además, incluye botones rápidos para registrar el consumo en minutos.
  4.  **Configuración:** Permite establecer la fecha límite de corte y ajustar manualmente las tasas de consumo (litros por minuto) de cada actividad.

### 2. Lógica de Negocio y Base de Datos

- Actualizado el archivo [logic.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/logic.py) para incluir el catálogo de consumo por minuto y el método [obtener_minutos_restantes](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/logic.py#L32-L41).
- Los datos ingresados por el administrador persistirán correctamente en el archivo SQLite.

---

## Análisis de Vulnerabilidad ante Scripts

### 1. Inyección SQL (Base de Datos)

- **Estado:** **Seguro.**
- **Análisis:** Todas las operaciones de escritura y lectura en [database.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/database.py) emplean consultas preparadas parametrizadas (mediante el placeholder `?`). Por lo tanto, el motor de SQLite trata cualquier cadena de entrada estrictamente como datos, neutralizando por completo la inyección de código SQL malicioso.

### 2. Inyección de Rich Text / HTML (Interfaz Gráfica)

- **Estado:** **Mitigado.**
- **Análisis:** En PyQt, las etiquetas `QLabel` interpretan por defecto formato HTML si la cadena introducida tiene sintaxis de etiquetas. Si un usuario creara un contenedor con el nombre `<font size=50>Peligro</font>`, la interfaz podría renderizarse mal y alterar la disposición visual. Para evitar esto, todas las entradas críticas de texto libre en diálogos se sanitizan, o se configuran de tal forma que no ejecuten código externo perjudicial ya que PyQt no incluye un entorno de ejecución JavaScript activo en etiquetas estáticas.

---

## Guía Rápida de Modificación (Cómo alterar el proyecto)

Si deseas realizar cambios rápidos tú mismo:

1.  **Modificar las Actividades:** En el archivo [logic.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/logic.py#L25-L33), puedes alterar los nombres y consumos estándar (litros por minuto de uso) dentro del diccionario `ACTIVIDADES`.
2.  **Cambiar Colores y Estilos:** Abre el archivo [styles.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/ui/styles.py) y edita las reglas QSS. Por ejemplo, para alterar el color del logo o el fondo, busca las reglas `QLabel#LogoLabel` o `QMainWindow` respectivamente.
3.  **Compilar una nueva versión:** Cada vez que realices cambios en el código de Python y desees empaquetar el ejecutable `.exe` definitivo, ejecuta el script de compilación en la terminal:
    ```powershell
    .venv\Scripts\python scripts/build.py
    ```

---

## Verificación Visual y Ejecutable

- Se compiló exitosamente el ejecutable `.exe` con todas las dependencias asociadas de PyQt5 y SQLite.
- El instalador/ejecutable resultante se encuentra disponible en la carpeta: [dist/A-P-R-C-H/](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/dist/A-P-R-C-H).
- La aplicación incluye ahora notificaciones flotantes tipo toast para alertar sobre el nivel del tanque en tiempo real.
