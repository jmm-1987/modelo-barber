#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla citas
"""

import sqlite3

def verificar_estructura():
    """Verifica la estructura de la tabla citas"""
    
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🔍 Verificando estructura de la tabla citas...")
    
    # Obtener información de la tabla
    c.execute("PRAGMA table_info(citas)")
    columnas = c.fetchall()
    
    print("\n📋 Estructura de la tabla citas:")
    for col in columnas:
        print(f"   {col[1]} ({col[2]})")
    
    # Mostrar una cita completa
    c.execute('SELECT * FROM citas LIMIT 1')
    cita = c.fetchone()
    
    if cita:
        print(f"\n📄 Ejemplo de cita:")
        print(f"   ID: {cita[0]}")
        print(f"   Nombre: {cita[1]}")
        print(f"   Teléfono: {cita[2]}")
        print(f"   Servicio: {cita[3]}")
        print(f"   Precio: {cita[4]}")
        print(f"   Día: {cita[5]}")
        print(f"   Hora: {cita[6]}")
        print(f"   Peluquero ID: {cita[7]}")
    
    conn.close()

if __name__ == "__main__":
    verificar_estructura() 