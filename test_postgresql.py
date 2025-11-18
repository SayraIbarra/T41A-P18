import pytest
import psycopg2
import os

def get_connection():
    """Crear conexión a la base de datos"""
    return psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="postgres"
    )

def test_arrays_operations():
    """Test operaciones con arrays"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Test: Consultar productos con etiqueta 'tecnología'
    cur.execute("SELECT COUNT(*) FROM productos WHERE 'tecnología' = ANY(etiquetas)")
    count = cur.fetchone()[0]
    # Verificamos que hay al menos 2 productos con tecnología
    if count < 2:
        raise AssertionError(f"Se esperaban al menos 2 productos con etiqueta 'tecnología', se encontraron {count}")
    
    # Test: Verificar estructura de datos
    cur.execute("SELECT nombre, etiquetas FROM productos WHERE nombre = 'Laptop'")
    result = cur.fetchone()
    if result is None:
        raise AssertionError("Producto 'Laptop' no encontrado")
    
    etiquetas = result[1]
    if 'tecnología' not in etiquetas:
        raise AssertionError("Laptop debería tener etiqueta 'tecnología'")
    
    cur.close()
    conn.close()
    print("✓ Test de arrays pasado correctamente")

def test_cte_recursivas():
    """Test CTE recursivas"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Test: Red de amigos de Ana (limitamos la profundidad)
    cur.execute("""
        WITH RECURSIVE red_amigos AS (
            SELECT id, nombre, amigo_id, 0 as nivel
            FROM amigos WHERE nombre = 'Ana'
            UNION ALL
            SELECT a.id, a.nombre, a.amigo_id, r.nivel + 1
            FROM amigos a
            INNER JOIN red_amigos r ON a.amigo_id = r.id
            WHERE r.nivel < 10  -- Límite para evitar bucles infinitos
        )
        SELECT COUNT(*) FROM red_amigos
    """)
    count = cur.fetchone()[0]
    if count <= 1:
        raise AssertionError(f"La red de amigos de Ana debería tener más de 1 persona, tiene {count}")
    
    # Test: Jerarquía de empleados (limitamos la profundidad)
    cur.execute("""
        WITH RECURSIVE jerarquia_empleados AS (
            SELECT id, nombre, jefe_id, 0 as nivel
            FROM empleados WHERE nombre = 'María'
            UNION ALL
            SELECT e.id, e.nombre, e.jefe_id, j.nivel + 1
            FROM empleados e
            INNER JOIN jerarquia_empleados j ON e.jefe_id = j.id
            WHERE j.nivel < 10  -- Límite para evitar bucles infinitos
        )
        SELECT COUNT(*) FROM jerarquia_empleados
    """)
    count = cur.fetchone()[0]
    if count < 3:
        raise AssertionError(f"La jerarquía debería tener al menos 3 empleados, tiene {count}")
    
    cur.close()
    conn.close()
    print("✓ Test de CTE recursivas pasado correctamente")

def test_ciudades_conexiones():
    """Test grafo de ciudades - Versión segura sin bucles infinitos"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Test: Ciudades alcanzables desde Madrid (versión limitada y segura)
    cur.execute("""
        WITH RECURSIVE ciudades_alcanzables AS (
            -- Caso base: Madrid
            SELECT 
                c.id,
                c.nombre,
                0 as distancia_total,
                ARRAY[c.id] as camino,
                0 as nivel
            FROM ciudades c 
            WHERE c.nombre = 'Madrid'
            
            UNION ALL
            
            -- Caso recursivo: ciudades conectadas
            SELECT 
                c.id,
                c.nombre,
                ca.distancia_total + r.distancia,
                ca.camino || c.id,
                ca.nivel + 1
            FROM ciudades c
            INNER JOIN rutas r ON c.id = r.ciudad_destino
            INNER JOIN ciudades_alcanzables ca ON r.ciudad_origen = ca.id
            WHERE 
                c.id != ALL(ca.camino)  -- Evitar ciclos
                AND ca.nivel < 5        -- Límite de profundidad
        )
        SELECT COUNT(DISTINCT nombre) FROM ciudades_alcanzables
    """)
    count = cur.fetchone()[0]
    if count <= 1:
        raise AssertionError(f"Debería haber más de 1 ciudad alcanzable desde Madrid, hay {count}")
    
    cur.close()
    conn.close()
    print("✓ Test de ciudades y conexiones pasado correctamente")

def test_ciudades_conexiones_simple():
    """Test alternativo más simple para ciudades"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Test más simple: verificar conexiones directas desde Madrid
    cur.execute("""
        SELECT COUNT(*) 
        FROM ciudades c
        WHERE c.nombre = 'Madrid' 
        AND array_length(conexiones_directas, 1) > 0
    """)
    count = cur.fetchone()[0]
    if count == 0:
        raise AssertionError("Madrid debería tener conexiones directas")
    
    # Verificar que tenemos rutas definidas
    cur.execute("SELECT COUNT(*) FROM rutas")
    count_rutas = cur.fetchone()[0]
    if count_rutas == 0:
        raise AssertionError("No hay rutas definidas en la base de datos")
    
    cur.close()
    conn.close()
    print("✓ Test simple de ciudades pasado correctamente")

def test_consultas_basicas():
    """Test de consultas básicas"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Test: Verificar que tenemos datos
    cur.execute("SELECT COUNT(*) FROM usuarios")
    count_usuarios = cur.fetchone()[0]
    if count_usuarios == 0:
        raise AssertionError("No hay usuarios en la base de datos")
    
    cur.execute("SELECT COUNT(*) FROM productos")
    count_productos = cur.fetchone()[0]
    if count_productos == 0:
        raise AssertionError("No hay productos en la base de datos")
    
    cur.close()
    conn.close()
    print("✓ Test de consultas básicas pasado correctamente")

if __name__ == "__main__":
    # Ejecutar tests manualmente
    try:
        test_consultas_basicas()
        test_arrays_operations()
        test_cte_recursivas()
        test_ciudades_conexiones_simple()  # Usamos la versión simple
        print("\n Todos los tests pasaron correctamente!")
    except Exception as e:
        print(f"\n Error en tests: {e}")
        raise
