"""
=============================================================================
ARCHIVO: main_window.py
PROPÓSITO: Define cómo se ve y se comporta la ventana del sistema Aqualy.
=============================================================================
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QComboBox,
    QGridLayout, QMessageBox, QScrollArea, QInputDialog,
    QStackedWidget, QLineEdit, QFormLayout, QButtonGroup
)
from PyQt5.QtCore import Qt
from datetime import datetime
from src.logic import GestorAgua
import src.database as db

class CardWidget(QFrame):
    """Un widget personalizado que actúa como una tarjeta (Card) para organizar el contenido."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setProperty("class", "Card")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        
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
        
        self.setWindowTitle("Aqualy - Control Inteligente de Agua")
        self.resize(1100, 800)
        
        self.init_ui()
        self.actualizar_interfaz()
        
    def init_ui(self):
        # Widget Central y Layout Principal Horizontal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==========================================
        # 1. BARRA LATERAL (SIDEBAR)
        # ==========================================
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 30)
        sidebar_layout.setSpacing(10)
        
        # Logo de Aqualy
        logo_label = QLabel("Aqualy")
        logo_label.setObjectName("LogoLabel")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        # Botones de menú
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        
        self.btn_sistema = QPushButton("  Sistema")
        self.btn_sistema.setProperty("class", "MenuButton")
        self.btn_sistema.setCheckable(True)
        self.btn_sistema.setChecked(True)
        self.btn_group.addButton(self.btn_sistema)
        sidebar_layout.addWidget(self.btn_sistema)
        
        self.btn_admin = QPushButton("  Administrador")
        self.btn_admin.setProperty("class", "MenuButton")
        self.btn_admin.setCheckable(True)
        self.btn_group.addButton(self.btn_admin)
        sidebar_layout.addWidget(self.btn_admin)
        
        self.btn_usuario = QPushButton("  Usuario")
        self.btn_usuario.setProperty("class", "MenuButton")
        self.btn_usuario.setCheckable(True)
        self.btn_group.addButton(self.btn_usuario)
        sidebar_layout.addWidget(self.btn_usuario)
        
        self.btn_config = QPushButton("  Configuración")
        self.btn_config.setProperty("class", "MenuButton")
        self.btn_config.setCheckable(True)
        self.btn_group.addButton(self.btn_config)
        sidebar_layout.addWidget(self.btn_config)
        
        sidebar_layout.addStretch()
        
        # Footer de la barra lateral (Versión)
        version_label = QLabel("v2.0 Premium")
        version_label.setStyleSheet("color: #64748B; font-size: 11px;")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # ==========================================
        # 2. CONTENEDOR MULTIPESTAÑA (QStackedWidget)
        # ==========================================
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("MainContentArea")
        main_layout.addWidget(self.stacked_widget, stretch=1)
        
        # Conectar cambios de pestaña
        self.btn_sistema.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_admin.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_usuario.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_config.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        
        # Crear las diferentes pantallas
        self.crear_pantalla_sistema()
        self.crear_pantalla_administrador()
        self.crear_pantalla_usuario()
        self.crear_pantalla_configuracion()
        
    # ==========================================
    # PANTALLA 1: SISTEMA
    # ==========================================
    def crear_pantalla_sistema(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Cabecera de bienvenida
        header_layout = QHBoxLayout()
        greeting_layout = QVBoxLayout()
        
        # Saludo dinámico según la hora del día
        hora = datetime.now().hour
        if hora < 12:
            saludo = "Buenos días"
        elif hora < 19:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
            
        self.lbl_bienvenida = QLabel(f"¡{saludo}, bienvenido a Aqualy!")
        self.lbl_bienvenida.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        lbl_sub = QLabel("Aquí tienes el resumen del estado hídrico del hogar para hoy.")
        lbl_sub.setStyleSheet("font-size: 14px; color: #94A3B8;")
        
        greeting_layout.addWidget(self.lbl_bienvenida)
        greeting_layout.addWidget(lbl_sub)
        header_layout.addLayout(greeting_layout)
        
        # Límite ideal diario superior
        self.lbl_limite_ideal_top = QLabel("Límite Diario Ideal: -- L")
        self.lbl_limite_ideal_top.setStyleSheet("font-size: 15px; color: #60A5FA; font-weight: bold;")
        self.lbl_limite_ideal_top.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_layout.addWidget(self.lbl_limite_ideal_top)
        
        layout.addLayout(header_layout)
        
        # Fila de Tarjetas Estadísticas Rápidas (Estilo ref)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # 1. Días restantes
        self.card_dias = CardWidget("Días Restantes")
        self.lbl_val_dias = QLabel("-- días")
        self.lbl_val_dias.setStyleSheet("font-size: 22px; font-weight: bold; color: #F8FAFC;")
        self.card_dias.add_widget(self.lbl_val_dias)
        stats_layout.addWidget(self.card_dias)
        
        # 2. Litros Totales
        self.card_litros = CardWidget("Reserva Total")
        self.lbl_val_litros = QLabel("-- L")
        self.lbl_val_litros.setStyleSheet("font-size: 22px; font-weight: bold; color: #3B82F6;")
        self.card_litros.add_widget(self.lbl_val_litros)
        stats_layout.addWidget(self.card_litros)
        
        # 3. Consumo hoy
        self.card_consumo = CardWidget("Consumo Hoy")
        self.lbl_val_consumo = QLabel("-- L")
        self.lbl_val_consumo.setStyleSheet("font-size: 22px; font-weight: bold; color: #EF4444;")
        self.card_consumo.add_widget(self.lbl_val_consumo)
        stats_layout.addWidget(self.card_consumo)
        
        layout.addLayout(stats_layout)
        
        # Contenido Principal: Gráficos de Contenedores y Probabilidad
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Panel Izquierdo: Contenedores
        self.panel_contenedores = CardWidget("Estado de Contenedores")
        self.barras_progreso = {}
        self.layout_contenedores = QVBoxLayout()
        self.panel_contenedores.add_layout(self.layout_contenedores)
        
        self.actualizar_contenedores_ui()
        content_layout.addWidget(self.panel_contenedores, stretch=2)
        
        # Panel Derecho: IA & Semáforo
        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)
        
        card_ia = CardWidget("Predicción de Supervivencia (IA)")
        self.lbl_probabilidad = QLabel("Probabilidad: --%")
        self.lbl_probabilidad.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.lbl_prob_desc = QLabel("Calculado con un análisis Bayesiano basado en tu comportamiento de consumo histórico.")
        self.lbl_prob_desc.setWordWrap(True)
        self.lbl_prob_desc.setStyleSheet("font-size: 13px; color: #94A3B8;")
        
        card_ia.add_widget(self.lbl_probabilidad)
        card_ia.add_widget(self.lbl_prob_desc)
        right_panel.addWidget(card_ia)
        
        card_semaforo = CardWidget("Semáforo de Consumo Diario")
        semaforo_h = QHBoxLayout()
        lbl_sem_txt = QLabel("Estado actual:")
        self.lbl_semaforo = QLabel("Cargando...")
        self.lbl_semaforo.setObjectName("SemaforoVerde")
        semaforo_h.addWidget(lbl_sem_txt)
        semaforo_h.addWidget(self.lbl_semaforo)
        semaforo_h.addStretch()
        card_semaforo.add_layout(semaforo_h)
        right_panel.addWidget(card_semaforo)
        
        content_layout.addLayout(right_panel, stretch=1)
        layout.addLayout(content_layout)
        
        self.stacked_widget.addWidget(widget)

    # ==========================================
    # PANTALLA 2: ADMINISTRADOR
    # ==========================================
    def crear_pantalla_administrador(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Panel de Administración")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        grid_admin = QGridLayout()
        grid_admin.setSpacing(20)
        
        # Tarjeta 1: Operaciones Rápidas
        card_ops = CardWidget("Operaciones Críticas")
        btn_recargar = QPushButton("Restablecer Tanques al 100%")
        btn_recargar.setProperty("class", "PrimaryButton")
        btn_recargar.clicked.connect(self.confirmar_recarga)
        
        btn_fuga = QPushButton("Reportar Fuga Detectada")
        btn_fuga.setProperty("class", "DangerButton")
        btn_fuga.clicked.connect(self.reportar_fuga)
        
        card_ops.add_widget(btn_recargar)
        card_ops.add_widget(btn_fuga)
        grid_admin.addWidget(card_ops, 0, 0)
        
        # Tarjeta 2: Modo de Operación
        card_modo = CardWidget("Modo de Operación")
        lbl_modo_desc = QLabel("Ajusta los consumos diarios recomendados aplicando factores de reducción.")
        lbl_modo_desc.setWordWrap(True)
        lbl_modo_desc.setStyleSheet("color: #94A3B8; font-size: 13px;")
        
        self.combo_modo = QComboBox()
        self.combo_modo.addItems(list(self.gestor.MODOS_OPERACION.keys()))
        self.combo_modo.setCurrentText(self.gestor.modo_actual)
        self.combo_modo.currentTextChanged.connect(self.cambiar_modo)
        
        card_modo.add_widget(lbl_modo_desc)
        card_modo.add_widget(self.combo_modo)
        grid_admin.addWidget(card_modo, 0, 1)
        
        # Tarjeta 3: Gestión de Contenedores
        card_gestion_cont = CardWidget("Gestión de Tanques")
        btn_nuevo_tanque = QPushButton("Añadir Nuevo Contenedor")
        btn_nuevo_tanque.setProperty("class", "SecondaryButton")
        btn_nuevo_tanque.clicked.connect(self.solicitar_nuevo_contenedor)
        
        btn_eliminar_tanque = QPushButton("Eliminar Contenedor")
        btn_eliminar_tanque.setProperty("class", "SecondaryButton")
        btn_eliminar_tanque.clicked.connect(self.solicitar_eliminar_contenedor)
        
        card_gestion_cont.add_widget(btn_nuevo_tanque)
        card_gestion_cont.add_widget(btn_eliminar_tanque)
        grid_admin.addWidget(card_gestion_cont, 1, 0, 1, 2)
        
        layout.addLayout(grid_admin)
        layout.addStretch()
        
        self.stacked_widget.addWidget(widget)

    # ==========================================
    # PANTALLA 3: USUARIO (TIEMPO EN MINUTOS)
    # ==========================================
    def crear_pantalla_usuario(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title_layout = QVBoxLayout()
        title = QLabel("Sección del Usuario")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        desc = QLabel("Conversión amigable del inventario actual en minutos o usos estimados por actividad diaria.")
        desc.setStyleSheet("font-size: 14px; color: #94A3B8;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(desc)
        layout.addLayout(title_layout)
        
        # Scroll Area para las actividades
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid_actividades_user = QGridLayout(scroll_content)
        self.grid_actividades_user.setSpacing(15)
        
        self.actualizar_actividades_usuario_ui()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.stacked_widget.addWidget(widget)

    # ==========================================
    # PANTALLA 4: CONFIGURACIÓN
    # ==========================================
    def crear_pantalla_configuracion(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Configuración del Sistema")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Formulario de Ajustes
        card_form = CardWidget("Parámetros Generales")
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        
        # Entrada de Fecha de Corte
        self.input_fecha_fin = QLineEdit(self.gestor.fecha_fin_str)
        self.input_fecha_fin.setPlaceholderText("AAAA-MM-DD")
        form_layout.addRow(QLabel("Fecha de Corte / Fin (AAAA-MM-DD):"), self.input_fecha_fin)
        
        card_form.add_layout(form_layout)
        layout.addWidget(card_form)
        
        # Tarjeta: Tasas de consumo
        card_tasas = CardWidget("Consumo de Actividades (Litros por Minuto/Uso)")
        self.inputs_tasas = {}
        form_tasas = QFormLayout()
        form_tasas.setVerticalSpacing(12)
        
        for act, litros in self.gestor.ACTIVIDADES.items():
            inp = QLineEdit(str(litros))
            form_tasas.addRow(QLabel(f"{act.replace('_', ' ').title()} (L/min):"), inp)
            self.inputs_tasas[act] = inp
            
        card_tasas.add_layout(form_tasas)
        layout.addWidget(card_tasas)
        
        # Botón para Guardar Todo
        btn_guardar = QPushButton("Guardar Configuración")
        btn_guardar.setProperty("class", "PrimaryButton")
        btn_guardar.clicked.connect(self.guardar_configuracion_general)
        layout.addWidget(btn_guardar)
        
        layout.addStretch()
        
        self.stacked_widget.addWidget(widget)

    # ==========================================
    # METODOS DE ACTUALIZACION & ACCIONES
    # ==========================================
    def actualizar_contenedores_ui(self):
        # Limpiar contenedor antiguo
        for i in reversed(range(self.layout_contenedores.count())):
            widget_to_remove = self.layout_contenedores.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
            else:
                # Si es un layout
                layout_to_remove = self.layout_contenedores.itemAt(i).layout()
                if layout_to_remove:
                    self.clear_layout(layout_to_remove)
                    
        self.barras_progreso.clear()
        
        for contenedor in self.gestor.contenedores:
            cont_layout = QVBoxLayout()
            
            lbl_title = QLabel(f"{contenedor.nombre} ({contenedor.tipo})")
            lbl_title.setStyleSheet("font-size: 14px; color: #F1F5F9; font-weight: bold;")
            cont_layout.addWidget(lbl_title)
            
            pbar = QProgressBar()
            pbar.setMaximum(int(contenedor.capacidad_maxima))
            pbar.setValue(int(contenedor.litros_actuales))
            pbar.setFormat("%v / %m L")
            cont_layout.addWidget(pbar)
            
            self.barras_progreso[contenedor.nombre] = pbar
            
            frame_cont = QFrame()
            frame_cont.setLayout(cont_layout)
            self.layout_contenedores.addWidget(frame_cont)
            
        self.layout_contenedores.addStretch()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def actualizar_actividades_usuario_ui(self):
        # Limpiar grid antiguo
        for i in reversed(range(self.grid_actividades_user.count())):
            item = self.grid_actividades_user.itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        # Obtener minutos restantes del gestor
        minutos_restantes = self.gestor.obtener_minutos_restantes()
        
        row, col = 0, 0
        for act, mins in minutos_restantes.items():
            card = QFrame()
            card.setProperty("class", "ActivityCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            
            lbl_nombre = QLabel(act.replace("_", " ").title())
            lbl_nombre.setProperty("class", "ActivityTitle")
            
            lbl_tiempo = QLabel(f"{mins} min")
            lbl_tiempo.setProperty("class", "ActivityTime")
            
            lbl_consumo = QLabel(f"Tasa: {self.gestor.ACTIVIDADES[act]} L/min")
            lbl_consumo.setStyleSheet("color: #64748B; font-size: 12px;")
            
            btn_usar = QPushButton("Registrar 1 min")
            btn_usar.setProperty("class", "SecondaryButton")
            btn_usar.clicked.connect(lambda checked, a=act: self.registrar_uso_minutos(a, 1))
            
            btn_usar_mas = QPushButton("Registrar N min")
            btn_usar_mas.setProperty("class", "SecondaryButton")
            btn_usar_mas.clicked.connect(lambda checked, a=act: self.registrar_uso_minutos_personalizado(a))
            
            card_layout.addWidget(lbl_nombre)
            card_layout.addWidget(lbl_tiempo)
            card_layout.addWidget(lbl_consumo)
            card_layout.addWidget(btn_usar)
            card_layout.addWidget(btn_usar_mas)
            
            self.grid_actividades_user.addWidget(card, row, col)
            col += 1
            if col > 2: # 3 columnas
                col = 0
                row += 1

    def actualizar_interfaz(self):
        # 1. Actualizar barras de progreso en pantalla Sistema
        for contenedor in self.gestor.contenedores:
            if contenedor.nombre in self.barras_progreso:
                pbar = self.barras_progreso[contenedor.nombre]
                pbar.setValue(int(contenedor.litros_actuales))
                
        # 2. Resumen General
        hoy = datetime.now().date()
        fecha_fin = datetime.strptime(self.gestor.fecha_fin_str, "%Y-%m-%d").date()
        dias_restantes = max((fecha_fin - hoy).days, 0)
        self.lbl_val_dias.setText(f"{dias_restantes} días")
        
        litros = self.gestor.litros_totales
        self.lbl_val_litros.setText(f"{litros:.1f} L")
        
        consumo_hoy = db.obtener_consumo_hoy()
        self.lbl_val_consumo.setText(f"{consumo_hoy:.1f} L")
        
        limite = self.gestor.obtener_limite_diario()
        self.lbl_limite_ideal_top.setText(f"Límite Diario Ideal: {limite:.1f} L")
        
        # 3. Probabilidad Bayesiana
        prob = self.gestor.probabilidad_supervivencia()
        self.lbl_probabilidad.setText(f"{prob}% de Probabilidad")
        if prob > 80:
            self.lbl_probabilidad.setStyleSheet("font-size: 24px; font-weight: bold; color: #22C55E;")
        elif prob > 40:
            self.lbl_probabilidad.setStyleSheet("font-size: 24px; font-weight: bold; color: #EAB308;")
        else:
            self.lbl_probabilidad.setStyleSheet("font-size: 24px; font-weight: bold; color: #EF4444;")
            
        # 4. Semáforo
        estado_sem = self.gestor.estado_semaforo(consumo_hoy)
        self.lbl_semaforo.setText(f" {estado_sem.upper()} ")
        if estado_sem == "Verde":
            self.lbl_semaforo.setObjectName("SemaforoVerde")
        elif estado_sem == "Amarillo":
            self.lbl_semaforo.setObjectName("SemaforoAmarillo")
        else:
            self.lbl_semaforo.setObjectName("SemaforoRojo")
            
        self.lbl_semaforo.style().unpolish(self.lbl_semaforo)
        self.lbl_semaforo.style().polish(self.lbl_semaforo)
        
        # 5. Pestaña de usuario
        self.actualizar_actividades_usuario_ui()

    def registrar_uso_minutos(self, actividad, minutos):
        # Multiplicamos minutos por la tasa de consumo de la actividad
        litros_gastados = self.gestor.registrar_actividad(actividad, minutos)
        if litros_gastados > 0:
            self.actualizar_interfaz()
            if self.gestor.litros_totales <= 0:
                QMessageBox.critical(self, "Alerta Crítica", "¡El sistema se ha quedado sin agua!")

    def registrar_uso_minutos_personalizado(self, actividad):
        minutos, ok = QInputDialog.getInt(
            self, "Registrar Actividad",
            f"¿Cuántos minutos duró la actividad de {actividad.replace('_', ' ')}?",
            value=5, min=1, max=600
        )
        if ok and minutos > 0:
            self.registrar_uso_minutos(actividad, minutos)

    def cambiar_modo(self, nuevo_modo):
        self.gestor.cambiar_modo(nuevo_modo)
        self.actualizar_interfaz()

    def reportar_fuga(self):
        litros, ok = QInputDialog.getDouble(
            self, "Reportar Fuga", 
            "Ingrese los litros aproximados perdidos por la fuga:", 
            value=10.0, min=0.0, max=self.gestor.litros_totales, decimals=1
        )
        if ok and litros > 0:
            self.gestor.registrar_fuga(litros)
            self.actualizar_interfaz()
            QMessageBox.information(self, "Fuga Registrada", f"Se han descontado {litros} L por la fuga.")
            if self.gestor.litros_totales <= 0:
                QMessageBox.critical(self, "Alerta Crítica", "¡El sistema se ha quedado sin agua!")

    def confirmar_recarga(self):
        reply = QMessageBox.question(
            self, "Confirmar Recarga", 
            "¿Desea restablecer todos los contenedores al 100%?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.gestor.recargar_contenedores()
            self.actualizar_interfaz()
            QMessageBox.information(self, "Recarga Exitosa", "Tanques restablecidos al 100%.")

    def solicitar_nuevo_contenedor(self):
        nombre, ok1 = QInputDialog.getText(self, "Nuevo Contenedor", "Nombre del Tanque/Pipa:")
        if not ok1 or not nombre.strip():
            return
        
        tipos = ["Tanque", "Pipa", "Tobo"]
        tipo, ok2 = QInputDialog.getItem(self, "Nuevo Contenedor", "Tipo:", tipos, 0, False)
        if not ok2:
            return
            
        capacidad, ok3 = QInputDialog.getDouble(self, "Nuevo Contenedor", "Capacidad Máxima (L):", 100.0, 1.0, 10000.0, 1)
        if not ok3:
            return
            
        # Insertar en base de datos
        conexion = db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO contenedores (nombre, tipo, capacidad_maxima, litros_actuales) VALUES (?, ?, ?, ?)",
                (nombre.strip(), tipo, capacidad, capacidad)
            )
            conexion.commit()
            QMessageBox.information(self, "Éxito", "Contenedor añadido correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el contenedor: {e}")
        finally:
            conexion.close()
            
        # Re-cargar gestor y actualizar
        self.gestor.contenedores.clear()
        db_conts = db.cargar_contenedores()
        from src.logic import ContenedorHidrico
        for c in db_conts:
            cont = ContenedorHidrico(c["nombre"], c["tipo"], c["capacidad_maxima"])
            cont.litros_actuales = c["litros_actuales"]
            self.gestor.contenedores.append(cont)
            
        self.actualizar_contenedores_ui()
        self.actualizar_interfaz()

    def solicitar_eliminar_contenedor(self):
        nombres = [c.nombre for c in self.gestor.contenedores]
        if not nombres:
            QMessageBox.warning(self, "Advertencia", "No hay contenedores para eliminar.")
            return
            
        nombre, ok = QInputDialog.getItem(self, "Eliminar Contenedor", "Selecciona el contenedor:", nombres, 0, False)
        if ok and nombre:
            reply = QMessageBox.question(
                self, "Confirmar eliminación", 
                f"¿Estás seguro de que deseas eliminar el contenedor '{nombre}'? Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                conexion = db.conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM contenedores WHERE nombre = ?", (nombre,))
                conexion.commit()
                conexion.close()
                
                # Quitar de la memoria del gestor
                self.gestor.contenedores = [c for c in self.gestor.contenedores if c.nombre != nombre]
                
                self.actualizar_contenedores_ui()
                self.actualizar_interfaz()
                QMessageBox.information(self, "Éxito", "Contenedor eliminado.")

    def guardar_configuracion_general(self):
        fecha = self.input_fecha_fin.text().strip()
        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Error de Validación", "La fecha debe estar en formato AAAA-MM-DD")
            return
            
        # Actualizar fecha en base de datos
        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE configuracion SET fecha_fin = ?", (fecha,))
        conexion.commit()
        conexion.close()
        
        self.gestor.fecha_fin_str = fecha
        
        # Guardar tasas de actividades
        for act, inp in self.inputs_tasas.items():
            try:
                nueva_tasa = int(inp.text().strip())
                if nueva_tasa < 0:
                    raise ValueError()
                self.gestor.ACTIVIDADES[act] = nueva_tasa
            except ValueError:
                QMessageBox.critical(self, "Error de Validación", f"La tasa de '{act}' debe ser un número entero positivo.")
                return
                
        QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
        self.actualizar_interfaz()
