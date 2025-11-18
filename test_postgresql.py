import pytest
import psycopg2
import os

def test_arrays_operations():
    """Test operaciones con arrays"""
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    # Test: Consultar productos con etiqueta 'tecnología'
    cur.execute("SELECT COUNT(*) FROM productos WHERE 'tecnología' = ANY(etiquetas)")
    count = cur.fetchone()[0]
    assert count >= 2, f"Se esperaban al menos 2 productos con etiqueta 'tecnología', se encontraron {count}"
    
    # Test: Verificar estructura de datos
    cur.execute("SELECT nombre, etiquetas FROM productos WHERE nombre = 'Laptop'")
    result = cur.fetchone()
    assert result is not None, "Producto 'Laptop' no encontrado"
    assert 'tecnología' in result[1], "Laptop debería tener etiqueta 'tecnología'"
    
    cur.close()
    conn.close()

def test_cte_recursivas():
    """Test CTE recursivas"""
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    # Test: Red de amigos de Ana
    cur.execute("""
        WITH RECURSIVE red_amigos AS (
            SELECT id, nombre, amigo_id, 0 as nivel
            FROM amigos WHERE nombre = 'Ana'
            UNION ALL
            SELECT a.id, a.nombre, a.amigo_id, r.nivel + 1
            FROM amigos a
            INNER JOIN red_amigos r ON a.amigo_id = r.id
        )
        SELECT COUNT(*) FROM red_amigos
    """)
    count = cur.fetchone()[0]
    assert count > 1, f"La red de amigos de Ana debería tener más de 1 persona, tiene {count}"
    
    # Test: Jerarquía de empleados
    cur.execute("""
        WITH RECURSIVE jerarquia_empleados AS (
            SELECT id, nombre, jefe_id, 0 as nivel
            FROM empleados WHERE nombre = 'María'
            UNION ALL
            SELECT e.id, e.nombre, e.jefe_id, j.nivel + 1
            FROM empleados e
            INNER JOIN jerarquia_empleados j ON e.jefe_id = j.id
        )
        SELECT COUNT(*) FROM jerarquia_empleados
    """)
    count = cur.fetchone()[0]
    assert count >= 3, f"La jerarquía debería tener al menos 3 empleados, tiene {count}"
    
    cur.close()
    conn.close()

def test_ciudades_conexiones():
    """Test grafo de ciudades"""
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    # Test: Ciudades alcanzables desde Madrid
    cur.execute("""
        WITH RECURSIVE ciudades_alcanzables AS (
            SELECT c.id, c.nombre, 0 as distancia_total
            FROM ciudades c WHERE c.nombre = 'Madrid'
            UNION ALL
            SELECT c.id, c.nombre, ca.distancia_total + r.distancia
            FROM ciudades c
            INNER JOIN rutas r ON c.id = r.ciudad_destino
            INNER JOIN ciudades_alcanzables ca ON r.ciudad_origen = ca.id
        )
        SELECT COUNT(DISTINCT nombre) FROM ciudades_alcanzables
    """)
    count = cur.fetchone()[0]
    assert count > 1, f"Debería haber más de 1 ciudad alcanzable desde Madrid, hay {count}"
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
