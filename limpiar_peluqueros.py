#!/usr/bin/env python3
"""
Script para limpiar peluqueros duplicados
"""

import sqlite3

DB_PATH = 'citas.db'

def limpiar_peluqueros():
    """Limpiar peluqueros duplicados y dejar solo 3 principales"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ver peluqueros actuales
    c.execute('SELECT id, nombre FROM peluqueros')
    peluqueros = c.fetchall()
    print(f"📋 Peluqueros actuales: {peluqueros}")
    
    # Eliminar todos los peluqueros
    c.execute('DELETE FROM peluqueros')
    
    # Insertar solo 3 peluqueros principales
    peluqueros_principales = [
        ('Juan',),
        ('Pedro',),
        ('María',)
    ]
    
    for peluquero in peluqueros_principales:
        c.execute('INSERT INTO peluqueros (nombre) VALUES (?)', peluquero)
    
    conn.commit()
    
    # Verificar resultado
    c.execute('SELECT id, nombre FROM peluqueros')
    peluqueros_finales = c.fetchall()
    print(f"✅ Peluqueros finales: {peluqueros_finales}")
    
    conn.close()
    print("🎉 Peluqueros limpiados correctamente!")

if __name__ == "__main__":
    limpiar_peluqueros() 