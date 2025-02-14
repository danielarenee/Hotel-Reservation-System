import mysql.connector # Importar librería para realizar la conexión con SQL

# Conexión a la base de datos (se deben pasar los datos para que pueda ingresar)
conexion = mysql.connector.connect(
  host="localhost",
  user="root",
  password="PASSWORD", # Change password!
  database="reservacion_hoteles",
  auth_plugin='mysql_native_password'
)

print(conexion)  # La conexión se realizó exitosamente
cursor = conexion.cursor() # Permite usar los comandos de SQL (SELECT, INSERT, UPDATE, DELETE), se usa mucho

#### Ingresar valores a la tabla huesped
tabla_huesped = """
REPLACE INTO Huesped (idHuesped, nombre, apellido, num_tel, correo)
VALUES (%s, %s, %s, %s, %s)
"""
# registros huesped
tuplas_huesped = [
  (1, 'María', 'López Ramírez', '12 34 56 78 00', 'marialo@gmail.com'),
  (2, 'Raúl Alejandro', 'Ocasio Ruiz', '32 45 76 10 23', 'rauw_ale@hotmail.com'),
  (3, 'Luis Eduardo', 'Blanco Castañeda', '22 53 46 95 45', 'luis_eduard@yahoo.com'),
  (4, "Alan David", 'Peña Aguilar', '22 34 54 19 53', 'david_alan05@gmail.com'),
  (5, "Diego", 'Ramos Crespo', '22 24 25 80 58', 'diegorcone@gmail.com'),
  (6, "Daniela Renée", 'Ramírez Gutiérrez', '22 65 23 23 09', 'daniela_rg@yahoo.com'),
  (7, "Sofía", 'Martínez Gómez', '55 12 34 56 78', 'sofia_ma@hotmail.com'),
  (8, "Fernando", 'García López', '55 23 45 67 89', 'fernandol0pez@gmail.com'),
  (9, "Laura", 'Hernández Rivera', '55 34 56 78 90', 'l.hdzrivera@yahoo.com')
]
cursor.executemany(tabla_huesped, tuplas_huesped)  # Función que ingresa los valores
conexion.commit()  # Guarda de forma permanente los cambios realizados en la base de datos


#### Ingresar valores a la tabla hotel
tabla_hotel = """
REPLACE INTO Hotel (idHotel, nombre, capacidad, pais, ciudad, direccion, num_tel, calificacion_estrellas)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Ingresar los registros
tuplas_hotel = [
  (1, "Hotel Altavista", 450, "México", "Acapulco", "Calle Himalaya #2093", "55 53 27 67 49", 4),
  (2, "Hotel Casablanca", 700, "México", "Puebla", "Calle Montblanc #1830", "55 58 46 77 77", 5),
  (3, "Hotel Libertad", 400, "México", "Acapulco", "Calle Pistache #2847", "55 38 52 22 66", 3),
  (4, "Hotel San Ángel", 350, "Costa Rica", "San José", "Calle Alajuela #93", "55 53 27 67 49", 4),
  (5, "Coral Residence Inn", 1000, "United States", "Miami", "Coral Bay Street #843", "40 823 23 89 00", 5)
]

cursor.executemany(tabla_hotel, tuplas_hotel)
conexion.commit() # Guarda los cambios permanentemnte


### Ingresar valores a la tabla reservacion

tabla_reservacion = """
REPLACE INTO Reservacion (idReservacion, tipo_habitacion, num_huespedes, fecha_llegada, fecha_salida, Huesped_idHuesped, Hotel_idHotel)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Ingresar registros
tuplas_reservacion = [
    # Hotel Altavista (ID: 1)
    (1, "Ejecutiva", 1, "2024-12-01", "2024-12-15", 1, 1),
    (2, "Suite", 2, "2024-12-20", "2024-12-30", 2, 1),

    # Hotel Casablanca (ID: 2)
    (3, "Sencilla", 1, "2024-11-01", "2024-11-10", 3, 2),
    (4, "Ejecutiva", 2, "2024-11-15", "2024-11-20", 5, 2),

    # Hotel Libertad (ID: 3)
    (5, "Suite", 3, "2024-10-01", "2024-10-05", 4, 3),
    (6, "Sencilla", 1, "2024-10-10", "2024-10-15", 5, 3),

    # Hotel San Ángel (ID: 4)
    (7, "Ejecutiva", 1, "2024-09-01", "2024-09-05", 6, 4),
    (8, "Sencilla", 1, "2024-09-10", "2024-09-15", 7, 4),

    # Coral Residence Inn (ID: 5)
    (9, "Suite", 2, "2024-08-01", "2024-08-10", 8, 5),
    (10, "Ejecutiva", 1, "2024-08-15", "2024-08-20", 9, 5),
]


cursor.executemany(tabla_reservacion, tuplas_reservacion)
conexion.commit()


### Ingresar valores a la tabla habitacion

tabla_habitacion = """
REPLACE INTO Habitacion (idHabitacion, codigo_habitacion, tipo_habitacion, num_piso, estado_habitacion, precio_noche, Reservacion_idReservacion, Hotel_idHotel)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Ingresar registros
tuplas_habitacion = [
    # Hotel Altavista (ID: 1)
    (1, "A101", "Ejecutiva", 2, "Ocupada", 650, 1, 1),  # Relacionada con Reservación ID: 1
    (2, "B201", "Suite", 3, "Ocupada", 1200, 2, 1),     # Relacionada con Reservación ID: 2
    (11, "A102", "Sencilla", 1, "Disponible", 400, None, 1), # Sin reservación
    (12, "B202", "Suite", 3, "Disponible", 1100, None, 1),   # Sin reservación
    (21, "A103", "Ejecutiva", 2, "Disponible", 700, None, 1), # Disponible
    (22, "B203", "Sencilla", 1, "Disponible", 420, None, 1),  # Disponible
    (31, "PH301", "Penthouse", 5, "Disponible", 8000, None, 1), # Disponible
    (32, "PH302", "Penthouse", 5, "Disponible", 8500, None, 1), # Disponible
    (41, "D301", "Doble", 2, "Disponible", 900, None, 1),       # Doble
    (42, "D302", "Doble", 3, "Disponible", 950, None, 1),       # Doble

    # Hotel Casablanca (ID: 2)
    (3, "C301", "Sencilla", 1, "Ocupada", 430, 3, 2),   # Relacionada con Reservación ID: 3
    (4, "D401", "Ejecutiva", 2, "Ocupada", 800, 4, 2),  # Relacionada con Reservación ID: 4
    (13, "C302", "Sencilla", 1, "Disponible", 450, None, 2), # Sin reservación
    (14, "D402", "Ejecutiva", 2, "Disponible", 850, None, 2), # Sin reservación
    (23, "C303", "Suite", 3, "Disponible", 1200, None, 2),    # Disponible
    (24, "D403", "Ejecutiva", 2, "Disponible", 900, None, 2), # Disponible
    (33, "PH401", "Penthouse", 5, "Disponible", 9500, None, 2), # Disponible
    (34, "PH402", "Penthouse", 5, "Disponible", 9000, None, 2), # Disponible
    (43, "D501", "Doble", 2, "Disponible", 880, None, 2),       # Doble
    (44, "D502", "Doble", 3, "Disponible", 920, None, 2),       # Doble

    # Hotel Libertad (ID: 3)
    (5, "E501", "Suite", 3, "Ocupada", 3000, 5, 3),     # Relacionada con Reservación ID: 5
    (6, "F601", "Sencilla", 1, "Ocupada", 500, 6, 3),   # Relacionada con Reservación ID: 6
    (15, "E502", "Ejecutiva", 2, "Disponible", 700, None, 3), # Sin reservación
    (16, "F602", "Suite", 4, "Disponible", 3200, None, 3),    # Sin reservación
    (25, "PH501", "Penthouse", 5, "Disponible", 5000, None, 3), # Disponible
    (26, "F603", "Sencilla", 1, "Disponible", 520, None, 3),  # Disponible
    (35, "PH502", "Penthouse", 5, "Disponible", 7000, None, 3), # Disponible
    (36, "PH503", "Penthouse", 5, "Disponible", 7500, None, 3), # Disponible
    (45, "E601", "Doble", 3, "Disponible", 940, None, 3),       # Doble
    (46, "E602", "Doble", 4, "Disponible", 970, None, 3),       # Doble

    # Hotel San Ángel (ID: 4)
    (7, "G701", "Ejecutiva", 1, "Ocupada", 700, 7, 4),  # Relacionada con Reservación ID: 7
    (8, "H801", "Sencilla", 2, "Ocupada", 450, 8, 4),   # Relacionada con Reservación ID: 8
    (17, "G702", "Sencilla", 1, "Disponible", 400, None, 4),  # Sin reservación
    (18, "H802", "Ejecutiva", 2, "Disponible", 750, None, 4), # Sin reservación
    (27, "G703", "Suite", 3, "Disponible", 1500, None, 4),    # Disponible
    (28, "H803", "Ejecutiva", 1, "Disponible", 800, None, 4), # Disponible
    (37, "PH601", "Penthouse", 5, "Disponible", 9500, None, 4), # Disponible
    (38, "PH602", "Penthouse", 5, "Disponible", 9700, None, 4), # Disponible
    (47, "G801", "Doble", 2, "Disponible", 890, None, 4),       # Doble
    (48, "G802", "Doble", 3, "Disponible", 910, None, 4),       # Doble

    # Coral Residence Inn (ID: 5)
    (9, "I901", "Suite", 3, "Ocupada", 4000, 9, 5),     # Relacionada con Reservación ID: 9
    (10, "J101", "Ejecutiva", 2, "Disponible", 1500, None, 5), # Sin reservación
    (19, "I902", "Sencilla", 1, "Disponible", 500, None, 5),   # Sin reservación
    (20, "J102", "Suite", 3, "Disponible", 4500, None, 5),     # Sin reservación
    (29, "PH701", "Penthouse", 5, "Disponible", 6000, None, 5), # Disponible
    (30, "J103", "Ejecutiva", 2, "Disponible", 1700, None, 5), # Disponible
    (39, "PH702", "Penthouse", 5, "Disponible", 6500, None, 5), # Disponible
    (40, "PH703", "Penthouse", 5, "Disponible", 7000, None, 5), # Disponible
    (49, "I801", "Doble", 3, "Disponible", 890, None, 5),       # Doble
    (50, "I802", "Doble", 4, "Disponible", 920, None, 5),       # Doble
]



cursor.executemany(tabla_habitacion, tuplas_habitacion)
conexion.commit()


### Ingresar valores a la tabla empleado

tabla_empleado = """
REPLACE INTO Empleado (idEmpleado, nombre, apellido, num_tel, correo, Hotel_idHotel)
VALUES (%s, %s, %s, %s, %s, %s)
"""

tuplas_empleado = [
    # Hotel Altavista (ID: 1)
    (1001, "Mateo", "Ruíz Limó", "46 31 11 98 30", "mateo@altavistahotel.com", 1),
    (1007, "Sofía", "Pérez Díaz", "55 44 33 22 11", "sofia_p.altavista@hotel.com", 1),

    # Hotel Casablanca (ID: 2)
    (1003, "Ana Sofía", "Moreno Cruz", "22 68 52 59 63", "anasof@casablancahotel.com", 2),
    (1008, "Fernando", "Gómez López", "33 55 66 77 88", "fernando@casablancahotel.com", 2),

    # Hotel Libertad (ID: 3)
    (1005, "Samuel", "García Limón", "55 68 52 59 63", "samuel@libertadhotel.com", 3),
    (1009, "María", "Fernández Ramos", "44 77 88 99 00", "maria@libertadhotel.com", 3),

    # Hotel San Ángel (ID: 4)
    (1010, "Rosa", "Vera Zambrano", "33 76 34 70 23", "rosa@sanangelhotel.com", 4),
    (1011, "Luis", "Hernández Gutiérrez", "22 88 66 44 55", "luis@sanangelhotel.com", 4),

    # Coral Residence Inn (ID: 5)
    (1012, "Clark", "Kent", "90 85 23 35 32", "clark@coralhotel.com", 5),
    (1013, "Hannah", "Miller", "41 43 32 77 12", "hannah@coralhotel.com", 5),
    (1014, "Elena", "Martínez López", "55 22 33 44 55", "elena@coralhotel.com", 5),
    (1015, "Carlos", "Ruíz Torres", "66 77 88 99 00", "carlos@coralhotel.com", 5),
]


cursor.executemany(tabla_empleado, tuplas_empleado)
conexion.commit()

# Ingresar valores a la tabla check-in

# Ingresar valores a la tabla check-out


# ----------------------------------------------------------------------------------

print(cursor.rowcount, "registros insertados.") # Cuenta el número de registros que se insertan

instruccion = """
SELECT * FROM Empleado
"""
cursor.execute(instruccion) # Selecciona todos los resultados de la tabla huéspedes (aquí se ejecutan las consultas como en SQL)
# Esta función ejecuta lo que se le pida

resultados = cursor.fetchall()  # Guarda los resultados en la variable (hay que hacerlo justo de después de hacer el SELECT)


# Imprime los resultados
print("\n\n------------------------------------------------------------------------------------------------\n")

for x in resultados:
    print(x)

print("\n------------------------------------------------------------------------------------------------\n")

# Cierra el cursor y la conexión
cursor.close()
conexion.close()

