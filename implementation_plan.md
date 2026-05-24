# Arquitectura: Sistema Inteligente de Recursos Hidrológicos (A-P-R-C-H)

Esta es la visión a nivel de Ingeniería de Software para convertir la idea en una aplicación real, multiplataforma y con inteligencia artificial.

## Arquitectura del Proyecto (Separación de Capas)

Como muy bien mencionaste, la clave del éxito es hacer **toda la lógica primero** y dejar la interfaz visual para el final. Esto se conoce en la industria como patrón **MVC (Modelo-Vista-Controlador)**.

1.  **Modelo (Datos):** `database.py` - Lo que ya tienes.
2.  **Controlador (Lógica/IA):** `logic.py` - Lo que vamos a construir ahora.
3.  **Vista (Frontend):** *(Para el futuro)*. Mencionaste "let", seguramente te referías a **Flet** (una excelente librería de Python que te permite hacer apps de escritorio, web y móvil con el mismo código).

---

## Nuevas Funcionalidades Propuestas

A continuación, las funcionalidades que desarrollaremos en `logic.py`, divididas por nivel de complejidad:

### Nivel 1: Plan de Consumo Inteligente (Base)
*   [x] **Cálculo Ideal Diario:** (Ya implementado) Litros totales / Días restantes.
*   [ ] **Catálogo de Actividades:** Diccionario con el costo en litros de cada acción (Bañarse: 18L, Lavar Platos: 15L, Lavar Ropa: 60L, etc.).
*   [ ] **Simulador de Rutinas:** Ingresar una lista de acciones diarias y ver cuántos días duraría el tanque si mantenemos ese ritmo.

### Nivel 2: Probabilidad y Teorema de Bayes (La verdadera IA)
En lugar de una matemática rígida (ej: siempre gastas 50L), usaremos estadística para modelar el comportamiento real de un hogar, donde los gastos varían.
*   [ ] **Probabilidad de Supervivencia Hídrica:** Basado en el teorema de Bayes y la desviación estándar de días anteriores. 
    *   *Ejemplo de salida:* "Con tu consumo actual, hay un **85% de probabilidad** de que llegues al 21 de Junio, y un **15% de probabilidad** de que te quedes sin agua 3 días antes."
*   [ ] **Ajuste Dinámico:** Si un fin de semana llega visita y gastan el doble, el sistema recalcula la probabilidad instantáneamente y te avisa cuánto debes recortar el lunes para volver a un porcentaje seguro.

---

## User Review Required
> [!IMPORTANT]  
> ¿Qué te parecen estas sugerencias adicionales para hacer tu app más robusta?
> 
> 1.  **Modos de Operación:** Botones en la app para activar "Modo Normal", "Modo Ahorro" o "Modo Extremo" (cada uno ajusta los límites sugeridos diarios).
> 2.  **Sistema de Semáforo (Alertas):** Verde (Consumo seguro), Amarillo (Alerta, estás gastando de más), Rojo (Peligro, tanque crítico).
> 3.  **Registro de Fugas:** Un botón para descontar un porcentaje de litros si se detecta un bote de agua o un inodoro dañado.

## Siguiente paso de ejecución
Si apruebas esta visión, el primer paso en el código será crear en `logic.py` la estructura para registrar la **Rutina Diaria (Nivel 1)** y poder restar litros según la actividad (baño, cocina, etc). ¿Comenzamos por ahí?
