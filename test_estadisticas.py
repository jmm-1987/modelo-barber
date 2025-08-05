#!/usr/bin/env python3
"""
Script para probar las estadísticas del panel
"""

import requests
import json

def test_estadisticas():
    """Prueba el endpoint de estadísticas"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Probando estadísticas...")
    
    # Probar estadísticas generales
    try:
        response = requests.get(f"{base_url}/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas generales:")
            print(f"   Total citas: {stats.get('total_citas', 0)}")
            print(f"   Citas hoy: {stats.get('citas_hoy', 0)}")
            print(f"   Citas semana: {stats.get('citas_semana', 0)}")
            print(f"   Citas pendientes: {stats.get('citas_pendientes', 0)}")
            print(f"   Total ingresos: {stats.get('total_ingresos', '0€')}")
            print(f"   Ingresos hoy: {stats.get('ingresos_hoy', '0€')}")
            print(f"   Ingresos semana: {stats.get('ingresos_semana', '0€')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando: {e}")
    
    # Probar estadísticas con filtro de peluquero
    try:
        response = requests.get(f"{base_url}/estadisticas?peluquero_id=1")
        if response.status_code == 200:
            stats = response.json()
            print("\n✅ Estadísticas para peluquero 1:")
            print(f"   Total citas: {stats.get('total_citas', 0)}")
            print(f"   Citas hoy: {stats.get('citas_hoy', 0)}")
            print(f"   Citas semana: {stats.get('citas_semana', 0)}")
            print(f"   Citas pendientes: {stats.get('citas_pendientes', 0)}")
            print(f"   Total ingresos: {stats.get('total_ingresos', '0€')}")
            print(f"   Ingresos hoy: {stats.get('ingresos_hoy', '0€')}")
            print(f"   Ingresos semana: {stats.get('ingresos_semana', '0€')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando: {e}")

if __name__ == "__main__":
    test_estadisticas() 