from datetime import datetime
import os
import winsound
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
        font (tuple): Fuente para el mensaje (opcional, por defecto ("Arial", 12, "bold")).

    NOTA: Modo de uso:
        snackbar = SnackBar(root)
        snackbar.show("Mensaje de ejemplo", tipo="exito") # Duración por defecto: 3000 ms (3 segundos)
        snackbar.show("Mensaje de ejemplo", tipo="informacion", duration=5000) # Duración: 5000 ms (5 segundos)

    Tipos de mensaje:
        - "exito": Letras azules, fondo negro, sonido de éxito.
        - "informacion": Letras blancas, fondo negro, sonido de información.
        - "error": Letras rojas, fondo negro, sonido de error.
        - "advertencia": Letras amarillo mostaza, fondo negro, sonido de advertencia.
    """
    def __init__(self, root, font=("Arial", 14, "bold")):
        self.root = root
        self.snackbar_window = None
        self.font = font
        self.contador_label = None  # Etiqueta para mostrar el tiempo restante

        # Sonidos predeterminados (puedes cambiar las rutas a archivos .wav o .mp3)
        self.sonidos = {
            "exito": "success.wav",  # Ruta a un archivo de sonido de éxito
            "informacion": "info.wav",  # Ruta a un archivo de sonido de información
            "error": "error.wav",  # Ruta a un archivo de sonido de error
            "advertencia": "warning.wav"  # Ruta a un archivo de sonido de advertencia
        }

    def reproducir_sonido(self, tipo):
        """
        Reproduce un sonido según el tipo de mensaje.
        :param tipo: El tipo de mensaje ("exito", "informacion", "error", "advertencia").
        """
        try:
            # Obtener la ruta del sonido
            ruta_sonido = self.sonidos.get(tipo, None)
            if ruta_sonido:
                # Reproducir el sonido (Windows)
                winsound.PlaySound(ruta_sonido, winsound.SND_ASYNC)
                # Si usas playsound (multiplataforma):
                # playsound(ruta_sonido)
        except Exception as e:
            messagebox.showerror("SnackBar - Error de Sonido", f"Error al reproducir el sonido: {e}")
            registrar_error(f"SnackBar - Error al reproducir el sonido: {e}")

    def actualizar_contador(self, tiempo_restante):
        """
        Actualiza el contador de tiempo restante en la ventana del SnackBar.
        :param tiempo_restante: El tiempo restante en segundos.
        """
        if self.contador_label:
            self.contador_label.configure(text=f"Esta ventana se cerrará en {tiempo_restante} segundos...")
            if tiempo_restante > 0:
                # Programar la próxima actualización en 1 segundo (1000 ms)
                self.snackbar_window.after(1000, self.actualizar_contador, tiempo_restante - 1)

    def show(self, message, tipo="informacion", duration=3000):
        """Muestra un SnackBar con un mensaje."""
        # Validación de parámetros
        if not isinstance(message, str):
            raise ValueError("El mensaje debe ser una cadena de texto.")
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("La duración debe ser un entero mayor que 0.")
        if tipo not in ["exito", "informacion", "error", "advertencia"]:
            raise ValueError("El tipo de mensaje debe ser 'exito', 'informacion', 'error' o 'advertencia'.")

        # Definir colores según el tipo de mensaje
        colores = {
            "exito": {"fg": "cyan", "bg": "black"},
            "informacion": {"fg": "white", "bg": "black"},
            "error": {"fg": "red", "bg": "black"},
            "advertencia": {"fg": "#FFDB58", "bg": "black"}  # Amarillo mostaza
        }

        # Obtener colores según el tipo de mensaje
        fg_color = colores[tipo]["fg"]
        bg_color = colores[tipo]["bg"]

        # Cerrar la ventana existente si hay una
        if self.snackbar_window:
            self.snackbar_window.destroy()

        # Crear una ventana Toplevel
        self.snackbar_window = ctk.CTkToplevel(self.root)
        self.snackbar_window.title(f"SnackBar - {tipo.capitalize()}")
        self.snackbar_window.resizable(False, False)
        self.snackbar_window.transient(self.root)  # Colocar la ventana sobre la principal
        self.snackbar_window.grab_set()

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
        label = ctk.CTkLabel(
            self.snackbar_window, text=message, text_color=fg_color, fg_color="black", font=self.font
        )
        label.pack(padx=20, pady=10)

        # Agregar una etiqueta para mostrar el tiempo restante
        self.contador_label = ctk.CTkLabel(
            self.snackbar_window, text="", text_color="white", fg_color="black", font=("Arial", 10)
        )
        self.contador_label.pack(pady=5)

        # Iniciar el contador de tiempo restante
        tiempo_restante = duration // 1000  # Convertir milisegundos a segundos
        self.actualizar_contador(tiempo_restante)

        # Reproducir el sonido correspondiente
        self.reproducir_sonido(tipo)

        # Cerrar la ventana después de un tiempo
        self.snackbar_window.after(duration, self.snackbar_window.destroy)

    def mostrar_snackbar(self, mensaje, tipo="informacion"):
        """Muestra un SnackBar con un mensaje."""
        self.show(mensaje, tipo=tipo, duration=3000)

class Generador_Botones:
    """
    Clase para generar botones en una ventana CTkinter.
    
    Atributos:
        root (Tk): La ventana CTkinter donde se generaran los botones.
        lista_botones (list): Una lista de textos para los botones.
        nro_columnas (int): El numero de columnas en la grilla donde se generaran los botones.
        fuente (tuple): La fuente para los botones (ej: ("Arial", 14, "bold")).
        ancho (int): Ancho de los botones (opcional, por defecto 150).
        alto (int): Alto de los botones (opcional, por defecto 30).
        callback (function): Función a ejecutar al hacer clic en un botón (opcional).
    
    NOTA: Modo de uso:
        generar_botones = Generador_Botones(root, ["Botón 1", "Botón 2", "Botón 3"], 3, ("Arial", 14, "bold"))
    """
    def __init__(self, root, lista_botones, nro_columnas, fuente, ancho=150, alto=30, callback=None):
        self.root = root
        self.lista_botones = lista_botones
        self.nro_columnas = nro_columnas
        self.font = fuente
        self.ancho = ancho
        self.alto = alto
        self.callback = callback

        # Validación de parámetros
        if not isinstance(lista_botones, list):
            raise ValueError("lista_botones debe ser una lista.")
        if not isinstance(nro_columnas, int) or nro_columnas <= 0:
            raise ValueError("nro_columnas debe ser un entero mayor que 0.")
        if not isinstance(fuente, tuple) or len(fuente) != 3:
            raise ValueError("fuente debe ser una tupla con el formato (nombre, tamaño, estilo).")

        # Contador para la posición de los botones
        contador = 0

        # Crear los botones y agregarle los textos
        for texto_btn in self.lista_botones:
            boton = ctk.CTkButton(
                self.root,
                text=f"{texto_btn}",
                width=self.ancho,
                height=self.alto,
                font=self.font,
                cursor="hand2",
                command=self.callback
            )
            boton.grid(row=contador // self.nro_columnas, column=contador % self.nro_columnas, padx=5, pady=5)
            contador += 1

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

def lector_de_qr(img):
    """
    Lee un código QR desde una imagen.

    :param img: La imagen del código QR a leer.
    :return: El texto contenido en el código QR o None si no se puede leer.
    
    NOTA: Modo de uso:
        texto = lector_de_qr(img)
    """
    # Leer el código QR desde la imagen
    qr = qrcode.QRCode()
    try:
        qr.read(img)
        return qr.data
    except:
        return None

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