# Documentación completa: IA local con scikit-learn

Este documento centraliza la información sobre el diseño, uso y mantenimiento del módulo de IA local para Aqualy.

## Resumen

El sistema incluye un clasificador local (scikit-learn) que realiza dos tareas:

- Detección de la intención general del usuario (estado, fuga, minutos, consejo, medidor, saludo).
- Mapeo de texto libre de actividad a un escenario simulado (ej: "ducha" → "Ducha Activa").

## Archivos relevantes

- `src/ia_modelo_sklearn.py`: implementación del pipeline sklearn, funciones `predict_activity`, `predict_intent`, `get_model` y `save_model`. [src/ia_modelo_sklearn.py](src/ia_modelo_sklearn.py)

- `src/ia_modulo.py`: capa usada por la interfaz; ahora consulta `predict_intent` y `predict_activity`. [src/ia_modulo.py](src/ia_modulo.py)
- `src/sensor_simulado.py`: define `ESCENARIOS` y `ACTIVIDAD_POR_ESCOPEGIO`. [src/sensor_simulado.py](src/sensor_simulado.py)
- `src/ui/main_window.py`: entrada de texto libre y control del medidor. [src/ui/main_window.py](src/ui/main_window.py)
- `src/main.py`: arranque y persistencia inicial del modelo. [src/main.py](src/main.py)

## Conceptos clave

- Dataset: pares `(texto, etiqueta)` usados para entrenar los clasificadores.
- Re-entrenar: volver a ajustar los parámetros del modelo con más datos.
- Persistencia: guardar el objeto del modelo entrenado en `data/ia_modelo.pkl` para evitar reentrenamientos en cada inicio.

## Pasos para probar localmente

1. Instale dependencias: `python -m pip install -r requirements.txt`.
2. Ejecutar prueba básica:

```bash
python -c "from src.ia_modelo_sklearn import predict_activity, predict_intent; print(predict_activity('ducha')); print(predict_intent('¿Cómo va el tanque?'))"
```

1. Re-entrenar y guardar modelo:

```bash
python -c "from src.ia_modelo_sklearn import get_model, save_model; m = get_model(); save_model()"
```

## Mejora del dataset

- Añadir frases locales en `data/ia_dataset_custom.csv` o editar `ACTIVIDAD_POR_ESCOPEGIO`.

- Re-entrenar con el nuevo dataset y validar rendimiento.

## Seguridad y privacidad

- Si agrega frases de usuarios reales, anonimice identificadores (nombres, direcciones).

## Siguientes pasos recomendados

- Añadir una herramienta UI para re-entrenar y versionar modelos.
- Construir un pequeño script de evaluación (accuracy/recall por etiqueta).
- Recolectar datos reales (Falcón) para robustecer el clasificador.

---

Para ver guías prácticas de extensión, consulte: [docs/ia_howto_extend.md](docs/ia_howto_extend.md)
