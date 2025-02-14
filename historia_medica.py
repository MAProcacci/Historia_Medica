from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import customtkinter as ctk
from customtkinter import *

from PIL import Image, ImageTk

from libreria import *
from paciente.gui import Frame

# Establecer el modo de apariencia como Modo Oscuro y el Tema al modo predeterminado.
ctk.set_appearance_mode("Dark") # Modo del tema Sistema ("System"(default), "Light", "Dark")
ctk.set_default_color_theme("blue") # Tema por defecto ("blue"(default), "dark-blue", "green")


# Funcion principal
def main():
    root = ctk.CTk()
    #root.geometry("1100x650+340+170")
    root.title("Historia Medica")
    root.resizable(False, False)

    frame = Frame(root)
    #frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
         