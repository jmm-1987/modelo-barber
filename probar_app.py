#!/usr/bin/env python3
"""
Script para probar la aplicación Flask
"""

import requests
import time

def probar_app():
    print("🧪 Probando la aplicación Flask...")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Esperar un poco para que la app se inicie
    print("⏳ Esperando que la aplicación se inicie...")
    time.sleep(2)
    
    try:
        # Probar la página principal
        print("\n1. Probando página principal...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Página principal funciona")
        else:
            print(f"   ❌ Error en página principal: {response.status_code}")
        
        # Probar el diagnóstico
        print("\n2. Probando endpoint de diagnóstico...")
        response = requests.get(f"{base_url}/diagnostico")
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print("   ✅ Diagnóstico funciona")
                print(f"   📁 Archivos estáticos: {len(data.get('static_files', []))}")
                print(f"   📄 Templates: {len(data.get('templates', []))}")
            else:
                print(f"   ❌ Error en diagnóstico: {data.get('error')}")
        else:
            print(f"   ❌ Error en diagnóstico: {response.status_code}")
        
        # Probar archivos estáticos
        print("\n3. Probando archivos estáticos...")
        archivos_test = ['logo.png', 'fondo.png', 'reloj.png']
        for archivo in archivos_test:
            response = requests.get(f"{base_url}/static/{archivo}")
            if response.status_code == 200:
                print(f"   ✅ {archivo} funciona")
            else:
                print(f"   ❌ {archivo} falla: {response.status_code}")
        
        print("\n" + "=" * 40)
        print("🎉 Pruebas completadas")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación")
        print("💡 Asegúrate de que la aplicación esté ejecutándose con: py app.py")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    probar_app() 