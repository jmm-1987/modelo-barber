#!/usr/bin/env python3
"""
Script para migrar la base de datos existente.
Agrega la columna precio a la tabla citas si no existe.
"""

import sqlite3
import os

DB_PATH = 'citas.db'

def migrar_base_datos():
    """Migra la base de datos agregando la columna precio si no existe"""
    
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró la base de datos citas.db")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Verificar si la tabla citas tiene el campo precio
        c.execute("PRAGMA table_info(citas)")
        columnas = [col[1] for col in c.fetchall()]
        
        if 'precio' in columnas:
            print("✅ La tabla citas ya tiene la columna precio.")
            return
        
        print("🔍 Agregando columna precio a la tabla citas...")
        
        # Agregar la columna precio a la tabla citas
        c.execute("ALTER TABLE citas ADD COLUMN precio TEXT DEFAULT '25€'")
        
        conn.commit()
        print("✅ Columna precio agregada correctamente.")
        
        # Verificar que la columna se agregó correctamente
        c.execute("PRAGMA table_info(citas)")
        columnas_actualizadas = [col[1] for col in c.fetchall()]
        
        if 'precio' in columnas_actualizadas:
            print("✅ Verificación exitosa: la columna precio está presente.")
            
            # Contar citas existentes
            c.execute("SELECT COUNT(*) FROM citas")
            total_citas = c.fetchone()[0]
            print(f"📊 Total de citas en la base de datos: {total_citas}")
            
            if total_citas > 0:
                print("💡 Ejecuta el script migrar_precios_citas.py para asignar precios a las citas existentes.")
        else:
            print("❌ Error: La columna precio no se agregó correctamente.")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando migración de la base de datos...")
    migrar_base_datos()
    print("🏁 Proceso completado.") 