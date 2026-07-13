# Guía: cómo ampliar el dataset y mejorar el modelo

Esta guía explica pasos concretos para ampliar el dataset, recolectar frases del habla local (Falcón) y re-entrenar el modelo.

1) Recolección de frases

- Cree un archivo de texto o CSV con pares `"texto","etiqueta"` y guárdelo en la carpeta `data/` con nombre `ia_dataset_custom.csv`.

- Ejemplo (CSV):

``
ducha,Ducha Activa
bañito,Ducha Activa
echar un baño,Ducha Activa
lavar cacharros,Lavar Platos
trastear,Lavar Platos
regar matas,Riego de Jardín
lavar carro,Lavado de Auto
se está goteando,Fuga Silenciosa
``

1) Integrar el dataset custom

- Dos opciones:
  - Editar `src/ia_modelo_sklearn.py` para que `_build_activity_dataset()` lea `data/ia_dataset_custom.csv` y añada sus pares.
  - O colocar las frases dentro de `ACTIVIDAD_POR_ESCOPEGIO` de `src/sensor_simulado.py` y entrenar.

1) Re-entrenar y guardar el modelo

- Pasos rápidos desde la raíz del proyecto:

```bash
python -c "from src.ia_modelo_sklearn import get_model, save_model; m = get_model(); save_model()"
```

1) Añadir variantes del habla falconense (consejo práctico)

- Pide a usuarios o al equipo que envíen frases como:
  - "irme a bañar" / "echar un baño" / "bañito"
  - "regar las matas" / "regar matas" / "regar las plantas"
  - "lavar el carro" / "lavar el coche"
  - "lavar los cacharros" / "trastear"

1) Validación

- Separe ~20% del dataset como validación y calcule precisión/recall por etiqueta antes de reemplazar el modelo en producción.

1) Automatizar desde la UI (opcional)

- Puede añadir un botón en la ventana de administración que invoque `save_model()` y muestre el resultado. Si quieres, lo implemento.

1) Buenas prácticas

- Versione modelos: `ia_modelo_YYYYMMDD.pkl`.
- Mantenga el dataset original en `data/ia_dataset_original.csv`.
