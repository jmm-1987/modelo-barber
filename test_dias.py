import requests
import json

# Obtener días disponibles
response = requests.get('http://127.0.0.1:5000/proximos_dias_disponibles')
data = response.json()

# Buscar el día 8 de agosto
dia_8_agosto = None
for dia in data['dias']:
    if dia['fecha'] == '2025-08-08':
        dia_8_agosto = dia
        break

print("Día 8 de agosto encontrado:", dia_8_agosto)

# Verificar días cerrados
response2 = requests.get('http://127.0.0.1:5000/debug_dias_cerrados')
data2 = response2.json()

print("Días cerrados:", data2['dias_cerrados'])
print("Test fechas:", data2['test_fechas'])

# Verificar si el 8 de agosto está cerrado
from app import es_dia_cerrado
print("¿8 de agosto está cerrado?", es_dia_cerrado('2025-08-08')) 