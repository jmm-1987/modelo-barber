#!/usr/bin/env python3
"""
Script para migrar las citas existentes que no tienen precio.
Agrega el campo precio a las citas que no lo tienen.
"""

import sqlite3
import os

DB_PATH = 'citas.db'

def migrar_precios_citas():
    """Migra las citas existentes agregando el precio si no existe"""
    
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró la base de datos citas.db")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Verificar si la tabla citas tiene el campo precio
        c.execute("PRAGMA table_info(citas)")
        columnas = [col[1] for col in c.fetchall()]
        
        if 'precio' not in columnas:
            print("❌ La tabla citas no tiene el campo precio. Ejecuta primero la aplicación para crear la nueva estructura.")
            return
        
        # Contar citas sin precio
        c.execute("SELECT COUNT(*) FROM citas WHERE precio IS NULL OR precio = ''")
        citas_sin_precio = c.fetchone()[0]
        
        if citas_sin_precio == 0:
            print("✅ Todas las citas ya tienen precio asignado.")
            return
        
        print(f"🔍 Encontradas {citas_sin_precio} citas sin precio. Iniciando migración...")
        
        # Obtener todas las citas sin precio
        c.execute("SELECT id, servicio FROM citas WHERE precio IS NULL OR precio = ''")
        citas_sin_precio = c.fetchall()
        
        # Obtener precios de servicios
        c.execute("SELECT nombre, precio FROM servicios")
        precios_servicios = dict(c.fetchall())
        
        # Migrar cada cita
        citas_migradas = 0
        citas_omitidas = 0
        for cita_id, servicio in citas_sin_precio:
            # Buscar el precio del servicio
            if servicio in precios_servicios:
                precio = precios_servicios[servicio]
                # Actualizar la cita con el precio
                c.execute("UPDATE citas SET precio = ? WHERE id = ?", (precio, cita_id))
                citas_migradas += 1
                print(f"📝 Cita {cita_id}: {servicio} -> {precio}")
            else:
                # Si el servicio no existe, eliminar la cita
                c.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
                citas_omitidas += 1
                print(f"🗑️ Cita {cita_id} eliminada: servicio '{servicio}' no existe")
        
        conn.commit()
        print(f"✅ Migración completada. {citas_migradas} citas actualizadas, {citas_omitidas} citas eliminadas (servicios no existentes).")
        
        # Verificar que todas las citas tienen precio
        c.execute("SELECT COUNT(*) FROM citas WHERE precio IS NULL OR precio = ''")
        citas_sin_precio_final = c.fetchone()[0]
        
        if citas_sin_precio_final == 0:
            print("✅ Todas las citas ahora tienen precio asignado.")
        else:
            print(f"⚠️ Aún quedan {citas_sin_precio_final} citas sin precio.")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando migración de precios de citas...")
    migrar_precios_citas()
    print("🏁 Proceso completado.") 