from funciones import *

while True:
    print("=== Agenda de contactos ===")
    print("1. Ingresar un contacto nuevo")
    print("2. Modificar un contacto")
    print("3. Eliminar un contacto")
    print("4. Listar los contactos")
    print("5. Salir")

    while True:
        try:
            opc = int(input("Seleccione una opción: "))
            if opc < 1 or opc > 5:
                print("Ingrese una opción válida")
                continue
            break
        except ValueError:
            print("Ingrese una opción válida")

    if opc == 1:
        datos = nuevo_contacto()
        insertar = mycol.insert_one(datos)
        print("Contacto agregado exitosamente")

    elif opc == 2:
        modificar_contacto()

    elif opc == 3:
        eliminar_contacto()

    elif opc == 4:
        listar_contactos()

    elif opc == 5:
        print("Adiós :)")
        break
