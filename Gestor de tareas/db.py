from tkinter import *
import sqlite3

root = Tk()
root.title("Gestor de tareas")
root.resizable(0, 0)





conexion = sqlite3.connect("todo.db")
c = conexion.cursor()

c.execute("""

    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );

"""
)

conexion.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,  ))
        conexion.commit()
        render_tareas()
    return _remove

def completo(id):
    def _completo():
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id,  )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conexion.commit()
        render_tareas()
    return _completo


def render_tareas():
    rows = c.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completado = rows[i][3]
        descripcion = rows[i][2]
        color = "#555555" if completado else "#000000"
        l = Checkbutton(frame, text=descripcion, fg=color,width=69,anchor="w", pady=5 , command=completo(id))
        l.grid(row=i, column=0, sticky="w")
        l.select() if completado else l.deselect()
        btn_remove = Button(frame, text="Eliminar", command=remove(id))
        btn_remove.grid(row=i, column=1)


def addTarea():
    tarea = e.get()
    if tarea:
        c.execute("""
            INSERT INTO todo (description, completed) VALUES (?, ?)   
        """, (tarea, False))
        conexion.commit()
        e.delete(0, END)
        render_tareas()
    else:
        pass


l = Label(root, text=" Tarea ")
l.grid(row=0, column=0)
l.config(underline=True)

e = Entry(root, width=67)
e.grid(row=0, column=1)

btn = Button(root, text="Agregar", command=addTarea, padx=5, width=10)
btn.grid(row=0, column=2, pady=10, padx=5)

frame = LabelFrame(root, text="Mis tareas", padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky="nswe", padx=5, pady=5)
frame.config(relief="groove")
frame.config(bd=3)

e.focus()

root.bind("<Return>", lambda x: addTarea())
render_tareas()
root.mainloop()