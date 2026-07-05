# Manual de Usuario y Tutorial Detallado de Aqualy

Este documento explica paso a paso cómo usar Aqualy, cada pantalla, acciones disponibles, ejemplos prácticos, cómo interpretar los resultados y qué hacer ante problemas comunes. Está pensado tanto para usuarios domésticos como para administradores del sistema.

---

## Resumen rápido (rápido para arrancar)

- Abrir app en desarrollo (desde `A-P-R-C-H`): ejecutar `python src/main.py`.
- Abrir app en desarrollo (desde `Proyecto`): ejecutar `python A-P-R-C-H/src/main.py`.
- Ejecutable Windows: `dist/A-P-R-C-H/A-P-R-C-H.exe` (creado con `scripts/build.py` desde `A-P-R-C-H`).
- Base de datos SQLite: `data/sistema.db` (copia de seguridad recomendada antes de cambios).
- Notificaciones de estado: la app muestra alertas flotantes tipo Windows cuando el nivel del tanque cambia de estado (verde, amarillo, rojo).

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

3. Al ejecutar el `.exe`, se iniciará la aplicación completa con notificaciones tipo Windows activas para los cambios de estado del tanque.

4. El ejecutable ya ha sido generado y verificado en la carpeta `dist/A-P-R-C-H/`.

Nota sobre PyInstaller: puede mostrar advertencias de "hidden imports" para paquetes opcionales (p. ej. scikit-learn). Si tu ejecución empacada falla por falta de librería, agrégala a `--hidden-import` en `scripts/build.py` o instala la dependencia en el entorno antes de empacar.

---

## 3. Estructura de la interfaz y uso paso a paso

La aplicación tiene una barra lateral izquierda con 2 secciones: `Mi Sistema`, `Configuración`.

Cada sección y sus controles se describen a continuación con la acción exacta y resultado esperado.

3.1 Pantalla principal — `Mi Sistema`

- Qué muestra:
  - Encabezado con saludo y resumen rápido: días estimados restantes, litros totales en todos los contenedores y consumo del día.
  - Tarjetas de contenedores: para cada tanque se ve nombre, barra de progreso, litros actuales y capacidad máxima.
  - Widget de IA: porcentaje de probabilidad de llegar a la fecha de corte con la reserva actual.
  - Semáforo: color según riesgo (verde/amarillo/rojo).

- Acciones habituales:
  - Click en Escenario de calibracion abre una lista de ciertas opciones de calibracion.
  - Barra de chat en el apartado del Asistente Virtual,.

    3.2 Pantalla `Configuracion` (acciones críticas)

- Apartados principales:
  - `Parametros de Operacion`: Aqui es donde se configura la fecha del suministro y se puede cambiar a los distintos modos de operacion(normal, ahorro, extremo).

---

## 4. Preguntas Frecuentes y Resolución de Problemas

### P1: ¿Qué pasa si el semáforo cambia a Rojo?

_Respuesta:_ Significa que tu consumo diario superó el límite diario ideal recomendado. Se aconseja activar el **Modo Ahorro** o **Modo Extremo** en la sección de Administrador para reajustar los límites.

### P2: ¿Por qué la IA de probabilidad bayesiana muestra 80% o 20% fijos al inicio?

_Respuesta:_ El cálculo requiere al menos 3 días de registro en el historial para trazar una desviación estándar real. Mientras no cuente con estos datos, se aplica una estimación base según tu consumo ideal diario.

### P3: ¿Las bases de datos o el programa son vulnerables a scripts maliciosos?

_Respuesta:_ **No.** Toda la base de datos se comunica mediante consultas preparadas en SQLite, lo que evita ataques de inyección SQL. Los datos mostrados en la UI son sanitizados previamente en los widgets QLabel de PyQt5.
