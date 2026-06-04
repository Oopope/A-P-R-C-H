from datetime import datetime
import statistics

class ContenedorHidrico:
    def __init__(self, nombre, tipo, capacidad_maxima):
        self.nombre = nombre
        self.tipo = tipo # "Tanque", "Pipa", "Tobo"
        self.capacidad_maxima = capacidad_maxima
        self.litros_actuales = capacidad_maxima
        
    def extraer(self, cantidad):
        """Extrae agua de este contenedor. Retorna la cantidad que no pudo extraer si se vació."""
        if self.litros_actuales >= cantidad:
            self.litros_actuales -= cantidad
            return 0 # Todo fue extraído exitosamente
        else:
            faltante = cantidad - self.litros_actuales
            self.litros_actuales = 0
            return faltante
            
    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.litros_actuales}/{self.capacidad_maxima}L"

class GestorAgua:
    # Catálogo de actividades estándar (litros estimados por acción)
    ACTIVIDADES = {
        "baño": 10,
        "lavar_platos": 15,
        "lavar_ropa": 60,
        "lavar_auto": 100,
        "cocinar": 5,
        "bajar_poceta": 6
    }

    
    # Multiplicador de consumo según el modo de operación
    MODOS_OPERACION = {
        "Normal": 1.0,
        "Ahorro": 0.8,
        "Extremo": 0.6
    }

    def __init__(self, contenedores=None, fecha_fin_str=None):
        import src.database as db
        # 1. Cargar Contenedores
        if contenedores is not None:
            self.contenedores = contenedores
        else:
            self.contenedores = []
            db_conts = db.cargar_contenedores()
            for c in db_conts:
                cont = ContenedorHidrico(c["nombre"], c["tipo"], c["capacidad_maxima"])
                cont.litros_actuales = c["litros_actuales"]
                self.contenedores.append(cont)
                
        # 2. Cargar Configuración (fecha_fin y modo_actual)
        db_fecha_fin, db_modo = db.cargar_configuracion()
        
        if fecha_fin_str is not None:
            self.fecha_fin_str = fecha_fin_str
        else:
            self.fecha_fin_str = db_fecha_fin
            
        self.modo_actual = db_modo
        
        # 3. Cargar Historial para Bayes
        self.historial_consumo = db.cargar_historial_completo()

    @property
    def litros_totales(self):
        """Calcula el total de litros sumando todos los contenedores dinámicamente."""
        return sum(contenedor.litros_actuales for contenedor in self.contenedores)
        
    def agregar_contenedor(self, contenedor):
        self.contenedores.append(contenedor)
        
    def extraer_agua(self, cantidad):
        """Descuenta agua en cascada: vacía contenedores uno por uno."""
        import src.database as db
        faltante = cantidad
        for contenedor in self.contenedores:
            if faltante <= 0:
                break
            if contenedor.litros_actuales > 0:
                # Extraemos y actualizamos el contenedor en memoria
                extraido = min(contenedor.litros_actuales, faltante)
                contenedor.extraer(extraido)
                faltante -= extraido
                # Guardamos en base de datos
                db.actualizar_nivel_contenedor(contenedor.nombre, contenedor.litros_actuales)
                
        if faltante > 0:
            print(f"Alerta: No hay suficiente agua en ningún tanque. Faltaron {faltante}L por extraer.")

    def calcular_consumo_ideal(self):
        hoy = datetime.now().date()
        fecha_fin = datetime.strptime(self.fecha_fin_str, "%Y-%m-%d").date()
        dias_restantes = (fecha_fin - hoy).days
        
        if dias_restantes <= 0:
            return 0 
            
        return self.litros_totales / dias_restantes

    def obtener_limite_diario(self):
        """Calcula el límite diario ajustado por el modo de operación."""
        ideal = self.calcular_consumo_ideal()
        multiplicador = self.MODOS_OPERACION.get(self.modo_actual, 1.0)
        return ideal * multiplicador
        
    def cambiar_modo(self, modo):
        """Cambia el modo de operación."""
        import src.database as db
        if modo in self.MODOS_OPERACION:
            self.modo_actual = modo
            db.guardar_modo(modo)
            print(f"Modo cambiado a: {modo}")
        else:
            print("Modo inválido.")

    def estado_semaforo(self, gasto_diario):
        """Devuelve el estado del consumo basado en el límite diario actual."""
        limite = self.obtener_limite_diario()
        if limite == 0:
            return "Rojo"
            
        porcentaje = gasto_diario / limite
        if porcentaje <= 0.8:
            return "Verde" # Seguro
        elif porcentaje <= 1.0:
            return "Amarillo" # Alerta
        else:
            return "Rojo" # Peligro
            
    def registrar_fuga(self, litros_perdidos):
        """Resta litros directamente por una fuga detectada."""
        import src.database as db
        self.extraer_agua(litros_perdidos)
        # Guardamos el consumo en la base de datos como una fuga
        db.registrar_consumo_db(litros_perdidos, "Fuga Detectada")
        # Actualizamos el historial en memoria
        self.historial_consumo = db.cargar_historial_completo()
        print(f"Fuga registrada: Se han perdido {litros_perdidos}L. Agua total restante: {self.litros_totales}L")

    def agregar_dia_historial(self, gasto_del_dia):
        """Agrega el gasto de un día al historial para cálculos estadísticos."""
        self.historial_consumo.append(gasto_del_dia)

    def registrar_actividad(self, actividad, cantidad=1):
        """Resta del sistema de tanques los litros correspondientes a la actividad."""
        import src.database as db
        if actividad in self.ACTIVIDADES:
            gasto = self.ACTIVIDADES[actividad] * cantidad
            self.extraer_agua(gasto)
            # Guardamos el consumo en la base de datos
            db.registrar_consumo_db(gasto, f"Actividad: {actividad.replace('_', ' ').title()}")
            # Actualizamos el historial en memoria
            self.historial_consumo = db.cargar_historial_completo()
            return gasto
        else:
            print(f"La actividad '{actividad}' no existe en el catálogo.")
            return 0

    def recargar_contenedores(self):
        """Recarga todos los contenedores al 100% de su capacidad en memoria y base de datos."""
        import src.database as db
        for contenedor in self.contenedores:
            contenedor.litros_actuales = contenedor.capacidad_maxima
        db.recargar_todos_los_contenedores()
        # Registramos una recarga con 0 litros gastados
        db.registrar_consumo_db(0, "Recarga de Contenedores al 100%")
        print("Contenedores recargados al 100%.")
            
    def simular_semana(self, rutina_diaria):
        """
        Calcula cuánta agua se gasta en 7 días con la rutina dada.
        rutina_diaria: un diccionario, ej: {"baño": 4, "lavar_platos": 3}
        """
        gasto_diario = 0
        for actividad, cantidad in rutina_diaria.items():
            if actividad in self.ACTIVIDADES:
                gasto_diario += self.ACTIVIDADES[actividad] * cantidad
        
        gasto_semanal = gasto_diario * 7
        return gasto_semanal, gasto_diario

    def probabilidad_supervivencia(self):
        """
        Calcula la probabilidad de llegar a la fecha de corte con agua,
        usando una distribución normal basada en el historial de consumo.
        """
        hoy = datetime.now().date()
        fecha_fin = datetime.strptime(self.fecha_fin_str, "%Y-%m-%d").date()
        dias_restantes = (fecha_fin - hoy).days
        
        if dias_restantes <= 0:
            return 100.0 if self.litros_totales > 0 else 0.0
            
        if len(self.historial_consumo) < 2:
            # No hay suficientes datos, cálculo básico basado en el consumo ideal
            limite = self.obtener_limite_diario()
            proyeccion = limite * dias_restantes
            if proyeccion <= self.litros_totales:
                return 80.0 # Estimación optimista sin datos
            else:
                return 20.0 # Estimación pesimista
                
        media_consumo = statistics.mean(self.historial_consumo)
        desviacion = statistics.stdev(self.historial_consumo)
        
        # Si la desviación es 0 (ej. todos los días gastan exactamente lo mismo)
        if desviacion == 0:
            if media_consumo * dias_restantes <= self.litros_totales:
                return 99.9
            else:
                return 0.1
                
        # Media y desviación de la distribución del consumo TOTAL en los días restantes
        media_total = media_consumo * dias_restantes
        desviacion_total = desviacion * (dias_restantes ** 0.5)
        
        # Calculamos P(Consumo Total <= Litros Totales)
        try:
            dist = statistics.NormalDist(mu=media_total, sigma=desviacion_total)
            probabilidad = dist.cdf(self.litros_totales) * 100
            return round(probabilidad, 2)
        except Exception:
            return 0.0

# --- Prueba de la lógica (Arquitectura de Contenedores) ---
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    
    import src.database as db
    db.inicializar_bd()
    db.cargar_datos_iniciales()
    
    # Creamos un par de contenedores
    tanque_principal = ContenedorHidrico("Tanque Subterráneo", "Tanque", 1000)
    pipa_respaldo = ContenedorHidrico("Pipa de Baño", "Pipa", 200)
    
    # Iniciamos el gestor con la lista de contenedores (Total = 1200L)
    gestor = GestorAgua([tanque_principal, pipa_respaldo], "2026-06-21")
    
    print(f"Inventario Hídrico Inicial: {gestor.litros_totales}L en total")
    for c in gestor.contenedores:
        print(f" - {c}")
        
    print(f"\nLímite diario ideal: {gestor.calcular_consumo_ideal():.2f}L")
    
    print("\n--- Simulación de Extracción en Cascada ---")
    print("Gastando 900L (lavado general)...")
    gestor.registrar_actividad("lavar_auto", 9) # 900L
    for c in gestor.contenedores:
        print(f" - {c}")
        
    print("\nGastando 150L adicionales...")
    gestor.extraer_agua(150)
    for c in gestor.contenedores:
        print(f" - {c}")
        
    print(f"\nTotal restante en el sistema: {gestor.litros_totales}L")
    
    print("\n--- Inteligencia Artificial ---")
    gestor.agregar_dia_historial(150)
    gestor.agregar_dia_historial(140)
    prob = gestor.probabilidad_supervivencia()
    print(f"Con {gestor.litros_totales}L restantes y este alto consumo, la probabilidad de sobrevivir es: {prob}%")


