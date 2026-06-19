DARK_THEME_QSS = """
/* Ventana Principal */
QMainWindow {
    background-color: #0F172A; /* Slate 900 */
}

QWidget {
    color: #F8FAFC; /* Slate 50 */
    font-family: 'Outfit', 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

/* --- Diálogos y Ventanas Emergentes --- */
QDialog {
    background-color: #1E293B; /* Slate 800 */
}

QDialog QLabel {
    color: #F8FAFC; /* Slate 50 */
}

QDialog QPushButton {
    background-color: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
}

QDialog QPushButton:hover {
    background-color: #475569;
}

QDialog QLineEdit, QDialog QSpinBox, QDialog QDoubleSpinBox, QDialog QComboBox {
    background-color: #0F172A;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px;
    color: white;
}

/* --- Barra Lateral (Sidebar) --- */
QFrame#Sidebar {
    background-color: #1E293B; /* Slate 800 */
    border-right: 1px solid #334155;
}

/* Logo Aqualy en Times New Roman */
QLabel#LogoLabel {
    font-family: 'Times New Roman', Times, 'Georgia', serif;
    font-size: 36px;
    font-weight: bold;
    font-style: italic;
    color: #FACC15; /* Yellow/Gold */
    padding: 20px 5px;
    margin-bottom: 10px;
}

/* Botones de Navegación del Menú */
QPushButton.MenuButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 8px;
    padding: 12px 15px;
    text-align: left;
    font-weight: bold;
    font-size: 14px;
    margin: 4px 5px;
}

QPushButton.MenuButton:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #F8FAFC;
}

QPushButton.MenuButton:checked {
    background-color: #3B82F6; /* Blue 500 */
    color: white;
}

/* Botón de Colapsar Menú */
QPushButton#BtnToggleSidebar {
    background-color: transparent;
    color: #F8FAFC;
    border: none;
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
    text-align: center;
}

QPushButton#BtnToggleSidebar:hover {
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 6px;
}

/* --- Área de Contenido Principal --- */
QFrame#MainContentArea {
    background-color: #0F172A;
}

/* Tarjetas (Glassmorphism) */
QFrame.Card {
    background-color: rgba(30, 41, 59, 0.7); /* Transparente Slate 800 */
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
}

QFrame.Card:hover {
    background-color: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(59, 130, 246, 0.3); /* Resaltar con azul */
}

QLabel.CardTitle {
    font-size: 18px;
    font-weight: bold;
    color: #F8FAFC;
    margin-bottom: 12px;
}

/* --- Elementos del Formulario / Controles --- */
QLabel {
    font-size: 14px;
}

QLineEdit {
    background-color: #1E293B;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
    color: white;
}

QLineEdit:focus {
    border: 1px solid #3B82F6;
}

/* IMPORTANTE: Solución de números invisibles */
QSpinBox, QDoubleSpinBox {
    background-color: #1E293B;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
    color: white;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #3B82F6;
}

QComboBox {
    background-color: #1E293B;
    color: white;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 150px;
}

QComboBox:on {
    border: 1px solid #3B82F6;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
}

QComboBox QAbstractItemView {
    background-color: #1E293B;
    color: white;
    selection-background-color: #3B82F6;
    border: 1px solid #475569;
}

/* --- Barras de Progreso --- */
QProgressBar {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #020617;
    text-align: center;
    color: white;
    font-weight: bold;
    height: 26px;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3B82F6, stop:1 #60A5FA);
    border-radius: 6px;
}

/* --- Botones Genéricos --- */
QPushButton.PrimaryButton {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}

QPushButton.PrimaryButton:hover {
    background-color: #3B82F6;
}

QPushButton.PrimaryButton:pressed {
    background-color: #1D4ED8;
}

QPushButton.SecondaryButton {
    background-color: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}

QPushButton.SecondaryButton:hover {
    background-color: #475569;
}

QPushButton.DangerButton {
    background-color: #DC2626;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}

QPushButton.DangerButton:hover {
    background-color: #EF4444;
}

/* --- Badges del Semáforo --- */
QLabel#SemaforoVerde {
    background-color: rgba(22, 163, 74, 0.2);
    color: #4ADE80;
    border: 1px solid #22C55E;
    font-size: 12px;
    font-weight: bold;
    border-radius: 6px;
    padding: 4px 8px;
}

QLabel#SemaforoAmarillo {
    background-color: rgba(202, 138, 4, 0.2);
    color: #FACC15;
    border: 1px solid #EAB308;
    font-size: 12px;
    font-weight: bold;
    border-radius: 6px;
    padding: 4px 8px;
}

QLabel#SemaforoRojo {
    background-color: rgba(220, 38, 38, 0.2);
    color: #F87171;
    border: 1px solid #EF4444;
    font-size: 12px;
    font-weight: bold;
    border-radius: 6px;
    padding: 4px 8px;
}

/* --- Scroll Area --- */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #0F172A;
    width: 10px;
    margin: 0px 0 0px 0;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

/* --- Estilos Adicionales para el Asistente y Medidor --- */
QWidget#PantallaBienvenida {
    background-color: #0F172A;
}

QLabel#BienvenidaTitulo {
    font-size: 28px;
    font-weight: bold;
    color: #FACC15;
    margin-bottom: 10px;
}

QLabel#BienvenidaTexto {
    font-size: 15px;
    color: #94A3B8;
}

/* Panel del Medidor Físico */
QFrame#PanelMedidor {
    background-color: #1E293B;
    border: 2px solid #334155;
    border-radius: 14px;
    padding: 15px;
}

QFrame#MedidorPantallaLCD {
    background-color: #020617;
    border: 1px solid #3B82F6;
    border-radius: 8px;
    padding: 12px;
}

QLabel.LecturaLCD {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 22px;
    font-weight: bold;
    color: #06B6D4;
}

QLabel.LecturaLCDLabel {
    font-size: 11px;
    font-weight: bold;
    color: #94A3B8;
}

/* Botones de sugerencia rápidos en Chat */
QPushButton.SugestButton {
    background-color: #1E293B;
    color: #3B82F6;
    border: 1px solid #3B82F6;
    border-radius: 15px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton.SugestButton:hover {
    background-color: #3B82F6;
    color: white;
}

/* Caja de entrada de chat */
QLineEdit#ChatInput {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 8px 15px;
    color: white;
    font-size: 13px;
}

QLineEdit#ChatInput:focus {
    border: 1px solid #3B82F6;
}
"""
