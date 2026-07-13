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
        "Cocina Activa": {
            "caudal_base": 4.5,
            "caudal_ruido": 0.35,
            "presion_base": 46.0,
            "presion_ruido": 0.7,
            "temp_base": 22.0,
            "actividad_id": 4,  # cocina
            "descripcion": "Uso de grifos en cocina para lavar ingredientes y preparar alimentos."
        },
        "Limpieza Doméstica": {
            "caudal_base": 6.5,
            "caudal_ruido": 0.35,
            "presion_base": 43.0,
            "presion_ruido": 0.8,
            "temp_base": 19.0,
            "actividad_id": 6,  # limpieza
            "descripcion": "Limpieza de pisos y superficies con cubeta y mopa en el hogar."
        },
        "Lavado de Auto": {
            "caudal_base": 9.5,
            "caudal_ruido": 0.45,
            "presion_base": 41.5,
            "presion_ruido": 1.0,
            "temp_base": 18.5,
            "actividad_id": 7,  # lavar_auto
            "descripcion": "Lavado del vehículo en el patio con manguera y chorro de agua."
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

    ACTIVIDAD_POR_ESCOPEGIO = [
        ("Ducha Activa", ["ducha", "baño", "bañito", "tina", "regadera", "duchas", "echar un baño", "tomar un baño"]),
        ("Lavar Platos", ["lavar platos", "platos", "lavaplatos", "fregadero", "cacharros", "trastear"]),
        ("Cocina Activa", ["cocina", "cocinar", "lavar ingredientes", "lavar verduras", "hacer sopa", "hacer comida"]),
        ("Lavadora Activa", ["lavadora", "ropa", "lavar ropa", "colada", "tender ropa"]),
        ("Limpieza Doméstica", ["limpiar", "trapear", "fregar", "mopa", "lavar piso", "limpieza"]),
        ("Lavado de Auto", ["lavar carro", "lavar coche", "lavar auto", "lavar camioneta", "lavar moto"]),
        ("Riego de Jardín", ["riego", "jardín", "jardin", "manguera", "regar", "regar matas", "regar plantas", "regar la parcela"]),
        ("Fuga Silenciosa", ["fuga", "goteo", "gotear", "filtración", "pierde agua"]),
    ]

    def __init__(self):
        self.escenario_actual = "Reposo"
        self.valvula_abierta = True

    def set_escenario(self, escenario):
        if escenario in self.ESCENARIOS:
            self.escenario_actual = escenario

    def set_actividad(self, actividad_texto):
        texto = actividad_texto.lower().strip()
        for escenario, claves in self.ACTIVIDAD_POR_ESCOPEGIO:
            if any(clave in texto for clave in claves):
                self.set_escenario(escenario)
                return escenario

        self.set_escenario("Reposo")
        return "Reposo"

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
