# Dataset usado por el modelo de IA local

Este proyecto incluye un clasificador simple construido con scikit-learn que sirve para dos fines:

- Detectar la intención de una consulta del usuario (estado, fuga, minutos, consejo, medidor, saludo).
- Mapear texto libre de actividad doméstica a un escenario simulado (ej: "ducha" → "Ducha Activa").

Estructura del dataset inicial

- `samples`: frases cortas o expresiones que el usuario podría escribir, por ejemplo: "ducha", "voy a lavar los platos", "hay una fuga".

- `labels`: etiqueta asociada a cada frase, por ejemplo: "Ducha Activa", "Lavar Platos", "Fuga Silenciosa".

Origen y limitaciones

- El dataset se genera a partir de las palabras clave definidas en `src/sensor_simulado.py` (variable `ACTIVIDAD_POR_ESCOPEGIO`) y un conjunto pequeño de frases de ejemplo.

- Es un dataset sintético y pequeño: las probabilidades devueltas por el clasificador serán bajas hasta que se enriquezca con ejemplos reales.

Mejoras recomendadas

- Recolectar frases reales de uso local (dialecto falconense) y añadir variaciones: "bañito", "echar un baño", "regar matas", "lavar carro".

- Etiquetar entre 50 y 200 frases por escenario para obtener un clasificador con rendimiento usable.

- Si dispone de registros históricos de actividades reales, anonimizarlos y usarlos para aumentar el dataset.

Persistencia

- El modelo entrenado se guarda (si se solicita) en `data/ia_modelo.pkl` para evitar reentrenar en cada inicio.
