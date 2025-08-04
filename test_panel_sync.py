#!/usr/bin/env python3
"""
Script para probar la sincronización entre vistas de escritorio y móvil del panel
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_panel_sync():
    """Prueba la sincronización entre las vistas del panel"""
    
    base_url = "http://localhost:5000"
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    
    print(f"🧪 Iniciando prueba de sincronización del panel")
    print(f"📅 Fecha de prueba: {fecha_hoy}")
    
    # Paso 1: Limpiar citas existentes para la fecha
    print(f"\n1️⃣ Limpiando citas existentes...")
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        citas_existentes = len(data.get('citas', []))
        print(f"📊 Citas existentes: {citas_existentes}")
        
        if citas_existentes > 0:
            print("⚠️  Hay citas existentes, esto podría afectar la prueba")
    except Exception as e:
        print(f"❌ Error al verificar citas existentes: {e}")
        return
    
    # Paso 2: Reservar una cita de prueba
    print(f"\n2️⃣ Reservando cita de prueba...")
    cita_prueba = {
        'nombre': 'Test Sincronización',
        'servicio': 'Corte Test',
        'dia': fecha_hoy,
        'hora': '15:00',
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
    
    # Paso 3: Verificar inmediatamente después de la reserva
    print(f"\n3️⃣ Verificando inmediatamente después de la reserva...")
    time.sleep(0.5)  # Pequeña pausa para simular el tiempo de procesamiento
    
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        citas = data.get('citas', [])
        horas_ocupadas = data.get('ocupadas', [])
        
        print(f"📊 Citas encontradas: {len(citas)}")
        print(f"⏰ Horas ocupadas: {horas_ocupadas}")
        
        cita_encontrada = None
        for cita in citas:
            if cita['hora'] == '15:00' and cita['nombre'] == 'Test Sincronización':
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            print(f"✅ Cita encontrada inmediatamente:")
            print(f"   - Hora: {cita_encontrada['hora']}")
            print(f"   - Nombre: {cita_encontrada['nombre']}")
            print(f"   - Servicio: {cita_encontrada['servicio']}")
        else:
            print(f"❌ Cita NO encontrada inmediatamente")
            print(f"📋 Todas las citas:")
            for cita in citas:
                print(f"   - {cita['hora']}: {cita['nombre']}")
    
    except Exception as e:
        print(f"❌ Error al verificar cita: {e}")
    
    # Paso 4: Verificar después de un tiempo (simulando actualización automática)
    print(f"\n4️⃣ Verificando después de 2 segundos (simulando actualización)...")
    time.sleep(2)
    
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_hoy})
        data = response.json()
        
        citas = data.get('citas', [])
        horas_ocupadas = data.get('ocupadas', [])
        
        print(f"📊 Citas encontradas: {len(citas)}")
        print(f"⏰ Horas ocupadas: {horas_ocupadas}")
        
        cita_encontrada = None
        for cita in citas:
            if cita['hora'] == '15:00' and cita['nombre'] == 'Test Sincronización':
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            print(f"✅ Cita encontrada después de 2 segundos:")
            print(f"   - Hora: {cita_encontrada['hora']}")
            print(f"   - Nombre: {cita_encontrada['nombre']}")
            print(f"   - Servicio: {cita_encontrada['servicio']}")
        else:
            print(f"❌ Cita NO encontrada después de 2 segundos")
            print(f"📋 Todas las citas:")
            for cita in citas:
                print(f"   - {cita['hora']}: {cita['nombre']}")
    
    except Exception as e:
        print(f"❌ Error al verificar cita: {e}")
    
    # Paso 5: Verificar con diferentes formatos de fecha
    print(f"\n5️⃣ Verificando con diferentes formatos de fecha...")
    
    # Formato DD/MM/YYYY
    fecha_formato_display = fecha_hoy.split('-')[2] + '/' + fecha_hoy.split('-')[1] + '/' + fecha_hoy.split('-')[0]
    print(f"📅 Probando formato DD/MM/YYYY: {fecha_formato_display}")
    
    try:
        response = requests.post(f"{base_url}/citas_dia", 
                               json={'dia': fecha_formato_display})
        data = response.json()
        
        if data.get('error'):
            print(f"❌ Error con formato DD/MM/YYYY: {data.get('error')}")
        else:
            citas = data.get('citas', [])
            print(f"✅ Formato DD/MM/YYYY funciona, citas encontradas: {len(citas)}")
    
    except Exception as e:
        print(f"❌ Error con formato DD/MM/YYYY: {e}")
    
    print(f"\n🏁 Prueba de sincronización completada")

if __name__ == "__main__":
    test_panel_sync() 