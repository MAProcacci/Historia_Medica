import sqlite3
from contextlib import contextmanager
from sqlite3 import Error
from tkinter import messagebox
from libreria import *


class QueriesSQLite:
    """
    Clase para manejar la conexion a la base de datos SQLite.
    Atributos:
        connection (sqlite3.Connection): Conexion a la base de datos.
    """
    @staticmethod
    def create_connection(path):
        """
        Metodo para crear una conexion a la base de datos

        :param path: Ruta de la base de datos
        :return: Conexion a la base de datos
        """
        connection = None
        try:
            connection = sqlite3.connect(path)            
        except Error as e:
            messagebox.showerror("Create_Connection - Error", f"El error '{e}' a ocurrido")            
            registrar_error(f"Create_Connection - Error al crear la conexion: {e}")

        return connection

    @contextmanager
    def get_db_connection(path):
        """
        Metodo para obtener una conexion a la base de datos

        :param path: Ruta de la base de datos
        :return: Conexion a la base de datos

        # Modo de uso en el codigo:
        with get_db_connection(DB_NAME) as connection:
            query = "SELECT * FROM articulos"
            result = QueriesSQLite.execute_read_query(connection, query)
        """
        connection = None
        try:
            connection = sqlite3.connect(path)
            yield connection
        except Error as e:
            messagebox.showerror("Get_DB_Connection - Error", f"El error '{e}' a ocurrido")
            registrar_error(f"Get_DB_Connection - Error al crear la conexion: {e}")
        finally:
            if connection:
                connection.close()    

    @staticmethod
    def execute_query(connection, query, data_tuple):
        """
        Metodo para ejecutar una consulta SQL

        :param connection: Conexion a la base de datos
        :param query: Consulta SQL a ejecutar
        :param data_tuple: Parametros de la consulta
        :return: El ultimo ID insertado
        """
        cursor = connection.cursor()
        try:
            connection.execute("BEGIN TRANSACTION")
            cursor.execute(query, data_tuple)
            connection.commit()            
            return cursor.lastrowid            
        except Error as e:
            connection.rollback()
            messagebox.showerror("Execute_Query - Error", f"El error '{e}' a ocurrido")            
            registrar_error(f"Execute_Query - Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()            

    @staticmethod
    def execute_read_query(connection, query, data_tuple=()):
        """
        Metodo para ejecutar una consulta SQL

        :param connection: Conexion a la base de datos
        :param query: Consulta SQL a ejecutar
        :param data_tuple: Parametros de la consulta
        :return: Resultado de la consulta
        """
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query, data_tuple)
            result = cursor.fetchall()            
            return result
        except Error as e:
            messagebox.showerror("Execute_Read_Query - Error", f"El error '{e}' a ocurrido")
            registrar_error(f"Execute_Read_Query - Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()

    def create_tables():
        connection = QueriesSQLite.create_connection(DB_NAME)

        tabla_personas = """
        CREATE TABLE IF NOT EXISTS personas(
         id_persona INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         nombre TEXT NOT NULL,
         apellido_paterno TEXT,
         apellido_materno TEXT,
         nro_id INTEGER,
         fecha_nacimiento DATE,
         edad INTEGER,
         sexo TEXT,
         antecedentes TEXT,
         direccion TEXT,
         telefono TEXT,
         correo TEXT,
         activo INTEGER DEFAULT 1
        );
        """

        tabla_historia_medica = """
        CREATE TABLE IF NOT EXISTS historia_medica(
         id_historia_medica INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         id_persona INTEGER NOT NULL,
         fecha_historia DATE,
         motivo_consulta TEXT,
         examen_auxiliar TEXT,
         tratamiento TEXT,
         detalle TEXT,
         diagnostico TEXT,
         observaciones TEXT,
         FOREIGN KEY (id_persona) REFERENCES personas(id_persona)
        );
        """        

        tabla_configuracion = """
        CREATE TABLE IF NOT EXISTS configuracion(
         id INTEGER PRIMARY KEY,
         logo_empresa TEXT,
         nombre_empresa TEXT,
         direccion_empresa TEXT,
         telefono_empresa TEXT,
         correo_empresa TEXT,
         web_empresa TEXT,
         uso_margen_ganancia TEXT,
         impuesto REAL
        );
        """

        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios(
         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         username TEXT NOT NULL, 
         password TEXT NOT NULL         
        );
        """

        QueriesSQLite.execute_query(connection, tabla_personas, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_historia_medica, tuple())
        QueriesSQLite.execute_query(connection, tabla_configuracion, tuple())
        QueriesSQLite.execute_query(connection, tabla_usuarios, tuple())

    def eliminar_restriccion_unique():
        try:
            conn = QueriesSQLite.create_connection(DB_NAME)
            
            # Paso 1: Crear una nueva tabla sin la restricción UNIQUE
            crear_tabla_nueva = """
            CREATE TABLE ventas_nueva (
                factura INTEGER NOT NULL,
                cliente TEXT NOT NULL,
                articulo TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                costo REAL NOT NULL
            );
            """
            QueriesSQLite.execute_query(conn, crear_tabla_nueva, tuple())

            # Paso 2: Copiar los datos de la tabla original a la nueva tabla
            copiar_datos = """
            INSERT INTO ventas_nueva (factura, cliente, articulo, precio, cantidad, total, fecha, hora, costo)
            SELECT factura, cliente, articulo, precio, cantidad, total, fecha, hora, costo
            FROM ventas;
            """
            QueriesSQLite.execute_query(conn, copiar_datos, tuple())

            # Paso 3: Eliminar la tabla original
            eliminar_tabla_original = "DROP TABLE ventas;"
            QueriesSQLite.execute_query(conn, eliminar_tabla_original, tuple())

            # Paso 4: Renombrar la nueva tabla con el nombre de la tabla original
            renombrar_tabla = "ALTER TABLE ventas_nueva RENAME TO ventas;"
            QueriesSQLite.execute_query(conn, renombrar_tabla, tuple())

            messagebox.showinfo("Éxito", "La restricción UNIQUE ha sido eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la restricción UNIQUE: {e}")
            registrar_error(f"Error al eliminar la restricción UNIQUE: {e}")
        finally:
            if conn:
                conn.close()

if __name__=="__main__":
    connection = QueriesSQLite.create_connection(DB_NAME)

    # Crear las tablas
    QueriesSQLite.create_tables()
    

    """ Inicializar tablas de Impuestos """
    # Primero verificamos si la tabla está vacía
    verificar_vacia = """ SELECT COUNT(*) FROM configuracion; """
    cantidad = QueriesSQLite.execute_read_query(connection, verificar_vacia)[0][0]

    # Solo insertamos si la tabla está vacía (cantidad == 0)
    if cantidad == 0:
        crear_impuesto = """ INSERT INTO configuracion (impuesto) VALUES (?); """
        QueriesSQLite.execute_query(connection, crear_impuesto, (0.0,))
    
    """ Inicializar tabla de Usuarios """
    # Verificar si la tabla está vacía
    query_verificar_tabla = "SELECT COUNT(*) FROM usuarios;"
    resultado = QueriesSQLite.execute_read_query(connection, query_verificar_tabla)

    # Si la tabla está vacía (COUNT(*) == 0), insertar el usuario admin
    if resultado and resultado[0][0] == 0:
        usuario_tuple = ('admin', 'admin')
        crear_usuario = """
        INSERT INTO
            usuarios (username, password)
        VALUES
            (?,?);
        """
        QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
