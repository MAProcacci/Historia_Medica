from datetime import datetime
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import re
from tkcalendar import Calendar, DateEntry
from tkinter import Toplevel, Button
from tkinter import messagebox

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

import qrcode


# Colores
COLOR_FONDO = "#2f343f" # "#007e8f"
COLOR_BOTON = "#4d636f"
COLOR_BOTON_ACTIVO = "#18232b"  # "#2E86C1"  "#3b4a51"
COLOR_BG_LISTAS = "#b5b7c7"  #"#2E86C1"
COLOR_BG_VENTANA_EMERGENTE = "#50b9e6"  # "#e68a22"
COLOR_BT_SALIR = "black"
COLOR_BT_SALIR_ACTIVO = "#3b3939"

# Nombre de la Base de Datos
DB_NAME = "db_historia_medica.db"

class SnackBar:
    """
    Clase para mostrar un SnackBar con un mensaje.
    Atributos:
        root (Tk): Ventana principal de la interfaz de usuario.

    NOTA: Modo de uso:
        snackbar = SnackBar(root)
        snackbar.show("Mensaje de ejemplo")

    NOTA: Personalizar colores:
        snackbar = SnackBar(root)
        snackbar.show("Mensaje de ejemplo", bg_color="red", fg_color="white")

    NOTA: Personalizar duración:
        snackbar = SnackBar(root)
        snackbar.show("Mensaje de ejemplo", duration=5000) # 5000 milisegundos = 5 segundos / por defecto 3 segundos.
    """
    def __init__(self, root):
        self.root = root
        self.snackbar_window = None

    def show(self, message, duration=3000, bg_color="green", fg_color="white"):
        """Muestra un SnackBar con un mensaje."""
        if self.snackbar_window:
            self.snackbar_window.destroy()

        # Crear una ventana Toplevel
        self.snackbar_window = tk.Toplevel(self.root)
        self.snackbar_window.overrideredirect(True)  # Eliminar la barra de título

        # Obtener las dimensiones de la pantalla
        screen_width = self.snackbar_window.winfo_screenwidth()
        screen_height = self.snackbar_window.winfo_screenheight()

        # Obtener las dimensiones del SnackBar
        self.snackbar_window.update_idletasks()  # Actualizar las dimensiones de la ventana
        snackbar_width = self.snackbar_window.winfo_width()
        snackbar_height = self.snackbar_window.winfo_height()

        # Calcular la posición central
        x = (screen_width // 2) - (snackbar_width // 2)
        y = (screen_height // 2) - (snackbar_height // 2)

        # Posicionar el SnackBar en el centro de la pantalla
        self.snackbar_window.geometry(f"+{x}+{y}")

        # Configurar el fondo y el mensaje
        self.snackbar_window.config(bg=bg_color)
        label = tk.Label(
            self.snackbar_window, text=message, bg=bg_color, fg=fg_color, font=("Arial", 12,"bold")
        )
        label.pack(padx=20, pady=10)

        # Cerrar la ventana después de un tiempo
        self.snackbar_window.after(duration, self.snackbar_window.destroy)

    def mostrar_snackbar(self, mensaje):
        """Muestra un SnackBar con un mensaje."""
        self.show(mensaje, duration=3000, bg_color="green", fg_color="white")  # Personalizar colores

def registrar_error(mensaje, nivel="ERROR"):
    """
    Registra un mensaje de error en un archivo de log.

    :param mensaje: El mensaje de error a registrar.
    :param nivel: El nivel de gravedad (INFO, WARNING, ERROR).

    NOTA: Modo de uso:
        registrar_error("Mensaje de error", "ERROR")
    """
    try:
        # Nombre de la carpeta de logs (relativa al directorio de trabajo actual)
        log_folder = os.path.join(os.getcwd(), "logs")
        # Crear la carpeta si no existe
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        
        # Ruta completa del archivo de log (relativa al directorio de trabajo actual)
        log_file = os.path.join(log_folder, "errores.log")
        
        # Obtener la fecha y hora actual
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formatear el mensaje con la fecha y hora
        log_message = f"[{timestamp}] [{nivel}] {mensaje}\n"
        
        # Abrir el archivo en modo de anexar (append)
        with open(log_file, "a") as file:
            file.write(log_message)
    except Exception as e:
        #print(f"Error al escribir en el archivo de log: {e}")
        messagebox.showerror("Registrar_Error - Error", f"Error al escribir en el archivo de log: {e}")        

def validar_correo(correo):
    """
    Valida si un correo electrónico tiene un formato válido.

    :param correo: El correo electrónico a validar.
    :return: True si el correo es válido, False en caso contrario.

    NOTA: Modo de uso:
        validar_correo(correo):            
    """
    # Expresión regular para validar un correo electrónico
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, correo) is not None

def sort_column(treeview, col):
    """
    Función para ordenar la columna de un Treeview cuando se hace clic en el encabezado
    :param treeview: El Treeview del cual se quiere ordenar la columna.
    :param col: La columna a ordenar.
    :return: None

    NOTA: Modo de uso:
        sort_column(treeview, col)
    """
    # Obtener los datos actuales del Treeview
    data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    
    # Intentar convertir a número si es posible, de lo contrario mantener como cadena
    try:
        # Para columnas numéricas como 'ID'
        if col == "ID":
            data = [(int(item[0]), item[1]) for item in data]
        else:
            # Intentar convertir otros campos a float si son numéricos
            data = [(float(item[0]), item[1]) for item in data]
    except ValueError:
        # Si no se puede convertir, mantener como cadena (orden alfabético)
        pass
        
    # Alternar entre ascendente y descendente
    if hasattr(treeview, 'ascending'):
        treeview.ascending = not treeview.ascending
    else:
        treeview.ascending = True
        
    # Ordenar los datos
    data.sort(reverse=not treeview.ascending)
        
    # Reorganizar las filas en el Treeview
    for index, (val, child) in enumerate(data):
        treeview.move(child, '', index)

def cargar_image_icono(file_path):
    """Carga una imagen desde un archivo y la muestra en un icono.

    :param file_path: La ruta del archivo de imagen.
    :return: Una imagen en formato PhotoImage.

    NOTA: Modo de uso:
        image_tk = cargar_image_icono(file_path)
    """
    img_folder = "Imagenes"

    if file_path:
        image = Image.open(file_path)
        image = image.resize((72, 72), Image.LANCZOS)
        image_name = os.path.basename(file_path)
        image_save_path = os.path.join(img_folder, image_name)
        image.save(image_save_path)
            
        image_tk = ImageTk.PhotoImage(image)
            
        return image_tk

def seleccionar_fecha(root, titulo="Seleccionar Fecha"):
    """
    Abre un calendario para que el usuario seleccione una fecha.
    
    :param root: La ventana principal o frame desde donde se llama la función.
    :param titulo: El título de la ventana emergente del calendario.
    :return: La fecha seleccionada en formato 'YYYY-MM-DD' o None si no se selecciona ninguna fecha.
    
    NOTA: Modo de uso:
        fecha_seleccionada = seleccionar_fecha(root)
    """
    def on_seleccionar():
        """
        Función para confirmar la selección de una fecha.
        
        :return: None
        """
        fecha_seleccionada.set(cal.get_date())
        top.destroy()

    fecha_seleccionada = tk.StringVar()

    # Crear una ventana emergente
    top = ctk.CTkToplevel(root)
    top.title(titulo)
    top.geometry("300x300+500+200")
    top.resizable(False, False)
    top.transient(root)
    top.grab_set()

    # Crear el widget de calendario
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', cursor='hand2')
    cal.pack(pady=20)

    # Botón para confirmar la selección
    btn_seleccionar = ctk.CTkButton(top, text="Seleccionar", command=on_seleccionar)
    btn_seleccionar.pack(pady=10)

    # Esperar a que la ventana se cierre
    top.wait_window(top)

    return fecha_seleccionada.get()

def validar_fechas(fecha_inicial_str, fecha_final_str):
    """
    Valida que la fecha final no sea menor que la fecha inicial y que la fecha inicial no sea mayor que la fecha actual.
    
    Parámetros:
        fecha_inicial_str (str): Fecha inicial en formato "YYYY-MM-DD".
        fecha_final_str (str): Fecha final en formato "YYYY-MM-DD".
    
    Retorna:
        bool: True si las fechas son válidas, False si no lo son.
    
    NOTA: Modo de uso:
        validacion = validar_fechas(fecha_inicial_str, fecha_final_str)
    """
    # Validar que si se dejo en blanco, se coloque por defecto la fecha 01-01-1900 y la fecha 01-01-2200
    if fecha_inicial_str == "" :
        fecha_inicial_str = "01-01-1900"
    if fecha_final_str == "" :
        fecha_final_str = "01-01-2200"

    try:
        # Convertir las fechas de cadena a objetos datetime
        fecha_inicial = datetime.strptime(fecha_inicial_str, "%m-%d-%Y").strftime("%Y-%m-%d")
        fecha_final = datetime.strptime(fecha_final_str, "%m-%d-%Y").strftime("%Y-%m-%d")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Validar que la fecha inicial no sea mayor que la fecha actual
        if fecha_inicial > fecha_actual:
            messagebox.showerror("Validar_Fechas - Error de Fecha", "La fecha inicial no puede ser mayor que la fecha actual.")
            return False

        # Validar que la fecha final no sea menor que la fecha inicial
        if fecha_final < fecha_inicial:
            messagebox.showerror("Validar_Fechas - Error de Fecha", "La fecha final no puede ser menor que la fecha inicial.")
            return False

        # Si todo está bien, retornar True
        return True

    except ValueError as e:
        messagebox.showerror("Validar_Fechas - Error de Formato", f"Formato de fecha inválido: {e}")
        return False

def confirmar_eliminacion(root):
    """Muestra un cuadro de diálogo personalizado para confirmar la eliminación.
    
    :param root: La ventana principal o frame desde donde se llama la función.
    :return: True si se confirma la eliminación, False si se cancela.
    
    NOTA: Modo de uso:
        confirmacion = confirmar_eliminacion(root)
    """
    # Crear una ventana emergente
    ventana_confirmacion = ctk.CTkToplevel(root)
    ventana_confirmacion.title("Confirmar Eliminación")
    ventana_confirmacion.geometry("310x150")
    ventana_confirmacion.resizable(False, False)
    ventana_confirmacion.transient(root)  # Hace que la ventana sea modal
    ventana_confirmacion.grab_set()  # Bloquea la ventana principal

    # Etiqueta de confirmación
    lbl_mensaje = ctk.CTkLabel(ventana_confirmacion, text="¿Estás seguro de continuar con la eliminación?")
    lbl_mensaje.pack(pady=20)

    # Función para manejar la respuesta del usuario
    def on_confirmar(confirmado):
        nonlocal respuesta
        respuesta = confirmado
        ventana_confirmacion.destroy()

    # Botones de confirmación
    frame_botones = ctk.CTkFrame(ventana_confirmacion)
    frame_botones.pack(pady=10)

    btn_si = ctk.CTkButton(frame_botones, text="Sí", command=lambda: on_confirmar(True), width=100)
    btn_si.pack(side="left", padx=10)

    btn_no = ctk.CTkButton(frame_botones, text="No", command=lambda: on_confirmar(False), width=100)
    btn_no.pack(side="right", padx=10)

    # Variable para almacenar la respuesta
    respuesta = False

    # Esperar a que la ventana se cierre
    ventana_confirmacion.wait_window(ventana_confirmacion)

    return respuesta

def generador_de_qr(objeto):
    """
    Genera un código QR basado en el objeto proporcionado.
    
    :param objeto: El objeto a incluir en el código QR.
    :return: La imagen del código QR generada.
    
    NOTA: Modo de uso:
        qr_code = generador_de_qr(objeto)
    """
    # Definir el objeto a incluir en el código QR
    objeto = str(objeto)

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2)

    # Agregar el objeto al código QR
    qr.add_data(objeto)
    qr.make(fit=True)

    # Crear la imagen del código QR
    img = qr.make_image(fill_color="black", back_color="white")
    #img.save("qr_code.png")
    return img

def enviar_correo(remitente, password_remitente, destinatario, asunto, cuerpo, adjuntos=None):
    """
    Envia un correo electrónico a un destinatario con un asunto y cuerpo determinados.
    
    :param remitente: La dirección de correo electrónico del remitente.
    :param password_remitente: La contraseña de la cuenta de correo electrónico del remitente.    
    :param destinatario: La dirección de correo electrónico del destinatario.
    :param asunto: El asunto del correo electrónico.
    :param cuerpo: El cuerpo del correo electrónico.
    :param adjuntos: Una lista de rutas de archivos adjuntos.
    :return: None
    
    NOTA: Modo de uso:
        enviar_correo(remitente, password_remitente, destinatario, asunto, cuerpo, adjuntos)
    """
    # Configurar el servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Iniciar sesión en la cuenta de correo electrónico
    server.login(remitente, password_remitente)

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = remitente
    message['To'] = destinatario
    message['Subject'] = asunto

    # Agregar el cuerpo del mensaje
    message.attach(MIMEText(cuerpo, 'plain'))

    # Agregar adjuntos (opcional)
    if adjuntos:
        for archivo in adjuntos:
            with open(archivo, 'rb') as f:
                msg = MIMEImage(f.read())
            message.attach(msg)

    # Enviar el mensaje
    server.sendmail(remitente, destinatario, message.as_string())

    # Cerrar la conexión SMTP
    server.quit()