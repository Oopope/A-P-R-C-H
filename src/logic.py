from datetime import datetime

def calcular_plan_diario(litros_totales, fecha_fin_str):
    """
    Calcula cuántos litros se pueden usar por día basándose en 
    la fecha actual y la fecha de finalización.
    """
    formato = "%Y-%m-%d"
    fecha_actual = datetime.now()
    fecha_fin = datetime.strptime(fecha_fin_str, formato)
    
    # Calcular días restantes
    dias_restantes = (fecha_fin - fecha_actual).days
    
    if dias_restantes <= 0:
        return litros_totales # O un manejo de error
    
    # Cálculo simple por ahora
    consumo_diario = litros_totales / dias_restantes
    
    return round(consumo_diario, 2), dias_restantes

# Botón de prueba para el Backend
if __name__ == "__main__":
    # Probando con 3000 litros hasta el 21 de junio
    consumo, dias = calcular_plan_diario(3000, "2026-06-21")
    print(f"Prueba Logic: Tienes {dias} días. Gasto diario: {consumo}L.")