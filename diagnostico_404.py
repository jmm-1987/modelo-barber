#!/usr/bin/env python3
"""
Diagnóstico simple para el error 404
"""

import os
from pathlib import Path

def main():
    print("🔍 Diagnóstico del error 404")
    print("=" * 40)
    
    # Verificar que Flask esté configurado correctamente
    print("1. Verificando configuración de Flask...")
    
    # Verificar archivos estáticos
    print("\n2. Verificando archivos estáticos...")
    static_dir = Path('static')
    if static_dir.exists():
        archivos = list(static_dir.glob('*'))
        print(f"   ✅ Directorio static/ existe con {len(archivos)} archivos")
        for archivo in archivos:
            if archivo.is_file():
                print(f"   📄 {archivo.name} ({archivo.stat().st_size} bytes)")
    else:
        print("   ❌ Directorio static/ no existe")
    
    # Verificar templates
    print("\n3. Verificando templates...")
    templates_dir = Path('templates')
    if templates_dir.exists():
        archivos = list(templates_dir.glob('*.html'))
        print(f"   ✅ Directorio templates/ existe con {len(archivos)} archivos HTML")
        for archivo in archivos:
            print(f"   📄 {archivo.name}")
    else:
        print("   ❌ Directorio templates/ no existe")
    
    # Verificar app.py
    print("\n4. Verificando app.py...")
    if Path('app.py').exists():
        print("   ✅ app.py existe")
        
        # Verificar si tiene la ruta para archivos estáticos
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if '@app.route(\'/static/<path:filename>\')' in contenido:
                print("   ✅ Ruta para archivos estáticos configurada")
            else:
                print("   ❌ Ruta para archivos estáticos NO configurada")
    else:
        print("   ❌ app.py no existe")
    
    # Verificar archivos específicos que se referencian
    print("\n5. Verificando archivos referenciados...")
    archivos_referenciados = [
        'fondo.png',
        'logo.png', 
        'reloj.png',
        'ubicacion.png',
        'galeria.png',
        'citas.png'
    ]
    
    for archivo in archivos_referenciados:
        ruta = static_dir / archivo
        if ruta.exists():
            print(f"   ✅ {archivo} existe")
        else:
            print(f"   ❌ {archivo} NO existe")
    
    print("\n" + "=" * 40)
    print("🎯 RECOMENDACIONES:")
    print("1. Asegúrate de que la aplicación Flask esté ejecutándose")
    print("2. Verifica que estés accediendo a la URL correcta")
    print("3. Revisa la consola del navegador para ver errores específicos")
    print("4. Si el problema persiste, ejecuta: py app.py")

if __name__ == "__main__":
    main() 