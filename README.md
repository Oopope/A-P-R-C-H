# A-P-R-C-H

Proyecto Aqualy — Monitor hídrico con asistente local y simulador de sensor.

Resumen rápido

- Aplicación PyQt5 que simula lecturas de caudal, presión y temperatura.
- Incluye un clasificador local (scikit-learn) para detectar intenciones y mapear actividades.

Archivos importantes

- `src/` — código fuente.
- `dist/` — ejecutable generado (no se sube al repo por defecto).
- `data/ia_modelo.pkl` — modelo entrenado (excluido por `.gitignore`).
- `docs/` — documentación sobre IA y re-entrenamiento.

Comandos útiles
Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar la app en desarrollo:

```bash
python src/main.py
```

Generar ejecutable (PyInstaller, se incluye `A-P-R-C-H.spec`):

```bash
pyinstaller A-P-R-C-H/A-P-R-C-H.spec --clean --noconfirm
```

Re-entrenar y persistir modelo IA (opcional):

```bash
python -c "from src.ia_modelo_sklearn import get_model, save_model; m = get_model(); save_model()"
```

Subida a GitHub (sugerencia)

1. Inicializar repo:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <URL_REMOTE>
git push -u origin main
```

1. Crear Release para adjuntar `dist/A-P-R-C-H.zip` (no publicar artefactos binarios en el repo principal).

Contacto

- Si quieres, te ayudo a crear la Release o a automatizar re-entrenamientos desde la UI.

## A-P-R-C-H — Aqualy (Proyecto de Gestión Hídrica)

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

## Notificaciones estilo Windows

- La aplicación muestra alertas tipo "toast" flotantes cuando el estado del tanque cambia a amarillo o rojo.
- Estas notificaciones aparecen en la esquina superior derecha de la ventana y se ocultan automáticamente tras unos segundos.

## Ejecutar en modo desarrollo

1. Activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

1. Ejecutar la app:

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
- La opción para ajustar las tasas de consumo por actividad fue eliminada de la interfaz.
  Si necesitas cambiar los valores por defecto, edita `src/logic.py` en el diccionario `ACTIVIDADES`.
- El ejecutable generado se encuentra en `dist/A-P-R-C-H/A-P-R-C-H.exe` tras ejecutar `scripts/build.py`.
- La aplicación incluye notificaciones estilo Windows (toast) para alertas de nivel de tanque en esquina superior derecha.
