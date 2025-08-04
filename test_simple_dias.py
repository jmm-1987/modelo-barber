#!/usr/bin/env python3
"""
Script simple para probar la verificación de citas antes de cerrar días
"""

import sqlite3
import datetime

DB_PATH = 'citas.db'

def probar_verificacion():
    """Probar la función de verificación de citas"""
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"📅 Probando para la fecha: {mañana}")
    
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
    
    # Crear una cita de prueba
    cita_prueba = ('Juan Pérez', 'Corte', mañana, '17:00', '123456789', peluqueros[0][0])
    c.execute('''
        INSERT INTO citas (nombre, servicio, dia, hora, telefono, peluquero_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', cita_prueba)
    print(f"✅ Cita creada: {cita_prueba[0]} - {cita_prueba[1]} - {cita_prueba[2]} {cita_prueba[3]} - Peluquero {cita_prueba[5]}")
    
    conn.commit()
    
    # Verificar si hay citas en la fecha
    c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (mañana,))
    count = c.fetchone()[0]
    print(f"🔍 Citas en {mañana}: {count}")
    
    # Verificar si hay citas para el peluquero específico
    c.execute('SELECT COUNT(*) FROM citas WHERE dia = ? AND peluquero_id = ?', (mañana, peluqueros[0][0]))
    count_peluquero = c.fetchone()[0]
    print(f"🔍 Citas en {mañana} para peluquero {peluqueros[0][1]}: {count_peluquero}")
    
    conn.close()
    
    print("\n✅ Verificación completada!")
    print("📋 Ahora puedes probar en el panel de administración:")
    print(f"   1. Ve a http://localhost:5000/panel")
    print(f"   2. Ve a la sección de configuración")
    print(f"   3. Intenta marcar {mañana} como día cerrado")
    print(f"   4. Deberías ver el mensaje: 'No se puede cerrar el día porque hay citas reservadas'")

if __name__ == "__main__":
    probar_verificacion() 