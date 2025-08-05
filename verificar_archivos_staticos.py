#!/usr/bin/env python3
"""
Script para verificar archivos estáticos
Verifica que todos los archivos referenciados en los templates existan en el directorio static/
"""

import os
import re
from pathlib import Path

def extraer_referencias_staticas(archivo_html):
    """Extrae todas las referencias a archivos estáticos de un archivo HTML"""
    referencias = []
    
    try:
        with open(archivo_html, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Buscar referencias reales a /static/ (no en JavaScript)
        patrones = [
            r'src=[\'"]/static/([^\'"]+)[\'"]',  # Referencias en src
            r'href=[\'"]/static/([^\'"]+)[\'"]',  # Referencias en href
            r'url\([\'"]?/static/([^\'"]+)[\'"]?\)',  # Referencias en CSS
        ]
        
        for patron in patrones:
            matches = re.findall(patron, contenido)
            referencias.extend(matches)
            
    except Exception as e:
        print(f"❌ Error leyendo {archivo_html}: {e}")
    
    return list(set(referencias))  # Eliminar duplicados

def verificar_archivo_statico(archivo):
    """Verifica si un archivo estático existe"""
    ruta_completa = os.path.join('static', archivo)
    existe = os.path.exists(ruta_completa)
    tamaño = os.path.getsize(ruta_completa) if existe else 0
    return existe, tamaño

def main():
    print("🔍 Verificando archivos estáticos...")
    print("=" * 50)
    
    # Verificar archivos en templates/
    templates_dir = Path('templates')
    archivos_html = list(templates_dir.glob('*.html'))
    
    todas_las_referencias = []
    
    for archivo_html in archivos_html:
        print(f"\n📄 Analizando: {archivo_html}")
        referencias = extraer_referencias_staticas(archivo_html)
        
        if referencias:
            print(f"   Referencias encontradas: {len(referencias)}")
            for ref in referencias:
                existe, tamaño = verificar_archivo_statico(ref)
                estado = "✅" if existe else "❌"
                tamaño_str = f"({tamaño} bytes)" if existe else ""
                print(f"   {estado} /static/{ref} {tamaño_str}")
                todas_las_referencias.append((ref, existe))
        else:
            print("   No se encontraron referencias a archivos estáticos")
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN:")
    
    total_referencias = len(todas_las_referencias)
    referencias_existentes = sum(1 for _, existe in todas_las_referencias if existe)
    referencias_faltantes = total_referencias - referencias_existentes
    
    print(f"   Total de referencias: {total_referencias}")
    print(f"   ✅ Archivos existentes: {referencias_existentes}")
    print(f"   ❌ Archivos faltantes: {referencias_faltantes}")
    
    if referencias_faltantes > 0:
        print("\n❌ ARCHIVOS FALTANTES:")
        for ref, existe in todas_las_referencias:
            if not existe:
                print(f"   - /static/{ref}")
    
    # Verificar archivos en static/ que no se referencian
    static_dir = Path('static')
    archivos_static = list(static_dir.glob('*'))
    archivos_static_nombres = [f.name for f in archivos_static if f.is_file()]
    
    referencias_nombres = [ref for ref, _ in todas_las_referencias]
    archivos_no_referenciados = [f for f in archivos_static_nombres if f not in referencias_nombres]
    
    if archivos_no_referenciados:
        print(f"\n⚠️ ARCHIVOS NO REFERENCIADOS ({len(archivos_no_referenciados)}):")
        for archivo in archivos_no_referenciados:
            print(f"   - {archivo}")
    
    print("\n" + "=" * 50)
    
    if referencias_faltantes == 0:
        print("🎉 ¡Todos los archivos estáticos están presentes!")
    else:
        print(f"⚠️ Hay {referencias_faltantes} archivo(s) faltante(s)")

if __name__ == "__main__":
    main() 