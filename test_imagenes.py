#!/usr/bin/env python3
"""
Script para probar las funciones de subida de imágenes
"""

import requests
import os

def test_imagenes():
    """Prueba las funciones de subida de imágenes"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Probando funciones de subida de imágenes...")
    
    # Crear un archivo de prueba
    test_file_path = "test_image.txt"
    with open(test_file_path, "w") as f:
        f.write("Este es un archivo de prueba")
    
    try:
        # Probar subida de imagen de servicio
        print("\n📤 Probando subida de imagen de servicio...")
        
        with open(test_file_path, "rb") as f:
            files = {'imagen': f}
            data = {'servicio_id': '1'}
            
            response = requests.post(f"{base_url}/subir_imagen_servicio", 
                                  files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Respuesta: {result}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
        
        # Probar subida de imagen de peluquero
        print("\n📤 Probando subida de imagen de peluquero...")
        
        with open(test_file_path, "rb") as f:
            files = {'imagen': f}
            data = {'peluquero_id': '1'}
            
            response = requests.post(f"{base_url}/subir_imagen_peluquero", 
                                  files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Respuesta: {result}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
    
    finally:
        # Limpiar archivo de prueba
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"\n🗑️ Archivo de prueba eliminado: {test_file_path}")

if __name__ == "__main__":
    test_imagenes() 