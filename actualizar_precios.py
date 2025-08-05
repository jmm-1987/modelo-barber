#!/usr/bin/env python3
"""
Script para actualizar los precios de las citas existentes.
"""

import sqlite3

DB_PATH = 'citas.db'

def actualizar_precios():
    """Actualiza los precios de las citas existentes"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Obtener servicios y sus precios
        c.execute("SELECT nombre, precio FROM servicios")
        servicios = dict(c.fetchall())
        print(f"📋 Servicios disponibles: {servicios}")
        
        # Obtener todas las citas
        c.execute("SELECT id, servicio, precio FROM citas")
        citas = c.fetchall()
        print(f"📊 Total de citas: {len(citas)}")
        
        # Actualizar cada cita
        actualizadas = 0
        for cita_id, servicio, precio_actual in citas:
            if servicio in servicios:
                precio_correcto = servicios[servicio]
                if precio_actual != precio_correcto:
                    c.execute("UPDATE citas SET precio = ? WHERE id = ?", (precio_correcto, cita_id))
                    print(f"✅ Cita {cita_id}: {servicio} -> {precio_correcto}")
                    actualizadas += 1
                else:
                    print(f"ℹ️ Cita {cita_id}: {servicio} ya tiene precio correcto ({precio_correcto})")
            else:
                print(f"⚠️ Cita {cita_id}: servicio '{servicio}' no encontrado")
        
        conn.commit()
        print(f"\n🎉 Proceso completado. {actualizadas} citas actualizadas.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Actualizando precios de citas...")
    actualizar_precios()
    print("🏁 Proceso completado.") 