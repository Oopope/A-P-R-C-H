import random

class SensorSimulado:
    # Catálogo de escenarios con sus valores típicos
    ESCENARIOS = {
        "Reposo": {
            "caudal_base": 0.0,
            "caudal_ruido": 0.0,
            "presion_base": 50.0,
            "presion_ruido": 0.3,
            "temp_base": 20.0,
            "actividad_id": 0,  # Ninguna
            "descripcion": "Sin consumo activo en la residencia. Válvulas cerradas."
        },
        "Ducha Activa": {
            "caudal_base": 10.0,
            "caudal_ruido": 0.5,
            "presion_base": 42.0,
            "presion_ruido": 1.0,
            "temp_base": 37.5,
            "actividad_id": 1,  # ducha
            "descripcion": "Uso de ducha en cuarto de baño. Consumo regular de agua tibia."
        },
        "Lavar Platos": {
            "caudal_base": 5.0,
            "caudal_ruido": 0.3,
            "presion_base": 45.0,
            "presion_ruido": 0.7,
            "temp_base": 21.0,
            "actividad_id": 2,  # lavar_platos
            "descripcion": "Grifo de cocina abierto para lavado de utensilios domésticos."
        },
        "Lavadora Activa": {
            "caudal_base": 12.0,
            "caudal_ruido": 0.6,
            "presion_base": 40.0,
            "presion_ruido": 1.2,
            "temp_base": 17.5,
            "actividad_id": 3,  # lavar_ropa
            "descripcion": "Ciclo automático de llenado de la lavadora de ropa."
        },
        "Riego de Jardín": {
            "caudal_base": 7.0,
            "caudal_ruido": 0.4,
            "presion_base": 44.0,
            "presion_ruido": 0.8,
            "temp_base": 16.0,
            "actividad_id": 5,  # riego
            "descripcion": "Riego externo con manguera de jardín."
        },
        "Fuga Silenciosa": {
            "caudal_base": 1.5,
            "caudal_ruido": 0.1,
            "presion_base": 48.0,
            "presion_ruido": 0.4,
            "temp_base": 19.0,
            "actividad_id": 0,  # Sin actividad declarada!
            "descripcion": "Fuga moderada no declarada, posible pérdida en inodoro o tubería."
        },
        "Goteo Constante": {
            "caudal_base": 0.3,
            "caudal_ruido": 0.05,
            "presion_base": 49.5,
            "presion_ruido": 0.2,
            "temp_base": 19.5,
            "actividad_id": 0,  # Sin actividad declarada!
            "descripcion": "Grifo mal cerrado o goteo constante en grifería de baño."
        }
    }

    def __init__(self):
        self.escenario_actual = "Reposo"
        self.valvula_abierta = True

    def set_escenario(self, escenario):
        if escenario in self.ESCENARIOS:
            self.escenario_actual = escenario

    def obtener_lectura(self):
        """Simula y retorna las lecturas actuales del sensor de agua."""
        esc = self.ESCENARIOS[self.escenario_actual]

        if not self.valvula_abierta:
            # Si la válvula está cerrada, no hay caudal ni consumo y la presión sube
            return {
                "caudal": 0.0,
                "presion": round(52.5 + random.uniform(-0.1, 0.1), 2),
                "temperatura": round(19.0 + random.uniform(-0.3, 0.3), 1),
                "actividad_id": 0,
                "valvula_estado": "CERRADA",
                "descripcion": "Válvula principal de paso cerrada. Flujo interrumpido."
            }

        # Simular lectura con ruido aleatorio
        caudal = max(0.0, esc["caudal_base"] + random.uniform(-esc["caudal_ruido"], esc["caudal_ruido"]))
        presion = max(0.0, esc["presion_base"] + random.uniform(-esc["presion_ruido"], esc["presion_ruido"]))
        temperatura = esc["temp_base"] + random.uniform(-0.4, 0.4)

        return {
            "caudal": round(caudal, 2),
            "presion": round(presion, 2),
            "temperatura": round(temperatura, 1),
            "actividad_id": esc["actividad_id"],
            "valvula_estado": "ABIERTA",
            "descripcion": esc["descripcion"]
        }
