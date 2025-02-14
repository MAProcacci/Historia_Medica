from tkinter import messagebox
from sqlqueries import QueriesSQLite
from libreria import *


def guardar_historia_medica(id_persona, fecha_historia, motivo_consulta, examen_auxiliar, tratamiento, detalle, \
                            diagnostico, observaciones):
    """
    Guarda una nueva historia médica para un paciente especificado por su ID.
    Args:
        id_persona (int): ID del paciente.
        fecha_historia (date): Fecha de la historia médica.
        motivo_consulta (str): Motivo de la consulta.
        examen_auxiliar (str): Examen auxiliar.
        tratamiento (str): Tratamiento recomendado.
        detalle (str): Detalle de la historia médica.
        diagnostico (str): Diagnóstico de la historia médica.
        observaciones (str): Observaciones sobre la historia médica.
    Returns:
        bool: True si la historia médica se guardo correctamente, False otherwise.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)

        query = "INSERT INTO historia_medica (id_persona, fecha_historia, motivo_consulta, " \
                       "examen_auxiliar, tratamiento, detalle, diagnostico, observaciones) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data = (id_persona, fecha_historia, motivo_consulta, examen_auxiliar, tratamiento, detalle,
                diagnostico, observaciones)

        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Guardar_Historia_Medica - Exitoso", 
                            "Se ha guardado la historia médica del paciente con exito")
        return True
    except Exception as e:
        messagebox.showerror("Guardar_Historia_Medica - Error", f"Error al guardar la historia médica: {e}")
        registrar_error(f"Guardar_Historia_Medica - Error al guardar la historia médica: {e}")
        return False

def editar_historia_medica(id_historia, fecha_historia, motivo_consulta, examen_auxiliar, tratamiento, detalle, \
                            diagnostico, observaciones):
    """
    Edita una historia médica existente.
    Args:
        id_historia (int): ID de la historia médica.
        fecha_historia (date): Fecha de la historia médica.
        motivo_consulta (str): Motivo de la consulta.
        examen_auxiliar (str): Examen auxiliar.
        tratamiento (str): Tratamiento recomendado.
        detalle (str): Detalle de la historia médica.
        diagnostico (str): Diagnóstico de la historia médica.
        observaciones (str): Observaciones sobre la historia médica.
    Returns:
        bool: True si la historia médica se edito correctamente, False otherwise.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)

        query = "UPDATE historia_medica SET fecha_historia = ?, motivo_consulta = ?, examen_auxiliar = ?, " \
                "tratamiento = ?, detalle = ?, diagnostico = ?, observaciones = ? WHERE id_historia_medica = ?"
        data = (fecha_historia, motivo_consulta, examen_auxiliar, tratamiento, detalle, diagnostico, 
                observaciones, id_historia)

        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Editar_Historia_Medica - Exitoso", 
                            "Se ha editado la historia médica del paciente con exito")
        return True
    except Exception as e:
        messagebox.showerror("Editar_Historia_Medica - Error", f"Error al editar la historia médica: {e}")
        registrar_error(f"Editar_Historia_Medica - Error al editar la historia médica: {e}")
        return False

def eliminar_historia_medica(id_historia):
    """
    Elimina una historia médica existente.
    Args:
        id_historia (int): ID de la historia médica.
    Returns:
        bool: True si la historia médica se elimino correctamente, False otherwise.
    """
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)

        query = "DELETE FROM historia_medica WHERE id_historia_medica = ?"
        data = (id_historia,)

        QueriesSQLite.execute_query(conn, query, data)
        messagebox.showinfo("Eliminar_Historia_Medica - Exitoso", 
                            "Se ha eliminado la historia médica del paciente con exito")
        return True
    except Exception as e:
        messagebox.showerror("Eliminar_Historia_Medica - Error", f"Error al eliminar la historia médica: {e}")
        registrar_error(f"Eliminar_Historia_Medica - Error al eliminar la historia médica: {e}")
        return False

def listar_historia_medica(id_persona):
    """
    Listar todas las historias médicas de un paciente especificado por su ID.
    Args:
        id_persona (int): ID del paciente.
    Returns:
        list: Lista de tuplas con los datos de cada historia médica.
    """
    lista_historia = []
    try:
        conn = QueriesSQLite.create_connection(DB_NAME)
        query = "SELECT h.id_historia_medica, p.apellido_paterno || ' ' || p.apellido_materno AS Apellidos, \
                h.fecha_historia, h.motivo_consulta, h.examen_auxiliar, h.tratamiento, h.detalle, \
                h.diagnostico, h.observaciones FROM historia_medica h INNER JOIN personas p ON \
                p.id_persona = h.id_persona WHERE p.id_persona = ?"
        result = QueriesSQLite.execute_read_query(conn, query, (id_persona,))
        lista_historia = list(result)
        return lista_historia
    except Exception as e:
        messagebox.showerror("Listar_Historias_Medicas - Error", f"Error al listar las historias médicas: {e}")
        registrar_error(f"Listar_Historias_Medicas - Error al listar las historias médicas: {e}")
        return []

class HistoriaMedica:
    """Clase que representa una historia médica.
    Atributos:
        id_historia_medica (int): ID de la historia médica.
        id_persona (int): ID del paciente.
        fecha_historia (date): Fecha de la historia médica.
        motivo_consulta (str): Motivo de la consulta.
        examen_auxiliar (str): Examen auxiliar.
        tratamiento (str): Tratamiento recomendado.
        detalle (str): Detalle de la historia médica.
        diagnostico (str): Diagnóstico de la historia médica.
        observaciones (str): Observaciones sobre la historia médica.
    """
    def __init__(self, id_persona, fecha_historia, motivo_consulta, examen_auxiliar, tratamiento, detalle, \
                diagnostico, observaciones):
        self.id_historia_medica = None
        self.id_persona = id_persona
        self.fecha_historia = fecha_historia
        self.motivo_consulta = motivo_consulta
        self.examen_auxiliar = examen_auxiliar
        self.tratamiento = tratamiento
        self.detalle = detalle
        self.diagnostico = diagnostico
        self.observaciones = observaciones

    def __str__(self):
        return f"historiaMedica({self.id_historia_medica}, {self.id_persona}, {self.fecha_historia}, " \
               f"{self.motivo_consulta}, {self.examen_auxiliar}, {self.tratamiento}, {self.detalle}, " \
               f"{self.diagnostico}, {self.observaciones})"