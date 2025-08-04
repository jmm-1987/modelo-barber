#!/usr/bin/env python3
"""
Script para probar el endpoint /citas_dia con diferentes peluqueros
"""

import requests
import json
import datetime

def test_endpoint_citas():
    """Probar el endpoint /citas_dia con diferentes peluqueros"""
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"📅 Probando endpoint para la fecha: {mañana}")
    
    # URL base
    base_url = "http://localhost:5000"
    
    # Probar sin filtro de peluquero (todas las citas)
    print(f"\n🔍 Probando sin filtro de peluquero:")
    print("=" * 50)
    
    response = requests.post(f"{base_url}/citas_dia", 
                           json={'dia': mañana, 'peluquero_id': None})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Todas las citas: {len(data['citas'])} citas encontradas")
        for cita in data['citas']:
            print(f"   - {cita['hora']} - {cita['nombre']} (Peluquero: {cita['peluquero_nombre']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Probar con filtro de peluquero 1
    print(f"\n🔍 Probando con filtro de peluquero 1:")
    print("=" * 50)
    
    response = requests.post(f"{base_url}/citas_dia", 
                           json={'dia': mañana, 'peluquero_id': 1})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Citas del peluquero 1: {len(data['citas'])} citas encontradas")
        for cita in data['citas']:
            print(f"   - {cita['hora']} - {cita['nombre']} (Peluquero: {cita['peluquero_nombre']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Probar con filtro de peluquero 2
    print(f"\n🔍 Probando con filtro de peluquero 2:")
    print("=" * 50)
    
    response = requests.post(f"{base_url}/citas_dia", 
                           json={'dia': mañana, 'peluquero_id': 2})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Citas del peluquero 2: {len(data['citas'])} citas encontradas")
        for cita in data['citas']:
            print(f"   - {cita['hora']} - {cita['nombre']} (Peluquero: {cita['peluquero_nombre']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # Probar con filtro de peluquero 3
    print(f"\n🔍 Probando con filtro de peluquero 3:")
    print("=" * 50)
    
    response = requests.post(f"{base_url}/citas_dia", 
                           json={'dia': mañana, 'peluquero_id': 3})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Citas del peluquero 3: {len(data['citas'])} citas encontradas")
        for cita in data['citas']:
            print(f"   - {cita['hora']} - {cita['nombre']} (Peluquero: {cita['peluquero_nombre']})")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    test_endpoint_citas() 