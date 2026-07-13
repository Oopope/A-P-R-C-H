# Re-entrenamiento del modelo local de IA

Qué significa re-entrenar
- Re-entrenar consiste en volver a ajustar los parámetros del modelo (entrenarlo) usando un conjunto de datos ampliado o corregido. En este proyecto, re-entrenar actualizará los clasificadores para mejorar la detección de actividades e intenciones.

Cuándo re-entrenar
- Después de recopilar nuevas muestras etiquetadas (por ejemplo, 50–200 frases nuevas por escenario).
- Tras corregir etiquetas erróneas o agregar variantes del habla local (p. ej. modismos de Falcón).

Cómo re-entrenar localmente
1. Añada/compile un archivo CSV o JSON con pares (texto, etiqueta) y guárdelo en `data/ia_dataset_custom.*`.
2. Desde el código, importe `src.ia_modelo_sklearn`, ejecute el método `train()` del modelo o elimine `data/ia_modelo.pkl` y reinicie la aplicación para forzar re-entrenamiento.
3. Opcionalmente, guarde el modelo entrenado con `src.ia_modelo_sklearn.save_model()`; esto persistirá el archivo `data/ia_modelo.pkl`.

Comandos sugeridos
```bash
# Forzar re-entrenamiento desde Python
python -c "from src.ia_modelo_sklearn import get_model, save_model; m = get_model(); save_model()"

# O en Windows PowerShell
py -c "from src.ia_modelo_sklearn import get_model, save_model; m = get_model(); save_model()"
```

Buenas prácticas
- Mantenga una copia del dataset original antes de hacer cambios masivos.
- Valide el rendimiento en un subconjunto de validación antes de reemplazar el modelo en producción.
- Versione los modelos guardados usando nombres con fecha, por ejemplo: `ia_modelo_2026-07-12.pkl`.
