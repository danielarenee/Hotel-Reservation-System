import mysql.connector
from datetime import datetime

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD", # change password
    database="reservacion_hoteles"
)

cursor = conexion.cursor()

# Condiciones de las habitaciones
tipos_habitaciones = ("Sencilla", "Doble", "Ejecutiva", "Suite", "Penthouse")
capacidad_habitacion = {"Sencilla": 2, "Doble": 4, "Ejecutiva": 2, "Suite": 4, "Penthouse": 6}

#FUNCIONES AUXILIARES

#formatear fecha
def formatear_fecha(fecha):
    return fecha.strftime('%Y-%m-%d') if isinstance(fecha, datetime) else fecha

#obtener nombre del huesped
def obtener_nombre_huesped(id_huesped):
    query = "SELECT nombre, apellido FROM Huesped WHERE idHuesped = %s"
    cursor.execute(query, (id_huesped,))
    huesped = cursor.fetchone()
    if huesped:
        return f"{huesped[0]} {huesped[1]}"
    return "Huésped desconocido"

# Validación de Empleado
def validar_empleado():
    print("\n--- Verificación de Empleado ---")
    id_empleado = input("Ingrese su ID de empleado de 4 dígitos: ")
    query = "SELECT * FROM Empleado WHERE idEmpleado = %s"
    cursor.execute(query, (id_empleado,))
    empleado = cursor.fetchone()
    if empleado:
        print(f"\nAcceso concedido. \033[1;33mBienvenido {empleado[1]} {empleado[2]}. \033[0m")
        return True
    else:
        print("ID de empleado no válido. Acceso denegado.")
        return False

#----------------------------------------------------------------------#

#FUNCIONES PRINCIPALES

# Selección de Hotel
def seleccionar_hotel():
    print("\n--- Selección de Hotel ---")
    query = "SELECT idHotel, nombre, calificacion_estrellas FROM Hotel"
    cursor.execute(query)
    hoteles = cursor.fetchall()

    for hotel in hoteles:
        print(f"ID: {hotel[0]} - Nombre: {hotel[1]:<20} \033[0;33m{' ★ ' * hotel[2]:<40}\033[0m")

    
    id_hotel = input("Ingrese el ID del hotel con el que desea trabajar: ")
    query_verificar = "SELECT * FROM Hotel WHERE idHotel = %s"
    cursor.execute(query_verificar, (id_hotel,))
    hotel = cursor.fetchone()
    if hotel:
        print(f"Trabajando con el hotel: {hotel[1]}")
        return id_hotel
    else:
        print("Hotel no encontrado. Intente de nuevo.")
        return seleccionar_hotel()

# Check-In
def realizar_checkin(id_hotel):
    print("\n--- Realizar Check-In ---")
    id_reserva = input("Ingrese el ID de la reservación: ")
    query = """
        SELECT R.idReservacion, R.tipo_habitacion, R.fecha_llegada, R.fecha_salida, R.Huesped_idHuesped, H.codigo_habitacion, H.estado_habitacion
        FROM Reservacion R
        JOIN Habitacion H ON R.idReservacion = H.Reservacion_idReservacion
        WHERE R.idReservacion = %s AND R.Hotel_idHotel = %s
    """
    cursor.execute(query, (id_reserva, id_hotel))
    resultado = cursor.fetchone()
    
    if resultado:
        id_reservacion, tipo_habitacion, fecha_llegada, fecha_salida, id_huesped, codigo_habitacion, estado_habitacion = resultado
        nombre_huesped = obtener_nombre_huesped(id_huesped)
        print(f"Reservación encontrada: ID: {id_reservacion}, Tipo: {tipo_habitacion}, "
              f"Desde: {formatear_fecha(fecha_llegada)}, Hasta: {formatear_fecha(fecha_salida)}, "
              f"A nombre de: {nombre_huesped}, Habitación asignada: {codigo_habitacion}, Estado actual: {estado_habitacion}")
        
        if estado_habitacion == 'Reservada':
            query_update = """
                UPDATE Habitacion
                SET estado_habitacion = 'Ocupada'
                WHERE codigo_habitacion = %s AND Hotel_idHotel = %s
            """
            cursor.execute(query_update, (codigo_habitacion, id_hotel))
            conexion.commit()
            print("Check-In realizado con éxito.")
        else:
            print("La habitación no está en estado 'Reservada'. No se puede realizar el Check-In.")
    else:
        print("No se encontró una reservación con ese ID para este hotel.")



# Check-Out
def realizar_checkout(id_hotel):
    print("\n--- Realizar Check-Out ---")
    codigo_habitacion = input("Ingrese el código de la habitación: ")
    query_select = """
        SELECT H.Reservacion_idReservacion, R.tipo_habitacion, R.fecha_llegada, R.fecha_salida, R.Huesped_idHuesped, H.estado_habitacion
        FROM Habitacion H
        JOIN Reservacion R ON H.Reservacion_idReservacion = R.idReservacion
        WHERE H.codigo_habitacion = %s AND H.Hotel_idHotel = %s
    """
    cursor.execute(query_select, (codigo_habitacion, id_hotel))
    resultado = cursor.fetchone()
    
    if resultado:
        id_reservacion, tipo_habitacion, fecha_llegada, fecha_salida, id_huesped, estado_habitacion = resultado
        nombre_huesped = obtener_nombre_huesped(id_huesped)
        print(f"Reservación encontrada: ID: {id_reservacion}, Tipo: {tipo_habitacion}, "
              f"Desde: {formatear_fecha(fecha_llegada)}, Hasta: {formatear_fecha(fecha_salida)}, "
              f"A nombre de: {nombre_huesped}, Estado actual: {estado_habitacion}")
        
        if estado_habitacion == 'Ocupada':
            query_update = """
                UPDATE Habitacion
                SET estado_habitacion = 'Disponible', Reservacion_idReservacion = NULL
                WHERE codigo_habitacion = %s AND Hotel_idHotel = %s
            """
            cursor.execute(query_update, (codigo_habitacion, id_hotel))
            conexion.commit()
            print("Check-Out realizado. Habitación ahora está disponible.")
        else:
            print("La habitación no está en estado 'Ocupada'. No se puede realizar el Check-Out.")
    else:
        print("No se encontró una reservación asociada a esta habitación.")



# Registrar Reservación
def registrar_reservacion(id_hotel, tipos_habitaciones, capacidad_habitacion):
    print("\n--- Registrar Reservación ---")

    # Crear el huésped
    print("\n--- Datos del Huésped ---")

    nombre = input("Nombre del huésped: ")
    apellido = input("Apellido del huésped: ")
    num_tel = input("Número de teléfono: ")
    correo = input("Correo electrónico: ")
    
    query_huesped = """
        INSERT IGNORE INTO Huesped (nombre, apellido, num_tel, correo)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_huesped, (nombre, apellido, num_tel, correo))
    conexion.commit()

    id_huesped_generado = cursor.lastrowid
    print(f"Huésped registrado exitosamente. ID del huésped: {id_huesped_generado}")

    # Crear la reservación
    print("\n--- Datos de la Reservación ---")

    tipo_habitacion = input("Tipo de habitación (Sencilla, Doble, Ejecutiva, Suite o Penthouse): ") # Checar la información
    while tipo_habitacion not in tipos_habitaciones:
        print(f"No existe la habitación tipo: \'{tipo_habitacion}\'. Intente de nuevo.\n")
        tipo_habitacion = input("Tipo de habitación (Sencilla, Doble, Ejecutiva, Suite o Penthouse): ")

    num_huespedes = int(input("Número de huéspedes: "))
    while num_huespedes > capacidad_habitacion[tipo_habitacion] or num_huespedes <= 0:
        print(f"{tipo_habitacion} no tiene la capacidad seleccionada. Intente de nuevo.\n")
        num_huespedes = int(input("Número de huéspedes: "))

    fecha_actual = datetime.now()
    fecha_llegada = input("Fecha de llegada (YYYY-MM-DD): ")
    fecha_salida = input("Fecha de salida (YYYY-MM-DD): ")
    fecha_llegada_frm = datetime.strptime(fecha_llegada, "%Y-%m-%d")
    fecha_salida_frm = datetime.strptime(fecha_salida, "%Y-%m-%d")

    while fecha_llegada_frm <= fecha_actual or fecha_llegada_frm >= fecha_salida_frm:
        print("Las fechas tienen un error. Intente de nuevo.\n")

        fecha_llegada = input("Fecha de llegada (YYYY-MM-DD): ")
        fecha_salida = input("Fecha de salida (YYYY-MM-DD): ")
        fecha_llegada_frm = datetime.strptime(fecha_llegada, "%Y-%m-%d")
        fecha_salida_frm = datetime.strptime(fecha_salida, "%Y-%m-%d")


    # Buscar una habitación disponible
    query_habitacion = """
        SELECT idHabitacion, codigo_habitacion 
        FROM Habitacion 
        WHERE Hotel_idHotel = %s AND tipo_habitacion = %s AND estado_habitacion = 'Disponible'
        LIMIT 1
    """
    cursor.execute(query_habitacion, (id_hotel, tipo_habitacion))
    habitacion_disponible = cursor.fetchone()

    if not habitacion_disponible:
        print("No hay habitaciones disponibles para este tipo.")
        return

    id_habitacion, codigo_habitacion = habitacion_disponible
    print(f"Habitación asignada: {codigo_habitacion}")

    query_reservacion = """
        INSERT INTO Reservacion 
        (tipo_habitacion, num_huespedes, fecha_llegada, fecha_salida, Huesped_idHuesped, Hotel_idHotel)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores_reservacion = (tipo_habitacion, num_huespedes, fecha_llegada, fecha_salida, id_huesped_generado, id_hotel)
    cursor.execute(query_reservacion, valores_reservacion)
    conexion.commit()

    id_reservacion_generado = cursor.lastrowid

    # Actualizar la habitación con la reservación y establecer su estado como 'Reservada'
    query_update_habitacion = """
        UPDATE Habitacion
        SET estado_habitacion = 'Reservada', Reservacion_idReservacion = %s
        WHERE idHabitacion = %s
    """
    cursor.execute(query_update_habitacion, (id_reservacion_generado, id_habitacion))
    conexion.commit()

    print(f"\033[0;31mReservación registrada exitosamente\033[0m. ID de la reservación: {id_reservacion_generado}, Habitación asignada: {codigo_habitacion}")

# Modificar Reservación
def modificar_reservacion(id_hotel):
    print("\n--- Modificar Reservación ---")
    id_reserva = input("Ingrese el ID de la reservación a modificar: ")
    query = """
        SELECT * FROM Reservacion 
        WHERE idReservacion = %s AND Hotel_idHotel = %s
    """
    cursor.execute(query, (id_reserva, id_hotel))
    reservacion = cursor.fetchone()
    
    if reservacion:
        nombre_huesped = obtener_nombre_huesped(reservacion[6])  # Obtener nombre del huésped
        print(f"Reservación encontrada: ID: {reservacion[0]}, Tipo: {reservacion[1]}, "
              f"Desde: {formatear_fecha(reservacion[3])}, Hasta: {formatear_fecha(reservacion[4])}, "
              f"A nombre de: {nombre_huesped}")
        
        print("\n--- Opciones de Modificación ---")
        print("1. Tipo de Habitación")
        print("2. Fecha de Llegada")
        print("3. Fecha de Salida")
        print("4. Número de Huéspedes")
        opcion = input("Seleccione el campo que desea modificar (1-4): ")
        
        campos = {
            '1': 'tipo_habitacion',
            '2': 'fecha_llegada',
            '3': 'fecha_salida',
            '4': 'num_huespedes'
        }

        if opcion in campos:
            campo = campos[opcion]
            nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
            
            # Validación adicional para fechas
            if campo in ['fecha_llegada', 'fecha_salida']:
                try:
                    datetime.strptime(nuevo_valor, '%Y-%m-%d')  # Verificar formato de fecha
                except ValueError:
                    print("El formato de la fecha debe ser YYYY-MM-DD. Intente de nuevo.")
                    return
            
            query_update = f"""
                UPDATE Reservacion
                SET {campo} = %s
                WHERE idReservacion = %s AND Hotel_idHotel = %s
            """
            cursor.execute(query_update, (nuevo_valor, id_reserva, id_hotel))
            conexion.commit()
            print("Reservación modificada exitosamente.")
        else:
            print("Opción no válida. Intente de nuevo.")
    else:
        print("No se encontró la reservación para este hotel.")

# Cancelar Reservación
def cancelar_reservacion(id_hotel):
    print("\n--- Cancelar Reservación ---")
    id_reserva = input("Ingrese el ID de la reservación a cancelar: ")
    query = """
        SELECT * FROM Reservacion 
        WHERE idReservacion = %s AND Hotel_idHotel = %s
    """
    cursor.execute(query, (id_reserva, id_hotel))
    reservacion = cursor.fetchone()
    
    if reservacion:
        nombre_huesped = obtener_nombre_huesped(reservacion[6])
        print(f"Reservación encontrada: ID: {reservacion[0]}, Tipo: {reservacion[1]}, "
              f"Desde: {formatear_fecha(reservacion[3])}, Hasta: {formatear_fecha(reservacion[4])}, "
              f"A nombre de: {nombre_huesped}")
        
        correo_ingresado = input("Ingrese el correo electrónico asociado a la reservación para confirmar: ")
        query_correo = "SELECT correo FROM Huesped WHERE idHuesped = %s"
        cursor.execute(query_correo, (reservacion[6],))
        correo_huesped = cursor.fetchone()[0]
        
        if correo_ingresado.strip().lower() == correo_huesped.strip().lower():
            query_update = """
                UPDATE Reservacion
                SET estado = 'cancelada'
                WHERE idReservacion = %s
            """
            cursor.execute(query_update, (id_reserva,))
            conexion.commit()
            print("Reservación cancelada exitosamente.")
        else:
            print("El correo electrónico no coincide. No se puede cancelar la reservación.")
    else:
        print("No se encontró una reservación con ese ID para este hotel.")

# Consultar Estado de Habitaciones
def consultar_estado_habitaciones(id_hotel):
    if not validar_empleado():
        return
    print("\n--- Consultar Estado de Habitaciones ---")
    query = """
        SELECT H.codigo_habitacion, H.estado_habitacion, H.tipo_habitacion, H.precio_noche, R.Huesped_idHuesped 
        FROM Habitacion H
        LEFT JOIN Reservacion R ON H.Reservacion_idReservacion = R.idReservacion
        WHERE H.Hotel_idHotel = %s
    """
    cursor.execute(query, (id_hotel,))
    habitaciones = cursor.fetchall()

    # Contar el número de habitaciones
    query_count = """
        SELECT estado_habitacion, COUNT(*) AS cantidad
        FROM Habitacion
        WHERE Hotel_idHotel = %s
        GROUP BY estado_habitacion
    """
    cursor.execute(query_count, (id_hotel,))
    disponibilidad_conteo = cursor.fetchall()

    if habitaciones:
        print("\nEstado de las habitaciones:")
        for habitacion in habitaciones:
            codigo = habitacion[0]
            estado = habitacion[1]
            tipo = habitacion[2]
            precio = habitacion[3]
            id_huesped = habitacion[4]

            if estado == 'Reservada':
                nombre_huesped = obtener_nombre_huesped(id_huesped)
                print(f"Código: {codigo}, Estado: {estado}, (Esperando Check-In), Tipo: {tipo}, Precio: ${precio}, Reservada por: {nombre_huesped}")
            elif estado == 'Ocupada' and id_huesped:
                nombre_huesped = obtener_nombre_huesped(id_huesped)
                print(f"Código: {codigo}, Estado:  \033[0;31m  {estado} (En uso) \033[0m, Tipo: {tipo}, Precio: ${precio}, Ocupada por: {nombre_huesped}")
            else:
                print(f"Código: {codigo}, Estado: \033[0;32m {estado} \033[0m, Tipo: {tipo}, Precio: ${precio}, No ocupada")
        
        print("\n")
        print(f"{'Estado':<15} {'Cantidad':<10}") # Encabezados
        print("-" * 25)
        for estado, cantidad in disponibilidad_conteo:
            print(f"{estado:<15} {cantidad:<10}")

    else:
        print("No hay habitaciones registradas para este hotel.")

# Consultar Reservaciones Activas
def consultar_reservaciones_activas(id_hotel):
    if not validar_empleado():
        return
    print("\n--- Consultar Reservaciones Activas ---")
    query = """
        SELECT idReservacion, tipo_habitacion, fecha_llegada, fecha_salida, Huesped_idHuesped
        FROM Reservacion
        WHERE Hotel_idHotel = %s AND estado = 'activa'
    """
    cursor.execute(query, (id_hotel,))
    reservaciones = cursor.fetchall()
    if reservaciones:
        print("\nReservaciones Activas:")
        for reservacion in reservaciones:
            id_reservacion, tipo_habitacion, fecha_llegada, fecha_salida, id_huesped = reservacion
            fecha_llegada_str = formatear_fecha(fecha_llegada)
            fecha_salida_str = formatear_fecha(fecha_salida)
            nombre_huesped = obtener_nombre_huesped(id_huesped)
            print(f"ID: {id_reservacion}, Tipo: {tipo_habitacion}, Llegada: {fecha_llegada_str}, Salida: {fecha_salida_str}, A nombre de: {nombre_huesped}")
    else:
        print("No hay reservaciones activas para este hotel.")

# Menú Principal
def menu_principal(id_hotel):
    while True:
        print("\n--- Sistema de Gestión de Hotel ---")
        print("1. Realizar Check-In")
        print("2. Realizar Check-Out")
        print("3. Registrar Reservación")
        print("4. Modificar Reservación")
        print("5. Cancelar Reservación")
        print("6. Consultar Estado de Habitaciones")
        print("7. Consultar Reservaciones Activas")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            realizar_checkin(id_hotel)
        elif opcion == '2':
            realizar_checkout(id_hotel)
        elif opcion == '3':
            registrar_reservacion(id_hotel, tipos_habitaciones, capacidad_habitacion)
        elif opcion == '4':
            modificar_reservacion(id_hotel)
        elif opcion == '5':
            cancelar_reservacion(id_hotel)
        elif opcion == '6':
            consultar_estado_habitaciones(id_hotel)
        elif opcion == '7':
            consultar_reservaciones_activas(id_hotel)
        elif opcion == '8':
            print("\n \033[1;36m Gracias por usar el sistema. ¡Hasta luego! \033[0m\n\n")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

# Inicio del programa
id_hotel = seleccionar_hotel()
menu_principal(id_hotel)

cursor.close()
conexion.close()
