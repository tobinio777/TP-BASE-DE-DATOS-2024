import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import os 
def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Biblioteca'
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL")
        return conexion
    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None
    
def ejecutar_query(conexion, query, datos=None):
    cursor = conexion.cursor()
    try:
        if datos:
            cursor.execute(query, datos)
        else:
            cursor.execute(query)
        conexion.commit()
        print("Operación realizada con éxito")
    except Error as error:
        print(f"Error en la operación: {error}")
    finally:
        cursor.close()

def menu_principal(conexion):
    while True:
        limpiar_pantalla()
        print("\nMenu Principal")
        print("1) Usuarios")
        print("2) Libros")
        print("3) Préstamos")
        print("4) Visualizar tablas")
        print("5) Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_usuarios(conexion)
        elif opcion == '2':
            menu_libros(conexion)
        elif opcion == '3':
            menu_prestamos(conexion)
        elif opcion == '4':
            menu_tablas(conexion)
        elif opcion == '5':
            limpiar_pantalla()
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

def menu_usuarios(conexion):
    tabla_usuarios(conexion)  
    while True:
        print("\nMenú Usuarios")
        print("a) Crear Usuario")
        print("b) Actualizar Usuario")
        print("c) Borrar Usuario")
        print("d) Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == 'a':
            crear_usuario(conexion)
        elif opcion == 'b':
            actualizar_usuario(conexion)
        elif opcion == 'c':
            inactivar_usuario(conexion)
        elif opcion == 'd':
            break
        else:
            print("Opción no válida, intente de nuevo.")

def tabla_usuarios(conexion):
    query = """
    CREATE TABLE IF NOT EXISTS USUARIOS (
        id INT NOT NULL AUTO_INCREMENT,
        nombre_completo VARCHAR(25) NOT NULL,
        dni VARCHAR(8) NOT NULL UNIQUE,
        telefono VARCHAR(16) NOT NULL UNIQUE,
        email VARCHAR(60) NOT NULL UNIQUE,
        creado_el TIMESTAMP DEFAULT NOW(),
        actualizado_el TIMESTAMP DEFAULT NOW(),
        estado TINYINT DEFAULT 1,
        PRIMARY KEY(id)
    );
    """
    ejecutar_query(conexion, query)

def crear_usuario(conexion):
        nombre = input("Ingrese el nombre completo: ")
        dni = input("Ingrese el DNI: ")
        telefono = input("Ingrese el teléfono: ")
        email = input("Ingrese el email: ")
    
        query = """
                    INSERT INTO USUARIOS (nombre_completo, dni, telefono, email)
                    VALUES (%s, %s, %s, %s);
                """
    
        ejecutar_query(conexion, query, (nombre, dni, telefono, email))

def actualizar_usuario(conexion):
        visualizar_tabla_usuarios(conexion)
        id_usuario = int(input("Ingrese el ID del usuario a actualizar: "))
        cursor = conexion.cursor()
        cursor.execute("SELECT estado FROM USUARIOS WHERE id = %s", (id_usuario,))
        usuario_estado = cursor.fetchone()
        if usuario_estado[0] == 0:
            pregunta=input("El usuario está inactivo ¿Desea reactivarlo? S/N: ")
            if pregunta == 'S':
                    query = """
                        UPDATE USUARIOS
                        SET estado = 1
                        WHERE id = %s;
                    """
                    ejecutar_query(conexion, query, (id_usuario,))
            elif pregunta != 'S':
                print("Entendido,prosigamos")
        nuevo_nombre = input("Ingrese el nuevo nombre a actualizar: ")
        nuevo_dni = input("Ingrese el nuevo DNI a actualizar: ")
        nuevo_telefono = input("Ingrese el nuevo teléfono: ")
        nuevo_email = input("Ingrese el nuevo email: ")
        query = """
                    UPDATE USUARIOS
                    SET nombre_completo = %s,dni = %s,telefono = %s, email = %s, actualizado_el = NOW()
                    WHERE id = %s;
                """
        ejecutar_query(conexion, query, (nuevo_nombre,nuevo_dni,nuevo_telefono, nuevo_email, id_usuario))

def inactivar_usuario(conexion):
        id_usuario = int(input("Ingrese el ID del usuario a inactivar: "))
        query = """
                    UPDATE USUARIOS
                    SET estado = 0
                    WHERE id = %s;
                """
        ejecutar_query(conexion, query, (id_usuario,))

def menu_libros(conexion):
    tabla_libros(conexion)  
    while True:
        print("\nMenú Libros")
        print("a) Agregar Libro")
        print("b) Actualizar Libro")
        print("c) Borrar Libro")
        print("d) Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            print("Estos son los generos disponibles:")
            visualizar_tabla_generos(conexion)
            print("¿Desea agregar algun genero?")
            respuesta=input ("S/N:")
            if respuesta== 's':
                tabla_generos(conexion)
                genero=input("inserta el genero del libro:")
                query="""
                        INSERT INTO generos_libro(genero)
                        VALUES(%s)
                    """
                ejecutar_query(conexion, query, (genero,))                       
                agregar_libro(conexion)
            elif respuesta != 's':
                 agregar_libro(conexion) 
        elif opcion == 'b':
            actualizar_libro(conexion)
        elif opcion == 'c':
            inactivar_libro(conexion)
        elif opcion == 'd':
            break
        else:
            print("Opción no válida, intente de nuevo.")

def tabla_libros(conexion):
    query = """
    CREATE TABLE IF NOT EXISTS LIBROS (
        id INT NOT NULL AUTO_INCREMENT,
        nombre_libro VARCHAR(40) NOT NULL,
        autor VARCHAR(25),
        fecha_lanzamiento VARCHAR(10) NOT NULL,
        id_genero INT,
        creado_el TIMESTAMP DEFAULT NOW(),
        actualizado_el TIMESTAMP DEFAULT NOW(),
        estado TINYINT DEFAULT 1,
        PRIMARY KEY(id),
        CONSTRAINT fk_generos FOREIGN KEY (id_genero) REFERENCES generos_libro(id)
    );
    """
    ejecutar_query(conexion, query)
def tabla_generos(conexion):
    query = """
        CREATE TABLE IF NOT EXISTS generos_libro (
        id INT NOT NULL AUTO_INCREMENT,
        genero VARCHAR(20) NOT NULL,
        PRIMARY KEY(id)
        );
        """
    ejecutar_query(conexion, query)

def agregar_libro(conexion):
        nombre_libro = input("Ingrese el nombre del libro: ")
        autor = input("Ingrese el autor del libro: ")
        fecha_lanzamiento = input("Ingrese la fecha de lanzamiento (AAAA-MM-DD): ")
        visualizar_tabla_generos(conexion)
        id_genero = int(input("Ingrese el ID del género del libro: "))
        query = """
                    INSERT INTO LIBROS (nombre_libro, autor, fecha_lanzamiento, id_genero)
                    VALUES (%s, %s, %s, %s);
                """
        ejecutar_query(conexion, query, (nombre_libro, autor, fecha_lanzamiento, id_genero))

def actualizar_libro(conexion):
        visualizar_tabla_libros(conexion)
        id_libro = int(input("Ingrese el ID del libro a actualizar: "))
        cursor = conexion.cursor()
        cursor.execute("SELECT estado FROM LIBROS WHERE id = %s", (id_libro,))
        libro_estado = cursor.fetchone()
        if libro_estado[0] == 0:
            pregunta=input("El libro está inactivo ¿Desea reactivarlo? S/N: ")
            if pregunta == 'S':
                query = """
                    UPDATE LIBROS
                    SET estado = 1
                    WHERE id = %s;
                """
                ejecutar_query(conexion, query, (id_libro,))
            elif pregunta != 'S':
                print("Entendido,prosigamos")
        nuevo_nombre = input("Ingrese el nuevo nombre del libro: ")
        nuevo_autor = input("Ingrese el nuevo autor: ")
        nueva_fecha_lanzamiento = input(" Ingrese la nueva fecha de lanzamieto (AAAA-MM-DD): ")
        nuevo_id_genero = int(input("Ingrese el nuevo id de genero al que corresponda el libro: "))
        query = """
                    UPDATE LIBROS
                    SET nombre_libro = %s, autor = %s, actualizado_el = NOW()
                    WHERE id = %s;
                """
        ejecutar_query(conexion, query, (nuevo_nombre, nuevo_autor,nueva_fecha_lanzamiento,nuevo_id_genero, id_libro))

def inactivar_libro(conexion):
        id_libro = int(input("Ingrese el ID del libro a inactivar: "))
        query = """
                    UPDATE LIBROS
                    SET estado = 0
                    WHERE id = %s;
                """
        ejecutar_query(conexion, query, (id_libro,))



def menu_prestamos(conexion):
    tabla_prestamos(conexion)  
    while True:
        print("\nMenú Préstamos")
        print("a) Crear Préstamo")
        print("b) Actualizar Préstamo")
        print("c) Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            crear_prestamo(conexion)
        elif opcion == 'b':
            actualizar_prestamo(conexion)
        elif opcion == 'c':
            break
        else:
            print("Opción no válida, intente de nuevo.")

def tabla_prestamos(conexion):
    query = """
    CREATE TABLE IF NOT EXISTS PRESTAMOS (
        id INT NOT NULL AUTO_INCREMENT,
        usuario_id INT NOT NULL,
        libro_id INT NOT NULL,
        fecha_prestamo TIMESTAMP DEFAULT NOW(),
        fecha_devolucion_estimada TIMESTAMP DEFAULT NOW(),
        fecha_devolucion_real TIMESTAMP,
        PRIMARY KEY(id),
        CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        CONSTRAINT fk_libro FOREIGN KEY (libro_id) REFERENCES libros(id)
    );
    """
    ejecutar_query(conexion, query)

def crear_prestamo(conexion):
        usuario_id = int(input("Ingrese el ID del usuario que pide el préstamo: "))
        libro_id = int(input("Ingrese el ID del libro a prestar: "))
        cursor = conexion.cursor()
        cursor.execute("SELECT estado FROM USUARIOS WHERE id = %s", (usuario_id,))
        usuario_estado = cursor.fetchone()
        cursor.execute("SELECT estado FROM LIBROS WHERE id = %s", (libro_id,))
        libro_estado = cursor.fetchone()
    
        if usuario_estado[0] == 0:
            print("El usuario está inactivo y no puede pedir un préstamo.")
            return
        if libro_estado[0] == 0:
            print("El libro está inactivo y no puede ser prestado.")
            return
        fecha_prestamo = datetime.now()
        fecha_devolucion_estimada = fecha_prestamo + timedelta(days=7)

        query = """
                    INSERT INTO PRESTAMOS (usuario_id, libro_id, fecha_prestamo, fecha_devolucion_estimada)
                    VALUES (%s, %s, %s, %s);
                """
        ejecutar_query(conexion, query, (usuario_id, libro_id, fecha_prestamo, fecha_devolucion_estimada))

def actualizar_prestamo(conexion):
        visualizar_tabla_prestamos(conexion)
        prestamo_id = int(input("Ingrese el ID del préstamo a actualizar: "))
        fecha_devolucion_real = input("Ingrese la fecha de devolución real (YYYY-MM-DD): ")
        fecha_devolucion_real = datetime.strptime(fecha_devolucion_real, '%Y-%m-%d')

        cursor = conexion.cursor()
        cursor.execute("SELECT usuario_id, fecha_devolucion_estimada FROM PRESTAMOS WHERE id = %s", (prestamo_id,))
        prestamo_info = cursor.fetchone()
        usuario_id = prestamo_info[0]
        fecha_devolucion_estimada = prestamo_info[1]

        if fecha_devolucion_real > fecha_devolucion_estimada:
            query_usuario_inactivo = "UPDATE USUARIOS SET estado = 0 WHERE id = %s"
            ejecutar_query(conexion, query_usuario_inactivo, (usuario_id,))
            print("El usuario ha devuelto fuera de término y ha sido inactivado.")

            query = """
                        UPDATE PRESTAMOS
                        SET fecha_devolucion_real = %s
                        WHERE id = %s;
                    """
            ejecutar_query(conexion, query, (fecha_devolucion_real, prestamo_id))

def menu_tablas(conexion):
    while True:
        print("¿Que tabla desea visualizar?")
        print("1)Tabla de usuarios")
        print("2)Tabla de libros")
        print("3)Tabla de prestamos")
        print("4)volver al menu principal")
        opcion=input("Elija una opcion:")
        if opcion=='1':
            visualizar_tabla_usuarios(conexion)
        elif opcion=='2':
            visualizar_tabla_libros(conexion)
        elif opcion=='3':
            visualizar_tabla_prestamos(conexion)
        elif opcion=='4':
            break
        else:
                print("Opción no válida, intente de nuevo.")



def visualizar_tabla_usuarios(conexion):
    """Visualiza la tabla USUARIOS."""
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM USUARIOS")
        usuarios = cursor.fetchall()
        print("\nTabla: USUARIOS")
        print(f"{'ID':<5} {'Nombre Completo':<25} {'DNI':<10} {'Teléfono':<15} {'Email':<40} {'Creado El':<20} {'Actualizado El':<20} {'Estado':<7}")
        print("-" * 150)
        for usuario in usuarios:
            creado_el = usuario[5].strftime('%Y-%m-%d %H:%M:%S') if usuario[5] else "N/A"
            actualizado_el = usuario[6].strftime('%Y-%m-%d %H:%M:%S') if usuario[6] else "N/A"
            print(f"{usuario[0]:<5} {usuario[1]:<25} {usuario[2]:<10} {usuario[3]:<15} {usuario[4]:<40} {creado_el:<20} {actualizado_el:<20} {usuario[7]:<7}")
    except Error as e:
        print(f"Error al visualizar tabla USUARIOS: {e}")

def visualizar_tabla_libros(conexion):
    """Visualiza la tabla LIBROS junto con el género desde GENEROS_LIBRO."""
    try:
        cursor = conexion.cursor()
        query = """
            SELECT LIBROS.id, LIBROS.nombre_libro, LIBROS.autor, LIBROS.fecha_lanzamiento,
                   GENEROS_LIBRO.genero, LIBROS.creado_el, LIBROS.actualizado_el, LIBROS.estado
            FROM LIBROS
            LEFT JOIN GENEROS_LIBRO ON LIBROS.id_genero = GENEROS_LIBRO.id
        """
        cursor.execute(query)
        libros = cursor.fetchall()
        print("\nTabla: LIBROS")
        print(f"{'ID':<5} {'Nombre del Libro':<40} {'Autor':<25} {'Fecha Lanzamiento':<20} {'Género':<20} {'Creado El':<20} {'Actualizado El':<20} {'Estado':<7}")
        print("-" * 160)
        for libro in libros:
            creado_el = libro[5].strftime('%Y-%m-%d %H:%M:%S') if libro[5] else "N/A"
            actualizado_el = libro[6].strftime('%Y-%m-%d %H:%M:%S') if libro[6] else "N/A"
            print(f"{libro[0]:<5} {libro[1]:<40} {libro[2]:<25} {libro[3]:<20} {libro[4]:<20} {creado_el:<20} {actualizado_el:<20} {libro[7]:<7}")
    except Error as e:
        print(f"Error al visualizar tabla LIBROS: {e}")



def visualizar_tabla_prestamos(conexion):
    """Visualiza la tabla PRESTAMOS."""
    try:
        cursor = conexion.cursor()
        query = """
            SELECT PRESTAMOS.id, USUARIOS.nombre_completo, LIBROS.nombre_libro, 
                   PRESTAMOS.fecha_prestamo, PRESTAMOS.fecha_devolucion_estimada, 
                   PRESTAMOS.fecha_devolucion_real
            FROM PRESTAMOS
            JOIN USUARIOS ON PRESTAMOS.usuario_id = USUARIOS.id
            JOIN LIBROS ON PRESTAMOS.libro_id = LIBROS.id
        """
        cursor.execute(query)
        prestamos = cursor.fetchall()
        print("\nTabla: PRESTAMOS")
        print(f"{'ID':<5} {'Usuario':<25} {'Libro':<40} {'Fecha Préstamo':<20} {'Fecha Estimada':<20} {'Fecha Real':<20}")
        print("-" * 140)
        for prestamo in prestamos:
            fecha_prestamo = prestamo[3].strftime('%Y-%m-%d %H:%M:%S') if prestamo[3] else "N/A"
            fecha_devolucion_estimada = prestamo[4].strftime('%Y-%m-%d %H:%M:%S') if prestamo[4] else "N/A"
            fecha_devolucion_real = prestamo[5].strftime('%Y-%m-%d %H:%M:%S') if prestamo[5] else "N/A"
            print(f"{prestamo[0]:<5} {prestamo[1]:<25} {prestamo[2]:<40} {fecha_prestamo:<20} {fecha_devolucion_estimada:<20} {fecha_devolucion_real:<20}")
    except Error as e:
        print(f"Error al visualizar tabla PRESTAMOS: {e}")

def visualizar_tabla_generos(conexion):
    """Visualiza la tabla GENEROS_LIBRO."""
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM generos_libro")
        generos = cursor.fetchall()
        print("\nTabla: GENEROS_LIBRO")
        print(f"{'ID':<5} {'Género':<20}")
        print("-" * 30)  
        for genero in generos:
            print(f"{genero[0]:<5} {genero[1]:<20}")
    except Error as e:
        print(f"Error al visualizar tabla GENEROS_LIBRO: {e}")



def limpiar_pantalla():
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')

conexion = crear_conexion()
if conexion:
    menu_principal(conexion)
    conexion.close()