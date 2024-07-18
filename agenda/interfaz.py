import tkinter as tk
from tkinter import messagebox, simpledialog
from funciones import *

class AgendaContactos:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos")
        self.create_widgets()

    def create_widgets(self):
        # botones del menussss creadosss
        btn_nuevo = tk.Button(self.root, text="Ingresar un contacto nuevo", command=self.nuevo_contacto)
        btn_nuevo.pack(pady=10)

        btn_modificar = tk.Button(self.root, text="Modificar un contacto", command=self.modificar_contacto)
        btn_modificar.pack(pady=10)

        btn_eliminar = tk.Button(self.root, text="Eliminar un contacto", command=self.eliminar_contacto)
        btn_eliminar.pack(pady=10)

        btn_listar = tk.Button(self.root, text="Listar los contactos", command=self.listar_contactos)
        btn_listar.pack(pady=10)

        btn_salir = tk.Button(self.root, text="Salir", command=self.root.quit)
        btn_salir.pack(pady=10)

    def nuevo_contacto(self):
        datos = self.nuevo_contacto_dialog()
        if datos:
            insertar = mycol.insert_one(datos)
            messagebox.showinfo("Contacto agregado", "Contacto agregado exitosamente")

    def modificar_contacto(self):
        busqueda = simpledialog.askstring("Modificar Contacto", "Ingrese el número telefónico del contacto que desea modificar:")
        if busqueda:
            try:
                busqueda = int(busqueda)
                consulta = {"datos_contacto.telefono": busqueda}
                documento = mycol.find_one(consulta)
                if documento:
                    nuevos_datos = self.nuevo_contacto_dialog()
                    if nuevos_datos:
                        mycol.update_one(consulta, {"$set": nuevos_datos})
                        messagebox.showinfo("Contacto actualizado", "Contacto actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "Documento no encontrado")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número de teléfono válido")

    def eliminar_contacto(self):
        busqueda = simpledialog.askstring("Eliminar Contacto", "Ingrese el número telefónico del contacto que desea eliminar:")
        if busqueda:
            try:
                busqueda = int(busqueda)
                consulta = {"datos_contacto.telefono": busqueda}
                documento = mycol.find_one(consulta)
                if documento:
                    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el contacto?")
                    if respuesta:
                        mycol.delete_one(consulta)
                        messagebox.showinfo("Contacto eliminado", "Contacto eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "Documento no encontrado")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número de teléfono válido")

    def listar_contactos(self):
        contactos = mycol.find().sort("favorito", pymongo.DESCENDING)
        lista = tk.Toplevel(self.root)
        lista.title("Lista de Contactos")
        text = tk.Text(lista)
        text.pack()
        for contacto in contactos:
            text.insert(tk.END, f"Nombre: {contacto['nombre']}\n")
            text.insert(tk.END, f"Edad: {contacto['edad']}\n")
            text.insert(tk.END, f"Categoría: {contacto['datos_contacto']['categoria']}\n")
            text.insert(tk.END, f"Dirección: {contacto['datos_contacto']['direccion']}\n")
            text.insert(tk.END, f"Teléfono: {contacto['datos_contacto']['telefono']}\n")
            text.insert(tk.END, f"Favorito: {'Sí' if contacto['favorito'] else 'No'}\n\n")
        text.config(state=tk.DISABLED)

    def nuevo_contacto_dialog(self):
        datos = {}

        datos['nombre'] = simpledialog.askstring("Nuevo Contacto", "Ingrese el nombre:")
        if not datos['nombre']:
            return None

        while True:
            try:
                datos['edad'] = int(simpledialog.askstring("Nuevo Contacto", "Ingrese la edad:"))
                if datos['edad'] < 1:
                    messagebox.showerror("Error", "Ingrese una edad válida")
                    continue
                break
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Ingrese una edad válida")
                return None

        while True:
            datos_contacto = {}
            categoria = simpledialog.askstring("Nuevo Contacto", "Ingrese categoría (trabajo, comercial o particular):").lower()
            if categoria not in ["trabajo", "comercial", "particular"]:
                messagebox.showerror("Error", "Categoría no válida. Intente de nuevo.")
                continue
            datos_contacto['categoria'] = categoria
            break

        datos_contacto['direccion'] = simpledialog.askstring("Nuevo Contacto", "Ingrese la dirección:")
        if not datos_contacto['direccion']:
            return None

        while True:
            try:
                telefono = int(simpledialog.askstring("Nuevo Contacto", "Ingrese su número telefónico de 9 dígitos:"))
                telefono_str = str(telefono)
                if telefono_str.isdigit() and len(telefono_str) == 9:
                    datos_contacto['telefono'] = telefono
                    break
                else:
                    messagebox.showerror("Error", "Ingrese un número de teléfono válido (9 dígitos)")
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Ingrese un número de teléfono válido (9 dígitos)")
                return None

        datos['datos_contacto'] = datos_contacto

        favorito = simpledialog.askstring("Nuevo Contacto", "¿Es favorito? (s/n):").lower()
        datos['favorito'] = favorito == 's'

        return datos

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaContactos(root)
    root.mainloop()

#python interfaz.py