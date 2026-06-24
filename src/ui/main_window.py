"""
=============================================================================
ARCHIVO: main_window.py
PROPÓSITO: Define la interfaz gráfica del sistema Aqualy.

Estructura de la Interfaz:
  - WelcomeDialog        : Ventana de bienvenida que aparece UNA SOLA VEZ al iniciar.
  - GestionRecipientesDialog : Diálogo modal para agregar/eliminar recipientes de agua.
  - AqualiDashboard      : Ventana principal con barra lateral de 2 pestañas:
      1. Mi Sistema      : Panel de nivel de recipientes + Asistente Virtual (chat) + Medidor en Línea
      2. Configuración   : Parámetros de fecha de corte, modo de operación y tasas de actividades
=============================================================================
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QComboBox,
    QGridLayout, QMessageBox, QScrollArea, QDialog,
    QStackedWidget, QLineEdit, QFormLayout, QButtonGroup,
    QTextBrowser, QDoubleSpinBox, QSpinBox, QDialogButtonBox,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from datetime import datetime
from src.logic import GestorAgua, ContenedorHidrico
import src.database as db
from src.sensor_simulado import SensorSimulado
from src.ia_modulo import obtener_respuesta_asistente


# =============================================================================
# DIÁLOGO: BIENVENIDA DE ÚNICA VEZ
# =============================================================================
class WelcomeDialog(QDialog):
    """
    Ventana emergente de bienvenida que se muestra una sola vez al iniciar la aplicación.
    Al pulsar 'Entrar al Sistema', se cierra y la ventana principal queda disponible.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bienvenido a Aqualy")
        self.setModal(True)
        self.setFixedSize(540, 380)
        self.setStyleSheet("background-color: #0F172A;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # --- Logotipo del sistema ---
        lbl_logo = QLabel("Aqualy")
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.setStyleSheet(
            "font-family: 'Times New Roman', serif; font-size: 44px; font-weight: bold; "
            "font-style: italic; color: #FACC15;"
        )
        layout.addWidget(lbl_logo)

        # --- Mensaje de bienvenida ---
        lbl_titulo = QLabel("Sistema Inteligente de Gestión Hídrica")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 15px; font-weight: bold; color: white;")
        layout.addWidget(lbl_titulo)

        lbl_desc = QLabel(
            "Estimado usuario, bienvenido a Aqualy.\n\n"
            "Este sistema monitorea en tiempo real sus reservas de agua del hogar "
            "y detecta fugas o consumos anormales de forma automática, "
            "sin requerir que usted ingrese datos manualmente de manera constante.\n\n"
            "Dispone de un asistente inteligente al que puede consultarle "
            "sobre el estado de sus reservas cuando lo requiera."
        )
        lbl_desc.setAlignment(Qt.AlignCenter)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 13px; color: #94A3B8; line-height: 150%;")
        layout.addWidget(lbl_desc)

        layout.addStretch()

        # --- Botón de acceso ---
        btn_entrar = QPushButton("Entrar al Sistema  →")
        btn_entrar.setProperty("class", "PrimaryButton")
        btn_entrar.setFixedHeight(42)
        btn_entrar.clicked.connect(self.accept)
        layout.addWidget(btn_entrar)


# =============================================================================
# DIÁLOGO: GESTIÓN DE RECIPIENTES
# =============================================================================
class GestionRecipientesDialog(QDialog):
    """
    Cuadro de diálogo modal que permite al usuario registrar nuevos recipientes
    de agua (con nombre libre y capacidad en litros) y eliminar los existentes.
    Se accede desde el botón 'Gestionar Recipientes' dentro de 'Mi Sistema'.
    """
    def __init__(self, gestor: GestorAgua, parent=None):
        super().__init__(parent)
        self.gestor = gestor
        self.setWindowTitle("Gestión de Recipientes de Agua")
        self.setModal(True)
        self.resize(520, 460)
        self.setStyleSheet("background-color: #1E293B;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # --- Encabezado ---
        lbl_titulo = QLabel("Registro de Recipientes de Agua")
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(lbl_titulo)

        lbl_desc = QLabel(
            "Registre aquí cada uno de sus depósitos indicando un nombre descriptivo "
            "y la capacidad máxima en litros."
        )
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #94A3B8; font-size: 13px;")
        layout.addWidget(lbl_desc)

        # --- Formulario de nuevo recipiente ---
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #0F172A; border-radius: 10px; padding: 12px;")
        form_layout = QHBoxLayout(form_frame)
        form_layout.setSpacing(10)

        # Campo de nombre
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre (ej: Tambor de techo, Cisterna)")
        form_layout.addWidget(self.input_nombre, stretch=3)

        # Campo de capacidad con valor visible (QDoubleSpinBox estilizado)
        self.spin_capacidad = QDoubleSpinBox()
        self.spin_capacidad.setRange(1.0, 50000.0)
        self.spin_capacidad.setValue(500.0)
        self.spin_capacidad.setSuffix(" L")
        self.spin_capacidad.setDecimals(0)
        form_layout.addWidget(self.spin_capacidad, stretch=1)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.setProperty("class", "PrimaryButton")
        btn_agregar.clicked.connect(self.agregar_recipiente)
        form_layout.addWidget(btn_agregar)

        layout.addWidget(form_frame)

        # --- Lista de recipientes registrados ---
        lbl_lista = QLabel("Recipientes Registrados:")
        lbl_lista.setStyleSheet("font-size: 13px; font-weight: bold; color: #94A3B8;")
        layout.addWidget(lbl_lista)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.cont_lista = QWidget()
        self.cont_lista.setStyleSheet("background-color: transparent;")
        self.layout_lista = QVBoxLayout(self.cont_lista)
        self.layout_lista.setContentsMargins(0, 0, 0, 0)
        self.layout_lista.setSpacing(8)
        self.scroll.setWidget(self.cont_lista)
        layout.addWidget(self.scroll, stretch=1)

        # --- Botón cerrar ---
        btn_cerrar = QPushButton("Cerrar y Aplicar Cambios")
        btn_cerrar.setProperty("class", "SecondaryButton")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

        # Cargar la lista actual de recipientes
        self.actualizar_lista()

    def actualizar_lista(self):
        """Reconstruye el listado de recipientes en el diálogo."""
        # Limpiar widgets anteriores
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # Crear una fila por cada contenedor registrado
        for cont in self.gestor.contenedores:
            row = QFrame()
            row.setStyleSheet(
                "background-color: #1E293B; border-radius: 8px; padding: 8px;"
            )
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 6, 10, 6)

            # Información del recipiente
            lbl = QLabel(f"<b>{cont.nombre}</b>  —  Capacidad: {cont.capacidad_maxima:.0f} L  |  Actual: {cont.litros_actuales:.0f} L")
            lbl.setStyleSheet("color: white; font-size: 13px;")
            row_layout.addWidget(lbl, stretch=1)

            # Botón eliminar
            btn_del = QPushButton("✕ Eliminar")
            btn_del.setStyleSheet(
                "background-color: transparent; color: #EF4444; border: 1px solid #EF4444; "
                "border-radius: 6px; padding: 4px 10px; font-size: 12px;"
            )
            btn_del.clicked.connect(lambda _, n=cont.nombre: self.eliminar_recipiente(n))
            row_layout.addWidget(btn_del)

            self.layout_lista.addWidget(row)

        self.layout_lista.addStretch()

    def agregar_recipiente(self):
        """Inserta el nuevo recipiente en la base de datos y recarga la lista."""
        nombre = self.input_nombre.text().strip()
        capacidad = self.spin_capacidad.value()

        if not nombre:
            QMessageBox.warning(self, "Campo requerido", "Por favor, ingrese un nombre para el recipiente.")
            return

        conexion = db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO contenedores (nombre, tipo, capacidad_maxima, litros_actuales) VALUES (?, ?, ?, ?)",
                (nombre, "Personalizado", capacidad, capacidad)
            )
            conexion.commit()
            self.input_nombre.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No fue posible registrar el recipiente:\n{e}")
            return
        finally:
            conexion.close()

        # Actualizar el gestor en memoria
        cont = ContenedorHidrico(nombre, "Personalizado", capacidad)
        cont.litros_actuales = capacidad
        self.gestor.contenedores.append(cont)
        self.actualizar_lista()

    def eliminar_recipiente(self, nombre):
        """Elimina un recipiente de la base de datos y de la memoria del gestor."""
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Desea eliminar el recipiente '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        conexion = db.conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM contenedores WHERE nombre = ?", (nombre,))
        conexion.commit()
        conexion.close()

        # Actualizar la lista en memoria del gestor
        self.gestor.contenedores = [c for c in self.gestor.contenedores if c.nombre != nombre]
        self.actualizar_lista()


# =============================================================================
# WIDGET: TARJETA GENÉRICA
# =============================================================================
class CardWidget(QFrame):
    """
    Contenedor visual estilo tarjeta (Card) para agrupar y presentar información
    con fondo translúcido, bordes redondeados y título descriptivo.
    """
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setProperty("class", "Card")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(18, 18, 18, 18)
        self._layout.setSpacing(10)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setProperty("class", "CardTitle")
            self._layout.addWidget(self.title_label)

    def add_widget(self, widget):
        self._layout.addWidget(widget)

    def add_layout(self, layout):
        self._layout.addLayout(layout)


# =============================================================================
# VENTANA PRINCIPAL: AQUALY DASHBOARD
# =============================================================================
class AqualiDashboard(QMainWindow):
    """
    Ventana principal de la aplicación Aqualy.

    Componentes:
      - Barra lateral colapsable (☰) con 2 pestañas: Mi Sistema / Configuración
      - Pestaña 'Mi Sistema':
          * Panel superior: Nivel en tiempo real de todos los recipientes registrados
          * Panel inferior izquierdo: Asistente Virtual (chat)
          * Panel inferior derecho: Medidor en Línea (lectura de caudal, presión, temperatura)
      - Pestaña 'Configuración': Ajuste de fecha de corte, modo de operación y tasas de consumo
    """

    def __init__(self, gestor: GestorAgua, sensor: SensorSimulado):
        super().__init__()
        self.gestor = gestor        # Controlador de la lógica de agua y recipientes
        self.sensor = sensor        # Medidor físico simulado (caudal, presión, temperatura)
        self.consumo_acumulado = 0.0  # Litros acumulados pendientes de guardar en la BD
        self.sidebar_expandido = True  # Estado inicial: barra lateral visible

        self.setWindowTitle("Aqualy — Monitoreo Hídrico Inteligente")
        self.resize(1200, 820)

        self._init_ui()
        self._actualizar_interfaz()

        # ── Temporizador del sensor ──────────────────────────────────────────
        # Se activa cada 2 segundos para leer el caudal y descontar agua
        # de los recipientes automáticamente sin intervención del usuario.
        self.timer_sensor = QTimer(self)
        self.timer_sensor.timeout.connect(self._tick_sensor)
        self.timer_sensor.start(2000)

    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────
    def _init_ui(self):
        """Construye el layout principal: barra lateral + área de contenido."""
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Barra lateral ────────────────────────────────────────────────────
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setMinimumWidth(65)
        self.sidebar.setMaximumWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(8)

        # Botón hamburguesa (=) para colapsar / expandir el menú lateral
        self.btn_toggle = QPushButton("=")
        self.btn_toggle.setObjectName("BtnToggleSidebar")
        self.btn_toggle.setFixedHeight(38)
        self.btn_toggle.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #F8FAFC; "
            "background-color: transparent; border: none; text-align: center;"
        )
        self.btn_toggle.clicked.connect(self._toggle_sidebar)
        sidebar_layout.addWidget(self.btn_toggle)

        # Nombre / Logo del sistema (solo visible cuando el menú está expandido)
        self.logo_label = QLabel("Aqualy")
        self.logo_label.setObjectName("LogoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)

        sidebar_layout.addSpacing(10)

        # ─── Botones de navegación ───────────────────────────────────────────
        # Solo uno puede estar activo a la vez (QButtonGroup exclusivo)
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        # Pestaña 1: Mi Sistema
        self.btn_sistema = QPushButton("[S]  Mi Sistema")
        self.btn_sistema.setProperty("class", "MenuButton")
        self.btn_sistema.setCheckable(True)
        self.btn_sistema.setChecked(True)
        self.btn_group.addButton(self.btn_sistema)
        sidebar_layout.addWidget(self.btn_sistema)

        # Pestaña 2: Configuración
        self.btn_config = QPushButton("[C]  Configuración")
        self.btn_config.setProperty("class", "MenuButton")
        self.btn_config.setCheckable(True)
        self.btn_group.addButton(self.btn_config)
        sidebar_layout.addWidget(self.btn_config)

        sidebar_layout.addStretch()

        # Versión del sistema (discreta)
        self.lbl_version = QLabel("v3.1")
        self.lbl_version.setStyleSheet("color: #475569; font-size: 10px;")
        self.lbl_version.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.lbl_version)

        root.addWidget(self.sidebar)

        # ── Área de contenido (QStackedWidget) ──────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setObjectName("MainContentArea")
        root.addWidget(self.stack, stretch=1)

        # Conectar la navegación
        self.btn_sistema.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_config.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # Construir las pestañas
        self._build_sistema()
        self._build_configuracion()

    # ─────────────────────────────────────────────────────────────────────────
    # COLAPSO / EXPANSIÓN DE LA BARRA LATERAL
    # ─────────────────────────────────────────────────────────────────────────
    def _toggle_sidebar(self):
        """
        Alterna la barra lateral entre su estado expandido (200px con texto)
        y contraído (65px con solo letras clave), mejorando el espacio en pantalla.
        """
        if self.sidebar_expandido:
            # Contraer: mostrar solo la inicial entre corchetes
            self.sidebar.setMaximumWidth(65)
            self.sidebar.setMinimumWidth(65)
            self.btn_sistema.setText("[S]")
            self.btn_config.setText("[C]")
            self.logo_label.hide()
            self.lbl_version.hide()
        else:
            # Expandir: restaurar el texto completo y anchura original
            self.sidebar.setMaximumWidth(200)
            self.sidebar.setMinimumWidth(65)
            self.btn_sistema.setText("[S]  Mi Sistema")
            self.btn_config.setText("[C]  Configuración")
            self.logo_label.show()
            self.lbl_version.show()

        self.sidebar_expandido = not self.sidebar_expandido

    # ─────────────────────────────────────────────────────────────────────────
    # PESTAÑA 0: MI SISTEMA
    # ─────────────────────────────────────────────────────────────────────────
    def _build_sistema(self):
        """
        Construye la pestaña 'Mi Sistema' con tres paneles:
          1. Nivel gráfico de recipientes (barras de progreso en tiempo real)
          2. Asistente Virtual (historial de chat + botones rápidos + entrada de texto)
          3. Medidor en Línea (lecturas de caudal/presión/temperatura + diagnóstico)
        """
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # ── 1. Panel de Nivel de Recipientes ─────────────────────────────────
        # Encabezado con botón para abrir el diálogo de gestión
        header_row = QHBoxLayout()

        lbl_title = QLabel("Estado Actual de sus Depósitos")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_row.addWidget(lbl_title, stretch=1)

        # Resumen rápido de litros y probabilidad
        self.lbl_resumen_top = QLabel("Reserva: -- L  |  Probabilidad: --%")
        self.lbl_resumen_top.setStyleSheet("font-size: 13px; color: #60A5FA; font-weight: bold;")
        self.lbl_resumen_top.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_row.addWidget(self.lbl_resumen_top)

        btn_gestionar = QPushButton("⚙ Gestionar Recipientes")
        btn_gestionar.setProperty("class", "SecondaryButton")
        btn_gestionar.setFixedHeight(34)
        btn_gestionar.clicked.connect(self._abrir_gestion_recipientes)
        header_row.addWidget(btn_gestionar)

        root.addLayout(header_row)

        # Scroll de barras de progreso (se reconstruyen cuando cambian los recipientes)
        self.scroll_barras = QScrollArea()
        self.scroll_barras.setWidgetResizable(True)
        self.scroll_barras.setMaximumHeight(150)
        self.scroll_barras.setStyleSheet("border: none; background-color: transparent;")
        self.cont_barras = QWidget()
        self.cont_barras.setStyleSheet("background-color: transparent;")
        self.layout_barras = QVBoxLayout(self.cont_barras)
        self.layout_barras.setContentsMargins(0, 4, 0, 4)
        self.layout_barras.setSpacing(10)
        self.scroll_barras.setWidget(self.cont_barras)
        self.barras_progreso = {}  # nombre -> QProgressBar
        root.addWidget(self.scroll_barras)

        # ── 2 + 3. Split horizontal: Chat (izquierda) | Medidor (derecha) ──
        split = QHBoxLayout()
        split.setSpacing(14)

        # ─── 2. Asistente Virtual (Chat con IA) ─────────────────────────────
        chat_frame = QFrame()
        chat_frame.setProperty("class", "Card")
        chat_outer = QVBoxLayout(chat_frame)
        chat_outer.setContentsMargins(16, 16, 16, 16)
        chat_outer.setSpacing(10)

        # Título centrado del chat
        lbl_chat_title = QLabel("Asistente Virtual")
        lbl_chat_title.setAlignment(Qt.AlignCenter)
        lbl_chat_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #F8FAFC; "
            "padding-bottom: 6px; border-bottom: 1px solid #334155;"
        )
        chat_outer.addWidget(lbl_chat_title)

        # ── Historial de mensajes ──────────────────────────────────────────
        # Los mensajes se acumulan de arriba hacia abajo dentro del ScrollArea.
        # El stretch al final empuja los mensajes hacia la parte superior cuando
        # hay poco contenido (comportamiento natural de chat).
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet(
            "background-color: #0F172A; border-radius: 12px; border: 1px solid #334155;"
        )
        self.chat_content = QWidget()
        self.chat_content.setStyleSheet("background-color: transparent;")
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        self.chat_layout.setSpacing(10)
        self.chat_layout.setAlignment(Qt.AlignTop)  # Los mensajes fluyen desde arriba
        self.chat_scroll.setWidget(self.chat_content)
        chat_outer.addWidget(self.chat_scroll, stretch=1)

        # Botones de sugerencia rápida
        sugest_row = QHBoxLayout()
        sugest_row.setSpacing(6)
        for texto, pregunta in [
            ("🏠 ¿Cómo va el tanque?", "¿Cómo va el tanque?"),
            ("🔍 ¿Hay alguna fuga?", "¿Hay alguna fuga?"),
            ("🚿 ¿Cuántos minutos de ducha?", "¿Cuántos minutos de ducha me quedan?"),
            ("💡 Consejo de la IA", "¿Qué me recomienda la IA para hoy?"),
        ]:
            btn = QPushButton(texto)
            btn.setProperty("class", "SugestButton")
            btn.clicked.connect(lambda _, p=pregunta: self._procesar_pregunta(p))
            sugest_row.addWidget(btn)
        sugest_row.addStretch()
        chat_outer.addLayout(sugest_row)

        # Barra de entrada de texto
        input_row = QHBoxLayout()
        self.input_chat = QLineEdit()
        self.input_chat.setObjectName("ChatInput")
        self.input_chat.setPlaceholderText("Pregúntele a Aqualy...")
        self.input_chat.returnPressed.connect(self._enviar_chat)
        btn_send = QPushButton("Enviar")
        btn_send.setProperty("class", "PrimaryButton")
        btn_send.setFixedHeight(36)
        btn_send.clicked.connect(self._enviar_chat)
        input_row.addWidget(self.input_chat, stretch=1)
        input_row.addWidget(btn_send)
        chat_outer.addLayout(input_row)

        split.addWidget(chat_frame, stretch=6)

        # ─── 3. Medidor en Línea ─────────────────────────────────────────────
        medidor_frame = QFrame()
        medidor_frame.setObjectName("PanelMedidor")
        medidor_layout = QVBoxLayout(medidor_frame)
        medidor_layout.setSpacing(10)

        # Encabezado del medidor con indicador de conexión activa
        header_med = QHBoxLayout()
        lbl_med_titulo = QLabel("Medidor en Línea")
        lbl_med_titulo.setStyleSheet("font-size: 15px; font-weight: bold; color: white;")
        self.lbl_conexion = QLabel("● Conectado")
        self.lbl_conexion.setStyleSheet("color: #22C55E; font-size: 12px; font-weight: bold;")
        header_med.addWidget(lbl_med_titulo, stretch=1)
        header_med.addWidget(self.lbl_conexion)
        medidor_layout.addLayout(header_med)

        # Pantalla LCD con las lecturas del medidor
        lcd_frame = QFrame()
        lcd_frame.setObjectName("MedidorPantallaLCD")
        lcd_grid = QGridLayout(lcd_frame)
        lcd_grid.setSpacing(10)

        def lcd_row(label_text, default_val):
            """Helper: crea una fila etiqueta + valor LCD en el panel del medidor."""
            lbl_lbl = QLabel(label_text)
            lbl_lbl.setProperty("class", "LecturaLCDLabel")
            lbl_val = QLabel(default_val)
            lbl_val.setProperty("class", "LecturaLCD")
            return lbl_lbl, lbl_val

        lbl_l1, self.lbl_caudal   = lcd_row("Caudal",       "0.00 L/min")
        lbl_l2, self.lbl_presion  = lcd_row("Presión",      "50.0 PSI")
        lbl_l3, self.lbl_temp     = lcd_row("Temperatura",  "20.0 °C")
        lbl_l4, self.lbl_valvula  = lcd_row("Válvula",      " ABIERTA ")

        for row_i, (ll, lv) in enumerate([(lbl_l1, self.lbl_caudal),
                                           (lbl_l2, self.lbl_presion),
                                           (lbl_l3, self.lbl_temp),
                                           (lbl_l4, self.lbl_valvula)]):
            lcd_grid.addWidget(ll, row_i, 0)
            lcd_grid.addWidget(lv, row_i, 1)

        medidor_layout.addWidget(lcd_frame)

        # Control de válvula principal
        self.btn_valvula = QPushButton("Cerrar Válvula Principal")
        self.btn_valvula.setProperty("class", "DangerButton")
        self.btn_valvula.clicked.connect(self._toggle_valvula)
        medidor_layout.addWidget(self.btn_valvula)

        # Separador visual hacia la sección de diagnóstico
        lbl_sep = QLabel("— Herramientas de Diagnóstico —")
        lbl_sep.setAlignment(Qt.AlignCenter)
        lbl_sep.setStyleSheet("color: #475569; font-size: 11px; margin-top: 8px;")
        medidor_layout.addWidget(lbl_sep)

        # Selector de escenarios de calibración (discreto, técnico)
        lbl_esc = QLabel("Escenario de calibración:")
        lbl_esc.setStyleSheet("color: #64748B; font-size: 12px;")
        medidor_layout.addWidget(lbl_esc)

        self.combo_escenario = QComboBox()
        self.combo_escenario.addItems(list(self.sensor.ESCENARIOS.keys()))
        self.combo_escenario.currentTextChanged.connect(self._cambiar_escenario)
        medidor_layout.addWidget(self.combo_escenario)

        self.lbl_esc_desc = QLabel(self.sensor.ESCENARIOS["Reposo"]["descripcion"])
        self.lbl_esc_desc.setWordWrap(True)
        self.lbl_esc_desc.setStyleSheet("color: #64748B; font-size: 11px;")
        medidor_layout.addWidget(self.lbl_esc_desc)

        # Estadísticas rápidas
        lbl_stats_sep = QLabel("— Resumen del Día —")
        lbl_stats_sep.setAlignment(Qt.AlignCenter)
        lbl_stats_sep.setStyleSheet("color: #475569; font-size: 11px; margin-top: 8px;")
        medidor_layout.addWidget(lbl_stats_sep)

        self.lbl_gasto_hoy = QLabel("Gasto hoy: -- L")
        self.lbl_gasto_hoy.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: bold;")
        medidor_layout.addWidget(self.lbl_gasto_hoy)

        self.lbl_prob = QLabel("Prob. abastecimiento: --%")
        self.lbl_prob.setStyleSheet("font-size: 13px; font-weight: bold;")
        medidor_layout.addWidget(self.lbl_prob)

        medidor_layout.addStretch()
        split.addWidget(medidor_frame, stretch=3)

        root.addLayout(split, stretch=1)

        # Cargar barras de progreso iniciales
        self._rebuild_barras()

        # Mensaje inicial del asistente
        self._agregar_burbuja("Asistente",
            "Buenos días. Soy Aqualy, su asistente de monitoreo hídrico. "
            "El medidor está activo y registrando en tiempo real. "
            "¿En qué le puedo ayudar?"
        )

        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    # FIN DE CONSTRUCCIÓN DE LA PESTAÑA 'MI SISTEMA'

    def _registrar_actividad(self, actividad, minutos):
        gasto = self.gestor.registrar_actividad(actividad, minutos)
        if gasto > 0:
            QMessageBox.information(
                self, "Actividad registrada",
                f"Se ha registrado el consumo de {minutos} min para '{actividad.replace('_', ' ').title()}'.\n" 
                f"Esto equivale a {gasto:.1f} L descontados de sus reservas."
            )
            self._actualizar_interfaz()

    def _registrar_actividad_personalizado(self, actividad):
        dialog = QDialog(self)
        dialog.setWindowTitle("Registrar consumo personalizado")
        dialog.setModal(True)
        dialog.setFixedSize(420, 210)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        lbl = QLabel("Ingrese los minutos de consumo para la actividad seleccionada:")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        spin = QSpinBox(dialog)
        spin.setRange(1, 240)
        spin.setValue(5)
        spin.setSuffix(" min")
        layout.addWidget(spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            minutos = spin.value()
            self._registrar_actividad(actividad, minutos)

    def _actualizar_resumen_admin(self):
        if hasattr(self, 'lbl_admin_resumen'):
            litros = self.gestor.litros_totales
            contadores = len(self.gestor.contenedores)
            fecha = self.gestor.fecha_fin_str
            self.lbl_admin_resumen.setText(
                f"Litros totales: {litros:.1f} L\nContenedores: {contadores}\nFecha de corte: {fecha}"
            )

    def _mostrar_registro_fuga(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Registrar Fuga")
        dialog.setModal(True)
        dialog.setFixedSize(420, 220)
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setContentsMargins(18, 18, 18, 18)
        dlg_layout.setSpacing(12)

        lbl = QLabel("Ingrese el volumen estimado de la fuga (Litros):")
        lbl.setWordWrap(True)
        dlg_layout.addWidget(lbl)

        self.spin_fuga = QDoubleSpinBox(dialog)
        self.spin_fuga.setRange(0.1, 5000.0)
        self.spin_fuga.setDecimals(1)
        self.spin_fuga.setValue(5.0)
        self.spin_fuga.setSuffix(" L")
        dlg_layout.addWidget(self.spin_fuga)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        dlg_layout.addWidget(btn_box)

        if dialog.exec_() == QDialog.Accepted:
            litros = self.spin_fuga.value()
            self.gestor.registrar_fuga(litros)
            QMessageBox.information(
                self, "Fuga registrada",
                f"Se registró una fuga de {litros:.1f} litros y se descontó de los contenedores."
            )
            self._actualizar_interfaz()
            self._rebuild_usuario_panel()

    def _recargar_contenedores(self):
        self.gestor.recargar_contenedores()
        QMessageBox.information(self, "Recarga completa", "Todos los contenedores se recargaron al 100%.")
        self._actualizar_interfaz()
        self._rebuild_usuario_panel()

    # ─────────────────────────────────────────────────────────────────────────
    # PESTAÑA 2: CONFIGURACIÓN
    # ─────────────────────────────────────────────────────────────────────────
    def _build_configuracion(self):
        """
        Construye la pestaña 'Configuración' con los controles para:
          - Establecer la fecha límite de corte del suministro
          - Cambiar el modo de operación (Normal / Ahorro / Extremo)
          - Ajustar las tasas de consumo por minuto de cada actividad doméstica
        """
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ── Encabezado ───────────────────────────────────────────────────────
        title = QLabel("Configuración General del Sistema")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        layout.addWidget(title)

        desc = QLabel(
            "Ajuste aquí los parámetros operativos del sistema. Los cambios se aplican "
            "inmediatamente al guardar y afectan las proyecciones del Asistente Virtual."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94A3B8; font-size: 13px;")
        layout.addWidget(desc)

        # ── Tarjeta: Parámetros Generales ────────────────────────────────────
        card_gen = CardWidget("Parámetros de Operación")
        form_gen = QFormLayout()
        form_gen.setVerticalSpacing(14)
        form_gen.setHorizontalSpacing(20)

        # Fecha de corte
        self.input_fecha = QLineEdit(self.gestor.fecha_fin_str)
        self.input_fecha.setPlaceholderText("AAAA-MM-DD")
        form_gen.addRow(QLabel("Fecha de corte del suministro (AAAA-MM-DD):"), self.input_fecha)

        # Modo de operación
        self.combo_modo = QComboBox()
        self.combo_modo.addItems(list(self.gestor.MODOS_OPERACION.keys()))
        self.combo_modo.setCurrentText(self.gestor.modo_actual)
        lbl_modo_help = QLabel("Normal = 100% del límite diario. Ahorro = 80%. Extremo = 60%.")
        lbl_modo_help.setStyleSheet("color: #64748B; font-size: 11px;")
        form_gen.addRow(QLabel("Modo de Operación:"), self.combo_modo)
        form_gen.addRow(QLabel(""), lbl_modo_help)

        card_gen.add_layout(form_gen)
        layout.addWidget(card_gen)

        # ── Tarjeta: Tasas de Consumo por Actividad ──────────────────────────
        card_tasas = CardWidget("Tasas de Consumo por Actividad (Litros / Minuto)")
        form_tasas = QFormLayout()
        form_tasas.setVerticalSpacing(12)
        form_tasas.setHorizontalSpacing(20)

        self.inputs_tasas = {}
        for act, litros in self.gestor.ACTIVIDADES.items():
            # Nombre legible de la actividad
            nombre = act.replace("_", " ").title()
            inp = QLineEdit(str(litros))
            inp.setPlaceholderText("L/min")
            form_tasas.addRow(QLabel(f"{nombre}:"), inp)
            self.inputs_tasas[act] = inp

        card_tasas.add_layout(form_tasas)
        layout.addWidget(card_tasas)

        # ── Botón Guardar ─────────────────────────────────────────────────────
        btn_guardar = QPushButton("Guardar Configuración")
        btn_guardar.setProperty("class", "PrimaryButton")
        btn_guardar.clicked.connect(self._guardar_configuracion)
        layout.addWidget(btn_guardar)

        layout.addStretch()
        self.stack.addWidget(page)

    # ─────────────────────────────────────────────────────────────────────────
    # LÓGICA DE ACTUALIZACIÓN EN TIEMPO REAL (QTIMER)
    # ─────────────────────────────────────────────────────────────────────────
    def _tick_sensor(self):
        """
        Se ejecuta cada 2 segundos vía QTimer.
        Lectura del medidor de agua → descuento proporcional del volumen en los
        recipientes → actualización de la UI → alerta si la IA detecta una anomalía.
        """
        lectura = self.sensor.obtener_lectura()
        caudal = lectura["caudal"]
        presion = lectura["presion"]
        temp = lectura["temperatura"]
        valvula = lectura["valvula_estado"]

        # ── Descontar agua de los recipientes si hay flujo activo ─────────────
        if caudal > 0 and valvula == "ABIERTA":
            # Litros consumidos en 2 segundos: (L/min × 2s) / 60s
            litros_tick = (caudal * 2.0) / 60.0
            self.gestor.extraer_agua(litros_tick)
            self.consumo_acumulado += litros_tick

            # Guardar en la BD cada vez que se acumule 1 litro completo
            if self.consumo_acumulado >= 1.0:
                db.registrar_consumo_db(
                    self.consumo_acumulado,
                    f"Medidor — {self.sensor.escenario_actual}"
                )
                self.gestor.historial_consumo = db.cargar_historial_completo()
                self.consumo_acumulado = 0.0

        # ── Actualizar display LCD ────────────────────────────────────────────
        self.lbl_caudal.setText(f"{caudal:.2f} L/min")
        self.lbl_presion.setText(f"{presion:.1f} PSI")
        self.lbl_temp.setText(f"{temp:.1f} °C")
        self.lbl_valvula.setText(f" {valvula} ")

        if valvula == "ABIERTA":
            self.lbl_valvula.setStyleSheet(
                "color: #4ADE80; font-family: 'Consolas', monospace; font-size: 14px; font-weight: bold;"
            )
        else:
            self.lbl_valvula.setStyleSheet(
                "color: #F87171; font-family: 'Consolas', monospace; font-size: 14px; font-weight: bold;"
            )

        # ── Refrescar estadísticas y barras ───────────────────────────────────
        self._actualizar_interfaz()

        # ── Verificar alertas de consumo en segundo plano ───────────────────────
        cap_total = sum(c.capacidad_maxima for c in self.gestor.contenedores)
        if cap_total > 0:
            pct = (self.gestor.litros_totales / cap_total) * 100
            if pct < 15.0:
                self._alerta_automatica("critico", caudal)
            elif caudal >= 0.5 and lectura["actividad_id"] == 0 and valvula == "ABIERTA":
                self._alerta_automatica("fuga", caudal)

    # Contador de ticks para no saturar el chat con alertas repetidas
    _alerta_contador = 0

    def _alerta_automatica(self, tipo, caudal):
        """
        Emite una alerta automática en el chat según el tipo de condición detectada.
        Se limita a una alerta cada 60 ticks (≈2 minutos) para evitar saturar el chat.
        """
        self._alerta_contador += 1
        if self._alerta_contador < 60:
            return
        self._alerta_contador = 0

        if tipo == "fuga":
            msg = (
                f"⚠️ Alerta automática: El medidor registra {caudal:.2f} L/min de flujo "
                "sin actividad declarada. Esto podría indicar una fuga en su instalación. "
                "Puede cerrar la válvula principal desde el panel del medidor."
            )
        else:
            msg = (
                "🚨 Alerta automática: El nivel de sus reservas ha caído a un valor crítico. "
                "Se recomienda limitar el uso de agua e iniciar una recarga pronto."
            )
        self._agregar_burbuja("Asistente", msg)

    # ─────────────────────────────────────────────────────────────────────────
    # ACTUALIZACIÓN GENERAL DE LA INTERFAZ
    # ─────────────────────────────────────────────────────────────────────────
    def _actualizar_interfaz(self):
        """Actualiza las barras de nivel, el resumen superior y las estadísticas del día."""
        # Barras de progreso de cada recipiente
        for cont in self.gestor.contenedores:
            if cont.nombre in self.barras_progreso:
                self.barras_progreso[cont.nombre].setValue(int(cont.litros_actuales))

        # Resumen superior
        litros = self.gestor.litros_totales
        prob = self.gestor.probabilidad_supervivencia()
        self.lbl_resumen_top.setText(f"Reserva: {litros:.1f} L  |  Prob. abastecimiento: {prob}%")

        # Gasto del día y probabilidad en el panel del medidor
        consumo_hoy = db.obtener_consumo_hoy()
        self.lbl_gasto_hoy.setText(f"Gasto hoy: {consumo_hoy:.1f} L")
        self.lbl_prob.setText(f"Prob. abastecimiento: {prob}%")
        if prob > 80:
            self.lbl_prob.setStyleSheet("font-size: 13px; font-weight: bold; color: #22C55E;")
        elif prob > 40:
            self.lbl_prob.setStyleSheet("font-size: 13px; font-weight: bold; color: #EAB308;")
        else:
            self.lbl_prob.setStyleSheet("font-size: 13px; font-weight: bold; color: #EF4444;")
        self._actualizar_resumen_admin()

    def _rebuild_barras(self):
        """Reconstruye desde cero las barras de progreso de los recipientes."""
        # Eliminar barras anteriores
        while self.layout_barras.count():
            item = self.layout_barras.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.barras_progreso.clear()

        if not self.gestor.contenedores:
            lbl_vacio = QLabel("Sin recipientes registrados. Pulse '⚙ Gestionar Recipientes' para agregar uno.")
            lbl_vacio.setStyleSheet("color: #64748B; font-size: 13px;")
            lbl_vacio.setAlignment(Qt.AlignCenter)
            self.layout_barras.addWidget(lbl_vacio)
        else:
            for cont in self.gestor.contenedores:
                row = QHBoxLayout()
                lbl_name = QLabel(f"<b>{cont.nombre}</b>")
                lbl_name.setFixedWidth(180)
                lbl_name.setStyleSheet("color: #F1F5F9; font-size: 13px;")
                pbar = QProgressBar()
                pbar.setMaximum(max(int(cont.capacidad_maxima), 1))
                pbar.setValue(int(cont.litros_actuales))
                pbar.setFormat("%v / %m L")
                row.addWidget(lbl_name)
                row.addWidget(pbar, stretch=1)
                frame = QFrame()
                frame.setStyleSheet("background-color: transparent;")
                frame.setLayout(row)
                self.layout_barras.addWidget(frame)
                self.barras_progreso[cont.nombre] = pbar

        self.layout_barras.addStretch()

    # ─────────────────────────────────────────────────────────────────────────
    # CHAT DEL ASISTENTE
    # ─────────────────────────────────────────────────────────────────────────
    def _enviar_chat(self):
        """Recoge el texto del input, lo muestra como burbuja del usuario y genera la respuesta."""
        texto = self.input_chat.text().strip()
        if not texto:
            return
        self.input_chat.clear()
        self._procesar_pregunta(texto)

    def _procesar_pregunta(self, pregunta: str):
        """
        Añade la burbuja del usuario, llama al módulo de IA para generar
        la respuesta y la muestra como burbuja del Asistente.
        """
        # Burbuja del usuario
        self._agregar_burbuja("Usuario", pregunta)

        # Obtener lectura del medidor para que la IA tenga contexto actual
        lectura = self.sensor.obtener_lectura()

        # Generar respuesta formal del asistente
        respuesta = obtener_respuesta_asistente(pregunta, self.gestor, lectura)
        self._agregar_burbuja("Asistente", respuesta)

    def _agregar_burbuja(self, remitente: str, texto: str):
        """
        Agrega un mensaje al historial del chat con estilo de burbuja diferenciado:
          - Usuario: burbuja azul alineada a la derecha (sin encabezado)
          - Asistente: burbuja oscura alineada a la izquierda
        Los bordes son notablemente redondeados (border-radius: 18px).
        """
        burbuja = QFrame()

        if remitente == "Usuario":
            # Burbuja del usuario — azul, derecha, sin encabezado
            burbuja.setStyleSheet(
                "background-color: #2563EB; border-radius: 18px; "
                "margin-left: 100px; margin-right: 6px;"
            )
            texto_html = texto.replace("\n", "<br/>")
            alineacion = Qt.AlignRight
        else:
            # Burbuja del asistente — oscura, izquierda
            burbuja.setStyleSheet(
                "background-color: #1E293B; border-radius: 18px; "
                "border: 1px solid #334155; margin-right: 100px; margin-left: 6px;"
            )
            texto_html = texto.replace("\n", "<br/>")
            alineacion = Qt.AlignLeft

        burbuja_layout = QVBoxLayout(burbuja)
        burbuja_layout.setContentsMargins(14, 10, 14, 10)

        lbl = QLabel(texto_html)
        lbl.setWordWrap(True)
        lbl.setTextFormat(Qt.RichText)
        lbl.setAlignment(alineacion)
        lbl.setStyleSheet("color: white; font-size: 13px; background-color: transparent;")
        burbuja_layout.addWidget(lbl)

        # Agregar la burbuja al final del layout (AlignTop ya garantiza el orden)
        self.chat_layout.addWidget(burbuja)

        # Scroll al final con un pequeño delay para que Qt renderice antes
        QTimer.singleShot(80, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))



    # ─────────────────────────────────────────────────────────────────────────
    # ACCIONES DEL MEDIDOR Y CONFIGURACIÓN
    # ─────────────────────────────────────────────────────────────────────────
    def _cambiar_escenario(self, nuevo: str):
        """
        Cambia el escenario de calibración del medidor y persiste
        el consumo acumulado antes de aplicar el nuevo flujo.
        """
        if self.consumo_acumulado > 0:
            db.registrar_consumo_db(self.consumo_acumulado, "Medidor — Fin de escenario")
            self.gestor.historial_consumo = db.cargar_historial_completo()
            self.consumo_acumulado = 0.0

        self.sensor.set_escenario(nuevo)
        self.lbl_esc_desc.setText(self.sensor.ESCENARIOS[nuevo]["descripcion"])

    def _toggle_valvula(self):
        """Abre o cierra la válvula principal del medidor y actualiza el botón."""
        if self.sensor.valvula_abierta:
            self.sensor.valvula_abierta = False
            self.btn_valvula.setText("Abrir Válvula Principal")
            self.btn_valvula.setProperty("class", "PrimaryButton")
            self.lbl_conexion.setText("● Válvula cerrada")
            self.lbl_conexion.setStyleSheet("color: #F87171; font-size: 12px; font-weight: bold;")
            # Persistir consumo acumulado al corte
            if self.consumo_acumulado > 0:
                db.registrar_consumo_db(self.consumo_acumulado, "Medidor — Válvula cerrada")
                self.gestor.historial_consumo = db.cargar_historial_completo()
                self.consumo_acumulado = 0.0
        else:
            self.sensor.valvula_abierta = True
            self.btn_valvula.setText("Cerrar Válvula Principal")
            self.btn_valvula.setProperty("class", "DangerButton")
            self.lbl_conexion.setText("● Conectado")
            self.lbl_conexion.setStyleSheet("color: #22C55E; font-size: 12px; font-weight: bold;")

        # Refrescar el estilo del botón en Qt
        self.btn_valvula.style().unpolish(self.btn_valvula)
        self.btn_valvula.style().polish(self.btn_valvula)

    def _abrir_gestion_recipientes(self):
        """
        Abre el diálogo modal de gestión de recipientes y, al cerrarlo,
        reconstruye las barras de progreso del panel principal.
        """
        dlg = GestionRecipientesDialog(self.gestor, self)
        dlg.exec_()
        # Reconstruir barras con los recipientes actualizados
        self._rebuild_barras()
        self._actualizar_interfaz()

    def _guardar_configuracion(self):
        """
        Valida y guarda en la base de datos los parámetros de configuración:
        fecha de corte, modo de operación y tasas de consumo por actividad.
        """
        fecha = self.input_fecha.text().strip()
        modo = self.combo_modo.currentText()

        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Fecha inválida", "La fecha debe tener el formato AAAA-MM-DD.")
            return

        # Guardar en la BD
        conn = db.conectar()
        cur = conn.cursor()
        cur.execute("UPDATE configuracion SET fecha_fin = ?, modo_actual = ?", (fecha, modo))
        conn.commit()
        conn.close()

        self.gestor.fecha_fin_str = fecha
        self.gestor.modo_actual = modo

        # Guardar tasas de actividades
        for act, inp in self.inputs_tasas.items():
            try:
                tasa = int(inp.text().strip())
                if tasa < 0:
                    raise ValueError
                self.gestor.ACTIVIDADES[act] = tasa
            except ValueError:
                QMessageBox.critical(self, "Valor inválido",
                    f"La tasa de '{act.replace('_', ' ').title()}' debe ser un número entero positivo.")
                return

        QMessageBox.information(self, "Guardado", "La configuración se ha guardado correctamente.")
        self._actualizar_interfaz()
