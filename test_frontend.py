#!/usr/bin/env python3
"""
Script para probar el frontend con peluqueros independientes
"""

import sqlite3
import datetime

DB_PATH = 'citas.db'

def crear_datos_prueba():
    """Crear datos de prueba para verificar peluqueros independientes"""
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"📅 Creando datos de prueba para: {mañana}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Obtener peluqueros existentes
    c.execute('SELECT id, nombre FROM peluqueros')
    peluqueros = c.fetchall()
    
    if not peluqueros:
        print("❌ No hay peluqueros en la base de datos")
        return
    
    print(f"📋 Peluqueros existentes: {peluqueros}")
    
    # Limpiar citas existentes para la fecha de prueba
    c.execute('DELETE FROM citas WHERE dia = ?', (mañana,))
    
    # Crear citas de prueba - MISMA HORA, DIFERENTES PELUQUEROS
    # Usar los IDs de los peluqueros existentes
    citas_prueba = [
        ('Juan Pérez', 'Corte', mañana, '17:00', '123456789', peluqueros[0][0]),  # Primer peluquero
        ('Pedro García', 'Barba', mañana, '17:00', '987654321', peluqueros[1][0]),  # Segundo peluquero
        ('María López', 'Combo', mañana, '18:00', '555666777', peluqueros[2][0]),   # Tercer peluquero
    ]
    
    for cita in citas_prueba:
        c.execute('''
            INSERT INTO citas (nombre, servicio, dia, hora, telefono, peluquero_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', cita)
        print(f"✅ Cita creada: {cita[0]} - {cita[1]} - {cita[2]} {cita[3]} - Peluquero {cita[5]}")
    
    conn.commit()
    
    # Verificar que las citas se crearon correctamente
    print(f"\n🔍 Verificando citas creadas:")
    print("=" * 40)
    
    c.execute('''
        SELECT c.hora, c.nombre, c.servicio, p.nombre as peluquero_nombre
        FROM citas c 
        LEFT JOIN peluqueros p ON c.peluquero_id = p.id 
        WHERE c.dia = ?
        ORDER BY c.hora, p.nombre
    ''', (mañana,))
    
    rows = c.fetchall()
    for row in rows:
        print(f"   - {row[0]} - {row[1]} ({row[3]})")
    
    # Verificar que las 17:00 están ocupadas para ambos peluqueros
    print(f"\n✅ Verificando disponibilidad a las 17:00:")
    print("=" * 40)
    
    c.execute('SELECT peluquero_id, nombre FROM citas WHERE dia = ? AND hora = ?', (mañana, '17:00'))
    citas_17 = c.fetchall()
    
    if len(citas_17) == 2:
        print("✅ CORRECTO: Dos peluqueros pueden tener citas a las 17:00 simultáneamente")
        for peluquero_id, nombre in citas_17:
            print(f"   - Peluquero {peluquero_id}: {nombre}")
    else:
        print(f"❌ INCORRECTO: Solo {len(citas_17)} cita(s) a las 17:00")
    
    conn.close()
    print("\n🎉 Datos de prueba creados correctamente!")
    print(f"\n📋 Para probar el frontend:")
    print(f"   1. Ve a http://localhost:5000")
    print(f"   2. Selecciona un servicio")
    print(f"   3. Selecciona el peluquero '{peluqueros[0][1]}'")
    print(f"   4. Selecciona la fecha {mañana}")
    print(f"   5. Verifica que las 17:00 aparecen como ocupadas")
    print(f"   6. Cambia al peluquero '{peluqueros[1][1]}'")
    print(f"   7. Verifica que las 17:00 aparecen como ocupadas")
    print(f"   8. Cambia al peluquero '{peluqueros[2][1]}'")
    print(f"   9. Verifica que las 17:00 aparecen como disponibles")

if __name__ == "__main__":
    crear_datos_prueba() 