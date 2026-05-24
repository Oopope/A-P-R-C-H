# Resumen: Implementación del Nivel 1

Hemos completado el primer bloque lógico del "Plan de Consumo Inteligente" en `logic.py`. Ahora el sistema es capaz de entender actividades de la vida real y proyectar el consumo.

## ¿Qué ha cambiado?

### 1. Catálogo de Actividades (`ACTIVIDADES`)
Se ha añadido un diccionario maestro que define cuánto gasta cada acción en el hogar. Esto permite que en el futuro la interfaz visual (Flet) solo necesite enviar el nombre de la acción:
```python
ACTIVIDADES = {
    "baño": 18,
    "lavar_platos": 15,
    "lavar_ropa": 60,
    "lavar_auto": 100,
    "cocinar": 5,
    "bajar_poceta": 6
}
```

### 2. Simulador de Semana (`simular_semana`)
Se ha creado un motor que toma una "Rutina" (un grupo de actividades que suceden en un día normal) y calcula:
- El **Gasto Diario Real** (basado en hábitos, no en el ideal matemático).
- El **Gasto Semanal**.

### 3. Sistema de Alerta Temprana
En el bloque de pruebas (al final del archivo), el sistema ahora cruza el "Límite Ideal" con el "Gasto Diario Real".
- Si la rutina consume menos del límite: **✅ Sistema Estable**.
- Si la rutina consume más del límite: **⚠️ ALERTA**, y calcula exactamente en cuántos días se secará el tanque a ese ritmo.

## Próximos Pasos (Arquitectura MVC & Flet)
Para continuar con la construcción de este sistema inteligente:
1. Deberemos conectar esta lógica pura con la base de datos `database.py` para que el tanque inicial no sea estático (`3000`), sino que lea lo que el usuario guardó.
2. Preparar las bases para la UI (Flet).
3. (Opcional pero recomendado) Empezar a pensar en cómo registrar los datos del pasado para aplicar el Nivel 2 (Teorema de Bayes).
