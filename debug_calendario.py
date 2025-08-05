#!/usr/bin/env python3
"""
Script para debuggear el problema del calendario
"""

import requests
import json

def debug_calendario():
    """Debuggea el problema del calendario"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Debuggeando problema del calendario...")
    
    # 1. Probar endpoint sin parámetros
    print("\n📅 Probando /proximos_dias_disponibles sin parámetros...")
    try:
        response = requests.get(f"{base_url}/proximos_dias_disponibles")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta: {len(data.get('dias', []))} días")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # 2. Probar endpoint con peluquero_id
    print("\n📅 Probando /proximos_dias_disponibles con peluquero_id=1...")
    try:
        response = requests.get(f"{base_url}/proximos_dias_disponibles?peluquero_id=1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta: {len(data.get('dias', []))} días")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # 3. Probar endpoint de horarios
    print("\n🕐 Probando /obtener_horarios_disponibles...")
    try:
        response = requests.get(f"{base_url}/obtener_horarios_disponibles")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Horarios: {len(data.get('horarios', []))}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_calendario() 