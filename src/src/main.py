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

# Asegurar que python puede importar desde 'src' estando en la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QApplication
from src.logic import GestorAgua, ContenedorHidrico
from src.ui.main_window import AqualiDashboard
from src.ui.styles import DARK_THEME_QSS

def main():
    # 1. Configurar Datos de Prueba (Igual que en logic.py)
    tanque_principal = ContenedorHidrico("Tanque Subterráneo", "Tanque", 1000)
    pipa_respaldo = ContenedorHidrico("Pipa de Baño", "Pipa", 200)
    
    gestor = GestorAgua([tanque_principal, pipa_respaldo], "2026-05-15")
    
    # Añadimos un poco de historial falso para que la probabilidad no sea básica
    gestor.agregar_dia_historial(150)
    gestor.agregar_dia_historial(140)
    gestor.agregar_dia_historial(160)

    # 2. Iniciar Aplicación PyQt5
    app = QApplication(sys.path)
    
    # Aplicar la Hoja de Estilos
    app.setStyleSheet(DARK_THEME_QSS)
    
    # 3. Crear y Mostrar la Ventana Principal
    ventana = AqualiDashboard(gestor)
    ventana.show()
    
    # 4. Bucle Principal de Eventos
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
