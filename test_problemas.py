#!/usr/bin/env python3
"""
Script para probar los problemas de imágenes y calendario
"""

import requests
import json

def test_problemas():
    """Prueba los problemas reportados"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Probando problemas reportados...")
    
    # 1. Probar obtención de servicios
    print("\n📤 Probando obtención de servicios...")
    try:
        response = requests.get(f"{base_url}/obtener_servicios")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servicios obtenidos: {len(data.get('servicios', []))}")
            for servicio in data.get('servicios', []):
                print(f"   - {servicio.get('nombre')}: img='{servicio.get('img')}'")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar obtención de días disponibles
    print("\n📅 Probando obtención de días disponibles...")
    try:
        response = requests.get(f"{base_url}/proximos_dias_disponibles")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Días obtenidos: {len(data.get('dias', []))}")
            for dia in data.get('dias', [])[:5]:  # Solo mostrar los primeros 5
                print(f"   - {dia.get('fecha')}: {dia.get('disponibles')} disponibles")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar obtención de peluqueros
    print("\n👨‍💼 Probando obtención de peluqueros...")
    try:
        response = requests.get(f"{base_url}/obtener_peluqueros")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Peluqueros obtenidos: {len(data.get('peluqueros', []))}")
            for peluquero in data.get('peluqueros', []):
                print(f"   - {peluquero.get('nombre')}: foto='{peluquero.get('foto_url')}'")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_problemas() 