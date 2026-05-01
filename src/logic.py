from datetime import datetime

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

    def __init__(self, litros_totales, fecha_fin_str):
        self.litros_totales = litros_totales
        self.fecha_fin_str = fecha_fin_str

    def calcular_consumo_ideal(self):
        hoy = datetime.now().date()
        fecha_fin = datetime.strptime(self.fecha_fin_str, "%Y-%m-%d").date()
        dias_restantes = (fecha_fin - hoy).days
        
        if dias_restantes <= 0:
            return 0 
            
        return self.litros_totales / dias_restantes

    def registrar_actividad(self, actividad, cantidad=1):
        """Resta del tanque los litros correspondientes a la actividad."""
        if actividad in self.ACTIVIDADES:
            gasto = self.ACTIVIDADES[actividad] * cantidad
            self.litros_totales -= gasto
            return gasto
        else:
            print(f"La actividad '{actividad}' no existe en el catálogo.")
            return 0
            
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

# --- Prueba de la lógica (Nivel 1) ---
if __name__ == "__main__":
    gestor = GestorAgua(1100, "2026-05-15")
    
    print(f"Tanque inicial: {gestor.litros_totales}L")
    consumo_ideal = gestor.calcular_consumo_ideal()
    print(f"Límite diario recomendado para llegar vivo al corte: {consumo_ideal:.2f}L")
    
    print("\n--- Simulador de Consumo Real ---")
    # Ejemplo de una casa con 4 personas
    rutina = {
        "baño": 4,          # 4 baños al día (18L x 4 = 72L)
        "lavar_platos": 3,  # Desayuno, almuerzo, cena (15L x 3 = 45L)
        "bajar_poceta": 8   # Usos de baño a lo largo del día (6L x 8 = 48L)
    }
    
    gasto_semanal, gasto_diario = gestor.simular_semana(rutina)
    print(f"Tu rutina diaria gasta: {gasto_diario}L")
    print(f"En una semana habrás gastado: {gasto_semanal}L")
    
    print("\n--- Verificación del Sistema ---")
    if gasto_diario > consumo_ideal:
        print("⚠️ ALERTA: La rutina actual gasta más de lo que el tanque permite.")
        dias_supervivencia = gestor.litros_totales / gasto_diario
        print(f"A este ritmo, te quedarás sin agua en apenas: {dias_supervivencia:.1f} días.")
    else:
        print("✅ Sistema Estable: Todo en orden. El tanque sobrevivirá con esta rutina.")
