"""
=============================================================================
ARCHIVO: main_window.py
PROPÓSITO: Define cómo se ve y se comporta la ventana del sistema.
=============================================================================

¿Qué hicimos aquí?
1. Creamos una clase `AqualiDashboard` que hereda de `QMainWindow`. Esta es nuestra ventana.
2. Usamos "Layouts" (QVBoxLayout para apilar de arriba hacia abajo, y QHBoxLayout para de izquierda a derecha) 
   para organizar los elementos visualmente sin tener que calcular píxeles exactos.
3. Conectamos los Botones (`QPushButton`) a los métodos de nuestra lógica (como `gestor.registrar_actividad()`).
   Cuando haces clic, PyQt5 emite una "señal" que llama a la función conectada.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QComboBox,
    QGridLayout, QMessageBox, QScrollArea, QInputDialog
)
from PyQt5.QtCore import Qt
from src.logic import GestorAgua

class CardWidget(QFrame):
    """Un widget personalizado que actúa como una tarjeta (Card) para organizar el contenido."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setProperty("class", "Card")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "CardTitle")
        self.layout.addWidget(self.title_label)
        
    def add_widget(self, widget):
        self.layout.addWidget(widget)
        
    def add_layout(self, layout):
        self.layout.addLayout(layout)

class AqualiDashboard(QMainWindow):
    def __init__(self, gestor: GestorAgua):
        super().__init__()
        self.gestor = gestor
        
        self.setWindowTitle("Aquali - Dashboard Administrativo")
        self.resize(1000, 750)
        
        self.init_ui()
        self.actualizar_interfaz()
        
    def init_ui(self):
        # Widget Central y Layout Principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # --- Cabecera ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Aquali")
        title_label.setObjectName("AppTitle")
        header_layout.addWidget(title_label)
        
        self.status_label = QLabel("Cargando estado...")
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #94A3B8;")
        header_layout.addWidget(self.status_label)
        
        main_layout.addLayout(header_layout)
        
        # --- Contenido Principal (Grid) ---
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # 1. Panel Izquierdo: Contenedores
        self.panel_contenedores = CardWidget("Estado de Contenedores")
        content_layout.addWidget(self.panel_contenedores, stretch=2)
        
        # Guardaremos referencias a las barras de progreso para actualizarlas
        self.barras_progreso = {}
        
        for contenedor in self.gestor.contenedores:
            cont_layout = QVBoxLayout()
            
            info_label = QLabel(f"{contenedor.nombre} ({contenedor.tipo})")
            info_label.setStyleSheet("font-size: 14px;")
            cont_layout.addWidget(info_label)
            
            pbar = QProgressBar()
            pbar.setMaximum(int(contenedor.capacidad_maxima))
            pbar.setValue(int(contenedor.litros_actuales))
            pbar.setFormat("%v / %m L")
            cont_layout.addWidget(pbar)
            
            self.barras_progreso[contenedor.nombre] = pbar
            self.panel_contenedores.add_layout(cont_layout)
            
        self.panel_contenedores.layout.addStretch() # Empuja todo hacia arriba
        
        # 2. Panel Derecho: Acciones e Información General
        right_panel_layout = QVBoxLayout()
        content_layout.addLayout(right_panel_layout, stretch=1)
        
        # Tarjeta: Resumen del Sistema
        self.panel_resumen = CardWidget("Resumen del Sistema")
        right_panel_layout.addWidget(self.panel_resumen)
        
        self.lbl_probabilidad = QLabel("Probabilidad de llegar con agua: --%")
        self.lbl_probabilidad.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        self.panel_resumen.add_widget(self.lbl_probabilidad)
        
        self.lbl_litros_totales = QLabel("Litros totales: -- L")
        self.lbl_litros_totales.setStyleSheet("font-size: 16px; color: #94A3B8; margin-top: 5px;")
        self.panel_resumen.add_widget(self.lbl_litros_totales)
        
        self.lbl_consumo_hoy = QLabel("Consumo de Hoy: -- L")
        self.lbl_consumo_hoy.setStyleSheet("font-size: 16px; color: #94A3B8; margin-top: 5px;")
        self.panel_resumen.add_widget(self.lbl_consumo_hoy)
        
        # Semáforo de Consumo
        semaforo_layout = QHBoxLayout()
        lbl_sem_title = QLabel("Semáforo:")
        lbl_sem_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.lbl_semaforo = QLabel("Cargando...")
        self.lbl_semaforo.setAlignment(Qt.AlignCenter)
        self.lbl_semaforo.setObjectName("SemaforoVerde")
        semaforo_layout.addWidget(lbl_sem_title)
        semaforo_layout.addWidget(self.lbl_semaforo)
        semaforo_layout.addStretch()
        self.panel_resumen.add_layout(semaforo_layout)
        
        # Configuración de Modo
        modo_layout = QHBoxLayout()
        modo_label = QLabel("Modo de Operación:")
        modo_label.setStyleSheet("color: white;")
        self.combo_modo = QComboBox()
        self.combo_modo.addItems(list(self.gestor.MODOS_OPERACION.keys()))
        self.combo_modo.setCurrentText(self.gestor.modo_actual)
        self.combo_modo.currentTextChanged.connect(self.cambiar_modo)
        
        modo_layout.addWidget(modo_label)
        modo_layout.addWidget(self.combo_modo)
        self.panel_resumen.add_layout(modo_layout)
        
        # Tarjeta: Registrar Actividad
        self.panel_actividades = CardWidget("Registrar Actividad")
        right_panel_layout.addWidget(self.panel_actividades)
        
        grid_actividades = QGridLayout()
        row, col = 0, 0
        for actividad, litros in self.gestor.ACTIVIDADES.items():
            btn = QPushButton(f"{actividad.replace('_', ' ').title()}\n(-{litros}L)")
            btn.clicked.connect(lambda checked, act=actividad: self.registrar_actividad(act))
            grid_actividades.addWidget(btn, row, col)
            col += 1
            if col > 1: # 2 columnas
                col = 0
                row += 1
                
        self.panel_actividades.add_layout(grid_actividades)
        
        # Tarjeta: Operaciones Especiales
        self.panel_operaciones = CardWidget("Panel de Control")
        right_panel_layout.addWidget(self.panel_operaciones)
        
        op_layout = QHBoxLayout()
        self.btn_fuga = QPushButton("Reportar Fuga")
        self.btn_fuga.setObjectName("BtnFuga")
        self.btn_fuga.clicked.connect(self.reportar_fuga)
        
        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.setObjectName("BtnRecargar")
        self.btn_recargar.clicked.connect(self.confirmar_recarga)
        
        op_layout.addWidget(self.btn_fuga)
        op_layout.addWidget(self.btn_recargar)
        self.panel_operaciones.add_layout(op_layout)
        
        right_panel_layout.addStretch()

    def actualizar_interfaz(self):
        """Actualiza todos los valores en pantalla basados en el estado del gestor."""
        # 1. Actualizar Barras de Progreso
        for contenedor in self.gestor.contenedores:
            if contenedor.nombre in self.barras_progreso:
                pbar = self.barras_progreso[contenedor.nombre]
                pbar.setValue(int(contenedor.litros_actuales))
                
        # 2. Actualizar Textos Resumen
        litros = self.gestor.litros_totales
        self.lbl_litros_totales.setText(f"Inventario Total: {litros:.1f} L")
        
        prob = self.gestor.probabilidad_supervivencia()
        self.lbl_probabilidad.setText(f"Probabilidad de llegar con agua: {prob}%")
        
        # Color de la probabilidad dependiendo del valor
        if prob > 80:
            color = "#22C55E" # Verde
        elif prob > 40:
            color = "#EAB308" # Amarillo
        else:
            color = "#EF4444" # Rojo
        self.lbl_probabilidad.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")
        
        # 3. Consumo de Hoy y Semáforo
        import src.database as db
        consumo_hoy = db.obtener_consumo_hoy()
        self.lbl_consumo_hoy.setText(f"Consumo de Hoy: {consumo_hoy:.1f} L")
        
        estado_sem = self.gestor.estado_semaforo(consumo_hoy)
        self.lbl_semaforo.setText(f" {estado_sem.upper()} ")
        
        # Cambiar el color del badge del semáforo asignando la clase QSS correspondiente
        if estado_sem == "Verde":
            self.lbl_semaforo.setObjectName("SemaforoVerde")
        elif estado_sem == "Amarillo":
            self.lbl_semaforo.setObjectName("SemaforoAmarillo")
        else:
            self.lbl_semaforo.setObjectName("SemaforoRojo")
            
        # Forzar a PyQt5 a recalcular estilos tras cambiar el objectName
        self.lbl_semaforo.style().unpolish(self.lbl_semaforo)
        self.lbl_semaforo.style().polish(self.lbl_semaforo)
        
        # 4. Status superior
        limite = self.gestor.obtener_limite_diario()
        self.status_label.setText(f"Límite Diario Ideal: {limite:.1f} L | Modo: {self.gestor.modo_actual}")

    def cambiar_modo(self, nuevo_modo):
        self.gestor.cambiar_modo(nuevo_modo)
        self.actualizar_interfaz()

    def registrar_actividad(self, actividad):
        """Maneja el clic de un botón de actividad."""
        litros_gastados = self.gestor.registrar_actividad(actividad, 1)
        
        if litros_gastados > 0:
            self.actualizar_interfaz()
            
            # Si nos quedamos sin agua, mostramos alerta
            if self.gestor.litros_totales <= 0:
                QMessageBox.critical(self, "Alerta Crítica", "¡El sistema se ha quedado sin agua!")

    def reportar_fuga(self):
        """Muestra un diálogo para registrar la pérdida de agua por fuga."""
        litros, ok = QInputDialog.getDouble(
            self, "Reportar Fuga", 
            "Ingrese los litros perdidos por la fuga:", 
            value=10.0, min=0.0, max=self.gestor.litros_totales, decimals=1
        )
        if ok and litros > 0:
            self.gestor.registrar_fuga(litros)
            self.actualizar_interfaz()
            QMessageBox.information(
                self, "Fuga Registrada", 
                f"Se han descontado {litros} L por fuga del sistema."
            )
            if self.gestor.litros_totales <= 0:
                QMessageBox.critical(self, "Alerta Crítica", "¡El sistema se ha quedado sin agua!")

    def confirmar_recarga(self):
        """Confirma y realiza la recarga de todos los contenedores al 100%."""
        reply = QMessageBox.question(
            self, "Confirmar Recarga", 
            "¿Desea recargar todos los tanques al 100% de su capacidad?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.gestor.recargar_contenedores()
            self.actualizar_interfaz()
            QMessageBox.information(
                self, "Recarga Exitosa", 
                "Todos los contenedores han sido restablecidos al 100%."
            )
