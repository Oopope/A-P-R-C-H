# Glosario Técnico y Documentación

Este documento es una recopilación de los conceptos clave de Ingeniería de Software que estamos aplicando en el desarrollo del **Sistema Inteligente de Recursos Hidrológicos (A-P-R-C-H)**.

---

## 1. Arquitectura de Software
Es el "plano de construcción" del programa. Define cómo se organiza el código a gran escala. Una buena arquitectura previene que el proyecto se convierta en un desastre inmanejable a medida que crece.

### MVC (Modelo-Vista-Controlador)
Es la arquitectura específica que elegimos para este proyecto. Divide el software en tres responsabilidades separadas:
*   **Modelo (`database.py`):** Se encarga exclusivamente de los datos. Es la base de datos (SQLite) y su conexión.
*   **Controlador (`logic.py`):** Es el "cerebro". Contiene la lógica matemática, los cálculos y el Teorema de Bayes. Pide datos al Modelo y se los entrega a la Vista.
*   **Vista (Flet):** Es la interfaz gráfica (los botones, pantallas y colores que verá el usuario final). No hace matemáticas complejas, solo muestra la información que le da el Controlador.

## 2. Refactorización
Consiste en **reestructurar y mejorar el código por dentro sin alterar lo que hace por fuera**.
*   *Ejemplo:* Cambiar un código largo y confuso por uno más corto y eficiente. El usuario no ve ninguna diferencia en la pantalla, pero el desarrollador sabe que ahora el programa es más rápido, seguro o fácil de leer.

## 3. POO (Programación Orientada a Objetos)
Es un estilo de programación donde se crean "Objetos" que tienen características y acciones.
*   En lugar de tener variables sueltas por todos lados, agrupamos la información en entidades. Por ejemplo, creamos la clase `ContenedorHidrico` para representar un tanque físico (con su propio nombre y capacidad).
*   **Composición:** Es una técnica avanzada de POO donde un objeto "administra" a otros objetos en lugar de tener todo mezclado. Ejemplo: Nuestra clase `GestorAgua` no guarda los litros directamente, sino que administra una lista de objetos `ContenedorHidrico`, sumando su capacidad dinámicamente y delegando responsabilidades de forma ordenada y profesional.

## 4. Consultas Parametrizadas (Prevención de Inyección SQL)
Es una medida de seguridad en bases de datos.
*   En lugar de construir comandos SQL juntando texto (lo cual permite que hackers inserten comandos maliciosos), usamos el símbolo `?` y le pasamos los datos por separado. Ejemplo: `cursor.execute("INSERT INTO tabla VALUES (?, ?)", (valor1, valor2))`.

---

## 5. Lógica del Sistema (A-P-R-C-H)

### Límite Diario y Modos de Operación
*   **Límite Diario Ideal:** Es el presupuesto máximo de agua del día (`Litros / Días restantes`) para asegurar llegar a la fecha de corte.
*   **Modos de Operación:** Modificadores matemáticos que ajustan este límite de forma artificial. Por ejemplo, el "Modo Ahorro" multiplica el límite ideal por `0.8` (80%), forzando al sistema a ser más estricto y generar un margen de seguridad.

### Sistema de Alertas (Semáforo)
Mecanismo de validación basado en porcentajes que compara tu consumo actual contra el límite diario:
*   🟢 **Verde** (`<= 80%`): Consumo seguro.
*   🟡 **Amarillo** (`<= 100%`): Consumo al ras.
*   🔴 **Rojo** (`> 100%`): Consumo excedido, compromete el futuro.

### Inteligencia Estadística (Probabilidad de Supervivencia)
En lugar de predicciones lineales, el sistema analiza el `historial_consumo` utilizando estadística avanzada para crear una **Campana de Gauss** (Distribución Normal). 
Se extrae:
1.  **La Media:** El promedio de gasto diario.
2.  **La Desviación Estándar:** Qué tan inestable o caótico es el comportamiento de consumo.
Al cruzar esto, la librería `statistics` calcula con precisión porcentual la probabilidad real de sobrevivir hasta la fecha final.

## 6. Módulos Nativos de Python (Librerías)

### `datetime` (Manejo de Tiempo)
Herramienta indispensable para manipular fechas de manera matemática, no solo como cadenas de texto.
*   `datetime.now()`: Obtiene la fecha y hora exacta del reloj del sistema.
*   `.date()`: Recorta la hora para trabajar únicamente con la información del día/mes/año.
*   `.strptime(texto, formato)`: Magia pura que transforma texto inerte (ej. `"2026-05-15"`) en un "Objeto Fecha" operable matemáticamente.

## 7. Explicación No Técnica (Analogía Financiera)
Para explicar el funcionamiento de esta aplicación a personas sin conocimientos de programación (como en una presentación), la mejor analogía es compararla con un **Asesor Financiero**:

*"La aplicación trata el agua de tu tanque como si fuera tu sueldo del mes en el banco. El objetivo es que no te quedes en bancarrota (sin agua) antes de que llegue el próximo pago."*

1.  **Presupuesto Diario (Límite):** Igual que divides tu sueldo entre los días del mes para saber cuánto puedes gastar por día, la app calcula tu presupuesto ideal de agua.
2.  **Semáforo de Gastos:** Si gastas menos de tu presupuesto estás en Verde. Si lo gastas justo estás en Amarillo. Si gastas de más estás en Rojo (le estás robando agua a tu 'yo' del futuro).
3.  **Modos de Ahorro:** Si sabes que el fin de semana lavarás mucha ropa, activas el Modo Ahorro. Esto baja tu presupuesto diario artificialmente en la semana, obligándote a guardar agua para el fin de semana.
4.  **Asesor Estadístico:** La app nota si eres caótico con tus gastos. Si un día gastas poco y al otro muchísimo, la estadística matemática detecta ese patrón y te lanza una probabilidad real (ej: *"Tienes solo un 15% de probabilidad de llegar con agua al último día"*), ayudándote a tomar medidas correctivas.

---

## 8. Enlaces de Documentación Oficiales
La documentación es el manual de instrucciones creado por los creadores de las herramientas.

*   **Python:** [https://docs.python.org/es/3/](https://docs.python.org/es/3/) (Manual oficial en español).
*   **SQLite:** [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html) (Instrucciones para la base de datos).
*   **Flet:** [https://flet.dev/docs/](https://flet.dev/docs/) (Guía para crear interfaces gráficas de PC y Teléfono usando Python).
*   **FreeCodeCamp:** [https://www.freecodecamp.org/espanol/](https://www.freecodecamp.org/espanol/) (Excelente para aprender conceptos y buenas prácticas de programación).
