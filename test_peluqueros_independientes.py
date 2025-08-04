#!/usr/bin/env python3
"""
Script de prueba para verificar que los peluqueros tienen calendarios independientes
"""

import sqlite3
import datetime
from app import DB_PATH, guardar_cita, citas_dia

def crear_peluqueros_prueba():
    """Crear peluqueros de prueba si no existen"""
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
    
    # Insertar peluqueros de prueba
    peluqueros = [
        ('Juan',),
        ('Pedro',),
        ('María',)
    ]
    
    for peluquero in peluqueros:
        c.execute('INSERT OR IGNORE INTO peluqueros (nombre) VALUES (?)', peluquero)
    
    conn.commit()
    conn.close()
    print("✅ Peluqueros de prueba creados")

def crear_citas_prueba():
    """Crear citas de prueba para diferentes peluqueros"""
    # Obtener IDs de peluqueros
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, nombre FROM peluqueros')
    peluqueros = c.fetchall()
    conn.close()
    
    if not peluqueros:
        print("❌ No hay peluqueros en la base de datos")
        return
    
    print(f"📋 Peluqueros disponibles: {peluqueros}")
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Crear citas de prueba
    citas_prueba = [
        # Juan tiene cita a las 17:00
        ('Juan', 'Corte', mañana, '17:00', 'Juan Pérez', '123456789', 1),
        # Pedro tiene cita a las 18:00  
        ('Pedro', 'Barba', mañana, '18:00', 'Pedro García', '987654321', 2),
        # María tiene cita a las 19:00
        ('María', 'Combo', mañana, '19:00', 'María López', '555666777', 3),
    ]
    
    for nombre_peluquero, servicio, fecha, hora, cliente, telefono, peluquero_id in citas_prueba:
        try:
            guardar_cita(cliente, servicio, fecha, hora, telefono, peluquero_id)
            print(f"✅ Cita creada: {cliente} - {servicio} - {fecha} {hora} - {nombre_peluquero}")
        except Exception as e:
            print(f"❌ Error creando cita para {cliente}: {e}")

def verificar_citas_por_peluquero():
    """Verificar que cada peluquero tiene su propio calendario"""
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"\n🔍 Verificando citas para {mañana}:")
    print("=" * 50)
    
    # Verificar citas por peluquero
    for peluquero_id in [1, 2, 3]:
        # Simular la consulta del endpoint
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            SELECT c.id, c.hora, c.nombre, c.servicio, c.telefono, c.peluquero_id, p.nombre as peluquero_nombre 
            FROM citas c 
            LEFT JOIN peluqueros p ON c.peluquero_id = p.id 
            WHERE c.dia = ? AND c.peluquero_id = ?
        ''', (mañana, peluquero_id))
        
        rows = c.fetchall()
        conn.close()
        
        if rows:
            print(f"📅 Peluquero ID {peluquero_id}:")
            for row in rows:
                print(f"   - {row[1]} - {row[2]} ({row[6]})")
        else:
            print(f"📅 Peluquero ID {peluquero_id}: Sin citas")
    
    # Verificar todas las citas juntas
    print(f"\n📋 Todas las citas del día:")
    print("=" * 30)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.hora, c.nombre, c.servicio, c.telefono, c.peluquero_id, p.nombre as peluquero_nombre 
        FROM citas c 
        LEFT JOIN peluqueros p ON c.peluquero_id = p.id 
        WHERE c.dia = ?
    ''', (mañana,))
    
    rows = c.fetchall()
    conn.close()
    
    for row in rows:
        print(f"   - {row[1]} - {row[2]} ({row[6]})")

def verificar_disponibilidad():
    """Verificar que las horas están disponibles para otros peluqueros"""
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"\n✅ Verificando disponibilidad:")
    print("=" * 40)
    
    horas_ocupadas_por_peluquero = {}
    
    for peluquero_id in [1, 2, 3]:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT hora FROM citas WHERE dia = ? AND peluquero_id = ?', (mañana, peluquero_id))
        horas = [row[0] for row in c.fetchall()]
        conn.close()
        
        horas_ocupadas_por_peluquero[peluquero_id] = horas
        print(f"   Peluquero {peluquero_id}: {horas}")
    
    # Verificar que las horas no se solapan entre peluqueros
    for peluquero1 in [1, 2, 3]:
        for peluquero2 in [1, 2, 3]:
            if peluquero1 != peluquero2:
                horas_comunes = set(horas_ocupadas_por_peluquero[peluquero1]) & set(horas_ocupadas_por_peluquero[peluquero2])
                if horas_comunes:
                    print(f"⚠️  CONFLICTO: Peluqueros {peluquero1} y {peluquero2} tienen citas a las mismas horas: {horas_comunes}")
                else:
                    print(f"✅ Peluqueros {peluquero1} y {peluquero2}: Sin conflictos")

if __name__ == "__main__":
    print("🧪 Iniciando prueba de peluqueros independientes...")
    
    # Crear peluqueros de prueba
    crear_peluqueros_prueba()
    
    # Crear citas de prueba
    crear_citas_prueba()
    
    # Verificar que funciona correctamente
    verificar_citas_por_peluquero()
    verificar_disponibilidad()
    
    print("\n🎉 Prueba completada!") 