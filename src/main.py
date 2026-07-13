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
  4. Instanciar el SensorSimulado.
  5. Mostrar el WelcomeDialog de bienvenida (solo la primera vez de la sesión).
    6. Si el usuario acepta, mostrar la ventana principal AqualyDashboard.
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
from src.ui.main_window import AqualyDashboard, WelcomeDialog
from src.ui.styles import DARK_THEME_QSS
import src.database as db
from src.sensor_simulado import SensorSimulado
from src.ia_modelo_sklearn import get_model, save_model


def main():
    # ── 1. Inicializar Base de Datos ─────────────────────────────────────────
    db.inicializar_bd()
    db.cargar_datos_iniciales()

    # ── 2. Crear el Gestor de Agua ────────────────────────────────────────────
    gestor = GestorAgua()

    # ── 3. Garantizar historial mínimo para el cálculo de proyecciones ──────
    if len(gestor.historial_consumo) < 2:
        db.registrar_consumo_db(140.0, "Histórico inicial")
        db.registrar_consumo_db(155.0, "Histórico inicial")
        db.registrar_consumo_db(148.0, "Histórico inicial")
        gestor.historial_consumo = db.cargar_historial_completo()

    # ── 4. Instanciar Sensor ────────────────────────────────────────────────
    sensor = SensorSimulado()

    # ── Inicializar / entrenar modelo IA local y persistir si es la primera vez
    try:
        m = get_model()
        # Intentar persistir modelo para evitar reentrenamiento en siguientes arranques
        saved = save_model()
        if saved:
            print(f"Modelo de IA persistido en: {saved}")
    except Exception:
        # No bloquear la UI si falla el entrenamiento/persistencia
        print("Advertencia: no se pudo inicializar el modelo de IA local.")

    # ── 5. Iniciar la Aplicación PyQt5 ───────────────────────────────────────
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)

    # ── 6. Mostrar el diálogo de bienvenida de única vez ─────────────────────
    welcome = WelcomeDialog()
    resultado = welcome.exec_()   # Bloquea hasta que el usuario pulse "Entrar al Sistema"

    if resultado != WelcomeDialog.Accepted:
        # El usuario cerró el diálogo sin aceptar → salir sin abrir la app
        sys.exit(0)

    # ── 7. Mostrar la Ventana Principal ───────────────────────────────────────
    ventana = AqualyDashboard(gestor, sensor)
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
