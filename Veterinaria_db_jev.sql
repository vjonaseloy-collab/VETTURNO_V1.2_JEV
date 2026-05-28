CREATE DATABASE veterinaria_db;
USE veterinaria_db;

CREATE TABLE duenos (
    id_dueno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE mascotas (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50),
    edad INT,
    id_dueno INT,
    FOREIGN KEY (id_dueno) REFERENCES duenos(id_dueno) ON DELETE CASCADE
);

CREATE TABLE veterinarios (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT,
    id_veterinario INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(255),
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota) ON DELETE CASCADE,
    FOREIGN KEY (id_veterinario) REFERENCES veterinarios(id_veterinario) ON DELETE CASCADE
);


-- ESTOS SON DATOS DE PRUEBA CHICOS, CUALQUIER COSA PUEDEN AGREGAR MAS USANDO PYTHON O DESDE EL MISMO WORKBENCH


-- =====================================================
-- VETTURNOS - DATOS DE PRUEBA
-- =====================================================

USE veterinaria_db;

-- =====================================================
-- 2. INSERTAR DUEÑOS (10 dueños)
-- =====================================================
INSERT INTO duenos (nombre, telefono) VALUES 
('Carlos Alberto Pérez', '3511234567'),
('María Fernanda Gómez', '3512345678'),
('Roberto José López', '3513456789'),
('Ana Silvia Martínez', '3514567890'),
('Javier Andrés Rodríguez', '3515678901'),
('Laura Beatriz Fernández', '3516789012'),
('Diego Sebastián Sánchez', '3517890123'),
('Carolina Inés Díaz', '3518901234'),
('Pablo Ezequiel Romero', '3519012345'),
('Verónica Soledad Torres', '3510123456');

-- =====================================================
-- 3. INSERTAR VETERINARIOS (6 veterinarios)
-- =====================================================
INSERT INTO veterinarios (nombre, especialidad) VALUES 
('Dra. Laura Gómez', 'Perros y Gatos'),
('Dr. Martín Rodríguez', 'Animales Exóticos'),
('Dra. Silvia Fernández', 'Grandes Animales'),
('Dr. Pablo Díaz', 'Emergencias y Urgencias'),
('Dra. Mónica Luna', 'Dermatología Veterinaria'),
('Dr. Ricardo Molina', 'Traumatología');

-- =====================================================
-- 4. INSERTAR MASCOTAS (20 mascotas con sus dueños)
-- =====================================================
INSERT INTO mascotas (nombre, especie, edad, id_dueno) VALUES 
-- Dueño 1: Carlos Pérez (id_dueno = 1)
('Firulais', 'Perro', 5, 1),
('Sassy', 'Gato', 3, 1),

-- Dueño 2: María Gómez (id_dueno = 2)
('Luna', 'Perro', 2, 2),
('Milo', 'Gato', 4, 2),

-- Dueño 3: Roberto López (id_dueno = 3)
('Rocky', 'Perro', 7, 3),
('Coco', 'Ave', 2, 3),
('Tortu', 'Tortuga', 12, 3),

-- Dueño 4: Ana Martínez (id_dueno = 4)
('Bella', 'Perro', 1, 4),
('Simba', 'Gato', 6, 4),
('Nemo', 'Pez', 1, 4),

-- Dueño 5: Javier Rodríguez (id_dueno = 5)
('Max', 'Perro', 8, 5),
('Lola', 'Gato', 3, 5),

-- Dueño 6: Laura Fernández (id_dueno = 6)
('Toby', 'Perro', 4, 6),
('Copito', 'Conejo', 2, 6),

-- Dueño 7: Diego Sánchez (id_dueno = 7)
('Charly', 'Perro', 6, 7),
('Pecas', 'Hámster', 1, 7),

-- Dueño 8: Carolina Díaz (id_dueno = 8)
('Nina', 'Perro', 3, 8),
('Tom', 'Gato', 5, 8),

-- Dueño 9: Pablo Romero (id_dueno = 9)
('Rex', 'Perro', 9, 9),

-- Dueño 10: Verónica Torres (id_dueno = 10)
('Lucky', 'Perro', 2, 10),
('Piolín', 'Ave', 3, 10);

-- =====================================================
-- 5. INSERTAR TURNOS (30 turnos entre mayo y junio 2026)
-- =====================================================
INSERT INTO turnos (id_mascota, id_veterinario, fecha, hora, motivo) VALUES 

-- Turnos de MAYO 2026
(1, 1, '2026-05-10', '09:00:00', 'Vacunación anual'),
(2, 1, '2026-05-10', '10:30:00', 'Control de salud general'),
(3, 3, '2026-05-11', '14:00:00', 'Herida en pata trasera'),
(4, 1, '2026-05-12', '11:00:00', 'Primera consulta - cachorro'),
(5, 4, '2026-05-12', '16:30:00', 'Vómitos recurrentes'),
(6, 2, '2026-05-13', '09:30:00', 'Control de plumaje'),
(7, 2, '2026-05-13', '10:00:00', 'Revisión de caparazón'),
(8, 1, '2026-05-14', '15:00:00', 'Desparasitación'),
(9, 1, '2026-05-15', '08:30:00', 'Vacunación triple felina'),
(10, 2, '2026-05-15', '11:30:00', 'Limpieza de pecera'),
(11, 4, '2026-05-16', '13:00:00', 'Dificultad para caminar'),
(12, 1, '2026-05-17', '10:00:00', 'Control de celo'),
(13, 1, '2026-05-18', '12:00:00', 'Corte de uñas y baño'),
(14, 2, '2026-05-19', '09:00:00', 'Revisión dental'),
(15, 3, '2026-05-20', '15:30:00', 'Tos persistente'),

-- Turnos de JUNIO 2026 (incluyendo turnos pasados y futuros)
(16, 1, '2026-06-01', '10:00:00', 'Control anual'),
(17, 1, '2026-06-01', '11:30:00', 'Vacunación'),
(18, 5, '2026-06-02', '14:00:00', 'Alopecia - pérdida de pelo'),
(19, 1, '2026-06-03', '09:00:00', 'Chequeo general'),
(20, 6, '2026-06-03', '16:00:00', 'Dolor en cadera'),
(1, 1, '2026-06-05', '09:30:00', 'Consulta de seguimiento'),
(3, 3, '2026-06-05', '11:00:00', 'Control de herida'),
(5, 4, '2026-06-06', '10:30:00', 'Análisis de sangre'),
(8, 1, '2026-06-07', '15:00:00', 'Segunda dosis de vacuna'),
(11, 6, '2026-06-08', '13:30:00', 'Radiografía de cadera'),
(13, 1, '2026-06-09', '12:00:00', 'Control de peso'),
(15, 3, '2026-06-10', '14:30:00', 'Tratamiento respiratorio'),
(17, 1, '2026-06-10', '16:00:00', 'Refuerzo vacunal'),
(19, 5, '2026-06-11', '09:00:00', 'Erupción cutánea'),
(20, 6, '2026-06-12', '11:00:00', 'Fisioterapia');

-- =====================================================
-- 6. VERIFICAR DATOS INSERTADOS
-- =====================================================
SELECT '🏥 VERIFICACIÓN DE DATOS CARGADOS' AS '';

SELECT 'Dueños' as 'Tabla', COUNT(*) as 'Registros' FROM duenos
UNION
SELECT 'Mascotas', COUNT(*) FROM mascotas
UNION
SELECT 'Veterinarios', COUNT(*) FROM veterinarios
UNION
SELECT 'Turnos', COUNT(*) FROM turnos;

-- =====================================================
-- 7. CONSULTAS DE EJEMPLO (para probar)
-- =====================================================

-- Ver dueños con sus mascotas
SELECT '👥 DUEÑOS CON SUS MASCOTAS' AS '';
SELECT d.nombre AS 'Dueño', d.telefono AS 'Teléfono', 
       m.nombre AS 'Mascota', m.especie AS 'Especie', m.edad AS 'Edad'
FROM duenos d
LEFT JOIN mascotas m ON d.id_dueno = m.id_dueno
ORDER BY d.nombre;

-- Ver veterinarios con sus atenciones
SELECT '👨‍⚕️ VETERINARIOS Y SUS ATENCIONES' AS '';
SELECT v.nombre AS 'Veterinario', v.especialidad AS 'Especialidad', 
       COUNT(t.id_turno) AS 'Total Turnos'
FROM veterinarios v
LEFT JOIN turnos t ON v.id_veterinario = t.id_veterinario
GROUP BY v.id_veterinario
ORDER BY COUNT(t.id_turno) DESC;

-- Ver próximos turnos (desde hoy)
SELECT '📅 PRÓXIMOS TURNOS' AS '';
SELECT t.fecha AS 'Fecha', t.hora AS 'Hora', 
       m.nombre AS 'Mascota', d.nombre AS 'Dueño',
       v.nombre AS 'Veterinario', t.motivo AS 'Motivo'
FROM turnos t
JOIN mascotas m ON t.id_mascota = m.id_mascota
JOIN duenos d ON m.id_dueno = d.id_dueno
JOIN veterinarios v ON t.id_veterinario = v.id_veterinario
WHERE t.fecha >= CURDATE()
ORDER BY t.fecha, t.hora
LIMIT 10;

-- =====================================================
-- ¡LISTO! Datos de prueba cargados correctamente
-- =====================================================
SELECT '✅ DATOS DE PRUEBA CARGADOS CORRECTAMENTE' AS '';
SELECT '¡Ya podés probar VetTurnos 2.0!' AS '';


-- CONSULTAS DE PRUEBA (saquen los "--" de los SELECT para ejecutarlos)

-- Ver todos los dueños
-- SELECT * FROM duenos;

-- Ver mascotas con sus dueños
-- SELECT m.nombre, d.nombre FROM mascotas m JOIN duenos d ON m.id_dueno = d.id_dueno;

-- Ver agenda completa
-- SELECT * FROM turnos ORDER BY fecha;