# Manual de Usuario y Tutorial de Aqualy

Documento elaborado siguiendo los lineamientos de la norma internacional **ISO/IEC 26514** (Ingeniería de Sistemas y Software - Requisitos para diseñadores y desarrolladores de documentación de usuario).

---

## 1. Introducción y Propósito

### 1.1 Propósito del Sistema
**Aqualy** es un Sistema Inteligente de Recursos Hídricos diseñado para monitorear, calcular y predecir el consumo de agua en el hogar. El objetivo es brindar una representación clara y elegante de la reserva hídrica disponible, convirtiendo métricas técnicas en datos de fácil comprensión humana para optimizar el consumo diario y evitar cortes de suministro imprevistos.

### 1.2 Audiencia Objetivo
Este manual está destinado a:
*   **Usuarios del Hogar:** Personas interesadas en monitorear su disponibilidad hídrica de manera amigable y registrar sus consumos cotidianos.
*   **Administradores del Sistema:** Encargados de configurar los parámetros generales, reportar anomalías (fugas), y gestionar los tanques o contenedores de almacenamiento.

---

## 2. Instalación y Puesta en Marcha

### 2.1 Requisitos Previos
*   Sistema Operativo: Windows 10 o superior.
*   Python 3.10+ (en caso de ejecutar desde código fuente).
*   Librerías principales: `PyQt5`, `sqlite3`.

### 2.2 Ejecución en Desarrollo (Código Fuente)
Para ejecutar la aplicación en modo desarrollo:
1.  Abre una terminal en la raíz del proyecto (`c:\Users\Usuario\Desktop\Proyecto\A-P-R-C-H`).
2.  Inicia el entorno virtual:
    ```powershell
    .venv\Scripts\activate
    ```
3.  Ejecuta el script principal:
    ```powershell
    python src/main.py
    ```

### 2.3 Compilación del Ejecutable (.exe)
Si has realizado modificaciones y deseas empaquetar de nuevo la aplicación en un ejecutable autónomo para Windows, ejecuta en tu terminal:
```powershell
.venv\Scripts\python scripts/build.py
```
El instalador o archivo portable resultante se guardará en la ruta:
`dist/A-P-R-C-H/A-P-R-C-H.exe`

---

## 3. Descripción de los Módulos del Sistema

La interfaz de **Aqualy** se compone de una barra lateral izquierda con tipografía serif elegante Times New Roman y cuatro secciones principales:

```
+-------------------------------------------------------------+
|  Aqualy      |  ¡Buenas tardes, bienvenido a Aqualy!       |
|              |  Resumen: [9 días restantes] [1200L reserva]|
|  [Sistema]   |                                             |
|  [Admin]     |  +-----------------------+ +-------------+  |
|  [Usuario]   |  | Tanque principal [|||]| | IA: 90%     |  |
|  [Config]    |  | Respaldo         [|||]| | Semáforo: OK|  |
|              |  +-----------------------+ +-------------+  |
+-------------------------------------------------------------+
```

### 3.1 Módulo 1: Sistema
*   **Propósito:** Brinda un diagnóstico en tiempo real de la situación de agua en el hogar.
*   **Elementos Visuales:**
    *   **Tarjetas Estadísticas Rápidas:** Días restantes hasta la fecha de corte, reserva total sumada de litros y consumo efectuado en el día de hoy.
    *   **Estado de Contenedores:** Barras de progreso que muestran los litros actuales y máximos de cada tanque o pipa registrado.
    *   **Inteligencia Artificial (Análisis Bayesiano):** Calcula el porcentaje de probabilidad de llegar a la fecha de corte sin quedarse sin agua en función del historial diario de consumos.
    *   **Semáforo de Consumo:** Indicador dinámico en tres estados (Verde = Consumo seguro, Amarillo = Consumo al límite, Rojo = Consumo excesivo/Alerta).

### 3.2 Módulo 2: Administrador
*   **Propósito:** Proporciona herramientas avanzadas de control y mantenimiento.
*   **Funciones Principales:**
    *   **Restablecer Tanques:** Restaura la capacidad al 100% de todos los contenedores de forma masiva tras una recarga.
    *   **Reportar Fuga:** Permite ingresar un volumen estimado de pérdida de agua por fuga, descontándolo inmediatamente en cascada.
    *   **Modo de Operación:** Ajusta dinámicamente los límites del consumo diario aplicando coeficientes multiplicadores:
        *   *Normal:* Límite del 100% sugerido.
        *   *Ahorro:* Limita el consumo ideal a un 80%.
        *   *Extremo:* Restringe el consumo al 60%.
    *   **Gestión de Tanques:** Permite agregar nuevos contenedores (especificando tipo y volumen máximo) o eliminar tanques antiguos del inventario.

### 3.3 Módulo 3: Usuario (Tiempo Restante de Actividades)
*   **Propósito:** Traducir los datos técnicos de litros a unidades comprensibles del día a día, respondiendo a la pregunta: *"¿Para qué me alcanza el agua que queda?"*.
*   **Visualización en Minutos:** En lugar de mostrar crudos porcentajes, la pantalla calcula cuántos **minutos acumulados** de uso le quedan a las siguientes actividades antes de agotar la reserva:
    *   **Ducha:** Estimada a 10 L/min.
    *   **Lavar Platos:** Estimado a 5 L/min.
    *   **Lavadora:** Estimada a 12 L/min.
    *   **Cocinar:** Estimado a 2 L/min.
    *   **Riego:** Estimado a 6 L/min.
    *   **Lavar Auto:** Estimado a 15 L/min.
*   **Acción de Registro:** Cada tarjeta de actividad cuenta con botones de acceso rápido para registrar consumos de `"1 min"` o `"N min"` (personalizado), actualizando automáticamente todo el sistema.

### 3.4 Módulo 4: Configuración
*   **Propósito:** Permite personalizar el comportamiento del sistema y adaptarlo a tu propio hogar.
*   **Parámetros Modificables:**
    *   **Fecha de Corte:** Define la fecha objetivo en la cual llegará el próximo suministro de agua (formato AAAA-MM-DD).
    *   **Tasas de Consumo:** Si tus grifos o electrodomésticos consumen más o menos agua de lo predeterminado, puedes reajustar los litros por minuto de cada actividad directamente en esta pantalla.

---

## 4. Preguntas Frecuentes y Resolución de Problemas

### P1: ¿Qué pasa si el semáforo cambia a Rojo?
*Respuesta:* Significa que tu consumo diario superó el límite diario ideal recomendado. Se aconseja activar el **Modo Ahorro** o **Modo Extremo** en la sección de Administrador para reajustar los límites.

### P2: ¿Por qué la IA de probabilidad bayesiana muestra 80% o 20% fijos al inicio?
*Respuesta:* El cálculo requiere al menos 3 días de registro en el historial para trazar una desviación estándar real. Mientras no cuente con estos datos, se aplica una estimación base según tu consumo ideal diario.

### P3: ¿Las bases de datos o el programa son vulnerables a scripts maliciosos?
*Respuesta:* **No.** Toda la base de datos se comunica mediante consultas preparadas en SQLite, lo que evita ataques de inyección SQL. Los datos mostrados en la UI son sanitizados previamente en los widgets QLabel de PyQt5.
