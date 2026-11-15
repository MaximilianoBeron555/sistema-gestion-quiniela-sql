# Módulos
import questionary
from colorama import Fore, Back, init
init()

clientes = {}

# --- Funciones Auxiliares para evitar repeticion de código ---

def mostrar_exito(mensaje):

    print(Fore.BLACK + Back.GREEN + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")

def mostrar_error(mensaje):

    print(Fore.BLACK + Back.RED + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")


# --- Funciones Principales ---

def cargar_datos():

    try:

        with open("clientes.txt", "r") as archivo:

            for linea in archivo:

                linea = linea.strip()

                if not linea:  # Salta líneas vacías

                    continue

                datos = linea.split(",")

                if len(datos) == 3:

                    nombre = datos[0]  # Ahora el DNI es la clave principal

                    clientes[nombre] = {

                        "monto": datos[1],

                        "tipo": datos[2]
                                       }

    except FileNotFoundError:

        # Si el archivo no existe, no hace falta lanzar error, se creará al agregar un cliente

        pass  

def agregar():

    print("\n Iniciando agregado de cliente... \n")   

    # Validamos el Nombre primero para ver si ya existe

    nombre = input(str("Nombre/Apellido : ")).strip()

    while nombre == "" or nombre.isdigit():

        mostrar_error("El Nombre ingresado es incorrecto, Ingrese Nombre/Apellido.")
        
        nombre = input(str("Nombre/Apellido : ")).strip()

        
    if nombre in clientes:

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


    monto = int(input("monto: ").strip())

    while True:
        tipo = questionary.select("Seleccione Tipo de pago",
        choices = [
        "Efectivo",
        "Transferencia",
        "Fiado",
        "Telekino",
        "Egresos"
        ]
        ).ask()
        break   
    # Guardamos en memoria usando el Nombre como clave

    clientes[nombre] = {"monto": monto, "tipo": tipo}
    
    # Persistencia en archivo

    with open("clientes.txt", "a") as archivo:

        archivo.write(f"{nombre},{monto},{tipo}\n")
         
    mostrar_exito("Cliente Incorporado")

def mostrar():

    if not clientes:
        mostrar_error("No se registran clientes en la lista.")
        return

    print(Fore.BLACK + Back.WHITE + "Lista de clientes incorporados en el sistema" + Fore.RESET + Back.RESET + "\n")

    for nombre, datos in clientes.items():
        print(f" Nombre/Apellido: {nombre}")

        print(f" monto: {datos['monto']}")

        print(f" tipo: {datos['tipo']} \n")

def buscar():

    nombre = input("Ingrese el Nombre/Apellido del cliente que desea Buscar: ").strip()

    print("\n Iniciando búsqueda... \n")

    # Se busca directamente en memoria, optimizando el proceso

    if nombre in clientes:

        cliente = clientes[nombre]

        mostrar_exito(f"El cliente con Nombre/Apellido {nombre} fue encontrado con éxito!")

        print(f" Nombre/apellido: {nombre}")

        print(f" Monto: {cliente['monto']}")

        print(f" Tipo: {cliente['tipo']} \n")

    else:

        mostrar_error("El cliente solicitado no se encuentra en la lista.")

def eliminar():

    nombre = input("Ingrese el Nombre/Apellido del cliente que desea eliminar: ").strip()

    print("\n Iniciando proceso de eliminación... \n")

    if nombre in clientes:

        clientes.pop(nombre)

        # Reescritura del archivo con los datos actualizados de memoria

        with open("clientes.txt", "w") as archivo:

            for k, v in clientes.items():

                archivo.write(f"{k},{v['monto']},{v['tipo']}\n")

        mostrar_exito(f"Cliente: {nombre} , eliminado con éxito!")

    else:

        mostrar_error("El cliente solicitado no existe o ya fue eliminado.")
   
######### Funciones Calculos
    
def calcular_monto_efectivo():
    cant_monto_efectivo = 0
    
    for _,datos in clientes.items():
              if datos['tipo'] == "Efectivo":
            
                cant_monto_efectivo = cant_monto_efectivo + datos['monto']           
    
    print(Fore.BLACK + Back.WHITE + f"Monto total de efectivo = {cant_monto_efectivo}" + Fore.RESET + Back.RESET + "\n")
    return cant_monto_efectivo
   
def calcular_monto_tranferencia():
    cant_monto_transferencia = 0

    for _,datos in clientes.items():
              if datos['tipo'] == "Transferencia":
            
                cant_monto_transferencia = cant_monto_transferencia + datos['monto']           
    
    print(Fore.BLACK + Back.WHITE + f"Monto total de tranferencias = {cant_monto_transferencia}" + Fore.RESET + Back.RESET + "\n")
    return cant_monto_transferencia

def calcular_monto_fiados():
    cant_monto_fiado = 0
    for _,datos in clientes.items():
    
        if datos['tipo'] == "Fiado":
                cant_monto_fiado = cant_monto_fiado + datos['monto']           
    
    print(Fore.BLACK + Back.WHITE + f"Monto total de fiados = {cant_monto_fiado}" + Fore.RESET + Back.RESET + "\n")
    return cant_monto_fiado

def calcular_monto_telekino():        
    cant_monto_telekino = 0
    for _,datos in clientes.items():
        
            if datos['tipo'] == "Telekino":
              
                  cant_monto_telekino = cant_monto_telekino + datos['monto']           
      
    print(Fore.BLACK + Back.WHITE + f"Monto total de telekinos = {cant_monto_telekino}" + Fore.RESET + Back.RESET + "\n")
    return cant_monto_telekino

def calcular_monto_egresos():        
      cant_monto_egresos = 0
      for _,datos in clientes.items():          
        if datos['tipo'] == "Egresos":          
            cant_monto_egresos = cant_monto_egresos + datos['monto']           
      
      print(Fore.BLACK + Back.WHITE + f"Monto total de egresos = {cant_monto_egresos}" + Fore.RESET + Back.RESET + "\n")
      return cant_monto_egresos
               
def calcular_montos():
    total = 0
    while True:
        opcionP = questionary.select("Seleccione monto a calcular...",
        choices = [                              
            "Efectivo",
            "Tranferencia",
            "Fiado",
            "Telekino",
            "Egresos",
            "Total"
        ]).ask()
        
        if opcionP == "Efectivo":
             calcular_monto_efectivo()        
        elif opcionP == "Tranferencia":
             calcular_monto_tranferencia()
        elif opcionP == "Fiado":
             calcular_monto_fiados()
        elif opcionP == "Egresos":
             calcular_monto_egresos()
        elif opcionP == "Telekino":
             calcular_monto_telekino()                  
        elif opcionP == "Total":
            total = calcular_monto_efectivo() + calcular_monto_tranferencia() - calcular_monto_fiados() + calcular_monto_telekino() - calcular_monto_egresos() 
            mostrar_exito(f"Cierre de caja total : ",{total})
        break

# Menú   
cargar_datos()

print(Fore.BLACK + Back.GREEN + "Programa Gestion Quiniela" + Fore.RESET + Back.RESET + "\n")

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








