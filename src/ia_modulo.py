from datetime import datetime


def obtener_respuesta_asistente(pregunta, gestor, sensor_reading):
    """Genera respuestas sencillas para el asistente sin usar un modelo de IA externo."""
    pregunta = pregunta.lower().strip()

    litros_totales = gestor.litros_totales
    capacidad_total = sum(c.capacidad_maxima for c in gestor.contenedores)
    porcentaje = (litros_totales / capacidad_total * 100) if capacidad_total > 0 else 0.0
    caudal = sensor_reading.get("caudal", 0.0)
    presion = sensor_reading.get("presion", 0.0)
    actividad_id = sensor_reading.get("actividad_id", 0)
    valvula_estado = sensor_reading.get("valvula_estado", "ABIERTA")

    minutos_restantes = gestor.obtener_minutos_restantes()
    prob = gestor.probabilidad_supervivencia()
    fecha_limite = gestor.fecha_fin_str

    if any(k in pregunta for k in ["tanque", "litros", "reserva", "agua", "estado", "porcentaje", "como va"]):
        return (
            f"Aqualy dice: Actualmente dispone de {litros_totales:.1f} L "
            f"({porcentaje:.1f}% de la capacidad total). La fecha límite de suministro es {fecha_limite}."
        )

    if any(k in pregunta for k in ["fuga", "perdiendo", "tubería", "goteo", "leak"]):
        if caudal >= 0.5 and actividad_id == 0 and valvula_estado == "ABIERTA":
            return (
                f"Aqualy detecta un flujo activo de {caudal:.2f} L/min "
                "sin actividad reportada. Esto puede indicar una fuga en la red hidráulica."
            )
        return (
            f"No se observa una fuga clara en este momento. El caudal actual es {caudal:.2f} L/min "
            f"y la presión es {presion:.1f} PSI."
        )

    if any(k in pregunta for k in ["minutos", "ducha", "baño", "lavar", "cocinar", "ropa", "tiempo", "duracion"]):
        return (
            "Aqualy estima el tiempo disponible por actividad según sus reservas:\n"
            f"- Ducha: {minutos_restantes.get('ducha', 0)} min\n"
            f"- Lavar platos: {minutos_restantes.get('lavar_platos', 0)} min\n"
            f"- Lavadora: {minutos_restantes.get('lavar_ropa', 0)} min\n"
            f"- Cocinar: {minutos_restantes.get('cocinar', 0)} min\n"
            f"- Riego: {minutos_restantes.get('riego', 0)} min"
        )

    if any(k in pregunta for k in ["consejo", "recomienda", "ahorrar", "sugerencia", "que hago", "ayuda"]):
        if prob > 85:
            return (
                f"Aqualy indica que su probabilidad de abastecimiento es alta ({prob}%). "
                "Mantenga sus hábitos actuales y evite consumos innecesarios."
            )
        if prob > 50:
            return (
                f"Aqualy indica que su probabilidad de abastecimiento es moderada ({prob}%). "
                "Considere activar el modo de ahorro para prolongar sus reservas."
            )
        return (
            f"Aqualy indica que su probabilidad de abastecimiento es baja ({prob}%). "
            "Reduzca el consumo inmediato y recargue sus depósitos si es posible."
        )

    if any(k in pregunta for k in ["medidor", "sensor", "funcionamiento", "para que sirve"]):
        return (
            "El medidor simulado registra el caudal y la presión del agua en tiempo real. "
            "Usa esos datos para mostrar el consumo actual y detectar posibles anomalías."
        )

    if any(k in pregunta for k in ["hola", "buenas", "saludo"]):
        hora = datetime.now().hour
        saludo = "Buenos días" if hora < 12 else "Buenas tardes" if hora < 19 else "Buenas noches"
        return f"{saludo}. Soy Aqualy, su asistente de monitoreo hídrico. ¿En qué puedo ayudarle?"

    return (
        "Aqualy no pudo interpretar su pregunta con claridad. "
        "Por favor pregunte sobre el estado del tanque, fugas, minutos disponibles o consejos de ahorro."
    )
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
