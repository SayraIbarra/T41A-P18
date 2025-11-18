
INSERT INTO usuarios (nombre, intereses) VALUES
('Ana', ARRAY['PostgreSQL', 'Grafos', 'NoSQL']),
('Luis', ARRAY['Python', 'Machine Learning', 'Datos']),
('Marta', ARRAY['SQL', 'Bases de Datos', 'Analytics']);


INSERT INTO productos (nombre, precio, etiquetas) VALUES
('Laptop', 1200.00, ARRAY['tecnología', 'computación', 'portátil']),
('Libro SQL', 45.00, ARRAY['educación', 'tecnología', 'base de datos']),
('Auriculares', 80.00, ARRAY['tecnología', 'audio', 'música']),
('Mesa', 150.00, ARRAY['hogar', 'muebles', 'oficina']);

INSERT INTO amigos (nombre, amigo_id) VALUES
('Ana', NULL),
('Luis', 1),
('Marta', 2),
('Pedro', 2),
('Carlos', 3),
('Sofia', 4);

INSERT INTO empleados (nombre, puesto, jefe_id) VALUES
('María', 'CEO', NULL),
('Juan', 'Gerente', 1),
('Ana', 'Supervisora', 2),
('Luis', 'Desarrollador', 3),
('Marta', 'Desarrolladora', 3),
('Pedro', 'Analista', 2);


INSERT INTO ciudades (nombre, conexiones_directas) VALUES
('Madrid', ARRAY[2, 3]),
('Barcelona', ARRAY[1, 4]),
('Valencia', ARRAY[1, 4]),
('Sevilla', ARRAY[2, 3, 5]),
('Granada', ARRAY[4]);


INSERT INTO rutas (ciudad_origen, ciudad_destino, distancia) VALUES
(1, 2, 600),
(1, 3, 350),
(2, 1, 600),
(2, 4, 1000),
(3, 1, 350),
(3, 4, 650),
(4, 2, 1000),
(4, 3, 650),
(4, 5, 250),
(5, 4, 250);
