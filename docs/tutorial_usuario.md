# Manual de Usuario y Tutorial Detallado de Aqualy

Este documento explica paso a paso cómo usar Aqualy, cada pantalla, acciones disponibles, ejemplos prácticos, cómo interpretar los resultados y qué hacer ante problemas comunes. Está pensado tanto para usuarios domésticos como para administradores del sistema.

---

## Resumen rápido (rápido para arrancar)

- Abrir app en desarrollo: ejecutar `python src/main.py` desde la raíz del proyecto.
- Ejecutable Windows: `dist/A-P-R-C-H/A-P-R-C-H.exe` (creado con `scripts/build.py`).
- Base de datos SQLite: `data/sistema.db` (copia de seguridad recomendada antes de cambios).

---

## 1. Introducción y propósito

**Aqualy** es una aplicación para monitorizar y gestionar una reserva doméstica de agua (tanques, cisternas o pipas). Convierte litros y porcentajes en acciones concretas (minutos de ducha, carga de lavadora, riego) y ayuda a planificar hasta la próxima fecha de corte.

Audiencia: usuarios del hogar (registro y seguimiento diario) y administradores (configuración, reporte de fugas, gestión de tanques).

---

## 2. Instalación y puesta en marcha (detallado)

Requisitos mínimos:

- Windows 10/11 (para ejecutable). Para desarrollo, cualquier SO donde Python y PyQt5 funcionen.
- Python 3.10+ con un entorno virtual (`.venv`).

  2.1 Ejecutar desde código (paso a paso):

1. Abrir PowerShell y situarse en la carpeta del proyecto:

```powershell
cd 'c:\Users\Usuario\Desktop\Proyecto\A-P-R-C-H'
```

2. Activar entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

3. Instalar dependencias (si es necesario):

```powershell
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```powershell
python src/main.py
```

Observación: si la ventana no aparece revise errores en consola (mensajes de import o PyQt5). Copie y pegue cualquier error y puedo ayudar a diagnosticarlo.

2.2 Empaquetar en .exe (paso a paso):

1. Desde la raíz del proyecto, con `.venv` activo, ejecutar:

```powershell
.venv\Scripts\python scripts/build.py
```

2. Al finalizar, verá `dist/A-P-R-C-H/A-P-R-C-H.exe`. Mueva o comprima `dist` para distribuir.

Nota sobre PyInstaller: puede mostrar advertencias de "hidden imports" para paquetes opcionales (p. ej. scikit-learn). Si tu ejecución empacada falla por falta de librería, agrégala a `--hidden-import` en `scripts/build.py` o instala la dependencia en el entorno antes de empacar.

---

## 3. Estructura de la interfaz y uso paso a paso

La aplicación tiene una barra lateral izquierda con 4 secciones: `Sistema`, `Administrador`, `Usuario`, `Configuración`.

Cada sección y sus controles se describen a continuación con la acción exacta y resultado esperado.

3.1 Pantalla principal — `Sistema`

- Qué muestra:
  - Encabezado con saludo y resumen rápido: días estimados restantes, litros totales en todos los contenedores y consumo del día.
  - Tarjetas de contenedores: para cada tanque se ve nombre, barra de progreso, litros actuales y capacidad máxima.
  - Widget de IA: porcentaje de probabilidad de llegar a la fecha de corte con la reserva actual.
  - Semáforo: color según riesgo (verde/amarillo/rojo).

- Acciones habituales:
  - Click en un contenedor abre un detalle con historial (últimos consumos) y botón `Ver historial`.
  - Si se actualiza el consumo desde otra pantalla, la barra y los litros se actualizan inmediatamente.

  3.2 Pantalla `Administrador` (acciones críticas)

- Botones principales:
  - `Recargar todo` (o `Restablecer tanques`): restaura todos los contenedores a su capacidad máxima. Usar cuando se recibe suministro.
  - `Reportar fuga`: se abre un diálogo para ingresar litros perdidos por fuga y una descripción. Al confirmar, el sistema resta el volumen indicado de los contenedores (distribución proporcional) y registra el evento en la tabla `consumos` con tipo `fuga`.
  - `Modo de operación` (selector): `Normal`, `Ahorro`, `Extremo`. Cambia un coeficiente global que el sistema usa para advertencias y límites diarios.
  - `Agregar tanque`: formulario con `nombre`, `capacidad_max_litros`, `litros_iniciales` y `tipo` (p. ej. cisterna, pipa). Al guardar, se actualiza la base de datos y aparece en `Sistema`.
  - `Eliminar tanque`: botón en cada tarjeta de tanque. Pide confirmación.

---

## 4. Preguntas Frecuentes y Resolución de Problemas

### P1: ¿Qué pasa si el semáforo cambia a Rojo?

_Respuesta:_ Significa que tu consumo diario superó el límite diario ideal recomendado. Se aconseja activar el **Modo Ahorro** o **Modo Extremo** en la sección de Administrador para reajustar los límites.

### P2: ¿Por qué la IA de probabilidad bayesiana muestra 80% o 20% fijos al inicio?

_Respuesta:_ El cálculo requiere al menos 3 días de registro en el historial para trazar una desviación estándar real. Mientras no cuente con estos datos, se aplica una estimación base según tu consumo ideal diario.

### P3: ¿Las bases de datos o el programa son vulnerables a scripts maliciosos?

_Respuesta:_ **No.** Toda la base de datos se comunica mediante consultas preparadas en SQLite, lo que evita ataques de inyección SQL. Los datos mostrados en la UI son sanitizados previamente en los widgets QLabel de PyQt5.
