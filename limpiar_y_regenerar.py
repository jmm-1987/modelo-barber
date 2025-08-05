#!/usr/bin/env python3
"""
Script para limpiar y regenerar citas correctamente
"""

import sqlite3
import datetime
import random

def limpiar_y_regenerar():
    """Limpia las citas y las regenera correctamente"""
    
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🧹 Limpiando citas existentes...")
    c.execute('DELETE FROM citas')
    
    # Obtener peluqueros
    c.execute('SELECT id, nombre FROM peluqueros WHERE activo = 1')
    peluqueros = c.fetchall()
    print(f"👨‍💼 Peluqueros disponibles: {len(peluqueros)}")
    
    # Obtener servicios
    c.execute('SELECT nombre, precio FROM servicios WHERE activo = 1')
    servicios = c.fetchall()
    print(f"✂️ Servicios disponibles: {len(servicios)}")
    
    # Obtener horarios
    c.execute('SELECT hora FROM horarios_disponibles WHERE activo = 1 ORDER BY hora')
    horarios = [row[0] for row in c.fetchall()]
    print(f"🕐 Horarios disponibles: {len(horarios)}")
    
    # Nombres de clientes
    nombres = [
        "María García", "Ana López", "Carmen Rodríguez", "Isabel Martínez", "Rosa Sánchez",
        "Elena Pérez", "Laura González", "Sofia Fernández", "Patricia Jiménez", "Mónica Ruiz",
        "Cristina Moreno", "Beatriz Díaz", "Nuria Martín", "Victoria Alonso", "Teresa Gutiérrez",
        "Pilar Romero", "Angeles Navarro", "Dolores Torres", "Concepción Domínguez", "Isabel Vázquez"
    ]
    
    # Generar citas para los próximos 7 días
    hoy = datetime.date.today()
    citas_generadas = 0
    
    for dia_offset in range(7):
        fecha = hoy + datetime.timedelta(days=dia_offset)
        fecha_str = fecha.strftime('%Y-%m-%d')
        
        # Saltar domingos
        if fecha.weekday() == 6:
            continue
            
        print(f"\n📅 Generando citas para {fecha_str}")
        
        # Seleccionar algunas horas para tener múltiples citas
        horas_multiples = random.sample(horarios[2:8], 3)  # Entre 10:30 y 15:30
        
        for hora in horas_multiples:
            # Generar 2-3 citas para la misma hora con distintos peluqueros
            num_citas = random.randint(2, min(3, len(peluqueros)))
            peluqueros_seleccionados = random.sample(peluqueros, num_citas)
            
            print(f"  🕐 {hora}: {num_citas} citas")
            
            for i, (peluquero_id, peluquero_nombre) in enumerate(peluqueros_seleccionados):
                # Seleccionar cliente y servicio
                cliente = random.choice(nombres)
                servicio, precio = random.choice(servicios)
                telefono = f"6{random.randint(10000000, 99999999)}"
                
                # Insertar cita con el orden correcto según la estructura de la tabla
                c.execute('''
                    INSERT INTO citas (nombre, telefono, servicio, dia, hora, peluquero_id, fecha_creacion, precio)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
                ''', (cliente, telefono, servicio, fecha_str, hora, peluquero_id, precio))
                
                print(f"    👤 {cliente} - {servicio} - {peluquero_nombre}")
                citas_generadas += 1
        
        # Generar algunas citas individuales también
        horas_individuales = random.sample(horarios[8:12], 2)  # Entre 16:00 y 18:00
        
        for hora in horas_individuales:
            cliente = random.choice(nombres)
            servicio, precio = random.choice(servicios)
            telefono = f"6{random.randint(10000000, 99999999)}"
            peluquero_id, peluquero_nombre = random.choice(peluqueros)
            
            c.execute('''
                INSERT INTO citas (nombre, telefono, servicio, dia, hora, peluquero_id, fecha_creacion, precio)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
            ''', (cliente, telefono, servicio, fecha_str, hora, peluquero_id, precio))
            
            print(f"  🕐 {hora}: {cliente} - {servicio} - {peluquero_nombre}")
            citas_generadas += 1
    
    # Guardar cambios
    conn.commit()
    conn.close()
    
    print(f"\n✅ Se generaron {citas_generadas} citas de prueba correctamente")
    print("🎯 Ahora puedes probar el panel para ver múltiples citas en la misma hora")
    
    return citas_generadas

if __name__ == "__main__":
    limpiar_y_regenerar() 