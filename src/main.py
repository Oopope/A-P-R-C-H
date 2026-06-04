import sys
import os

"""
=============================================================================
ARCHIVO: main.py
PROPÓSITO: Es el "Punto de Entrada" (Entry Point) de tu aplicación gráfica.
=============================================================================

¿Qué es PyQt5?
PyQt5 es una herramienta que nos permite usar 'Qt' (un motor gráfico hecho en C++) 
desde Python. Sirve para crear ventanas, botones y cajas de texto de forma profesional.

¿Qué hicimos aquí?
1. Preparamos el entorno para que Python encuentre nuestra carpeta 'src'.
2. Creamos los 'Contenedores' (Tanque y Pipa) y el 'GestorAgua' de tu lógica (logic.py).
3. Iniciamos `QApplication`, que es el motor que mantiene la ventana abierta y 
   escucha cuando haces clic.
4. Creamos y mostramos la ventana `AqualiDashboard` (que diseñamos en main_window.py).
"""

# Asegurar que python puede importar desde la raíz del proyecto
if getattr(sys, 'frozen', False):
    # Si se ejecuta compilado con PyInstaller
    base_dir = sys._MEIPASS
else:
    # Si se ejecuta en desarrollo normal
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, base_dir)

from PyQt5.QtWidgets import QApplication
from src.logic import GestorAgua
from src.ui.main_window import AqualiDashboard
from src.ui.styles import DARK_THEME_QSS
import src.database as db

def main():
    # 1. Inicializar la Base de Datos y cargar valores iniciales
    db.inicializar_bd()
    db.cargar_datos_iniciales()
    
    # 2. Instanciar el Gestor de Agua (se conectará solo a la base de datos)
    gestor = GestorAgua()
    
    # Asegurar que el historial estadístico tenga al menos 3 consumos iniciales para Bayes
    if len(gestor.historial_consumo) < 2:
        db.registrar_consumo_db(140.0, "Consumo Inicial Simulado")
        db.registrar_consumo_db(160.0, "Consumo Inicial Simulado")
        db.registrar_consumo_db(150.0, "Consumo Inicial Simulado")
        gestor.historial_consumo = db.cargar_historial_completo()

    # 3. Iniciar Aplicación PyQt5
    app = QApplication(sys.argv)
    
    # Aplicar la Hoja de Estilos
    app.setStyleSheet(DARK_THEME_QSS)
    
    # 4. Crear y Mostrar la Ventana Principal
    ventana = AqualiDashboard(gestor)
    ventana.show()
    
    # 5. Bucle Principal de Eventos
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
