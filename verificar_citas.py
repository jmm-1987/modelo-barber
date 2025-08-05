#!/usr/bin/env python3
"""
Script para verificar las citas en la base de datos
"""

import sqlite3
from datetime import datetime, date

def verificar_citas():
    """Verifica las citas en la base de datos"""
    
    try:
        conn = sqlite3.connect('citas.db')
        c = conn.cursor()
        
        print("🔍 Verificando citas en la base de datos...")
        
        # Contar total de citas
        c.execute('SELECT COUNT(*) FROM citas')
        total = c.fetchone()[0]
        print(f"📊 Total de citas: {total}")
        
        if total > 0:
            # Mostrar algunas citas
            c.execute('SELECT * FROM citas LIMIT 10')
            citas = c.fetchall()
            
            print("\n📅 Primeras 10 citas:")
            for cita in citas:
                print(f"   ID: {cita[0]}, Cliente: {cita[1]}, Fecha: {cita[5]}, Hora: {cita[6]}, Precio: {cita[4]}")
            
            # Verificar fecha actual
            hoy = date.today().strftime('%Y-%m-%d')
            print(f"\n📅 Fecha actual: {hoy}")
            
            # Contar citas de hoy
            c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (hoy,))
            citas_hoy = c.fetchone()[0]
            print(f"📊 Citas de hoy: {citas_hoy}")
            
            # Contar citas futuras
            c.execute('SELECT COUNT(*) FROM citas WHERE dia >= ?', (hoy,))
            citas_futuras = c.fetchone()[0]
            print(f"📊 Citas futuras: {citas_futuras}")
            
            # Mostrar fechas únicas
            c.execute('SELECT DISTINCT dia FROM citas ORDER BY dia')
            fechas = c.fetchall()
            print(f"\n📅 Fechas con citas: {len(fechas)}")
            for fecha in fechas[:5]:  # Mostrar solo las primeras 5
                print(f"   {fecha[0]}")
        else:
            print("❌ No hay citas en la base de datos")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_citas() 