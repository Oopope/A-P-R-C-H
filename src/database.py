import sqlite3
import os

# Definimos la ruta de la base de datos de forma relativa al proyecto
DB_PATH = os.path.join("data", "sistema.db")

def conectar():
    """Establece conexión con SQLite."""
    return sqlite3.connect(DB_PATH)

def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    # Aseguramos que la carpeta 'data' exista
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. Tabla de configuración (Estado del tanque y fechas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            litros_totales REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL
        )
    ''')

    # 2. Tabla de registros diarios (Lo que el usuario gasta)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT DEFAULT (datetime('now', 'localtime')),
            litros_gastados REAL NOT NULL,
            nota TEXT
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos configurada correctamente. 🫡")

def cargar_datos_iniciales(litros, f_inicio, f_fin):
    """Inserta los datos del proyecto si la tabla está vacía."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificamos si ya hay datos para no duplicar
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO configuracion (litros_totales, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?)
        ''', (litros, f_inicio, f_fin))
        conexion.commit()
        print(f"Carga inicial exitosa: {litros}L registrados.")
    
    conexion.close()

# El "if main" para probar el backend por separado
if __name__ == "__main__":
    inicializar_bd()
    # Cargamos tus datos de Paraguaná
    cargar_datos_iniciales(3000.0, "2026-04-21", "2026-06-21")