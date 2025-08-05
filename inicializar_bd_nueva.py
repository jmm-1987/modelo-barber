#!/usr/bin/env python3
"""
Script para inicializar una base de datos completamente nueva
"""

import sqlite3
import os

def inicializar_bd_nueva():
    """Inicializa una base de datos completamente nueva con datos de ejemplo"""
    
    # Eliminar la base de datos si existe
    if os.path.exists('citas.db'):
        os.remove('citas.db')
        print("🗑️ Base de datos anterior eliminada")
    
    # Crear nueva base de datos
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🔧 Creando nueva base de datos...")
    
    # Crear todas las tablas
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            servicio TEXT NOT NULL,
            precio TEXT NOT NULL,
            dia TEXT NOT NULL,
            hora TEXT NOT NULL,
            peluquero_id INTEGER,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS horarios_disponibles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora TEXT UNIQUE,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio TEXT NOT NULL,
            descripcion TEXT,
            imagen_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS peluqueros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            foto_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_negocio (
            id INTEGER PRIMARY KEY,
            nombre_negocio TEXT DEFAULT 'Barbería del Oeste',
            direccion TEXT DEFAULT 'Calle Principal 123',
            telefono TEXT DEFAULT '+34 123 456 789',
            email TEXT DEFAULT 'info@barberia.com',
            hora_apertura TEXT DEFAULT '10:00',
            hora_cierre TEXT DEFAULT '19:00',
            dias_laborables TEXT DEFAULT 'lunes-viernes',
            duracion_corte INTEGER DEFAULT 30,
            duracion_barba INTEGER DEFAULT 20,
            duracion_combo INTEGER DEFAULT 45,
            duracion_tratamiento INTEGER DEFAULT 60,
            intervalo_citas INTEGER DEFAULT 30,
            anticipacion_reserva INTEGER DEFAULT 2,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS dias_cerrados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT,
            peluquero_id INTEGER NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(fecha, peluquero_id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS dias_festivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            tipo TEXT DEFAULT 'festivo',
            activo BOOLEAN DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    print("✅ Tablas creadas correctamente")
    
    # Insertar datos de ejemplo
    
    # Horarios disponibles
    horarios = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
        '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
        '17:00', '17:30', '18:00', '18:30'
    ]
    
    for hora in horarios:
        c.execute('INSERT INTO horarios_disponibles (hora) VALUES (?)', (hora,))
    
    print(f"✅ {len(horarios)} horarios insertados")
    
    # Servicios
    servicios = [
        ('Corte de Cabello', '15€', 'Corte de cabello profesional'),
        ('Barba', '10€', 'Arreglo de barba y bigote'),
        ('Corte + Barba', '20€', 'Corte de cabello y arreglo de barba'),
        ('Color', '25€', 'Tinte de cabello profesional')
    ]
    
    for servicio in servicios:
        c.execute('INSERT INTO servicios (nombre, precio, descripcion) VALUES (?, ?, ?)', servicio)
    
    print(f"✅ {len(servicios)} servicios insertados")
    
    # Peluqueros
    peluqueros = [
        ('María García', '/static/peluquero1.png'),
        ('Juan López', '/static/peluquero2.png'),
        ('Pedro Martínez', '/static/peluquero3.png')
    ]
    
    for peluquero in peluqueros:
        c.execute('INSERT INTO peluqueros (nombre, foto_url) VALUES (?, ?)', peluquero)
    
    print(f"✅ {len(peluqueros)} peluqueros insertados")
    
    # Configuración del negocio
    c.execute('''
        INSERT INTO configuracion_negocio (
            id, nombre_negocio, direccion, telefono, email,
            hora_apertura, hora_cierre, dias_laborables
        ) VALUES (1, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Barbería del Oeste',
        'Calle Principal 123, Madrid',
        '+34 123 456 789',
        'info@barberia.com',
        '09:00',
        '19:00',
        'lunes-viernes'
    ))
    
    print("✅ Configuración del negocio insertada")
    
    # Guardar cambios
    conn.commit()
    conn.close()
    
    print("\n🎉 ¡Base de datos nueva creada exitosamente!")
    print("📋 Datos incluidos:")
    print("   - Horarios disponibles: 20 horarios")
    print("   - Servicios: 4 servicios")
    print("   - Peluqueros: 3 peluqueros")
    print("   - Configuración del negocio")
    print("\n🚀 Ahora puedes hacer tus propias pruebas desde cero")

if __name__ == "__main__":
    inicializar_bd_nueva() 