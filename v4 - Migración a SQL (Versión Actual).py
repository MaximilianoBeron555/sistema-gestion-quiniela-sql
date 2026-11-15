# Módulos
import sqlite3
import questionary
from colorama import Fore, Back, init
init()

DB_name = "Clientes.db"

# --- Funciones Auxiliares para evitar repeticion de código y conexion de sql3 ---

def mostrar_exito(mensaje):

    print(Fore.BLACK + Back.GREEN + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")

def mostrar_error(mensaje):

    print(Fore.BLACK + Back.RED + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")

def conectar():
    return sqlite3.connect(DB_name)

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS clientes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT NOT NULL,
          monto REAL NOT NULL,
          tipo TEXT NOT NULL
       )          
    """)
    conn.commit()
    conn.close()

# --- Funciones de Base de Datos (SQL) ---

def existe_cliente(nombre):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM clientes WHERE LOWER(nombre) = LOWER(?)", (nombre,))

    resultado = cursor.fetchone()
    
    conn.close()
    return resultado is not None 

def crear_cliente(nombre, monto, tipo):
    
    #Guarda el registro en la base de datos SQLite.

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clientes(nombre, monto, tipo)
    VALUES(?, ?, ?)
    """, (nombre, monto, tipo))

    conn.commit()
    conn.close()

def obtener_todos_clientes():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, monto, tipo FROM clientes")
    registros = cursor.fetchall()  #trae todos los clientes
    
    conn.close()
    return registros

def buscar_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, monto, tipo FROM clientes WHERE LOWER(nombre) LIKE LOWER(?)", (f"%{nombre}%",))
    registros = cursor.fetchall()
    
    conn.close()
    return registros

def eliminar_por_id(id_cliente):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    filas_borradas = cursor.rowcount

    conn.commit()
    conn.close()
    return filas_borradas > 0

def sumar_por_tipo(tipo):
    conn = conectar()
    cursor = conn.cursor()
    
    #coalesce = devuelve 0 en lugar de None (caso que no hay nada)
   
    cursor.execute("SELECT COALESCE(SUM(monto),0) FROM clientes WHERE tipo = ?", (tipo,))
    total = cursor.fetchone()[0]

    conn.close()
    return total

# --- Funciones Principales ---

def agregar():
    
    print("\n Iniciando agregado de cliente... \n")   
    
    # Pide y valida los datos por consola antes de enviarlos a SQL.

    nombre = str(input("Nombre/Apellido : ").strip())

    while nombre == "" or nombre.isdigit():

        mostrar_error("El Nombre ingresado es incorrecto, Ingrese Nombre/Apellido.")

        nombre = str(input("Nombre/Apellido : ").strip())


    if existe_cliente(nombre):
        #verifico si esta en la base 

        mostrar_error("Ya existe un cliente registrado con ese Nombre/Apellido.")
        while True:
         opcion = questionary.select("Seleccione opcion que quiere realizar :",
           choices = [
            "Agregar Cliente de todas maneras",
            "Regresar Atras"
            ]).ask()
         if opcion == "Agregar Cliente de todas maneras":
            break
         elif opcion == "Regresar Atras":
            return   

    monto = float(input("monto: ").strip())

    tipo = questionary.select("Seleccione Tipo de pago",
        choices = [
        "Efectivo",
        "Transferencia",
        "Fiado",
        "Telekino",
        "Egresos"
        ]
        ).ask()
    # la seleccion del tipo se guarda directo en la variable   
    
    # Persistencia en archivo
    try:
        crear_cliente(nombre, monto, tipo)
        mostrar_exito("Cliente Incorporado")

    except sqlite3.Error as e:
        # imprimo error de cual es el error  
        mostrar_error(f"Error al guardar en la base de datos: {e}")
            
def mostrar():
    registros = obtener_todos_clientes()

    if not registros:
        mostrar_error("No se registran clientes en la lista.")
        return

    print(Fore.BLACK + Back.WHITE + "Lista de clientes incorporados en el sistema" + Fore.RESET + Back.RESET + "\n")

    for id_reg, nombre, monto, tipo in registros:
        print(f" ID: #{id_reg}")

        print(f" Nombre/Apellido: {nombre}")

        print(f" Monto: ${monto}")

        print(f" Tipo: {tipo} \n")

def buscar():

    nombre = input("Ingrese el Nombre/Apellido del cliente que desea Buscar: ").strip()

    print("\n Iniciando búsqueda... \n")
    
    #busco en la def si existe
    resultados = buscar_por_nombre(nombre)    
    
    if resultados:
        mostrar_exito(f"Se encontraron {len(resultados)} registro(s)!")
        for id_reg, nombre, monto, tipo in resultados:
         print(f" ID: #{id_reg}")

         print(f" Nombre/Apellido: {nombre}")

         print(f" Monto: {monto}")

         print(f" Tipo: {tipo} \n")

    else:
        mostrar_error("El cliente solicitado no se encuentra en la lista.")

def eliminar():

    nombre = input("Ingrese el Nombre/Apellido del cliente que desea eliminar: ").strip()

    print("\n Iniciando proceso de eliminación... \n")

    resultados = buscar_por_nombre(nombre)
    
    if not resultados:
        mostrar_error("El cliente solicitado no existe o ya fue eliminado.")
        return

    # Opciones claras con questionary (mas de un movimiento)    
    
    opciones = [f" ID #{id_reg} - {nombre} (${monto} - {tipo})" for id_reg, nombre, monto, tipo in resultados]
    opciones.append("Cancelar")
    
    seleccion = questionary.select("Seleccione el registro exacto que desea eliminar: ",
       choices = opciones 
    ).ask()
   
    if seleccion == "Cancelar" or seleccion is None:
        return
    
    # Guardar el id a eliminar
    id_a_eliminar = int(seleccion.split(" - ")[0].strip().replace("ID #", ""))  
    
    if eliminar_por_id(id_a_eliminar):
       mostrar_exito(f"Registro #{id_a_eliminar} eliminado con éxito!")
    else:
        mostrar_error("No se pudo eliminar el registro.")

######### Funciones Calculos
               
def calcular_montos():
    opcionP = questionary.select("Seleccione monto a calcular...",
        choices = [                              
            "Efectivo",
            "Transferencia",
            "Fiado",
            "Telekino",
            "Egresos",
            "Total"
        ]).ask()
    
    if opcionP is None:
        return
        
    # Si selecciono cualquiera de los 5 tipos, usa la misma funcion
    if opcionP in [
        "Efectivo",
        "Transferencia",
        "Fiado",
        "Telekino",
        "Egresos"]:
        subtotal = sumar_por_tipo(opcionP)
        print(Fore.BLACK + Back.WHITE + f"Monto total de {opcionP} = ${subtotal}" + Fore.RESET + Back.RESET + "\n")

    elif opcionP == "Total":
            
        efectivo = sumar_por_tipo("Efectivo")
            
        transferencia = sumar_por_tipo("Transferencia")
            
        fiado = sumar_por_tipo("Fiado")
            
        telekino = sumar_por_tipo("Telekino")
            
        egresos = sumar_por_tipo("Egresos")

        # Calculo resultado en variable total 

        total = efectivo + transferencia  + telekino - fiado - egresos
            
        #pantalla resultados  
        print(Fore.BLACK + Back.WHITE + "--- DETALLE DE CAJA ---" + Fore.RESET + Back.RESET)
            
        print(f" Efectivo:      ${efectivo}")
            
        print(f" Transferencia: ${transferencia}")
            
        print(f" Telekino:      ${telekino}")
            
        print(f" Fiado (-):     ${fiado}")
            
        print(f" Egresos (-):   ${egresos}")

        mostrar_exito(f"Cierre de caja total : ${total}")

# Menú   

crear_tabla()
print(Fore.BLACK + Back.GREEN + "Programa Gestion Quiniela SQL" + Fore.RESET + Back.RESET + "\n")


while True:
    opcion = questionary.select("Seleccione la opción que desea realizar",
    choices = [
    "Agregar cliente",
    "Calcular Montos",
    "Buscar cliente",
    "Mostrar lista",
    "Eliminar cliente",
    "Finalizar Programa"
    ]
    ).ask()

    if opcion == "Agregar cliente":
        agregar()
    elif opcion == "Calcular Montos":
        calcular_montos()                         
    elif opcion == "Buscar cliente":
        buscar()
    elif opcion == "Mostrar lista":
        mostrar()
    elif opcion == "Eliminar cliente": 
        eliminar()
    elif opcion == "Finalizar Programa":
        opcion1 = questionary.select("Confirmar Finalizacion de Programa.",
            choices = [
              "No",
              "Si" ]).ask()         
        if opcion1 == "Si":
          print(Fore.BLUE + Back.BLACK + "\nPrograma Finalizado. \n" + Fore.RESET + Back.RESET)
          break
        elif opcion1 == "No":
           continue 
    else:
        mostrar_error("Opción inválida. Por favor, elija una opcion Correcta.")

