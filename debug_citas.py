#!/usr/bin/env python3
"""
Script para debuggear las citas y ver exactamente qué hay en cada columna
"""

import sqlite3

def debug_citas():
    """Debuggea las citas para ver qué hay en cada columna"""
    
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🔍 Debuggeando citas...")
    
    # Obtener información de la tabla
    c.execute("PRAGMA table_info(citas)")
    columnas = c.fetchall()
    
    print("\n📋 Estructura de la tabla citas:")
    for col in columnas:
        print(f"   {col[0]}: {col[1]} ({col[2]})")
    
    # Mostrar algunas citas con todos los campos
    c.execute('SELECT * FROM citas LIMIT 5')
    citas = c.fetchall()
    
    print(f"\n📄 Primeras 5 citas con todos los campos:")
    for cita in citas:
        print(f"\n   Cita ID: {cita[0]}")
        print(f"   nombre: '{cita[1]}'")
        print(f"   telefono: '{cita[2]}'")
        print(f"   servicio: '{cita[3]}'")
        print(f"   dia: '{cita[4]}'")
        print(f"   hora: '{cita[5]}'")
        print(f"   peluquero_id: '{cita[6]}'")
        print(f"   fecha_creacion: '{cita[7]}'")
        print(f"   precio: '{cita[8]}'")
    
    # Probar consultas específicas
    print(f"\n🔍 Probando consultas específicas:")
    
    # Contar total de citas
    c.execute('SELECT COUNT(*) FROM citas')
    total = c.fetchone()[0]
    print(f"   Total citas: {total}")
    
    # Buscar citas con fecha específica
    c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', ('2025-08-05',))
    citas_hoy = c.fetchone()[0]
    print(f"   Citas con dia = '2025-08-05': {citas_hoy}")
    
    # Buscar citas con precio específico
    c.execute('SELECT COUNT(*) FROM citas WHERE precio = ?', ('2025-08-05',))
    citas_precio = c.fetchone()[0]
    print(f"   Citas con precio = '2025-08-05': {citas_precio}")
    
    # Buscar citas con hora específica
    c.execute('SELECT COUNT(*) FROM citas WHERE hora = ?', ('12:00',))
    citas_hora = c.fetchone()[0]
    print(f"   Citas con hora = '12:00': {citas_hora}")
    
    # Mostrar valores únicos en cada columna
    print(f"\n📊 Valores únicos por columna:")
    
    c.execute('SELECT DISTINCT dia FROM citas LIMIT 5')
    dias = c.fetchall()
    print(f"   Días únicos (primeros 5): {[d[0] for d in dias]}")
    
    c.execute('SELECT DISTINCT precio FROM citas LIMIT 5')
    precios = c.fetchall()
    print(f"   Precios únicos (primeros 5): {[p[0] for p in precios]}")
    
    c.execute('SELECT DISTINCT hora FROM citas LIMIT 5')
    horas = c.fetchall()
    print(f"   Horas únicas (primeros 5): {[h[0] for h in horas]}")
    
    conn.close()

if __name__ == "__main__":
    debug_citas() 