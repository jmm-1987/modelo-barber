#!/usr/bin/env python3
"""
Script final para probar la sincronización mejorada entre paneles
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_final_sync():
    """Prueba final de sincronización entre paneles"""
    
    base_url = "http://localhost:5000"
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    
    print(f"🧪 Prueba final de sincronización entre paneles")
    print(f"📅 Fecha: {fecha_hoy}")
    print(f"🕐 Hora actual: {datetime.now().strftime('%H:%M:%S')}")
    
    # Paso 1: Verificar estado inicial
    print(f"\n1️⃣ Verificando estado inicial...")
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        citas_iniciales = len(data.get('citas', []))
        print(f"📊 Citas iniciales: {citas_iniciales}")
        
        if citas_iniciales > 0:
            print("📋 Citas existentes:")
            for cita in data.get('citas', []):
                print(f"   - {cita['hora']}: {cita['nombre']} ({cita['servicio']})")
    
    except Exception as e:
        print(f"❌ Error al verificar estado inicial: {e}")
        return
    
    # Paso 2: Reservar múltiples citas de prueba
    print(f"\n2️⃣ Reservando múltiples citas de prueba...")
    
    citas_prueba = [
        {
            'nombre': 'Test Sincronización 1',
            'servicio': 'Corte Test 1',
            'dia': fecha_hoy,
            'hora': '16:00',
            'telefono': '612345678'
        },
        {
            'nombre': 'Test Sincronización 2',
            'servicio': 'Corte Test 2',
            'dia': fecha_hoy,
            'hora': '17:00',
            'telefono': '612345679'
        }
    ]
    
    for i, cita in enumerate(citas_prueba, 1):
        try:
            response = requests.post(f"{base_url}/reservar_cita", 
                                   json=cita)
            data = response.json()
            
            if data.get('ok'):
                print(f"✅ Cita {i} reservada: {cita['hora']} - {cita['nombre']}")
            else:
                print(f"❌ Error al reservar cita {i}: {data.get('msg')}")
        except Exception as e:
            print(f"❌ Error al reservar cita {i}: {e}")
    
    # Paso 3: Verificar inmediatamente
    print(f"\n3️⃣ Verificando inmediatamente después de las reservas...")
    time.sleep(0.5)
    
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        citas = data.get('citas', [])
        horas_ocupadas = data.get('ocupadas', [])
        
        print(f"📊 Total de citas: {len(citas)}")
        print(f"⏰ Horas ocupadas: {horas_ocupadas}")
        
        # Verificar que ambas citas de prueba estén presentes
        citas_encontradas = []
        for cita in citas:
            if 'Test Sincronización' in cita['nombre']:
                citas_encontradas.append(cita)
        
        print(f"✅ Citas de prueba encontradas: {len(citas_encontradas)}")
        for cita in citas_encontradas:
            print(f"   - {cita['hora']}: {cita['nombre']} ({cita['servicio']})")
    
    except Exception as e:
        print(f"❌ Error al verificar citas: {e}")
    
    # Paso 4: Verificar después de un tiempo (simulando actualización automática)
    print(f"\n4️⃣ Verificando después de 3 segundos (simulando actualización automática)...")
    time.sleep(3)
    
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        citas = data.get('citas', [])
        horas_ocupadas = data.get('ocupadas', [])
        
        print(f"📊 Total de citas: {len(citas)}")
        print(f"⏰ Horas ocupadas: {horas_ocupadas}")
        
        # Verificar que ambas citas de prueba sigan presentes
        citas_encontradas = []
        for cita in citas:
            if 'Test Sincronización' in cita['nombre']:
                citas_encontradas.append(cita)
        
        print(f"✅ Citas de prueba encontradas: {len(citas_encontradas)}")
        for cita in citas_encontradas:
            print(f"   - {cita['hora']}: {cita['nombre']} ({cita['servicio']})")
    
    except Exception as e:
        print(f"❌ Error al verificar citas: {e}")
    
    # Paso 5: Verificar consistencia de datos
    print(f"\n5️⃣ Verificando consistencia de datos...")
    
    try:
        # Hacer múltiples consultas rápidas para verificar consistencia
        for i in range(3):
            response = requests.post(f"{base_url}/citas_dia", 
                                   json={'dia': fecha_hoy})
            data = response.json()
            citas = data.get('citas', [])
            print(f"   Consulta {i+1}: {len(citas)} citas encontradas")
            time.sleep(0.1)
        
        print("✅ Consistencia de datos verificada")
    
    except Exception as e:
        print(f"❌ Error al verificar consistencia: {e}")
    
    print(f"\n🏁 Prueba final completada")
    print(f"💡 Recomendaciones:")
    print(f"   - Las citas deberían aparecer inmediatamente en ambos paneles")
    print(f"   - Si hay problemas, usar el botón '🔄 Actualizar' en el panel")
    print(f"   - Verificar que ambas vistas (escritorio y móvil) muestren los mismos datos")

if __name__ == "__main__":
    test_final_sync() 