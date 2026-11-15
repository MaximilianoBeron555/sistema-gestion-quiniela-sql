# Módulos
from colorama import Fore, Back, init
init()

clientes = {}

# --- Funciones Auxiliares para evitar repetición de código ---

def mostrar_exito(mensaje):

    print(Fore.BLACK + Back.GREEN + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")

def mostrar_error(mensaje):

    print(Fore.BLACK + Back.RED + f"\n {mensaje} " + Fore.RESET + Back.RESET + "\n")

def solicitar_entero(mensaje_input, mensaje_error="Error: Debe ingresar un número entero."):

    """Valida que el dato ingresado sea estrictamente numérico."""

    while True:

        try:

            return int(input(mensaje_input).strip())

        except ValueError:

            mostrar_error(mensaje_error)

# --- Funciones Principales ---

def cargar_datos():

    try:

        with open("clientes.txt", "r") as archivo:

            for linea in archivo:

                linea = linea.strip()

                if not linea:  # Salta líneas vacías

                    continue

                datos = linea.split(",")

                if len(datos) == 4:

                    dni = datos[0]  # Ahora el DNI es la clave principal

                    clientes[dni] = {

                        "nombre": datos[1],

                        "apellido": datos[2],

                        "telefono": datos[3]  # Se mantiene como texto por consistencia

                    }

    except FileNotFoundError:

        # Si el archivo no existe, no hace falta lanzar error, se creará al agregar un cliente

        pass  

def agregar():

    print("\n Iniciando agregado de cliente... \n")   

    

    # Validamos el DNI primero para ver si ya existe

    dni = input("DNI (sin puntos): ").strip()

    while not dni.isdigit():

        mostrar_error("El DNI debe contener solo números.")

        dni = input("DNI (sin puntos): ").strip()

        

    if dni in clientes:

        mostrar_error("Error: Ya existe un cliente registrado con ese DNI.")

        return



    nombre = input("Nombre: ").strip()

    apellido = input("Apellido: ").strip()

    

    # Validación del teléfono

    telefono = input("Teléfono: ").strip()

    while not telefono.isdigit():

        mostrar_error("El teléfono debe contener solo números.")

        telefono = input("Teléfono: ").strip()

        

    # Guardamos en memoria usando el DNI como clave

    clientes[dni] = {"nombre": nombre, "apellido": apellido, "telefono": telefono}

    

    # Persistencia en archivo

    with open("clientes.txt", "a") as archivo:

        archivo.write(f"{dni},{nombre},{apellido},{telefono}\n")

         

    mostrar_exito("Cliente Incorporado")

def mostrar():

    if not clientes:

        mostrar_error("No se registran clientes en la lista.")

        return



    print(Fore.BLACK + Back.WHITE + "Lista de clientes incorporados en el sistema" + Fore.RESET + Back.RESET + "\n")

    for dni, datos in clientes.items():

        print(f" DNI: {dni}")

        print(f" Nombre: {datos['nombre']}")

        print(f" Apellido: {datos['apellido']}")

        print(f" Teléfono: {datos['telefono']} \n")

def buscar():

    dni = input("Ingrese el DNI del cliente que desea Buscar: ").strip()

    print("\n Iniciando búsqueda... \n")

    

    # Se busca directamente en memoria, optimizando el proceso

    if dni in clientes:

        cliente = clientes[dni]

        mostrar_exito(f"El cliente con DNI {dni} fue encontrado con éxito!")

        print(f" Nombre: {cliente['nombre']}")

        print(f" Apellido: {cliente['apellido']}")

        print(f" Teléfono: {cliente['telefono']} \n")

    else:

        mostrar_error("El cliente solicitado no se encuentra en la lista.")

def calcular_cantidad():

    print("Calculando cantidad total... \n")

    cant_clientes = len(clientes)

    # Corregido: Ya no hace 'return print()', solo imprime en pantalla

    print(Fore.BLACK + Back.WHITE + f"Cantidad total de clientes actual = {cant_clientes}" + Fore.RESET + Back.RESET + "\n")

def eliminar():

    dni = input("Ingrese el DNI del cliente que desea eliminar: ").strip()

    print("\n Iniciando proceso de eliminación... \n")



    if dni in clientes:

        clientes.pop(dni)

        # Reescritura del archivo con los datos actualizados de memoria

        with open("clientes.txt", "w") as archivo:

            for k, v in clientes.items():

                archivo.write(f"{k},{v['nombre']},{v['apellido']},{v['telefono']}\n")

        mostrar_exito(f"Cliente con DNI {dni} eliminado con éxito!")

    else:

        mostrar_error("El cliente solicitado no existe.")
   
# Menú   
cargar_datos()

print(Fore.BLACK + Back.GREEN + "Programa Proyecto Txt - Clientes de Quiniela" + Fore.RESET + Back.RESET + "\n")

while True:
    print("Opciones:")
    print(" 1: Agregar cliente nuevo")
    print(" 2: Mostrar lista")
    print(" 3: Buscar cliente")
    print(" 4: Cantidad total de clientes")
    print(" 5: Eliminar cliente")
    print(" 6: Finalizar Programa")

    opcion = solicitar_entero("Seleccione una opción: ", "Por favor, ingrese un número entero válido.")
    
    if opcion == 1:
        agregar()
    elif opcion == 2:
        mostrar()
    elif opcion == 3:
        buscar()
    elif opcion == 4:
        calcular_cantidad()
    elif opcion == 5: 
        eliminar()
    elif opcion == 6:
        print(Fore.BLUE + Back.BLACK + "\nPrograma Finalizado. \n" + Fore.RESET + Back.RESET)
        break    
    else:
        mostrar_error("Opción inválida. Por favor, elija un número del 1 al 6.")