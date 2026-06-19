import sys
import os

"""
=============================================================================
ARCHIVO: main.py
PROPÓSITO: Punto de entrada de la aplicación Aqualy.

Secuencia de arranque:
  1. Inicializar la base de datos SQLite y cargar los datos de fábrica.
  2. Crear el GestorAgua (controlador de lógica y recipientes).
  3. Asegurar que existan consumos históricos para el cálculo bayesiano.
  4. Instanciar el SensorSimulado y entrenar el modelo de IA simbólica.
  5. Mostrar el WelcomeDialog de bienvenida (solo la primera vez de la sesión).
  6. Si el usuario acepta, mostrar la ventana principal AqualiDashboard.
=============================================================================
"""

# Asegurar que Python puede importar desde la raíz del proyecto
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS      # Modo compilado (PyInstaller)
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, base_dir)

from PyQt5.QtWidgets import QApplication
from src.logic import GestorAgua
from src.ui.main_window import AqualiDashboard, WelcomeDialog
from src.ui.styles import DARK_THEME_QSS
import src.database as db
from src.ia_modulo import IAModeloHidrico
from src.sensor_simulado import SensorSimulado


def main():
    # ── 1. Inicializar Base de Datos ─────────────────────────────────────────
    db.inicializar_bd()
    db.cargar_datos_iniciales()

    # ── 2. Crear el Gestor de Agua ────────────────────────────────────────────
    gestor = GestorAgua()

    # ── 3. Garantizar historial mínimo para el cálculo bayesiano ─────────────
    if len(gestor.historial_consumo) < 2:
        db.registrar_consumo_db(140.0, "Histórico inicial")
        db.registrar_consumo_db(155.0, "Histórico inicial")
        db.registrar_consumo_db(148.0, "Histórico inicial")
        gestor.historial_consumo = db.cargar_historial_completo()

    # ── 4. Instanciar Sensor y Modelo de IA ──────────────────────────────────
    sensor = SensorSimulado()
    ia = IAModeloHidrico()
    ia.entrenar()   # Entrena el árbol de decisión de scikit-learn

    # ── 5. Iniciar la Aplicación PyQt5 ────────────────────────────────────────
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)

    # ── 6. Mostrar el diálogo de bienvenida de única vez ─────────────────────
    welcome = WelcomeDialog()
    resultado = welcome.exec_()   # Bloquea hasta que el usuario pulse "Entrar al Sistema"

    if resultado != WelcomeDialog.Accepted:
        # El usuario cerró el diálogo sin aceptar → salir sin abrir la app
        sys.exit(0)

    # ── 7. Mostrar la Ventana Principal ───────────────────────────────────────
    ventana = AqualiDashboard(gestor, sensor, ia)
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
