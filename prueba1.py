import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3

# Database setup
conn = sqlite3.connect(':memory:')  # Use ':memory:' for testing; replace with a file for persistence
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mesas (
        id INTEGER PRIMARY KEY,
        capacidad INTEGER,
        estatus TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ordenes (
        id INTEGER PRIMARY KEY,
        mesa_id INTEGER,
        estado TEXT,
        total REAL,
        FOREIGN KEY (mesa_id) REFERENCES Mesas(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Menu (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        tipo TEXT,
        precio REAL
    )
''')

# Insert sample data
cursor.executemany('INSERT INTO Mesas (id, capacidad, estatus) VALUES (?, ?, ?)', [
    (1, 4, 'Libre'), (2, 6, 'Ocupada'), (3, 4, 'Libre')
])

cursor.executemany('INSERT INTO Menu (nombre, tipo, precio) VALUES (?, ?, ?)', [
    ('Pizza', 'Comida', 15.99), ('Agua', 'Bebida', 1.99), ('Hamburguesa', 'Comida', 12.99)
])

conn.commit()

# GUI Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Restaurante")
        self.geometry("800x600")

        # Tab control
        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.tab_mesas = ctk.CTkFrame(self.tab_control)
        self.tab_cajero = ctk.CTkFrame(self.tab_control)
        self.tab_cocina = ctk.CTkFrame(self.tab_control)
        self.tab_admin = ctk.CTkFrame(self.tab_control)
        self.tab_menu = ctk.CTkFrame(self.tab_control)

        self.tab_control.add(self.tab_mesas, text='Mesas')
        self.tab_control.add(self.tab_cajero, text='Cajero')
        self.tab_control.add(self.tab_cocina, text='Cocina')
        self.tab_control.add(self.tab_admin, text='Administrador')
        self.tab_control.add(self.tab_menu, text='Menú')

        self.tab_control.pack(expand=1, fill="both")

        # Initialize tabs
        self.init_tab_mesas()
        self.init_tab_cajero()
        self.init_tab_cocina()
        self.init_tab_admin()
        self.init_tab_menu()

    def init_tab_mesas(self):
        label = ctk.CTkLabel(self.tab_mesas, text="Vista de Mesas")
        label.pack(pady=10)

        # Display mesas
        self.display_mesas()

    def display_mesas(self):
        cursor.execute('SELECT * FROM Mesas')
        mesas = cursor.fetchall()

        for mesa in mesas:
            mesa_frame = ctk.CTkFrame(self.tab_mesas)
            mesa_frame.pack(pady=5, padx=10, fill="x")

            mesa_label = ctk.CTkLabel(mesa_frame, text=f"Mesa {mesa[0]} - Capacidad: {mesa[1]} - Estado: {mesa[2]}")
            mesa_label.pack(side="left", padx=10)

            if mesa[2] == "Libre":
                asignar_button = ctk.CTkButton(mesa_frame, text="Asignar", command=lambda m=mesa: self.asignar_mesa(m))
                asignar_button.pack(side="right", padx=10)

    def asignar_mesa(self, mesa):
        cursor.execute('UPDATE Mesas SET estatus = ? WHERE id = ?', ('Ocupada', mesa[0]))
        conn.commit()
        self.refresh_tab_mesas()

    def refresh_tab_mesas(self):
        for widget in self.tab_mesas.winfo_children():
            widget.destroy()
        self.init_tab_mesas()

    def init_tab_cajero(self):
        label = ctk.CTkLabel(self.tab_cajero, text="Vista del Cajero")
        label.pack(pady=10)

    def init_tab_cocina(self):
        label = ctk.CTkLabel(self.tab_cocina, text="Vista de la Cocina")
        label.pack(pady=10)

    def init_tab_admin(self):
        label = ctk.CTkLabel(self.tab_admin, text="Vista del Administrador")
        label.pack(pady=10)

    def init_tab_menu(self):
        label = ctk.CTkLabel(self.tab_menu, text="Gestión del Menú")
        label.pack(pady=10)

        # Display menu items
        cursor.execute('SELECT * FROM Menu')
        menu_items = cursor.fetchall()

        for item in menu_items:
            item_frame = ctk.CTkFrame(self.tab_menu)
            item_frame.pack(pady=5, padx=10, fill="x")

            item_label = ctk.CTkLabel(item_frame, text=f"{item[1]} - {item[2]} - ${item[3]:.2f}")
            item_label.pack(side="left", padx=10)

if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()