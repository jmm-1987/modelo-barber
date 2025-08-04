#!/usr/bin/env python3
"""
Script simple para probar peluqueros independientes
"""

import sqlite3
import datetime

DB_PATH = 'citas.db'

def test_peluqueros_independientes():
    """Probar que los peluqueros tienen calendarios independientes"""
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"📅 Probando para la fecha: {mañana}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Crear tabla de peluqueros si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS peluqueros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Crear tabla de citas si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            servicio TEXT NOT NULL,
            dia TEXT NOT NULL,
            hora TEXT NOT NULL,
            telefono TEXT,
            peluquero_id INTEGER,
            FOREIGN KEY (peluquero_id) REFERENCES peluqueros (id)
        )
    ''')
    
    # Insertar peluqueros de prueba
    peluqueros = [
        ('Juan',),
        ('Pedro',),
        ('María',)
    ]
    
    for peluquero in peluqueros:
        c.execute('INSERT OR IGNORE INTO peluqueros (nombre) VALUES (?)', peluquero)
    
    # Limpiar citas existentes para la fecha de prueba
    c.execute('DELETE FROM citas WHERE dia = ?', (mañana,))
    
    # Crear citas de prueba
    citas_prueba = [
        ('Juan Pérez', 'Corte', mañana, '17:00', '123456789', 1),
        ('Pedro García', 'Barba', mañana, '17:00', '987654321', 2),  # Misma hora, diferente peluquero
        ('María López', 'Combo', mañana, '18:00', '555666777', 3),
    ]
    
    for cita in citas_prueba:
        c.execute('''
            INSERT INTO citas (nombre, servicio, dia, hora, telefono, peluquero_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', cita)
        print(f"✅ Cita creada: {cita[0]} - {cita[1]} - {cita[2]} {cita[3]} - Peluquero {cita[5]}")
    
    conn.commit()
    
    # Verificar citas por peluquero
    print(f"\n🔍 Verificando citas por peluquero:")
    print("=" * 50)
    
    for peluquero_id in [1, 2, 3]:
        c.execute('''
            SELECT c.hora, c.nombre, c.servicio, p.nombre as peluquero_nombre
            FROM citas c 
            LEFT JOIN peluqueros p ON c.peluquero_id = p.id 
            WHERE c.dia = ? AND c.peluquero_id = ?
        ''', (mañana, peluquero_id))
        
        rows = c.fetchall()
        if rows:
            print(f"📅 Peluquero ID {peluquero_id}:")
            for row in rows:
                print(f"   - {row[0]} - {row[1]} ({row[3]})")
        else:
            print(f"📅 Peluquero ID {peluquero_id}: Sin citas")
    
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
    print("\n🎉 Prueba completada!")

if __name__ == "__main__":
    test_peluqueros_independientes() 