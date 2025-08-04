#!/usr/bin/env python3
"""
Script para probar la verificación de citas antes de cerrar días
"""

import sqlite3
import datetime
import requests
import json

DB_PATH = 'citas.db'
BASE_URL = 'http://localhost:5000'

def crear_datos_prueba():
    """Crear datos de prueba para verificar la funcionalidad"""
    
    # Fecha de mañana
    mañana = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"📅 Creando datos de prueba para: {mañana}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Obtener peluqueros existentes
    c.execute('SELECT id, nombre FROM peluqueros')
    peluqueros = c.fetchall()
    
    if not peluqueros:
        print("❌ No hay peluqueros en la base de datos")
        return
    
    print(f"📋 Peluqueros existentes: {peluqueros}")
    
    # Limpiar citas existentes para la fecha de prueba
    c.execute('DELETE FROM citas WHERE dia = ?', (mañana,))
    
    # Crear una cita de prueba
    cita_prueba = ('Juan Pérez', 'Corte', mañana, '17:00', '123456789', peluqueros[0][0])
    c.execute('''
        INSERT INTO citas (nombre, servicio, dia, hora, telefono, peluquero_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', cita_prueba)
    print(f"✅ Cita creada: {cita_prueba[0]} - {cita_prueba[1]} - {cita_prueba[2]} {cita_prueba[3]} - Peluquero {cita_prueba[5]}")
    
    conn.commit()
    conn.close()
    
    return mañana

def probar_cerrar_dia_con_citas():
    """Probar cerrar un día que tiene citas reservadas"""
    
    fecha = crear_datos_prueba()
    print(f"\n🔍 Probando cerrar día con citas: {fecha}")
    print("=" * 50)
    
    # Probar cerrar día para un peluquero específico
    print("\n1️⃣ Probando cerrar día para un peluquero específico:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_cerrado', 
                               json={'fecha': fecha, 'motivo': 'Prueba', 'peluquero_id': 1})
        data = response.json()
        print(f"   Respuesta: {data}")
        if not data['ok']:
            print("   ✅ CORRECTO: No se pudo cerrar el día porque hay citas")
        else:
            print("   ❌ ERROR: Se pudo cerrar el día a pesar de tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")
    
    # Probar cerrar día para todos los peluqueros
    print("\n2️⃣ Probando cerrar día para todos los peluqueros:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_cerrado_todos_peluqueros', 
                               json={'fecha': fecha, 'motivo': 'Prueba'})
        data = response.json()
        print(f"   Respuesta: {data}")
        if not data['ok']:
            print("   ✅ CORRECTO: No se pudo cerrar el día porque hay citas")
        else:
            print("   ❌ ERROR: Se pudo cerrar el día a pesar de tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")
    
    # Probar marcar como festivo
    print("\n3️⃣ Probando marcar como festivo:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_festivo', 
                               json={'fecha': fecha, 'nombre': 'Prueba', 'tipo': 'festivo'})
        data = response.json()
        print(f"   Respuesta: {data}")
        if not data['ok']:
            print("   ✅ CORRECTO: No se pudo marcar como festivo porque hay citas")
        else:
            print("   ❌ ERROR: Se pudo marcar como festivo a pesar de tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")

def probar_cerrar_dia_sin_citas():
    """Probar cerrar un día que NO tiene citas reservadas"""
    
    # Fecha de pasado mañana (sin citas)
    pasado_mañana = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    print(f"\n🔍 Probando cerrar día SIN citas: {pasado_mañana}")
    print("=" * 50)
    
    # Limpiar cualquier cita existente
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM citas WHERE dia = ?', (pasado_mañana,))
    conn.commit()
    conn.close()
    
    # Probar cerrar día para un peluquero específico
    print("\n1️⃣ Probando cerrar día para un peluquero específico:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_cerrado', 
                               json={'fecha': pasado_mañana, 'motivo': 'Prueba', 'peluquero_id': 1})
        data = response.json()
        print(f"   Respuesta: {data}")
        if data['ok']:
            print("   ✅ CORRECTO: Se pudo cerrar el día porque no hay citas")
        else:
            print("   ❌ ERROR: No se pudo cerrar el día a pesar de no tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")
    
    # Probar cerrar día para todos los peluqueros
    print("\n2️⃣ Probando cerrar día para todos los peluqueros:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_cerrado_todos_peluqueros', 
                               json={'fecha': pasado_mañana, 'motivo': 'Prueba'})
        data = response.json()
        print(f"   Respuesta: {data}")
        if data['ok']:
            print("   ✅ CORRECTO: Se pudo cerrar el día porque no hay citas")
        else:
            print("   ❌ ERROR: No se pudo cerrar el día a pesar de no tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")
    
    # Probar marcar como festivo
    print("\n3️⃣ Probando marcar como festivo:")
    try:
        response = requests.post(f'{BASE_URL}/agregar_dia_festivo', 
                               json={'fecha': pasado_mañana, 'nombre': 'Prueba', 'tipo': 'festivo'})
        data = response.json()
        print(f"   Respuesta: {data}")
        if data['ok']:
            print("   ✅ CORRECTO: Se pudo marcar como festivo porque no hay citas")
        else:
            print("   ❌ ERROR: No se pudo marcar como festivo a pesar de no tener citas")
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")

if __name__ == "__main__":
    print("🧪 PROBANDO VERIFICACIÓN DE CITAS ANTES DE CERRAR DÍAS")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f'{BASE_URL}/')
        print("✅ Servidor está corriendo")
    except:
        print("❌ ERROR: El servidor no está corriendo. Ejecuta 'python app.py' primero.")
        exit(1)
    
    probar_cerrar_dia_con_citas()
    probar_cerrar_dia_sin_citas()
    
    print("\n🎉 Pruebas completadas!") 