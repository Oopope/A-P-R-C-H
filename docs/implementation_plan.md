# Plan de Implementación: Interfaz Elegante y Funcionalidades de Aqualy

Este plan detalla los cambios para rediseñar la interfaz de usuario de la aplicación **Aqualy** inspirada en el diseño premium de la referencia visual proporcionada (barra lateral moderna con esquinas redondeadas, tarjetas con estilo de vidrio esmerilado/glassmorphism, y paleta de colores sofisticada). Además, se implementarán los 4 apartados solicitados y una vista amigable de "tiempo restante por actividad en minutos" en lugar de porcentajes crudos.

## User Review Required

> [!IMPORTANT]
>
> - **Apartado de Usuario**: Para simplificar la comprensión, convertiremos el inventario de agua en minutos disponibles para realizar actividades cotidianas. Por ejemplo:
>   - **Ducha**: Consumo estimado de 10 litros por minuto (ej: 1200L = 120 minutos de ducha).
>   - **Lavar Platos**: Consumo de 5 litros por minuto.
>   - **Cocinar**: Consumo de 2 litros por minuto.
>   - **Lavadora**: Consumo de 12 litros por minuto.
> - **Tipografía del Logo**: El nombre **Aqualy** tendrá una fuente serif elegante estilizada (tipo Times New Roman en cursiva y negrita) en la parte superior de la barra lateral.
> - **Seguridad ante Scripts**: Explicaremos los riesgos de inyección SQL (prevenidos mediante consultas parametrizadas que ya tiene el proyecto) e inyección de HTML/Rich Text en etiquetas `QLabel` (que sanitizaremos al mostrar texto ingresado por el usuario).

## Proposed Changes

### 1. Interfaz Gráfica (Frontend)

#### [MODIFY] [styles.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/ui/styles.py)

- Redefinir la hoja de estilo QSS para lograr un look premium:
  - Fondo oscuro con sutiles gradientes de azul/gris pizarra.
  - Barra lateral de navegación con botones redondos/ovalados y hover dinámico.
  - Tarjetas estilo _Glassmorphism_ (fondo translúcido con bordes finos y sombras).
  - Tipografía refinada del logo **Aqualy** en Times New Roman.

#### [MODIFY] [main_window.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/ui/main_window.py)

- Reestructurar el layout usando `QStackedWidget` para soportar las 4 pestañas:
  - **Sistema**: Visualización del inventario actual, barras de progreso de los contenedores, probabilidad bayesiana de supervivencia y modo de operación.
  - **Administrador**: Botones para Reportar Fuga, Recargar Tanques, y opciones para agregar/editar contenedores.
  - **Usuario**: Sección amigable de minutos restantes. Mostrará tarjetas para cada actividad (Ducha, Lavar Platos, Lavadora, Cocinar) indicando cuántos minutos quedan disponibles en total. También incluirá botones interactivos para registrar su uso de forma directa.
  - **Configuración**: Entrada para modificar la fecha de corte y el modo de operación. (Los controles para ajustar consumos por actividad fueron eliminados de la UI; editar `src/logic.py` para cambiar los valores por defecto.)

### 2. Lógica y Base de Datos (Backend)

#### [MODIFY] [logic.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/logic.py)

- Agregar tasas de consumo por minuto a la estructura de actividades.
- Proveer funciones de conversión de litros a minutos para la vista de usuario.

#### [MODIFY] [database.py](file:///c:/Users/Usuario/Desktop/Proyecto/A-P-R-C-H/src/database.py)

- Asegurar persistencia de los nuevos parámetros de configuración si fuera necesario.

---

## Guía de Modificación Rápida para el Usuario

Explicaremos en los comentarios y en la documentación final cómo cambiar rápidamente:

1. Las tasas de consumo de las actividades.
2. Los colores y estilos en `styles.py`.
3. Agregar nuevos botones o campos en la interfaz.

---

## Plan de Verificación

### Pruebas Manuales

1. Ejecutar la aplicación usando `.venv\Scripts\python src/main.py` desde la carpeta `A-P-R-C-H`.
   Si estás en la carpeta superior `Proyecto`, usa `python A-P-R-C-H/src/main.py`.
2. Probar la navegación entre las 4 pestañas de la barra lateral.
3. Verificar que las actividades del usuario muestren los minutos calculados correctamente y descuenten el agua en tiempo real.
4. Generar el ejecutable usando `scripts/build.py` y verificar que abra correctamente.
