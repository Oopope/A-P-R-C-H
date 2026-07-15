# Documentación completa: IA local con scikit-learn

Este documento centraliza la información sobre el diseño, uso, mantenimiento y build del módulo de IA local para Aqualy.

## Resumen

El sistema incluye un clasificador local (scikit-learn) que realiza dos tareas principales:

- Detección de la intención del usuario (`estado`, `fuga`, `minutos`, `consejo`, `medidor`, `saludo`).
- Mapeo de texto libre de actividad a un escenario simulado (ej: "ducha" → "Ducha Activa").

## Archivos relevantes

- `src/ia_modelo_sklearn.py`: implementación del pipeline sklearn, funciones `predict_activity`, `predict_intent`, `get_model` y `save_model`.
- `src/ia_modulo.py`: capa intermediaria usada por la UI; ahora llama a `predict_intent` y `predict_activity`.
- `src/sensor_simulado.py`: define `ESCENARIOS`, `ACTIVIDAD_POR_ESCOPEGIO` y el mapeo de actividades.
- `src/ui/main_window.py`: entrada de texto libre del usuario para la actividad y la visualización del medidor.
- `src/main.py`: arranque de la aplicación y persistencia inicial del modelo.
- `A-P-R-C-H.spec`: configuración de PyInstaller para generar el ejecutable.

## Estructura actual de `src/ia_modelo_sklearn.py`

- `MODEL_PATH`: resuelve la ruta al archivo `data/ia_modelo.pkl`.
- `IAEnsemble`: mantiene dos pipelines de scikit-learn (TF-IDF + MultinomialNB).
- `get_model()`: intenta cargar el modelo persistido y, si no existe, entrena uno en memoria.
- `save_model()`: guarda el modelo entrenado en `data/ia_modelo.pkl`.

### Comportamiento esperado

- Si `data/ia_modelo.pkl` existe, se carga directamente.
- Si no existe o hay error, se entrena un modelo en memoria.
- Las funciones `predict_activity` y `predict_intent` devuelven la etiqueta y su probabilidad.

## Importante: editor y entorno

Los subrayados amarillos en `src/ia_modelo_sklearn.py` son advertencias de Pylance que indican que el editor no está usando el mismo intérprete que tu terminal.

- En terminal funciona con tu entorno virtual (`.venv`).
- En VS Code necesitas seleccionar el intérprete `A-P-R-C-H\.venv\Scripts\python.exe`.

Si no seleccionas ese intérprete, Pylance puede marcar `joblib` y `sklearn` como importaciones faltantes, aunque el código funcione.

## Pruebas locales

Probar el módulo desde la terminal del proyecto:

```powershell
python -c "import sys, os; sys.path.insert(0, os.getcwd()); from src.ia_modelo_sklearn import predict_activity, predict_intent; print(predict_activity('ducha')); print(predict_intent('¿Hay una fuga?'))"
```

Probar solo importación y ruta del modelo:

```powershell
python -c "import sys, os; sys.path.insert(0, os.getcwd()); import src.ia_modelo_sklearn as m; print(m.MODEL_PATH); print(os.path.exists(m.MODEL_PATH))"
```

## Compilación del ejecutable

El EXE se genera con PyInstaller usando `A-P-R-C-H.spec`.

Comando recomendado:

```powershell
python -m PyInstaller A-P-R-C-H.spec --clean --noconfirm
```

El resultado funcional debe quedar en:

- `A-P-R-C-H\dist\A-P-R-C-H\A-P-R-C-H.exe`

Y el directorio temporal de build en:

- `A-P-R-C-H\build\A-P-R-C-H`

Solo debe existir un conjunto de `build`/`dist` funcionales. Si hay duplicados como `build_new` o `dist_new`, bórralos.

## Resolución de problemas comunes del EXE

- Asegúrate de cerrar cualquier instancia previa del ejecutable antes de reconstruir.
- Si PyInstaller no puede generar el EXE, elimina manualmente `build` y `dist` y vuelve a ejecutar el comando.
- Si el EXE lanza errores de importación, añade los módulos necesarios a `hiddenimports` en `A-P-R-C-H.spec`.

## Persistencia de datos y modelo

- `data/ia_modelo.pkl`: modelo entrenado persistente.
- `data/sistema.db` y `data/sistema.sql`: datos de aplicación.

No subas `data/ia_modelo.pkl` ni los artefactos generados en `build/` y `dist/` al repositorio.

## Re-entrenamiento

Para re-entrenar y guardar el modelo:

```powershell
python -c "from src.ia_modelo_sklearn import get_model, save_model; get_model(); save_model()"
```

Si quieres cambiar el dataset, actualiza `src/sensor_simulado.py` o añade frases locales a `ACTIVIDAD_POR_ESCOPEGIO` y vuelve a re-entrenar.

## Enlaces a documentación adicional

- [docs/ia_retraining.md](ia_retraining.md)
- [docs/ia_dataset.md](ia_dataset.md)
- [docs/ia_howto_extend.md](ia_howto_extend.md)
- [docs/tutorial_usuario.md](tutorial_usuario.md)
