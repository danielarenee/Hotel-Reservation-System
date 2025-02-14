CREATE DATABASE IF NOT EXISTS reservacion_hoteles; -- Crea la base de datos
USE reservacion_hoteles; -- Indica que se usará esta base para las siguientes instruccioneshuesped

-- Tabla Huesped
CREATE TABLE IF NOT EXISTS Huesped (
  idHuesped INT NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  apellido VARCHAR(45) NOT NULL,
  num_tel VARCHAR(45) NOT NULL,
  correo VARCHAR(45) NOT NULL
);

-- Tabla Hotel
CREATE TABLE IF NOT EXISTS Hotel (
  idHotel INT NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  capacidad INT NOT NULL, 
  pais VARCHAR(45) NOT NULL,
  ciudad VARCHAR(45) NOT NULL,
  direccion VARCHAR(45) NOT NULL,
  num_tel VARCHAR(45) NOT NULL,
  calificacion_estrellas INT CHECK (calificacion_estrellas BETWEEN 1 AND 5) NOT NULL -- Checa que el núm de estrellas esté entre 0 y 1
);

-- Tabla Reservacion
CREATE TABLE IF NOT EXISTS Reservacion (
  idReservacion INT NOT NULL PRIMARY KEY,
  tipo_habitacion VARCHAR(45) NOT NULL,
  num_huespedes INT NOT NULL,
  fecha_llegada DATETIME NOT NULL,
  fecha_salida DATETIME NOT NULL,
  Huesped_idHuesped INT NOT NULL,
  Hotel_idHotel INT NOT NULL,
  FOREIGN KEY (Huesped_idHuesped) REFERENCES Huesped(idHuesped) ON DELETE CASCADE,
  FOREIGN KEY (Hotel_idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE,
  CHECK(fecha_llegada < fecha_salida) -- La fecha de llegada debe ser menor a fecha de salida
);

-- Tabla Habitacion
CREATE TABLE IF NOT EXISTS Habitacion (
  idHabitacion INT NOT NULL PRIMARY KEY,  
  codigo_habitacion VARCHAR(10) NOT NULL,
  tipo_habitacion VARCHAR(45) NOT NULL,
  num_piso INT NOT NULL,
  estado_habitacion VARCHAR(45) NOT NULL,
  precio_noche DECIMAL(10, 2) NOT NULL, 
  Reservacion_idReservacion INT NOT NULL,
  Hotel_idHotel INT NOT NULL,
  FOREIGN KEY (Reservacion_idReservacion) REFERENCES Reservacion(idReservacion) ON DELETE CASCADE,
  FOREIGN KEY (Hotel_idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE
);

-- Tabla Empleado
CREATE TABLE IF NOT EXISTS Empleado (
  idEmpleado INT NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  apellido VARCHAR(45) NOT NULL,
  num_tel VARCHAR(45) NOT NULL,
  correo VARCHAR(45) NOT NULL,
  Hotel_idHotel INT NOT NULL,
  FOREIGN KEY (Hotel_idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE
);

-- Tabla Check_In
CREATE TABLE IF NOT EXISTS Check_In (
  idCheckIn INT NOT NULL PRIMARY KEY,
  fecha_checkIn DATE NOT NULL,
  hora_checkIn TIME NOT NULL,
  Reservacion_idReservacion INT NOT NULL,
  Empleado_idEmpleado INT NOT NULL,
  FOREIGN KEY (Reservacion_idReservacion) REFERENCES Reservacion(idReservacion) ON DELETE CASCADE,
  FOREIGN KEY (Empleado_idEmpleado) REFERENCES Empleado(idEmpleado) ON DELETE CASCADE
);

-- Tabla Check_Out
CREATE TABLE IF NOT EXISTS Check_Out (
  idCheckOut INT NOT NULL PRIMARY KEY,
  fecha_checkOut DATE NOT NULL,
  hora_checkOut TIME NOT NULL,
  Reservacion_idReservacion INT NOT NULL,
  Empleado_idEmpleado INT NOT NULL,
  FOREIGN KEY (Reservacion_idReservacion) REFERENCES Reservacion(idReservacion) ON DELETE CASCADE,
  FOREIGN KEY (Empleado_idEmpleado) REFERENCES Empleado(idEmpleado) ON DELETE CASCADE
);

SELECT * FROM Habitacion;
