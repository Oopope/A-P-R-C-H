DARK_THEME_QSS = """
QMainWindow {
    background-color: #0F172A; /* Slate 900 */
}

QWidget {
    color: #F8FAFC; /* Slate 50 */
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Título de la Aplicación */
QLabel#AppTitle {
    font-size: 32px;
    font-weight: bold;
    color: #38BDF8; /* Light Blue */
    margin: 10px;
}

/* Paneles/Tarjetas */
QFrame.Card {
    background-color: #1E293B; /* Slate 800 */
    border-radius: 12px;
    padding: 20px;
}

QLabel.CardTitle {
    font-size: 18px;
    font-weight: bold;
    color: #94A3B8; /* Slate 400 */
    margin-bottom: 15px;
}

/* Barras de Progreso */
QProgressBar {
    border: 2px solid #334155; /* Slate 700 */
    border-radius: 8px;
    background-color: #0F172A;
    text-align: center;
    color: white;
    font-weight: bold;
    height: 24px;
}

QProgressBar::chunk {
    background-color: #3B82F6; /* Blue 500 */
    border-radius: 6px;
}

/* Botones */
QPushButton {
    background-color: #2563EB; /* Blue 600 */
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 15px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #3B82F6; /* Blue 500 */
}

QPushButton:pressed {
    background-color: #1D4ED8; /* Blue 700 */
}

/* ComboBox (Desplegable) */
QComboBox {
    background-color: #334155; /* Slate 700 */
    color: white;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #475569; /* Slate 600 */
}

QComboBox::drop-down {
    border: none;
}

/* Botones de acción especial */
QPushButton#BtnFuga {
    background-color: #EA580C; /* Orange 600 */
}
QPushButton#BtnFuga:hover {
    background-color: #F97316; /* Orange 500 */
}
QPushButton#BtnFuga:pressed {
    background-color: #C2410C; /* Orange 700 */
}

QPushButton#BtnRecargar {
    background-color: #0D9488; /* Teal 600 */
}
QPushButton#BtnRecargar:hover {
    background-color: #14B8A6; /* Teal 500 */
}
QPushButton#BtnRecargar:pressed {
    background-color: #0F766E; /* Teal 700 */
}

/* Etiquetas del Semáforo */
QLabel#SemaforoVerde {
    background-color: #16A34A; /* Green 600 */
    color: white;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    padding: 6px 12px;
}

QLabel#SemaforoAmarillo {
    background-color: #CA8A04; /* Yellow 600 */
    color: white;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    padding: 6px 12px;
}

QLabel#SemaforoRojo {
    background-color: #DC2626; /* Red 600 */
    color: white;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    padding: 6px 12px;
}
"""
