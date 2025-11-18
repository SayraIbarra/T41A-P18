SELECT nombre, intereses FROM usuarios;


SELECT nombre, intereses[1] AS primer_interes FROM usuarios;


SELECT nombre, precio, etiquetas 
FROM productos 
WHERE 'tecnología' = ANY(etiquetas);

SELECT nombre, precio, etiquetas
FROM productos
WHERE etiquetas @> ARRAY['tecnología', 'audio']::TEXT[];


WITH RECURSIVE red_amigos AS (
    SELECT id, nombre, amigo_id, 0 as nivel
    FROM amigos 
    WHERE nombre = 'Ana'
    
    UNION ALL
    
    SELECT a.id, a.nombre, a.amigo_id, r.nivel + 1
    FROM amigos a
    INNER JOIN red_amigos r ON a.amigo_id = r.id
    WHERE r.nivel < 10  -- Límite de profundidad
)
SELECT * FROM red_amigos ORDER BY nivel;


WITH RECURSIVE jerarquia_empleados AS (
    SELECT id, nombre, puesto, jefe_id, 0 as nivel
    FROM empleados 
    WHERE nombre = 'María'
    
    UNION ALL
    
    SELECT e.id, e.nombre, e.puesto, e.jefe_id, j.nivel + 1
    FROM empleados e
    INNER JOIN jerarquia_empleados j ON e.jefe_id = j.id
    WHERE j.nivel < 10  -- Límite de profundidad
)
SELECT 
    nivel,
    REPEAT('  ', nivel) || nombre as nombre_indentado,
    puesto
FROM jerarquia_empleados 
ORDER BY nivel, nombre;

WITH RECURSIVE ciudades_alcanzables AS (
    SELECT 
        c.id,
        c.nombre,
        ARRAY[c.id] as camino,
        0 as distancia_total,
        0 as nivel
    FROM ciudades c
    WHERE c.nombre = 'Madrid'
    
    UNION ALL
    
    SELECT 
        c.id,
        c.nombre,
        ca.camino || c.id,
        ca.distancia_total + r.distancia,
        ca.nivel + 1
    FROM ciudades c
    INNER JOIN rutas r ON c.id = r.ciudad_destino
    INNER JOIN ciudades_alcanzables ca ON r.ciudad_origen = ca.id
    WHERE 
        c.id != ALL(ca.camino)  -- Evitar ciclos
        AND ca.nivel < 5        -- Límite de profundidad
)
SELECT 
    nombre as ciudad_destino,
    distancia_total,
    camino
FROM ciudades_alcanzables 
ORDER BY distancia_total;

SELECT 
    c1.nombre as origen,
    c2.nombre as destino,
    r.distancia
FROM rutas r
JOIN ciudades c1 ON r.ciudad_origen = c1.id
JOIN ciudades c2 ON r.ciudad_destino = c2.id
WHERE c1.nombre = 'Madrid'
ORDER BY r.distancia;
