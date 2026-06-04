import sqlite3
import os
import sys

# Definimos la ruta de la base de datos de forma absoluta
if getattr(sys, 'frozen', False):
    # Si está compilado, la base de datos se guarda al lado del ejecutable .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Si está en modo desarrollo
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "sistema.db")

def conectar():
    """Establece conexión con SQLite."""
    return sqlite3.connect(DB_PATH)

def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    # Aseguramos que la carpeta 'data' exista
    data_dir = os.path.join(BASE_DIR, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. Tabla de configuración (Estado del tanque, fechas y modo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            litros_totales REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            modo_actual TEXT DEFAULT 'Normal'
        )
    ''')

    # 2. Tabla de contenedores individuales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            capacidad_maxima REAL NOT NULL,
            litros_actuales REAL NOT NULL
        )
    ''')

    # 3. Tabla de registros diarios (Lo que el usuario gasta)
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
    print("Base de datos configurada correctamente.")

def cargar_datos_iniciales():
    """Inserta los datos iniciales si las tablas están vacías."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. Configuración por defecto
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO configuracion (litros_totales, fecha_inicio, fecha_fin, modo_actual)
            VALUES (?, ?, ?, ?)
        ''', (1200.0, "2026-05-15", "2026-06-21", "Normal"))
        conexion.commit()
        print("Carga inicial de configuración exitosa.")
        
    # 2. Contenedores por defecto
    cursor.execute("SELECT COUNT(*) FROM contenedores")
    if cursor.fetchone()[0] == 0:
        default_contenedores = [
            ("Tanque Subterráneo", "Tanque", 1000.0, 1000.0),
            ("Pipa de Baño", "Pipa", 200.0, 200.0)
        ]
        cursor.executemany('''
            INSERT INTO contenedores (nombre, tipo, capacidad_maxima, litros_actuales)
            VALUES (?, ?, ?, ?)
        ''', default_contenedores)
        conexion.commit()
        print("Carga inicial de contenedores exitosa.")
        
    conexion.close()

def cargar_configuracion():
    """Retorna la fecha de fin y el modo de operación actual."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha_fin, modo_actual FROM configuracion ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conexion.close()
    if row:
        return row[0], row[1]
    return "2026-06-21", "Normal"

def guardar_modo(modo):
    """Actualiza el modo de operación actual."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE configuracion SET modo_actual = ?", (modo,))
    conexion.commit()
    conexion.close()

def cargar_contenedores():
    """Retorna una lista de diccionarios con la información de los contenedores."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, tipo, capacidad_maxima, litros_actuales FROM contenedores")
    rows = cursor.fetchall()
    conexion.close()
    return [{"nombre": r[0], "tipo": r[1], "capacidad_maxima": r[2], "litros_actuales": r[3]} for r in rows]

def actualizar_nivel_contenedor(nombre, litros):
    """Actualiza los litros actuales de un contenedor."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE contenedores SET litros_actuales = ? WHERE nombre = ?", (litros, nombre))
    conexion.commit()
    conexion.close()

def recargar_todos_los_contenedores():
    """Restablece los litros actuales de todos los contenedores al máximo."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE contenedores SET litros_actuales = capacidad_maxima")
    conexion.commit()
    conexion.close()

def registrar_consumo_db(litros, nota):
    """Registra una actividad o pérdida de agua en el historial de consumos."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO consumos (litros_gastados, nota) VALUES (?, ?)", (litros, nota))
    conexion.commit()
    conexion.close()

def obtener_consumo_hoy():
    """Suma los consumos del día actual."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(litros_gastados) FROM consumos WHERE date(fecha) = date('now', 'localtime')")
    val = cursor.fetchone()[0]
    conexion.close()
    return val if val is not None else 0.0

def cargar_historial_completo():
    """Devuelve los litros gastados agrupados por día para el cálculo estadístico."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT date(fecha), SUM(litros_gastados) 
        FROM consumos 
        GROUP BY date(fecha) 
        ORDER BY date(fecha) ASC
    """)
    rows = cursor.fetchall()
    conexion.close()
    return [r[1] for r in rows]

# El "if main" para probar el backend por separado
if __name__ == "__main__":
    inicializar_bd()
    cargar_datos_iniciales()