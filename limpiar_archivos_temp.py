#!/usr/bin/env python3
"""
Script para limpiar archivos temporales de desarrollo
"""

import os

def limpiar_archivos_temp():
    """Elimina archivos temporales de desarrollo"""
    
    archivos_a_eliminar = [
        'test_estadisticas.py',
        'verificar_citas.py',
        'verificar_estructura.py',
        'limpiar_y_regenerar.py',
        'generar_citas_correcto.py',
        'debug_citas.py',
        'inicializar_bd_nueva.py',
        'limpiar_archivos_temp.py'
    ]
    
    print("🧹 Limpiando archivos temporales de desarrollo...")
    
    eliminados = 0
    for archivo in archivos_a_eliminar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"🗑️ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
        else:
            print(f"⚠️ No encontrado: {archivo}")
    
    print(f"\n✅ Limpieza completada: {eliminados} archivos eliminados")
    print("🎯 La base de datos nueva está lista para tus pruebas")

if __name__ == "__main__":
    limpiar_archivos_temp() 