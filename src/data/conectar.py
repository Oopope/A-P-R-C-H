#esto es la conexion de la base de datos al sistema
import sqlite3
conexion = sqlite3.connect('base de dato')
cursor = conexion.cursor()
conexion.commit()
print(cursor.fetchall())
conexion.close()