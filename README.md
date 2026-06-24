# A-P-R-C-H — Aqualy (Proyecto de Gestión Hídrica)

> Nota: este proyecto debe ejecutarse desde la carpeta `A-P-R-C-H`.
> Si estás en la carpeta superior `Proyecto`, ejecuta `python A-P-R-C-H/src/main.py`.

Resumen rápido y pasos para ejecutar y compilar el proyecto.

## Estructura principal

- `src/` — Código fuente de la aplicación (UI, lógica, base de datos, IA, sensor simulado).
- `scripts/` — Scripts de ayuda (p. ej. `build.py` para empaquetar con PyInstaller).
- `docs/` — Documentación del proyecto (tutorial de usuario, plan de implementación, walkthrough).
- `data/` — Base de datos SQLite y otros datos persistentes.
- `build/`, `dist/` — Carpetas generadas por PyInstaller tras compilar.

## Requisitos

- Windows 10+ (para el ejecutable entregable)
- Python 3.10+ (se recomienda usar el entorno virtual provisto)

## Ejecutar en modo desarrollo

1. Activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

2. Ejecutar la app:

```powershell
python src/main.py
```

## Compilar ejecutable (Windows)

Desde la raíz del proyecto:

```powershell
.venv\Scripts\python scripts/build.py
```

El ejecutable resultante estará en `dist/A-P-R-C-H/A-P-R-C-H.exe`.

## Notas

- La documentación del usuario y los planes están en `docs/`.
- Si necesitas ajustar las tasas de consumo por actividad, edita `src/logic.py` en el diccionario `ACTIVIDADES`.
