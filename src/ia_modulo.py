import random
from datetime import datetime

try:
    import numpy as np
    from sklearn.tree import DecisionTreeClassifier
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class IAModeloHidrico:
    def __init__(self):
        self.clases = {
            0: "Normal (Reposo)",
            1: "Normal (Uso Esperado)",
            2: "Alerta (Posible Fuga en la Red)",
            3: "Alerta (Consumo Excesivo Detectado)",
            4: "Crítico (Reserva de Agua Baja)"
        }
        self.entrenado = False
        if HAS_SKLEARN:
            # max_depth de 4 o 5 para que el árbol sea simple, explicable y simbólico
            self.clf = DecisionTreeClassifier(max_depth=5, random_state=42)
        else:
            self.clf = None

    def entrenar(self):
        """Genera un conjunto de datos sintético exhaustivo y entrena el Árbol de Decisión."""
        if not HAS_SKLEARN:
            print("Aviso: scikit-learn no está instalado. Se utilizará el motor de reglas simbólicas en Python puro.")
            self.entrenado = True
            return

        print("Entrenando el modelo de IA simbólica (DecisionTreeClassifier de Scikit-Learn)...")
        X = []
        y = []

        # Catálogo de Actividades para entrenamiento:
        # ID 0: Ninguna (flujo ~0)
        # ID 1: Ducha (flujo ~10 L/min)
        # ID 2: Lavar Platos (flujo ~5 L/min)
        # ID 3: Lavadora (flujo ~12 L/min)
        # ID 4: Cocinar (flujo ~2 L/min)
        # ID 5: Riego (flujo ~7 L/min)
        # ID 6: Lavar Auto (flujo ~15 L/min)

        # 1. CLASE 4: Crítico (Reserva de Agua Baja) - Si el nivel del tanque es < 15%
        # Esta es la alerta de mayor prioridad sin importar el flujo
        for _ in range(300):
            porcentaje = random.uniform(0.0, 14.99)
            caudal = random.uniform(0.0, 25.0)
            presion = random.uniform(20.0, 52.0)
            act = random.randint(0, 6)
            X.append([caudal, presion, act, porcentaje])
            y.append(4)

        # Para las siguientes clases, el nivel del tanque es seguro (>= 15%)
        # 2. CLASE 0: Normal (Reposo) - Flujo nulo o goteo mínimo, sin actividad
        for _ in range(400):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(0.0, 0.49)  # caudal muy bajo
            presion = random.uniform(49.0, 52.0)  # presión máxima estable
            act = 0
            X.append([caudal, presion, act, porcentaje])
            y.append(0)

        # 3. CLASE 1: Normal (Uso Esperado) - Flujo y presión corresponden a la actividad declarada
        # Ducha (ID 1): caudal 8-12
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(8.0, 12.0)
            presion = random.uniform(40.0, 44.0)
            act = 1
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # Lavar Platos (ID 2): caudal 4-6
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(4.0, 6.5)
            presion = random.uniform(43.0, 47.0)
            act = 2
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # Lavadora (ID 3): caudal 10-14
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(10.0, 14.0)
            presion = random.uniform(38.0, 42.0)
            act = 3
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # Cocinar (ID 4): caudal 1.5 - 3
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(1.5, 3.5)
            presion = random.uniform(46.0, 49.0)
            act = 4
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # Riego (ID 5): caudal 5.5 - 8.5
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(5.5, 8.5)
            presion = random.uniform(42.0, 45.0)
            act = 5
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # Lavar Auto (ID 6): caudal 13 - 17
        for _ in range(100):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(13.0, 17.0)
            presion = random.uniform(35.0, 39.0)
            act = 6
            X.append([caudal, presion, act, porcentaje])
            y.append(1)

        # 4. CLASE 2: Alerta (Posible Fuga en la Red) - Caudal considerable sin actividad declarada (act = 0)
        # Esto incluye pérdidas por roturas o grifos abiertos por descuido
        for _ in range(300):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(0.5, 5.0)  # Fuga
            presion = random.uniform(45.0, 49.0)
            act = 0  # Declarado: Reposo
            X.append([caudal, presion, act, porcentaje])
            y.append(2)

        # 5. CLASE 3: Alerta (Consumo Excesivo Detectado) - Flujo anormalmente alto
        # Caudal supera los 17.5 L/min o es demasiado alto para actividades cotidianas
        for _ in range(250):
            porcentaje = random.uniform(15.0, 100.0)
            caudal = random.uniform(17.5, 30.0)  # Flujo muy alto
            presion = random.uniform(28.0, 36.0)  # Caída notable de presión
            act = random.choice([1, 2, 4, 5])  # Actividades que no justifican tal flujo
            X.append([caudal, presion, act, porcentaje])
            y.append(3)

        X = np.array(X)
        y = np.array(y)

        # Entrenar el clasificador
        self.clf.fit(X, y)
        self.entrenado = True
        print("Entrenamiento completado. El árbol de decisión simbólico está listo.")

    def predecir(self, caudal, presion, act_id, porcentaje_tanque):
        """Predice el estado hídrico actual utilizando el modelo de clasificación."""
        if not self.entrenado:
            self.entrenar()

        if HAS_SKLEARN:
            X_test = np.array([[caudal, presion, act_id, porcentaje_tanque]])
            pred = self.clf.predict(X_test)[0]
            prob = self.clf.predict_proba(X_test)[0][pred] * 100
            return pred, self.clases[pred], round(prob, 1)
        else:
            # Fallback en Python Puro (Motor de reglas lógicas idénticas al árbol de decisión)
            # Prioridad 1: Nivel de reserva crítico
            if porcentaje_tanque < 15.0:
                return 4, self.clases[4], 99.9

            # Prioridad 2: Consumo Excesivo (Caudal excesivo)
            if caudal > 17.5:
                return 3, self.clases[3], 95.0

            # Prioridad 3: Posible fuga (Caudal activo sin actividad declarada)
            if caudal >= 0.5 and act_id == 0:
                return 2, self.clases[2], 94.5

            # Prioridad 4: Normal Reposo
            if caudal < 0.5 and act_id == 0:
                return 0, self.clases[0], 98.0

            # Prioridad 5: Normal en Uso
            return 1, self.clases[1], 90.0

    def obtener_reglas_simbolicas(self):
        """Traduce la estructura del árbol de decisión de Scikit-Learn a reglas lógicas legibles (IF-THEN)."""
        if not self.entrenado:
            self.entrenar()

        if HAS_SKLEARN:
            tree = self.clf.tree_
            feature_names = ["Caudal (L/min)", "Presión (PSI)", "Actividad Declarada (ID)", "Nivel Tanque (%)"]
            reglas = []

            def recurse(node, depth, path):
                if tree.feature[node] != -2:  # Nodo interno
                    name = feature_names[tree.feature[node]]
                    threshold = tree.threshold[node]

                    # Rama izquierda
                    left_path = path + [f"{name} <= {threshold:.2f}"]
                    recurse(tree.children_left[node], depth + 1, left_path)

                    # Rama derecha
                    right_path = path + [f"{name} > {threshold:.2f}"]
                    recurse(tree.children_right[node], depth + 1, right_path)
                else:  # Nodo hoja
                    val = tree.value[node][0]
                    clase_id = np.argmax(val)
                    clase_nombre = self.clases[clase_id]
                    reglas.append(f"SI {' Y '.join(path)} -> ENTONCES {clase_nombre}")

            recurse(0, 1, [])
            return reglas
        else:
            return [
                "SI Nivel Tanque (%) < 15.00 -> ENTONCES Crítico (Reserva de Agua Baja)",
                "SI Caudal (L/min) > 17.50 Y Nivel Tanque (%) >= 15.00 -> ENTONCES Alerta (Consumo Excesivo Detectado)",
                "SI Caudal (L/min) >= 0.50 Y Actividad Declarada (ID) == 0 Y Nivel Tanque (%) >= 15.00 -> ENTONCES Alerta (Posible Fuga en la Red)",
                "SI Caudal (L/min) < 0.50 Y Actividad Declarada (ID) == 0 Y Nivel Tanque (%) >= 15.00 -> ENTONCES Normal (Reposo)",
                "SI Caudal (L/min) >= 0.50 Y Actividad Declarada (ID) != 0 Y Nivel Tanque (%) >= 15.00 -> ENTONCES Normal (Uso Esperado)"
            ]


def obtener_respuesta_asistente(pregunta, gestor, sensor_reading, ia_modelo):
    """
    Analiza la pregunta del usuario formalmente y emite una respuesta clara y respetuosa.
    Utiliza el motor de IA simbólica y los datos del medidor de agua.
    """
    pregunta = pregunta.lower().strip()

    # Cálculo de métricas básicas
    litros_totales = gestor.litros_totales
    capacidad_total = sum(c.capacidad_maxima for c in gestor.contenedores)
    porcentaje = (litros_totales / capacidad_total * 100) if capacidad_total > 0 else 0.0

    # Lectura del medidor físico
    caudal = sensor_reading["caudal"]
    presion = sensor_reading["presion"]
    act_id = sensor_reading["actividad_id"]

    # Predicción mediante el modelo simbólico
    pred_id, pred_nombre, pred_prob = ia_modelo.predecir(caudal, presion, act_id, porcentaje)

    # Cálculo de tiempos restantes
    minutos_restantes = gestor.obtener_minutos_restantes()
    hoy = datetime.now().date()
    try:
        fecha_fin = datetime.strptime(gestor.fecha_fin_str, "%Y-%m-%d").date()
        dias_restantes = max((fecha_fin - hoy).days, 0)
    except Exception:
        dias_restantes = 0

    # Respuestas formalizadas (Usted/Estimado usuario)
    
    # 1. Estado de tanques y reservas
    if any(k in pregunta for k in ["tanque", "litros", "reserva", "agua", "cuanta queda", "estado", "porcentaje", "como va"]):
        res = (
            f"🤖 **Asistente Aqualy:**\n\n"
            f"Estimado usuario, me dirijo a usted para informarle sobre el estado actual de sus depósitos de reserva:\n\n"
            f"💧 **Volumen disponible:** {litros_totales:.1f} Litros.\n"
            f"📊 **Nivel de almacenamiento:** {porcentaje:.1f}% de la capacidad total ({capacidad_total:.0f} L).\n"
            f"📅 **Tiempo disponible:** Le restan aproximadamente **{dias_restantes} días** hasta la fecha límite establecida ({gestor.fecha_fin_str}).\n\n"
        )
        if pred_id == 4:
            res += "⚠️ **ALERTA CRÍTICA:** Sus reservas se encuentran en un nivel extremadamente bajo (inferior al 15%). Le sugiero encarecidamente gestionar una recarga inmediata."
        else:
            res += f"Basado en su historial de consumo, usted cuenta con una probabilidad del **{gestor.probabilidad_supervivencia()}%** de abastecimiento continuo hasta la fecha de corte."
        return res

    # 2. Fugas de agua
    elif any(k in pregunta for k in ["fuga", "perdiendo", "tubería", "goteo", "perdiendo agua", "leak"]):
        if pred_id == 2:
            return (
                f"🤖 **Asistente Aqualy:**\n\n"
                f"⚠️ **ADVERTENCIA DE SEGURIDAD HÍDRICA**\n"
                f"He detectado un flujo continuo en el medidor de **{caudal:.2f} L/min** a una presión de **{presion:.1f} PSI**, "
                f"sin embargo, usted no ha reportado ninguna actividad doméstica activa.\n\n"
                f"Existe un riesgo muy elevado de **fuga de agua** en su red hidráulica.\n\n"
                f"👉 **Recomendación:** Le aconsejo cerrar de inmediato la **Válvula Principal** desde el panel de control del medidor para mitigar el desperdicio."
            )
        elif caudal > 0 and act_id == 0:
            return (
                f"🤖 **Asistente Aqualy:**\n\n"
                f"Se registra un flujo de agua muy leve (**{caudal:.2f} L/min**). Esto podría deberse a un grifo mal cerrado o un goteo menor en su residencia.\n"
                f"El modelo de IA clasifica este comportamiento como una fuga menor con una confianza del {pred_prob}%."
            )
        else:
            return (
                f"🤖 **Asistente Aqualy:**\n\n"
                f"Le informo que no se ha detectado ninguna anomalía o fuga en sus tuberías.\n"
                f"El caudal actual se mantiene en **{caudal:.2f} L/min** (Reposo) y la presión hidráulica es óptima a **{presion:.1f} PSI**."
            )

    # 3. Minutos restantes por actividades domésticas
    elif any(k in pregunta for k in ["ducha", "minutos", "baño", "lavar", "cocinar", "ropa", "tiempo", "duracion"]):
        ducha_m = minutos_restantes.get("ducha", 0)
        platos_m = minutos_restantes.get("lavar_platos", 0)
        ropa_m = minutos_restantes.get("lavar_ropa", 0)
        cocinar_m = minutos_restantes.get("cocinar", 0)
        riego_m = minutos_restantes.get("riego", 0)
        
        return (
            f"🤖 **Asistente Aqualy:**\n\n"
            f"Estimado usuario, traduciendo su reserva total de **{litros_totales:.1f} Litros** a minutos de uso exclusivo por actividad doméstica:\n\n"
            f"🚿 **Ducha**: dispone usted de **{ducha_m} minutos**.\n"
            f"🍽️ **Lavar Vajilla**: dispone de **{platos_m} minutos**.\n"
            f"🧺 **Lavadora**: dispone de **{ropa_m} minutos**.\n"
            f"🍳 **Cocinar**: dispone de **{cocinar_m} minutos**.\n"
            f"🌿 **Riego de Plantas**: dispone de **{riego_m} minutos**.\n\n"
            f"Le recordamos que estas estimaciones se basan en las tasas de flujo por minuto configuradas en su panel."
        )

    # 4. Consejos de ahorro y recomendaciones de la IA
    elif any(k in pregunta for k in ["consejo", "recomienda", "ahorrar", "ia", "sugerencia", "que hago", "ayuda"]):
        prob = gestor.probabilidad_supervivencia()
        modo = gestor.modo_actual

        res = f"🤖 **Recomendaciones del Sistema Aqualy:**\n\n"
        if prob > 85:
            res += (
                f"Su probabilidad de llegar a la fecha de corte es excelente (**{prob}%**). Su modo de operación actual es **{modo}**.\n"
                f"Le sugiero mantener sus buenos hábitos de consumo actuales. Recuerde realizar un uso prudente del recurso."
            )
        elif prob > 50:
            res += (
                f"Usted cuenta con una probabilidad moderada (**{prob}%**) de abastecimiento. \n"
                f"Le recomiendo encarecidamente activar el **Modo de Ahorro** en el Panel de Administración. "
                f"Esto reducirá de forma automática los límites de consumo diario en un 20% para asegurar el agua."
            )
        else:
            res += (
                f"🚨 **ESTADO DE ATENCIÓN PRIORITARIA:** Su probabilidad de supervivencia hídrica es muy baja (**{prob}%**).\n"
                f"Le aconsejo formalmente cambiar su modo de operación a **Extremo** (lo que aplica una reducción del 40% en consumos diarios).\n"
                f"Asimismo, le insto a posponer actividades no indispensables como el riego o el lavado de vehículos hasta regularizar su reserva."
            )
        return res

    # 5. Qué es el medidor físico simulado
    elif any(k in pregunta for k in ["medidor", "fisico", "sensor", "funcionamiento", "explicacion", "para que sirve"]):
        return (
            f"🤖 **Asistente Aqualy:**\n\n"
            f"El **Medidor Hídrico Digital** es un simulador que representa el sensor físico de caudal acoplado a las tuberías de su hogar.\n"
            f"Monitorea el flujo en tiempo real (L/min) y la presión hidráulica (PSI).\n"
            f"A través de nuestro Árbol de Decisión Simbólico (IA), el sistema analiza estos parámetros para:\n\n"
            f"1. **Descontar automáticamente** el volumen de agua de sus reservas a medida que fluye, sin necesidad de que usted registre datos manualmente.\n"
            f"2. **Identificar fugas de agua** si detecta flujo sin que se haya reportado una actividad.\n"
            f"3. **Proteger sus recursos** sugiriendo el cierre de la válvula principal en caso de incidentes."
        )

    # 6. Saludo formal inicial
    elif any(k in pregunta for k in ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "saludo"]):
        hora = datetime.now().hour
        if hora < 12:
            saludo = "Buenos días"
        elif hora < 19:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
        return (
            f"🤖 **Asistente Aqualy:**\n\n"
            f"¡{saludo}! Es un placer asistirle hoy, estimado usuario.\n"
            f"Me encuentro monitoreando de forma activa el caudal y el estado de sus reservas hidráulicas.\n"
            f"¿En qué puedo serle de utilidad en este momento? Puede consultarme sobre sus reservas, fugas de agua o recomendaciones de ahorro."
        )

    # Default
    else:
        return (
            f"🤖 **Asistente Aqualy:**\n\n"
            f"Disculpe, estimado usuario, no he logrado interpretar con claridad su consulta.\n"
            f"Le invito a consultarme formalmente sobre los siguientes aspectos del sistema hídrico:\n"
            f"• El nivel de sus recipientes (ej: *¿Cómo va el tanque?*)\n"
            f"• La presencia de fugas en la instalación (ej: *¿Tengo alguna fuga?*)\n"
            f"• Los minutos restantes para sus actividades (ej: *¿Cuánta agua me queda para la ducha?*)\n"
            f"• Sugerencias de optimización (ej: *¿Qué me recomienda la IA?*)\n"
            f"• El sensor físico (ej: *¿Cómo funciona el medidor?*)\n\n"
            f"Si lo prefiere, usted puede presionar cualquiera de los **botones de preguntas rápidas** situados al final de esta ventana."
        )
