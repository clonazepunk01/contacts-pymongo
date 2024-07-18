import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["agenda"]
mycol = mydb["contactos"]

# personas que vienen por defaulttttt
personas = [
    {
        "nombre": "Gustavo",
        "edad": 23,
        "datos_contacto": {
            "categoria": "personal",
            "direccion": "Villa Angachilla, Pasaje 2, 158",
            "telefono": 941727291
        },
        "favorito": True
    },
    {
        "nombre": "Marco",
        "edad": 19,
        "datos_contacto": {
            "categoria": "comercial",
            "direccion": "San José",
            "telefono": 912345678
        },
        "favorito": False
    },
    {
        "nombre": "Luis",
        "edad": 20,
        "datos_contacto": {
            "categoria": "trabajo",
            "direccion": "San José",
            "telefono": 912345678
        },
        "favorito": False
    }
]

# borrar colecc existente y agregar datos iniciales
mycol.drop()
x = mycol.insert_many(personas)

def nuevo_contacto():
    nombre = input("Ingrese nombre: ")
    while True:
        try:
            edad = int(input("Ingrese edad: "))
            if edad < 1:
                print("Ingrese una edad válida")
                continue
            break
        except ValueError:
            print("Ingrese una edad válida")
    
    while True:
        categoria = input("Ingrese categoría (trabajo, comercial o particular): ").lower()
        if categoria not in ["trabajo", "comercial", "particular"]:
            print("Categoría no válida. Intente de nuevo.")
        else:
            break
    
    direccion = input("Ingrese la dirección: ")
    
    while True:
        try:
            telefono = int(input("Ingrese su número telefónico de 9 dígitos: "))
            telefono_str = str(telefono)
            if telefono_str.isdigit() and len(telefono_str) == 9:
                break
            else:
                print("Ingrese un número de teléfono válido (9 dígitos)")
        except ValueError:
            print("Ingrese un número de teléfono válido (9 dígitos)")
    
    while True:
        fav = input("¿Es favorito? (s/n): ").lower()
        if fav not in ["s", "n"]:
            print("Ingrese una opción válida (s/n).")
        else:
            break
    
    favorito = (fav == "s")
    
    return {
        "nombre": nombre,
        "edad": edad,
        "datos_contacto": {
            "categoria": categoria,
            "direccion": direccion,
            "telefono": telefono
        },
        "favorito": favorito
    }

def modificar_contacto():
    busqueda = int(input("Ingrese el número telefónico del contacto que desea modificar: "))
    consulta = {"datos_contacto.telefono": busqueda}
    documento = mycol.find_one(consulta)
    if documento:
        print("Contacto encontrado: ", documento)
        nuevos_datos = {"$set": nuevo_contacto()}
        mycol.update_one(consulta, nuevos_datos)
        print("Contacto actualizado!")
    else:
        print("Documento no encontrado")

def eliminar_contacto():
    busqueda = int(input("Ingrese el número telefónico del contacto que desea eliminar: "))
    consulta = {"datos_contacto.telefono": busqueda}
    documento = mycol.find_one(consulta)
    if documento:
        print("Contacto encontrado: ", documento)
        while True:
            eliminar = input("¿Desea eliminar el contacto? (s/n): ").lower()
            if eliminar not in ["s", "n"]:
                print("Ingrese una opción válida (s/n)")
            else:
                break
        if eliminar == "s":
            mycol.delete_one(consulta)
            print("Contacto eliminado exitosamente")
        else:
            print("Se ha cancelado la eliminación")
    else:
        print("Documento no encontrado")

def listar_contactos():
    mydoc = mycol.find().sort("favorito", pymongo.DESCENDING)
    for x in mydoc:
        print(x)



    




