CREATE DATABASE veterinaria_db;
USE veterinaria_db;

-- Tabla de dueños
CREATE TABLE duenos (
    id_dueno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20)
);

-- Tabla de mascotas (con relación a dueños)
CREATE TABLE mascotas (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50),
    edad INT,
    id_dueno INT,
    FOREIGN KEY (id_dueno) REFERENCES duenos(id_dueno) ON DELETE CASCADE
);

-- Tabla de veterinarios
CREATE TABLE veterinarios (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);




-- Datos de Prueba

INSERT INTO duenos (nombre, telefono) VALUES 
('Carlos Pérez', '3511234567'),
('María Gómez', '3512345678'),
('Roberto López', '3513456789');

INSERT INTO mascotas (nombre, especie, edad, id_dueno) VALUES
('Firulais', 'Perro', 5, 1),
('Sassy', 'Gato', 3, 1),
('Luna', 'Perro', 2, 2);

INSERT INTO veterinarios (nombre, especialidad) VALUES
('Dra. Laura Gómez', 'Perros y Gatos'),
('Dr. Martín Rodríguez', 'Exóticos');