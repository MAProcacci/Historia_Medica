from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext, LabelFrame

import customtkinter as ctk
from customtkinter import *

from PIL import Image, ImageTk
import tkcalendar as tc
from tkcalendar import Calendar, DateEntry
from datetime import datetime

from libreria import *
from sqlqueries import QueriesSQLite
from modelo.pacienteDao import Persona, cargar_persona, guardar_dato_paciente, actualizar_dato_paciente, \
                            listar_personas, eliminar_persona
from modelo.historiaMedicaDao import HistoriaMedica, guardar_historia_medica, listar_historia_medica, \
                                    editar_historia_medica, eliminar_historia_medica


class Frame(ctk.CTkFrame):
    """
    Clase que representa el marco principal de la interfaz de usuario.
    Atributos:
        root2 (Tk): Ventana principal de la interfaz de usuario.
    """
    def __init__(self, root2):
        super().__init__(root2, width=1280, height=720)
        self.root = root2
        self.pack()
        self.configure(fg_color=COLOR_FONDO)
        self.id_persona = None  # Definir id_persona como None por defecto
        self.id_PersonaHistoria = None
        self.id_historiaMedica = None
        self.swith1 = False
        self.snackbar = SnackBar(self)
        self.campos_paciente()
        self.desabilitar_entrys()
        self.tabla_paciente()

    def campos_paciente(self):
        """Muestra los campos del paciente."""

        # Labels de los campos del paciente
        self.lbl_nombre = ctk.CTkLabel(self, text="Nombre: ", font=("Arial", 15, "bold"))
        self.lbl_nombre.grid(row=0, column=0, padx=10, pady=5)

        self.lbl_Ape_Pat = ctk.CTkLabel(self, text="Apellido Paterno: ", font=("Arial", 15, "bold"))
        self.lbl_Ape_Pat.grid(row=1, column=0, padx=10, pady=5)

        self.lbl_Ape_Mat = ctk.CTkLabel(self, text="Apellido Materno: ", font=("Arial", 15, "bold"))
        self.lbl_Ape_Mat.grid(row=2, column=0, padx=10, pady=5)

        self.lbl_Doc = ctk.CTkLabel(self, text="Nro. ID: ", font=("Arial", 15, "bold"))
        self.lbl_Doc.grid(row=3, column=0, padx=10, pady=5)

        self.lbl_Fecha_Nac = ctk.CTkLabel(self, text="Fecha Nac: ", font=("Arial", 15, "bold"))
        self.lbl_Fecha_Nac.grid(row=5, column=0, padx=10, pady=5)

        self.lbl_edad = ctk.CTkLabel(self, text="Edad: ", font=("Arial", 15, "bold"))
        self.lbl_edad.grid(row=6, column=0, padx=10, pady=5)

        self.lbl_Sexo = ctk.CTkLabel(self, text="Sexo: ", font=("Arial", 15, "bold"))
        self.lbl_Sexo.grid(row=7, column=0, padx=10, pady=5)

        self.lbl_antecedentes = ctk.CTkLabel(self, text="Antecedentes: ", font=("Arial", 15, "bold"))
        self.lbl_antecedentes.grid(row=8, column=0, padx=10, pady=5)

        self.lbl_Direc = ctk.CTkLabel(self, text="Dirección: ", font=("Arial", 15, "bold"))
        self.lbl_Direc.grid(row=9, column=0, padx=10, pady=5)

        self.lbl_Telef = ctk.CTkLabel(self, text="Teléfono: ", font=("Arial", 15, "bold"))
        self.lbl_Telef.grid(row=10, column=0, padx=10, pady=5)

        self.lbl_Email = ctk.CTkLabel(self, text="Email: ", font=("Arial", 15, "bold"))
        self.lbl_Email.grid(row=11, column=0, padx=10, pady=5)

        # Entradas de los campos del paciente
        self.svNombre = tk.StringVar()
        self.txt_nombre = ctk.CTkEntry(self, 
                                    placeholder_text="Nombre", 
                                    textvariable=self.svNombre, 
                                    font=("Arial", 15), 
                                    width=300)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

        self.svApe_Pat = tk.StringVar()
        self.txt_Ape_Pat = ctk.CTkEntry(self, 
                                        placeholder_text="Apellido Paterno", 
                                        textvariable=self.svApe_Pat, 
                                        font=("Arial", 15), 
                                        width=300)
        self.txt_Ape_Pat.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

        self.svApe_Mat = tk.StringVar()
        self.txt_Ape_Mat = ctk.CTkEntry(self, 
                                        placeholder_text="Apellido Materno", 
                                        textvariable=self.svApe_Mat, 
                                        font=("Arial", 15), 
                                        width=300)
        self.txt_Ape_Mat.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

        self.svDoc = tk.StringVar()
        self.txt_Doc = ctk.CTkEntry(self, 
                                    placeholder_text="Nro. ID", 
                                    textvariable=self.svDoc, 
                                    font=("Arial", 15), 
                                    width=300)
        self.txt_Doc.grid(row=3, column=1, padx=10, pady=5, columnspan=2) 

        self.svFecha_Nac = tk.StringVar()
        self.txt_Fecha_Nac = ctk.CTkEntry(self, 
                                        placeholder_text="MM-DD-YYYY", 
                                        textvariable=self.svFecha_Nac, 
                                        font=("Arial", 15), 
                                        width=140,
                                        state="readonly")
        self.txt_Fecha_Nac.grid(row=5, column=1, padx=10, pady=5, sticky="e")

        # Botón para seleccionar fecha
        self.btn_seleccionar_fecha = ctk.CTkButton(self, 
                                                   text="Seleccionar Fecha", 
                                                   font=("Arial", 12),
                                                   width=140,
                                                   command=self.abrir_calendario)
        self.btn_seleccionar_fecha.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        self.svEdad = tk.StringVar()
        self.txt_edad = ctk.CTkEntry(self, 
                                    placeholder_text="Edad", 
                                    textvariable=self.svEdad, 
                                    font=("Arial", 15), 
                                    width=300,
                                    state="readonly")
        self.txt_edad.grid(row=6, column=1, padx=10, pady=5, columnspan=2)

        # Cambiar CTkEntry por CTkComboBox para el campo de Sexo
        self.svSexo = tk.StringVar()
        self.cmb_Sexo = ctk.CTkComboBox(self, 
                                        values=["Male", "Female"], 
                                        variable=self.svSexo, 
                                        font=("Arial", 15), 
                                        width=300,
                                        state="readonly")
        self.cmb_Sexo.grid(row=7, column=1, padx=10, pady=5, columnspan=2)
        self.cmb_Sexo.set("Male")  # Establecer un valor por defecto

        self.svAntecedentes = tk.StringVar()
        self.txt_antecedentes = ctk.CTkEntry(self, 
                                            placeholder_text="Antecedentes", 
                                            textvariable=self.svAntecedentes, 
                                            font=("Arial", 15), 
                                            width=300)
        self.txt_antecedentes.grid(row=8, column=1, padx=10, pady=5, columnspan=2)

        self.svDirec = tk.StringVar()
        self.txt_Direc = ctk.CTkEntry(self, 
                                    placeholder_text="Dirección", 
                                    textvariable=self.svDirec, 
                                    font=("Arial", 15), 
                                    width=300)
        self.txt_Direc.grid(row=9, column=1, padx=10, pady=5, columnspan=2)

        self.svTelef = tk.StringVar()
        self.txt_Telef = ctk.CTkEntry(self, 
                                    placeholder_text="Teléfono", 
                                    textvariable=self.svTelef, 
                                    font=("Arial", 15), 
                                    width=300)
        self.txt_Telef.grid(row=10, column=1, padx=10, pady=5, columnspan=2)

        self.svEmail = tk.StringVar()
        self.txt_Email = ctk.CTkEntry(self, 
                                    placeholder_text="Email", 
                                    textvariable=self.svEmail, 
                                    font=("Arial", 15), 
                                    width=300)
        self.txt_Email.grid(row=11, column=1, padx=10, pady=5, columnspan=2)

        # Botones
        self.btn_nuevo = ctk.CTkButton(self, 
                                        text="Nuevo", 
                                        font=("Arial", 14, "bold"),
                                        height=30,
                                        width=150, 
                                        command=self.habilitar_entrys,
                                        fg_color="green", 
                                        hover_color="darkgreen",
                                        cursor="hand2")
        self.btn_nuevo.grid(row=12, column=0, padx=10, pady=5)

        self.btn_guardar = ctk.CTkButton(self, 
                                        text="Guardar", 
                                        font=("Arial", 14, "bold"),
                                        height=30,
                                        width=150, 
                                        command=self.guardar_paciente,
                                        cursor="hand2")
        self.btn_guardar.grid(row=12, column=1, padx=10, pady=5)

        self.btn_cancelar = ctk.CTkButton(self, 
                                        text="Cancelar", 
                                        font=("Arial", 14, "bold"),
                                        height=30,
                                        width=150, 
                                        command=self.desabilitar_entrys,
                                        fg_color="red", 
                                        hover_color="darkred",
                                        cursor="hand2")
        self.btn_cancelar.grid(row=12, column=2, padx=10, pady=5)

        # Buscador por apellido y/o DNI
        # Labels para el buscador
        self.buscar_nro_id = ctk.CTkLabel(self, 
                                        text="Buscar Nro. ID", 
                                        font=("Arial", 15,"bold"))
        self.buscar_nro_id.grid(row=0, column=3, padx=10, pady=5)

        self.buscar_ap_paterno = ctk.CTkLabel(self,
                                        text="Buscar Ap. Paterno", 
                                        font=("Arial", 15,"bold"))
        self.buscar_ap_paterno.grid(row=1, column=3, padx=10, pady=5)

        # Entrys para el buscador
        self.svBuscadorNroId = tk.StringVar()
        self.entry_buscador_nro_id = ctk.CTkEntry(self, 
                                                textvariable=self.svBuscadorNroId,
                                                placeholder_text="Nro. ID", 
                                                font=("Arial", 15), 
                                                width=300)
        self.entry_buscador_nro_id.grid(row=0, column=4, padx=10, pady=5, columnspan=2)

        self.svBuscadorApPaterno = tk.StringVar()
        self.entry_buscador_ap_paterno = ctk.CTkEntry(self, 
                                                textvariable=self.svBuscadorApPaterno,
                                                placeholder_text="Apellido Paterno", 
                                                font=("Arial", 15), 
                                                width=300)
        self.entry_buscador_ap_paterno.grid(row=1, column=4, padx=10, pady=5, columnspan=2)

        # Botones para el buscador
        self.btn_buscar = ctk.CTkButton(self, 
                                        text="Buscar", 
                                        font=("Arial", 14, "bold"),
                                        height=30,
                                        width=150, 
                                        command=self.buscar_paciente,
                                        fg_color="#076dd7", 
                                        hover_color="#053c75",
                                        cursor="hand2")
        self.btn_buscar.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Botones para limpiar
        self.btn_limpiar = ctk.CTkButton(self, 
                                        text="Limpiar", 
                                        font=("Arial", 14, "bold"),
                                        height=30,
                                        width=150, 
                                        command=self.limpiar_entrys_buscar,
                                        fg_color="#c5a304", 
                                        hover_color="#756103",
                                        cursor="hand2")
        self.btn_limpiar.grid(row=2, column=4, padx=10, pady=5, sticky="e")

    def buscar_paciente(self):
        """Busca un paciente en la base de datos por Nro. ID o Apellido Paterno."""
        try:
            # Obtener el valor del entry
            nro_id = self.svBuscadorNroId.get().strip()
            ap_paterno = self.svBuscadorApPaterno.get().strip()

            # Inicializar la cláusula WHERE
            condiciones = []

            # Agregar condición para nro_id si no está vacío
            if nro_id:
                try:
                    # Validar que nro_id sea un número
                    nro_id_int = int(nro_id)
                    condiciones.append(f"nro_id = {nro_id_int}")
                except ValueError:
                    #self.snackbar.show("El número de ID debe ser un valor numérico.", tipo="advertencia")
                    messagebox.showwarning("Buscar_Paciente - Warning", "El número de ID debe ser un valor numérico.")
                    return

            # Agregar condición para apellido paterno si no está vacío
            if ap_paterno:
                condiciones.append(f"apellido_paterno LIKE '%{ap_paterno}%'")
                # Solo aplicar activo = 1 cuando se busca por apellido paterno
                condiciones.append("activo = 1")

            # Construir la cláusula WHERE
            where = " AND ".join(condiciones) if condiciones else ""

            if len(nro_id) == 0 and len(ap_paterno) == 0:
                # Llamar a tabla_paciente sin la cláusula WHERE
                self.tabla_paciente()                
            else:
                # Llamar a tabla_paciente con la cláusula WHERE
                self.tabla_paciente(where)

            # Limpiar los entrys de Buscar
            self.limpiar_entrys_buscar(sw = False)
        
        except Exception as e:
            messagebox.showerror("Buscar_Paciente - Error", f"Ocurrió un error al buscar el paciente: {str(e)}")
            registrar_error(f"Buscar_Paciente - Error al buscar el paciente: {str(e)}")

    def limpiar_entrys_buscar(self, sw = True):
        """Limpia los entrys de Buscar.
        Args:
            sw (bool): True para limpiar y mostrar todos los pacientes, False para limpiar los entrys de Buscar.
        """
        if sw:
            self.svBuscadorNroId.set("")
            self.svBuscadorApPaterno.set("")

            # Llamar a tabla_paciente sin la cláusula WHERE para limpiar y mostrar todos los pacientes.
            self.tabla_paciente()
            return
        self.svBuscadorNroId.set("")
        self.svBuscadorApPaterno.set("")

    def abrir_calendario(self):
        """Abre un calendario para seleccionar la fecha de nacimiento."""
        # Abrir el calendario para seleccionar la fecha de nacimiento y obtener la fecha seleccionada
        fecha_seleccionada = seleccionar_fecha(self.root, titulo="Fecha de Nacimiento")
        if fecha_seleccionada:
            # Formatear la fecha seleccionada
            fecha_formateada = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').strftime('%m-%d-%Y')
            self.svFecha_Nac.set(fecha_formateada)
            
            # Calcular la edad a partir de la fecha de nacimiento
            edad = self.calcular_edad(fecha_seleccionada)
            self.svEdad.set(edad)  # Mostrar la edad en el campo correspondiente

    def calcular_edad(self, fecha_nacimiento):
        """
        Calcula la edad en años a partir de la fecha de nacimiento.
        :param fecha_nacimiento: La fecha de nacimiento en formato 'YYYY-MM-DD'.
        :return: La edad en años.
        """
        # Obtener la fecha actual
        hoy = datetime.today()
        # Convertir la fecha de nacimiento a datetime
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        # Calcular la edad
        edad = hoy.year - fecha_nac.year
        # Ajustar si aun no ha pasado el cumpleaños este año
        if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
            edad -= 1
        return edad
    
    def guardar_paciente(self):
        """Guarda los datos del paciente después de validar el correo electrónico."""
        # Validar el correo electrónico
        correo = self.svEmail.get()
        if not validar_correo(correo):
            messagebox.showwarning("Guardar_Paciente - Warning", "El correo electrónico no es válido.")
            return

        # Validate nro_id is not empty
        nro_id = self.svDoc.get()
        if not nro_id:
            messagebox.showwarning("Guardar_Paciente - Warning", "El número de ID es obligatorio.")
            return        
        
        # Crea una instancia de Persona con los datos del formulario
        persona = Persona(
            self.svNombre.get(),
            self.svApe_Pat.get(),
            self.svApe_Mat.get(),
            self.svDoc.get(),
            self.svFecha_Nac.get(),
            self.svEdad.get(),
            self.svSexo.get(),
            self.svAntecedentes.get(),
            self.svDirec.get(),
            self.svTelef.get(),
            self.svEmail.get(),
            1
        )
        persona.id_persona = self.id_persona  # Asignar el id_persona después de crear la instancia
        

        if self.id_persona == None:
            # Chequea si el nro_id ya existe (solo para pacientes nuevos)
            if self.id_persona is None:  # Solo chequear para pacientes nuevos
                try:
                    # Consulta para verificar si el nro_id ya existe
                    conn = QueriesSQLite.create_connection(DB_NAME)
                    query = "SELECT COUNT(*) FROM personas WHERE nro_id = ? AND activo = 1"
                    result = QueriesSQLite.execute_read_query(conn, query, (nro_id,))
                    
                    if result[0][0] > 0:
                        messagebox.showwarning("Guardar_Paciente - Warning", f"Ya existe un paciente con ese número de ID: ({nro_id}).")
                        return
                except Exception as e:
                    messagebox.showerror("Guardar_Paciente - Error", f"Error al accesar el paciente y corroborar su existencia: {e}")
                    registrar_error("Guardar_Paciente - Error al accesar el paciente y corroborar su existencia: {e}")
            # Guardar nuevo paciente
            guardar_dato_paciente(persona)
        else:
            # Actualizar paciente existente
            actualizar_dato_paciente(persona)
            
        # Desabilitar los entrys y actualizar tabla de pacientes
        self.desabilitar_entrys()
        self.tabla_paciente()

    def desabilitar_entrys(self):
        """Deshabilita los entrys para evitar ediciones."""
        # Deshabilitar botones
        self.btn_guardar.configure(state="disabled")
        self.btn_cancelar.configure(state="disabled")
        self.btn_seleccionar_fecha.configure(state="disabled")

        # Limpiar id_persona
        self.id_persona = None
                
        # Limpiar los entrys
        self.svNombre.set("")
        self.svApe_Pat.set("")
        self.svApe_Mat.set("")
        self.svDoc.set("")
        self.svFecha_Nac.set("")
        self.svEdad.set("")
        self.svSexo.set("Male")
        self.svAntecedentes.set("")
        self.svDirec.set("")
        self.svTelef.set("")
        self.svEmail.set("")        
        
        # Deshabilitar los entrys
        self.txt_nombre.configure(state="disabled")
        self.txt_Ape_Pat.configure(state="disabled")
        self.txt_Ape_Mat.configure(state="disabled")
        self.txt_Doc.configure(state="disabled")
        self.txt_Fecha_Nac.configure(state="disabled")
        self.txt_edad.configure(state="disabled")
        self.cmb_Sexo.configure(state="disabled")
        self.txt_antecedentes.configure(state="disabled")
        self.txt_Direc.configure(state="disabled")
        self.txt_Telef.configure(state="disabled")
        self.txt_Email.configure(state="disabled")

    def habilitar_entrys(self):
        """Habilita los entrys para ediciones."""
        # Habilitar botones
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_seleccionar_fecha.configure(state="normal")

        # Limpiar id_persona
        #self.id_persona = None

        # Limpiar los entrys
        self.svNombre.set("")
        self.svApe_Pat.set("")
        self.svApe_Mat.set("")
        self.svDoc.set("")
        self.svFecha_Nac.set("")
        self.svEdad.set("")
        self.svSexo.set("Male")
        self.svAntecedentes.set("")
        self.svDirec.set("")
        self.svTelef.set("")
        self.svEmail.set("")

        # Habilitar los entrys
        self.txt_nombre.configure(state="normal")
        self.txt_Ape_Pat.configure(state="normal")
        self.txt_Ape_Mat.configure(state="normal")
        self.txt_Doc.configure(state="normal")
        self.txt_Fecha_Nac.configure(state="readonly")
        self.txt_edad.configure(state="readonly")
        self.cmb_Sexo.configure(state="readonly")
        self.txt_antecedentes.configure(state="normal")
        self.txt_Direc.configure(state="normal")
        self.txt_Telef.configure(state="normal")
        self.txt_Email.configure(state="normal")

    def tabla_paciente(self, where=""):
        """Muestra los pacientes en un Treeview.
        
        Args:
            where (str): Filtro para la consulta.
        """
        # Validar si se debe realizar un filtro
        if len(where) > 0:
            self.listarPersonas = cargar_persona(where)
        else:
            self.listarPersonas = listar_personas()
            #self.listarPersonas.reverse() # Ordenar de manera descendente

        # Crear Frame para el Treeview (usar ttk.Frame en lugar de CTkFrame)
        self.frame_tabla = ttk.Frame(self, style="Treeview")
        self.frame_tabla.grid(row=13, column=0, columnspan=12, pady=10, padx=10, sticky="nsew")

        # Configurar el grid para que el frame_tabla se expanda correctamente
        #self.grid_rowconfigure(13, weight=1)
        #self.grid_columnconfigure(0, weight=1)

        # Crear Scrollbars
        self.scroll_y = ctk.CTkScrollbar(self.frame_tabla, orientation="vertical")
        self.scroll_y.pack(side="right", fill="y")

        self.scroll_x = ctk.CTkScrollbar(self.frame_tabla, orientation="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")

        # Creamos el Style del Treeview
        style = ttk.Style()
        # Configurar el estilo del Treeview
        style.configure("Treeview",  # Nombre del estilo personalizado
                        background="darkgray",  # Color de fondo
                        foreground="black",    # Color del texto
                        headingbackground=COLOR_BOTON,  # Color de fondo del encabezado
                        headingforeground="white",     # Color del texto del encabezado
                        rowheight=20,          # Altura de las filas
                        font=('Arial', 8))    # Fuente y tamaño del texto

        # Configurar el estilo de las filas alternas (opcional)
        style.map("Treeview",
              background=[('selected', '#347083')])  # Color de fondo cuando una fila está seleccionada 
        # Crear el Treeview
        self.tabla = ttk.Treeview(self.frame_tabla,
                                #height=10, 
                                show="headings",
                                style="Treeview",
                                columns=("id", "nombre", "ape_pat", "ape_mat", "doc", "fecha_nac", 
                                        "edad", "sexo", "antecedentes", "direccion", "telefono", "email"),
                                yscrollcommand=self.scroll_y.set,
                                xscrollcommand=self.scroll_x.set)
        self.tabla.pack(fill="both", expand=True)

        self.scroll_y.configure(command=self.tabla.yview, cursor="hand2")
        self.scroll_x.configure(command=self.tabla.xview, cursor="hand2")

        # Encabezados de la tabla
        self.tabla.heading("id", text="Id")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("ape_pat", text="Ap. Paterno")
        self.tabla.heading("ape_mat", text="Ap. Materno")
        self.tabla.heading("doc", text="Nro. ID")
        self.tabla.heading("fecha_nac", text="F. Nacimiento")
        self.tabla.heading("edad", text="Edad")
        self.tabla.heading("sexo", text="Sexo")
        self.tabla.heading("antecedentes", text="Antecedentes")
        self.tabla.heading("direccion", text="Direccion")
        self.tabla.heading("telefono", text="Telefono")
        self.tabla.heading("email", text="Email")        

        # Definir el ancho y alineacion de las columnas
        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("nombre", width=150, anchor="center")
        self.tabla.column("ape_pat", width=120, anchor="center")
        self.tabla.column("ape_mat", width=120, anchor="center")
        self.tabla.column("doc", width=80, anchor="center")
        self.tabla.column("fecha_nac", width=100, anchor="center")
        self.tabla.column("edad", width=50, anchor="center")
        self.tabla.column("sexo", width=60, anchor="center")
        self.tabla.column("antecedentes", width=300, anchor="center")
        self.tabla.column("direccion", width=250, anchor="center")
        self.tabla.column("telefono", width=85, anchor="center")
        self.tabla.column("email", width=200, anchor="center")

        # Insertar los datos en la tabla
        for p in self.listarPersonas:
            self.tabla.insert("", 
                            "end", 
                            text=p[0], 
                            values=(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]),
                            tags='evenrow',)
        
        # Botones
        self.btn_editar_paciente = ctk.CTkButton(self, 
                                                text="Editar Paciente", 
                                                command=self.editar_paciente,
                                                width=150, 
                                                height=30,
                                                font=("Arial", 14, "bold"),
                                                fg_color="#8827c5", 
                                                hover_color="#503561",
                                                cursor="hand2")
        self.btn_editar_paciente.grid(row=14, column=0, padx=10, pady=5)

        self.btn_eliminar_paciente = ctk.CTkButton(self, 
                                                text="Eliminar Paciente", 
                                                command=self.eliminar_paciente,
                                                width=150, 
                                                height=30, 
                                                font=("Arial", 14, "bold"), 
                                                fg_color="#bf0f06", 
                                                hover_color="#6b1611", 
                                                cursor="hand2")
        self.btn_eliminar_paciente.grid(row=14, column=1, padx=10, pady=5)

        self.btn_historial_paciente = ctk.CTkButton(self, 
                                                    text="Historial Paciente", 
                                                    command=self.historia_medica,
                                                    width=150, 
                                                    height=30, 
                                                    font=("Arial", 14, "bold"), 
                                                    fg_color="#079ab5", 
                                                    hover_color="#0d6777", 
                                                    cursor="hand2")
        self.btn_historial_paciente.grid(row=14, column=2, padx=10, pady=5)

        self.btn_salir = ctk.CTkButton(self, 
                                    text="Salir", 
                                    command=self.root.destroy,
                                    width=150, 
                                    height=30, 
                                    font=("Arial", 14, "bold"), 
                                    fg_color=COLOR_BT_SALIR, 
                                    hover_color=COLOR_BT_SALIR_ACTIVO, 
                                    cursor="hand2")
        self.btn_salir.grid(row=14, column=11, padx=10, pady=5)

    def historia_medica(self):
        """
        Muestra la historia médica del paciente seleccionado.
        
        """
        try:
            # Verificar si se ha seleccionado un paciente
            if self.id_persona == None:
                self.id_persona = self.tabla.item(self.tabla.focus(), "text")
                self.id_PersonaHistoria = self.tabla.item(self.tabla.focus(), "text")   
            
            # Convertir el ID a un entero si es necesario (para evitar errores)
            if isinstance(self.id_persona, int) and self.id_persona > 0:
                id_persona = self.id_persona
            else:
                messagebox.showwarning("Historia_Medica - Advertencia", "Seleccione un paciente")
                #self.tabla.focus_set()
                self.id_persona = None
                return

            # Crear la ventana emergente para la historia médica (usar CTkToplevel en lugar de Toplevel)
            self.top_historia_medica = ctk.CTkToplevel(self)
            self.top_historia_medica.title("Historia Medica")
            #self.top_historia_medica.geometry("1100x600")
            self.top_historia_medica.resizable(False, False)
            self.top_historia_medica.transient(self)
            self.top_historia_medica.grab_set()
            
            # Crear el contenido de la ventana emergente
            self.lista_historia = listar_historia_medica(id_persona)

            # Crear la tabla para mostrar los datos
            self.tabla_historia = ttk.Treeview(self.top_historia_medica,
                                            show="headings",
                                            columns=("ID", "Apellidos", "Fecha Historia", "Motivo", 
                                                    "Examen Auxiliar", "Tratamiento", "Detalle", 
                                                    "Diagnostico", "Observaciones"))
            self.tabla_historia.grid(row=0, column=0, pady=10, columnspan=8, sticky="nse")

            # Crear el scroll para la tabla
            self.scroll_y = ctk.CTkScrollbar(self.top_historia_medica, 
                                            orientation="vertical", 
                                            command=self.tabla_historia.yview)
            self.scroll_y.grid(row=0, column=8, sticky="nse")
            self.tabla_historia.configure(yscrollcommand=self.scroll_y.set, cursor="hand2", style="Custom.Treeview")

            # Configurar los encabezados de la tabla
            self.tabla_historia.heading("#01", text="ID")
            self.tabla_historia.heading("#02", text="Apellidos")
            self.tabla_historia.heading("#03", text="Fecha y Hora")
            self.tabla_historia.heading("#04", text="Motivo")
            self.tabla_historia.heading("#05", text="Examen Auxiliar")
            self.tabla_historia.heading("#06", text="Tratamiento")
            self.tabla_historia.heading("#07", text="Detalle")
            self.tabla_historia.heading("#08", text="Diagnostico")
            self.tabla_historia.heading("#09", text="Observaciones")

            # Definir el ancho y alineacion de las columnas
            self.tabla_historia.column("#01", width=50, anchor=CENTER)
            self.tabla_historia.column("#02", width=100, anchor=CENTER)
            self.tabla_historia.column("#03", width=100, anchor=CENTER)
            self.tabla_historia.column("#04", width=120, anchor=CENTER)
            self.tabla_historia.column("#05", width=250, anchor=CENTER)
            self.tabla_historia.column("#06", width=200, anchor=CENTER)
            self.tabla_historia.column("#07", width=300, anchor=CENTER)
            self.tabla_historia.column("#08", width=350, anchor=CENTER)
            self.tabla_historia.column("#09", width=300, anchor=CENTER)
            
            # Insertar los datos en la tabla
            for p in self.lista_historia:
                self.tabla_historia.insert("", 
                                        "end", 
                                        text=p[0], 
                                        values=(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

            self.id_persona = None
            #self.id_PersonaHistoria = None

            # Crear los botones
            self.btn_guardar_historia = CTkButton(self.top_historia_medica, 
                                                text="Agregar Historia", 
                                                command=self.top_agregar_historia,
                                                width=140,
                                                fg_color="blue",
                                                hover_color="#7198e0",
                                                font=("Arial", 14, "bold"),
                                                cursor="hand2")
            self.btn_guardar_historia.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

            self.btn_editar_historia = CTkButton(self.top_historia_medica, 
                                                text="Editar Historia", 
                                                command=self.editar_historia,
                                                width=140,
                                                fg_color="#3a005d",
                                                hover_color="#b47cd6",
                                                font=("Arial", 14, "bold"),
                                                cursor="hand2")
            self.btn_editar_historia.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

            self.btn_eliminar_historia = CTkButton(self.top_historia_medica, 
                                                text="Eliminar Historia", 
                                                command=self.eliminar_historia,
                                                width=140,
                                                fg_color="#890011",
                                                hover_color="#5d1503",
                                                font=("Arial", 14, "bold"),
                                                cursor="hand2")
            self.btn_eliminar_historia.grid(row=2, column=2, padx=10, pady=5, columnspan=2)

            self.btn_cerrar_historia = CTkButton(self.top_historia_medica, 
                                                text="Cerrar", 
                                                command=self.cerrar_historia,
                                                width=140,
                                                fg_color=COLOR_BT_SALIR,
                                                hover_color=COLOR_BT_SALIR_ACTIVO,
                                                font=("Arial", 14, "bold"),
                                                cursor="hand2")
            self.btn_cerrar_historia.grid(row=2, column=3, padx=10, pady=5, columnspan=2)

        except Exception as e:
            messagebox.showerror("Historia_Medica - Error", f"Error al mostrar la historia médica: {e}")
            registrar_error(f"Historia_Medica - Error al mostrar la historia médica: {e}")

    def cerrar_historia(self):
        """
        Este método permite cerrar la ventana de agregar o editar historia medica.
        """
        self.top_historia_medica.destroy()
        self.tabla_paciente()

    def top_agregar_historia(self):
        """
        Este método permite abrir un nuevo top-level para agregar una nueva historia medica al 
        paciente seleccionado.
        """
        # Top-level para agregar historia
        self.top_Ag_historia = ctk.CTkToplevel(self)
        if self.swith1 == True:
            self.top_Ag_historia.title("Editar Historia Medica")
        else:
            self.top_Ag_historia.title("Agregar Historia Medica")
        #self.top_agregar_historia.geometry("1100x600")
        self.top_Ag_historia.resizable(False, False)
        self.top_Ag_historia.transient(self)
        self.top_Ag_historia.grab_set()

        # Frame principal
        self.frame_agregar_historia = ctk.CTkFrame(self.top_Ag_historia)
        self.frame_agregar_historia.pack(fill="both", expand=True, padx=20, pady=10)

        # Labels de los campos de la historia medica
        self.lbl_motivoHistoria = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Motivo de la Historia",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_motivoHistoria.grid(row=0, column=0, padx=5, pady=3, columnspan=4)

        self.lbl_examenAuxiliar = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Examen Auxiliar",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_examenAuxiliar.grid(row=2, column=0, padx=5, pady=3, columnspan=4)

        self.lbl_tratamiento = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Tratamiento",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_tratamiento.grid(row=4, column=0, padx=5, pady=3, columnspan=4)

        self.lbl_detalle = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Detalle",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_detalle.grid(row=6, column=0, padx=5, pady=3, columnspan=4)

        self.lbl_diagnostico = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Diagnostico",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_diagnostico.grid(row=8, column=0, padx=5, pady=3, columnspan=4)

        self.lbl_observaciones = ctk.CTkLabel(self.frame_agregar_historia, 
                                            text="Observaciones",
                                            width=20, 
                                            font=("Arial", 15, "bold"))
        self.lbl_observaciones.grid(row=10, column=0, padx=5, pady=3, columnspan=4)

        # Entry de los campos de la historia medica
        self.svMotivoHistoria = ctk.StringVar()
        self.txt_motivoHistoria = ctk.CTkEntry(self.frame_agregar_historia,
                                            textvariable=self.svMotivoHistoria, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_motivoHistoria.grid(row=1, column=0, padx=5, pady=3, columnspan=4)

        self.svExamenAuxiliar = ctk.StringVar()
        self.txt_examenAuxiliar = ctk.CTkEntry(self.frame_agregar_historia, 
                                            textvariable=self.svExamenAuxiliar, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_examenAuxiliar.grid(row=3, column=0, padx=5, pady=3, columnspan=4)

        self.svTratamiento = ctk.StringVar()
        self.txt_tratamiento = ctk.CTkEntry(self.frame_agregar_historia, 
                                            textvariable=self.svTratamiento, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_tratamiento.grid(row=5, column=0, padx=5, pady=3, columnspan=4)

        self.svDetalle = ctk.StringVar()
        self.txt_detalle = ctk.CTkEntry(self.frame_agregar_historia, 
                                            textvariable=self.svDetalle, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_detalle.grid(row=7, column=0, padx=5, pady=3, columnspan=4)

        self.svDiagnostico = ctk.StringVar()
        self.txt_diagnostico = ctk.CTkEntry(self.frame_agregar_historia, 
                                            textvariable=self.svDiagnostico, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_diagnostico.grid(row=9, column=0, padx=5, pady=3, columnspan=4)

        self.svObservaciones = ctk.StringVar()
        self.txt_observaciones = ctk.CTkEntry(self.frame_agregar_historia, 
                                            textvariable=self.svObservaciones, 
                                            width=550, 
                                            font=("Arial", 15))
        self.txt_observaciones.grid(row=11, column=0, padx=5, pady=3, columnspan=4)

        # Frame Fecha historia
        self.frame_fechaHistoria = ctk.CTkFrame(self.top_Ag_historia)
        self.frame_fechaHistoria.pack(fill="both", expand=True, padx=20, pady=10)

        # Label Fecha/Hora agregar historia 
        self.label_fechaHistoria = ctk.CTkLabel(self.frame_fechaHistoria, 
                                                text="Fecha y Hora",
                                                width=20, 
                                                font=("Arial", 15, "bold"))
        self.label_fechaHistoria.grid(row=1, column=2, padx=5, pady=3, sticky=W)

        # Entry Fecha/Hora agregar historia
        self.svFechaHistoria = ctk.StringVar()
        self.entry_fechaHistoria = ctk.CTkEntry(self.frame_fechaHistoria, 
                                                textvariable=self.svFechaHistoria, 
                                                width=130, 
                                                state="readonly",
                                                font=("Arial", 15))
        self.entry_fechaHistoria.grid(row=1, column=3, padx=5, pady=3)

        # Traer la fecha y hora actual
        self.svFechaHistoria.set(datetime.now().strftime("%m-%d-%Y %H:%M"))

        # Botones
        self.btn_agregar_historia = ctk.CTkButton(self.frame_fechaHistoria, 
                                                text="Agregar Historia", 
                                                command=self.agregar_historia,
                                                width=140,
                                                cursor="hand2",
                                                fg_color=("#006dff"),
                                                hover_color=("#013780"),
                                                font=("Arial", 14, "bold"))
        self.btn_agregar_historia.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

        self.btn_salir_historia = ctk.CTkButton(self.frame_fechaHistoria, 
                                                text="Salir", 
                                                command=self.top_Ag_historia.destroy,
                                                width=140,
                                                cursor="hand2",
                                                fg_color=COLOR_BT_SALIR,
                                                hover_color=COLOR_BT_SALIR_ACTIVO,
                                                font=("Arial", 14, "bold"))
        self.btn_salir_historia.grid(row=2, column=4, padx=10, pady=5, columnspan=2)

    def agregar_historia(self):
        """
        Este método permite agregar o editar una historia medica.
        """
        try:
            # Valida si es un registro nuevo o editar
            if self.id_historiaMedica == None:
                guardar_historia_medica(self.id_PersonaHistoria, 
                                        self.svFechaHistoria.get(),
                                        self.svMotivoHistoria.get(), 
                                        self.svExamenAuxiliar.get(), 
                                        self.svTratamiento.get(), 
                                        self.svDetalle.get(), 
                                        self.svDiagnostico.get(), 
                                        self.svObservaciones.get())
                self.top_Ag_historia.destroy()
                self.top_historia_medica.destroy()
                self.tabla_paciente()
                #self.id_historiaMedica = None
            else:
                editar_historia_medica(self.id_historiaMedica, 
                                        self.svFechaHistoria.get(),
                                        self.svMotivoHistoria.get(), 
                                        self.svExamenAuxiliar.get(), 
                                        self.svTratamiento.get(), 
                                        self.svDetalle.get(), 
                                        self.svDiagnostico.get(), 
                                        self.svObservaciones.get())
                self.top_Ag_historia.destroy()
                self.top_historia_medica.destroy()
                self.tabla_paciente()
                #self.id_historiaMedica = None

        except Exception as e:
            messagebox.showerror("Agregar_Historia - Error", f"Error al agregar la historia medica: {e}")
            registrar_error(f"Agregar_Historia - Error al agregar la historia medica: {e}")

    def eliminar_historia(self):
        """
        Este método permite eliminar una historia medica seleccionada en la tabla.
        """
        # Obtener el ID de la historia medica seleccionada desde la tabla
        self.tabla_historia.selection()
        selected_item = self.tabla_historia.focus()

        # Verificar si se ha seleccionado una historia medica
        if not selected_item:
            messagebox.showwarning("Eliminar_Historia - Warning", "No se ha seleccionado una historia medica")
            return

        # Obtener el ID de la historia medica seleccionada desde la tabla 
        self.id_historiaMedica = self.tabla_historia.item(selected_item, "text")

        # Confirmacion de la eliminacion de la historia medica por parte del usuario
        confirmacion = confirmar_eliminacion(self.root)

        # Si el usuario no confirma la eliminacion de la historia medica, se sale de la funcion
        if not confirmacion:
            return

        # Si el usuario confirma la eliminacion de la historia medica, se procede a eliminarla
        if eliminar_historia_medica(self.id_historiaMedica):
            self.tabla_historia.delete(selected_item)
            self.id_historiaMedica = None
            #self.top_historia_medica.destroy()
            messagebox.showinfo("Eliminar_Historia - Exitoso", 
                                "Se ha eliminado la historia medica del paciente con exito")
        else:
            messagebox.showerror("Eliminar_Historia - Error", 
                                "Error al eliminar la historia medica")
            registrar_error(f"Eliminar_Historia - Error al eliminar la historia medica.")

    def editar_historia(self):
        """
        Este método permite editar una historia medica seleccionada en la tabla.
        """
        # Obtener el ID de la historia medica seleccionada desde la tabla
        self.tabla_historia.selection()
        selected_item = self.tabla_historia.focus()

        # Verificar si se ha seleccionado una historia medica
        if not selected_item:
            messagebox.showwarning("Editar_Historia - Warning", "No se ha seleccionado una historia medica")
            return

        # Obtener el ID de la historia medica seleccionada desde la tabla
        self.id_historiaMedica = self.tabla_historia.item(selected_item, "text")

        # Llamar al método para mostrar los campos de la historia medica
        self.swith1 = True
        self.top_agregar_historia()
        self.llenar_campos_historia()
        self.swith1 = False

    def llenar_campos_historia(self):
        """
        Este método permite llenar los campos de la historia medica con los datos seleccionados en la tabla.
        """
        try:
            # Obtiener los datos de la historia medica seleccionada desde la tabla y
            # asignarlos a los campos correspondientes
            self.svFechaHistoria.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[2])
            self.svMotivoHistoria.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[3])
            self.svExamenAuxiliar.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[4])
            self.svTratamiento.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[5])
            self.svDetalle.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[6])
            self.svDiagnostico.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[7])
            self.svObservaciones.set(self.tabla_historia.item(self.tabla_historia.focus(), "values")[8])
        except IndexError as e:
            messagebox.showerror("Llenar_Campos_Historia - Error", 
                                "No se ha podido llenar los campos de la historia medica.")
            registrar_error(f"Llenar_Campos_Historia - Error al llenar los campos de la historia medica: {e}")
            return
            
    def editar_paciente(self):
        """Abre una ventana para editar un paciente."""
        # Capturar el ID del paciente seleccionado (si hubo una selección)
        self.tabla.selection()
        selected_item = self.tabla.focus()
        # Verificar si se ha seleccionado un paciente
        if not selected_item:
            messagebox.showwarning("Editar_Paciente - Warning", "No se ha seleccionado un paciente")
            return

        # Obtener el ID del paciente seleccionado desde la tabla
        self.id_persona = self.tabla.item(selected_item, "text")

        # Habilitar los entrys para que el usuario pueda editar los datos
        self.habilitar_entrys()

        # Llamar al método para abrir la ventana de edicion de paciente
        self.abrir_editar_paciente()

    def abrir_editar_paciente(self):
        """Obtiene los datos del paciente para editarlos"""
        try:
            # Obtener los datos del paciente
            self.nombrePaciente = self.tabla.item(self.tabla.focus(), "values")[1]
            self.apellidoPatPaciente = self.tabla.item(self.tabla.focus(), "values")[2]
            self.apellidoMatPaciente = self.tabla.item(self.tabla.focus(), "values")[3]
            self.docPaciente = self.tabla.item(self.tabla.focus(), "values")[4]
            self.fechaNacPaciente = self.tabla.item(self.tabla.focus(), "values")[5]
            self.edadPaciente = self.tabla.item(self.tabla.focus(), "values")[6]
            self.sexoPaciente = self.tabla.item(self.tabla.focus(), "values")[7]
            self.antecedentesPaciente = self.tabla.item(self.tabla.focus(), "values")[8]
            self.direccionPaciente = self.tabla.item(self.tabla.focus(), "values")[9]
            self.telefonoPaciente = self.tabla.item(self.tabla.focus(), "values")[10]
            self.emailPaciente = self.tabla.item(self.tabla.focus(), "values")[11]

            # Asignar los valores a los entrys
            self.svNombre.set(self.nombrePaciente)
            self.svApe_Pat.set(self.apellidoPatPaciente)
            self.svApe_Mat.set(self.apellidoMatPaciente)
            self.svDoc.set(self.docPaciente)
            self.svFecha_Nac.set(self.fechaNacPaciente)
            self.svEdad.set(self.edadPaciente)
            self.svSexo.set(self.sexoPaciente)
            self.svAntecedentes.set(self.antecedentesPaciente)
            self.svDirec.set(self.direccionPaciente)
            self.svTelef.set(self.telefonoPaciente)
            self.svEmail.set(self.emailPaciente)
        except IndexError as e:
            messagebox.showerror("Abrir_Editar_Paciente - Error", f"No se pudo cargar los datos del paciente seleccionado: {e}")
            registrar_error(f"Abrir_Editar_Paciente - Error al cargar los datos del paciente: {e}")
            return
    
    def eliminar_paciente(self):
        """Elimina un paciente después de confirmar con el usuario."""
        # Capturar el ID del paciente seleccionado (si hubo una selección)
        selected_item = self.tabla.focus()
        
        # Verificar si se ha seleccionado un paciente
        if not selected_item:
            messagebox.showwarning("Eliminar_Paciente - Warning", "No se ha seleccionado un paciente")
            return
        
        # Obtener el ID del paciente seleccionado
        self.id_persona = self.tabla.item(selected_item, "text")
        
        '''# Mostrar una ventana de confirmación
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este paciente?"
        )'''

        # Mostrar el cuadro de diálogo personalizado
        confirmacion = confirmar_eliminacion(self.root)

        # Si el usuario confirma la eliminación
        if confirmacion:
            try:
                eliminar_persona(self.id_persona)
                messagebox.showinfo("Eliminar_Paciente - Éxito", "El paciente ha sido eliminado correctamente.")
                self.tabla_paciente()  # Actualizar la tabla después de eliminar
            except Exception as e:
                messagebox.showerror("Eliminar_Paciente - Error", f"Ocurrió un error al eliminar el paciente: {e}")
                registrar_error(f"Eliminar_Paciente - Error al eliminar el paciente: {e}")
        else:
            # Si el usuario cancela la eliminación
            messagebox.showinfo("Eliminar_Paciente - Cancelado", "La eliminación del paciente ha sido cancelada.")
        
        # Actualizar la tabla
        self.tabla_paciente()
        # Limpiar el ID del paciente
        self.id_persona = None
            