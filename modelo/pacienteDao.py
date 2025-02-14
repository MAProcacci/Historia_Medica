from tkinter import messagebox
from sqlqueries import QueriesSQLite
from libreria import *


def guardar_dato_paciente(persona):
    """Guarda los datos del paciente en la base de datos.
    Args:
        persona (Persona): Objeto Persona con los datos del paciente a guardar.
    Returns:
        bool: True si se guardan los datos correctamente, False en caso contrario.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)

        query = "INSERT INTO personas (nombre, apellido_paterno, apellido_materno, nro_id, \
                fecha_nacimiento, edad, sexo, antecedentes, direccion, telefono, correo, activo) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        data = (persona.nombre, persona.apellido_paterno, persona.apellido_materno, persona.nro_id, 
                persona.fecha_nacimiento, persona.edad, persona.sexo, persona.antecedentes, 
                persona.direccion, persona.telefono, persona.correo, 1)

        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Guardar_Dato_Paciente - Exitoso", f"Se ha guardado los datos del paciente con exito")
        return True
    except Exception as e:
        messagebox.showerror("Guardar_Dato_Paciente - Error", f"Error al guardar los datos del paciente: {e}")
        registrar_error(f"Guardar_Dato_Paciente - Error al guardar los datos del paciente: {e}")
        return False

def actualizar_dato_paciente(persona):
    """Actualiza los datos del paciente en la base de datos.
    Args:
        persona (Persona): Objeto Persona con los datos del paciente a actualizar.
    Returns:
        bool: True si se actualiza correctamente, False en caso contrario.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)
        
        # Primero obtenemos el nro_id actual
        query_current = "SELECT nro_id FROM personas WHERE id_persona = ?"
        current_id = QueriesSQLite.execute_read_query(conn, query_current, (persona.id_persona,))
        
        if current_id[0][0] == persona.nro_id:
            # Si el nro_id no ha cambiado, actualizamos sin tocar ese campo
            query = """UPDATE personas 
                      SET nombre = ?, apellido_paterno = ?, apellido_materno = ?,
                          fecha_nacimiento = ?, edad = ?, sexo = ?, antecedentes = ?, 
                          direccion = ?, telefono = ?, correo = ?, activo = ? 
                      WHERE id_persona = ?"""
            data = (persona.nombre, persona.apellido_paterno, persona.apellido_materno,
                    persona.fecha_nacimiento, persona.edad, persona.sexo, persona.antecedentes, 
                    persona.direccion, persona.telefono, persona.correo, 1, persona.id_persona)
        else:
            # Si el nro_id ha cambiado, verificamos que no exista y actualizamos todo
            query_check = "SELECT COUNT(*) FROM personas WHERE nro_id = ? AND id_persona != ? AND activo = 1"
            result = QueriesSQLite.execute_read_query(conn, query_check, (persona.nro_id, persona.id_persona))
            
            if result[0][0] > 0:
                messagebox.showwarning("Actualizar_Dato_Paciente - Warning", f"El número de ID ya existe en otro paciente")
                return False
                
            query = """UPDATE personas 
                      SET nombre = ?, apellido_paterno = ?, apellido_materno = ?, nro_id = ?,
                          fecha_nacimiento = ?, edad = ?, sexo = ?, antecedentes = ?, 
                          direccion = ?, telefono = ?, correo = ?, activo = ? 
                      WHERE id_persona = ?"""
            data = (persona.nombre, persona.apellido_paterno, persona.apellido_materno, persona.nro_id,
                    persona.fecha_nacimiento, persona.edad, persona.sexo, persona.antecedentes, 
                    persona.direccion, persona.telefono, persona.correo, 1, persona.id_persona)
            
        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Actualizar_Dato_Paciente - Exitoso", "Se han actualizado los datos del paciente con éxito")
        return True
    except Exception as e:
        messagebox.showerror("Actualizar_Dato_Paciente - Error", f"Error al actualizar los datos del paciente: {e}")
        registrar_error(f"Actualizar_Dato_Paciente - Error al actualizar los datos del paciente: {e}")
        return False

def listar_personas():
    """Listar los pacientes registrados en la base de datos.
    Returns:
        list: Lista de tuplas con los datos de cada paciente.
    """
    lista_personas = []
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)
        query = "SELECT * FROM personas WHERE activo = 1"
        rows = QueriesSQLite.execute_read_query(conn, query)
        lista_personas = list(rows)
        return lista_personas
    except Exception as e:
        messagebox.showerror("Listar_Pacientes - Error", f"Error al listar los pacientes: {e}")
        registrar_error(f"Listar_Pacientes - Error al listar los pacientes: {e}")
        return []

def cargar_persona(where=""):
    """Cargar los datos de un paciente de la base de datos.
    Args:
        where (str): Condiciones para filtrar los datos del paciente.
    Returns:
        list: Lista de tuplas con los datos del paciente.
    """
    persona = []
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)
        query = "SELECT * FROM personas"
        
        # Si no se busca por nro_id, aplicar el filtro activo = 1
        if "nro_id =" not in where:
            query += " WHERE activo = 1"
        
        # Si hay condiciones adicionales, concatenarlas
        if where:
            if "nro_id =" in where:
                # Si se busca por nro_id, no aplicar activo = 1
                query += " WHERE " + where
            else:
                query += " AND " + where
        
        rows = QueriesSQLite.execute_read_query(conn, query)
        persona = list(rows)
        return persona
    except Exception as e:
        messagebox.showerror("Cargar_Persona - Error", f"Error al cargar los datos del paciente: {e}")
        registrar_error(f"Cargar_Persona - Error al cargar los datos del paciente: {e}")
        return None

def eliminar_persona(id_persona):
    """Eliminar un paciente de la base de datos.
    Args:
        id_persona (int): ID del paciente a eliminar.
    Returns:
        bool: True si se elimina correctamente, False en caso contrario.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)
        query = "UPDATE personas SET activo = 0 WHERE id_persona = ?"
        data = (id_persona,)
        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Eliminar_Persona - Exitoso", f"Se ha eliminado el paciente con exito.")
        return True
    except Exception as e:
        messagebox.showerror("Eliminar_Persona - Error", f"Error al eliminar el paciente: {e}")
        registrar_error(f"Eliminar_Persona - Error al eliminar el paciente: {e}")
        return False

class Persona:
    """Clase que representa a un paciente.
    Atributos:
        id_persona (int): ID del paciente.
        nombre (str): Nombre del paciente.
        apellido_paterno (str): Apellido paterno del paciente.
        apellido_materno (str): Apellido materno del paciente.
        nro_id (int): Nro. de identidad del paciente.
        fecha_nacimiento (date): Fecha de nacimiento del paciente.
        edad (int): Edad del paciente.
        sexo (str): Sexo del paciente.
        antecedentes (str): Antecedentes del paciente.
        direccion (str): Dirección del paciente.
        telefono (str): Número de teléfono del paciente.
        correo (str): Correo electrónico del paciente.
        activo (int): Estado del paciente (1: activo, 0: inactivo).
    """
    def __init__(self, nombre, apellido_paterno, apellido_materno, nro_id, fecha_nacimiento, 
                edad, sexo, antecedentes, direccion, telefono, correo, activo):
        self.id_persona = None
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nro_id = nro_id
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.sexo = sexo
        self.antecedentes = antecedentes
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.activo = activo

    def __str__(self):
        return f"Persona: ({self.nombre}, {self.apellido_paterno}, {self.apellido_materno}, \
                        {self.nro_id}, {self.fecha_nacimiento}, {self.edad}, {self.sexo}, \
                        {self.antecedentes}, {self.direccion}, {self.telefono}, {self.correo}, \
                        {self.activo})"