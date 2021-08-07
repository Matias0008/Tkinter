from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import tkinter

root = Tk()
root.title("Gestor de clientes")
root.resizable(0, 0)

conexion = sqlite3.connect("crm.db")
c = conexion.cursor()

c.execute("""
    CREATE TABLE if not exists clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL
    );
""")

def render_clientes():
    rows = c.execute("SELECT * FROM clientes").fetchall()
    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert("", END, row[0], values=(row[1], row[2], row[3]))

def insertar(cliente):
    c.execute("""
        INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)
    """, (cliente["nombre"], cliente["telefono"], cliente["correo"]))
    conexion.commit()
    render_clientes()


def nuevo_cliente():
    def guardar():
        if not nombre_e.get():
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return

        if not telefono_e.get():
            messagebox.showerror("Error", "El teléfono es obligatorio.")
            return

        if not correo_e.get():
            messagebox.showerror("Error", "El correo es obligatorio.")
            return

        cliente = {
            "nombre": nombre_e.get(),
            "telefono": telefono_e.get(),
            "correo": correo_e.get()
        }
        insertar(cliente)
        top.wm_attributes("-topmost", True)
        top.destroy()

    top = Toplevel()
    top.title("Nuevo cliente")


    l_nombre = Label(top, text="Nombre")
    nombre_e = Entry(top, width=40)
    l_nombre.grid(row=0, column=0, pady=5)
    nombre_e.grid(row=0, column=1, pady=5, padx=5)

    l_telefono = Label(top, text="Teléfono")
    telefono_e = Entry(top, width=40)
    l_telefono.grid(row=1, column=0, pady=5, padx=5)
    telefono_e.grid(row=1, column=1, pady=5)

    l_correo = Label(top, text="Correo")
    correo_e = Entry(top, width=40)
    l_correo.grid(row=2, column=0, pady=5, padx=5)
    correo_e.grid(row=2, column=1, pady=5)

    btn_guardar = Button(top, text="Guardar", width=10, command=guardar)
    btn_guardar.grid(row=3, column=1, pady=5)



    top.mainloop()
def eliminar_cliente():
    id = tree.selection()[0]
    cliente = c.execute("SELECT * FROM clientes WHERE ID = ?", (id, )).fetchone()

    respuesta = messagebox.askokcancel("Seguro", f"¿Estás seguro de querer eliminar el cliente {cliente[1]}?")
    if respuesta:
        c.execute("DELETE FROM clientes WHERE ID = ?", (id, ))
        conexion.commit()
        render_clientes()
    else:
        pass

# Creando botones
btn_agregar = Button(root, text="Nuevo Cliente", command=nuevo_cliente)
btn_agregar.grid(row=0, column=0, pady=5)

btn_eliminar = Button(root, text="Eliminar Cliente", command=eliminar_cliente)
btn_eliminar.grid(row=0, column=1, pady=5)

# Creando Treeview
tree = ttk.Treeview(root)
tree["columns"] = ("Nombre", "Telefono", "Correo")
tree.grid(column=0, row=1, columnspan=2, pady=5)

tree.column("#0", width=0, stretch=NO)
tree.column("Nombre")
tree.column("Telefono")
tree.column("Correo")

# Heading
tree.heading("Nombre", text="Nombre")
tree.heading("Telefono", text="Teléfono")
tree.heading("Correo", text="Correo")



render_clientes()
root.mainloop()