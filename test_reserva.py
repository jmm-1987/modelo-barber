#!/usr/bin/env python3
"""
Script de prueba para verificar la consistencia de citas entre paneles
"""

import requests
import json
from datetime import datetime, timedelta

def test_reserva_cita():
    """Prueba la reserva de una cita y verifica que aparezca en ambos paneles"""
    
    # URL base
    base_url = "http://localhost:5000"
    
    # Datos de la cita de prueba
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    hora_prueba = "14:00"
    
    print(f"🧪 Iniciando prueba de reserva de cita")
    print(f"📅 Fecha: {fecha_hoy}")
    print(f"⏰ Hora: {hora_prueba}")
    
    # Paso 1: Verificar citas existentes para la fecha
    print("\n1️⃣ Verificando citas existentes...")
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        print(f"📊 Citas existentes para {fecha_hoy}: {len(data.get('citas', []))}")
        for cita in data.get('citas', []):
            print(f"   - {cita['hora']}: {cita['nombre']} ({cita['servicio']})")
    except Exception as e:
        print(f"❌ Error al verificar citas existentes: {e}")
        return
    
    # Paso 2: Reservar una nueva cita
    print(f"\n2️⃣ Reservando nueva cita...")
    cita_prueba = {
        'nombre': 'Cliente Prueba',
        'servicio': 'Corte de prueba',
        'dia': fecha_hoy,
        'hora': hora_prueba,
        'telefono': '612345678'
    }
    
    try:
        response = requests.post(f"{base_url}/reservar_cita", 
                               json=cita_prueba)
        data = response.json()
        
        if data.get('ok'):
            print(f"✅ Cita reservada exitosamente")
        else:
            print(f"❌ Error al reservar cita: {data.get('msg')}")
            return
    except Exception as e:
        print(f"❌ Error al reservar cita: {e}")
        return
    
    # Paso 3: Verificar que la cita aparezca en la consulta
    print(f"\n3️⃣ Verificando que la cita aparezca en la consulta...")
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        citas_actuales = data.get('citas', [])
        cita_encontrada = None
        
        for cita in citas_actuales:
            if cita['hora'] == hora_prueba and cita['nombre'] == 'Cliente Prueba':
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            print(f"✅ Cita encontrada en la consulta:")
            print(f"   - Hora: {cita_encontrada['hora']}")
            print(f"   - Nombre: {cita_encontrada['nombre']}")
            print(f"   - Servicio: {cita_encontrada['servicio']}")
            print(f"   - Teléfono: {cita_encontrada['telefono']}")
        else:
            print(f"❌ La cita no aparece en la consulta")
            print(f"📊 Citas actuales: {len(citas_actuales)}")
            for cita in citas_actuales:
                print(f"   - {cita['hora']}: {cita['nombre']}")
    
    except Exception as e:
        print(f"❌ Error al verificar cita: {e}")
    
    # Paso 4: Verificar horas ocupadas
    print(f"\n4️⃣ Verificando horas ocupadas...")
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        horas_ocupadas = data.get('ocupadas', [])
        if hora_prueba in horas_ocupadas:
            print(f"✅ La hora {hora_prueba} aparece como ocupada")
        else:
            print(f"❌ La hora {hora_prueba} NO aparece como ocupada")
            print(f"📊 Horas ocupadas: {horas_ocupadas}")
    
    except Exception as e:
        print(f"❌ Error al verificar horas ocupadas: {e}")
    
    print(f"\n🏁 Prueba completada")

if __name__ == "__main__":
    test_reserva_cita() 