import mysql.connector

def closeConnection(cursor, conexion):
    cursor.close()
    conexion.close()

def openConnection():       
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="tiktok"
    )
    

# Crear registro
def crear_registro(query, *args):
    conexion = openConnection()
    cursor = conexion.cursor()
    if args:
            cursor.execute(query, args)
    else:
        cursor.execute(query)
    conexion.commit()
    closeConnection(cursor, conexion)

# Leer registros
def leer_registros(query):
    conexion = openConnection()
    cursor = conexion.cursor()
    cursor.execute(query)
    return cursor.fetchall()
    closeConnection(cursor, conexion)

def leer_registro(query):
    conexion = openConnection()
    cursor = conexion.cursor()
    cursor.execute(query)
    return cursor.fetchone()
    closeConnection(cursor, conexion)