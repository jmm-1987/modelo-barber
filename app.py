from flask import Flask, request, jsonify, render_template

import os
import smtplib
from email.message import EmailMessage
import re
import sqlite3
import dateparser
import datetime

# load_dotenv()  # Eliminado

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Eliminado
app = Flask(__name__)

# Variables globales (simples, sin sesiones)
# Nota: Se eliminaron las variables del chatbot que no se usan

# Función para enviar el correo con los datos (mantenida para recordatorios)
def enviar_correo(nombre, telefono, conversacion):
    try:
        print("✉️ Intentando enviar correo...")

        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        email_receiver = os.getenv("EMAIL_RECEIVER")

        msg = EmailMessage()
        msg["Subject"] = "Nuevo lead captado desde el chatbot"
        msg["From"] = email_user
        msg["To"] = email_receiver

        cuerpo = f"""
Nuevo cliente potencial desde el chatbot de la web.

Nombre: {nombre}
Teléfono: {telefono}

Conversación completa:
{conversacion}
"""
        msg.set_content(cuerpo)

        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)

        print("✅ Correo enviado con éxito.")
    except Exception as e:
        print(f"❌ Error real al enviar correo: {e}")

# --- BASE DE DATOS PARA CITAS ---
DB_PATH = 'citas.db'

# Utilidad para normalizar fechas

def normalizar_fecha(texto):
    """Normaliza una fecha a formato YYYY-MM-DD"""
    if not texto:
        return None
    
    # Si ya está en formato YYYY-MM-DD, devolverlo tal cual
    if len(texto) == 10 and texto[4] == '-' and texto[7] == '-':
        try:
            datetime.datetime.strptime(texto, '%Y-%m-%d')
            return texto
        except:
            pass
    
    # Intentar con dateparser
    try:
        dt = dateparser.parse(texto, languages=['es'])
        if dt:
            return dt.strftime('%Y-%m-%d')
    except:
        pass
    
    # Si no se puede parsear, devolver el texto original
    return texto

def formatear_fecha_display(fecha_str):
    """Convierte fecha YYYY-MM-DD a DD/MM/AAAA"""
    try:
        dt = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return fecha_str

# Inicializar la base de datos (si no existe)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabla de citas
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            servicio TEXT NOT NULL,
            dia TEXT NOT NULL,
            hora TEXT NOT NULL,
            peluquero_id INTEGER,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de horarios disponibles
    c.execute('''
        CREATE TABLE IF NOT EXISTS horarios_disponibles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora TEXT UNIQUE,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de servicios
    c.execute('''
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio TEXT NOT NULL,
            descripcion TEXT,
            imagen_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de peluqueros
    c.execute('''
        CREATE TABLE IF NOT EXISTS peluqueros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            foto_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de configuración del negocio
    c.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_negocio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_negocio TEXT DEFAULT 'Barbería del Oeste',
            direccion TEXT DEFAULT 'Calle Principal 123',
            telefono TEXT DEFAULT '+34 123 456 789',
            email TEXT DEFAULT 'info@barberia.com',
            hora_apertura TEXT DEFAULT '10:00',
            hora_cierre TEXT DEFAULT '19:00',
            intervalo_citas INTEGER DEFAULT 30,
            dias_laborables TEXT DEFAULT '1,2,3,4,5,6'
        )
    ''')
    
    # Insertar datos por defecto si las tablas están vacías
    c.execute('SELECT COUNT(*) FROM horarios_disponibles')
    if c.fetchone()[0] == 0:
        horas_default = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', 
                        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', 
                        '18:00', '18:30', '19:00']
        for hora in horas_default:
            c.execute('INSERT INTO horarios_disponibles (hora) VALUES (?)', (hora,))
    
    c.execute('SELECT COUNT(*) FROM servicios')
    if c.fetchone()[0] == 0:
        servicios_default = [
            ('Corte de Cabello', '15€', 'Corte clásico o moderno', '/static/corte.jpg'),
            ('Barba', '10€', 'Arreglo y perfilado de barba', '/static/barba.jpg'),
            ('Corte + Barba', '20€', 'Corte completo con barba', '/static/combo.jpg'),
            ('Color', '25€', 'Tinte y coloración', '/static/color.jpg')
        ]
        for servicio in servicios_default:
            c.execute('INSERT INTO servicios (nombre, precio, descripcion, imagen_url) VALUES (?, ?, ?, ?)', servicio)
    
    c.execute('SELECT COUNT(*) FROM peluqueros')
    if c.fetchone()[0] == 0:
        peluqueros_default = [
            ('Juan Pérez', '/static/peluquero1.jpg'),
            ('Carlos García', '/static/peluquero2.jpg'),
            ('Miguel López', '/static/peluquero3.jpg')
        ]
        for peluquero in peluqueros_default:
            c.execute('INSERT INTO peluqueros (nombre, foto_url) VALUES (?, ?)', peluquero)
    
    c.execute('SELECT COUNT(*) FROM configuracion_negocio')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO configuracion_negocio DEFAULT VALUES')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# Obtener horarios disponibles desde la BD
def obtener_horarios_disponibles():
    """Obtiene todos los horarios disponibles desde la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT hora FROM horarios_disponibles WHERE activo = 1 ORDER BY hora')
    horarios = [row[0] for row in c.fetchall()]
    conn.close()
    return horarios

# Actualizar horarios disponibles
def actualizar_horarios_disponibles(horarios):
    """Actualiza los horarios disponibles en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Desactivar todos los horarios
    c.execute('UPDATE horarios_disponibles SET activo = 0')
    
    # Activar solo los horarios proporcionados
    for hora in horarios:
        c.execute('''
            INSERT OR REPLACE INTO horarios_disponibles (hora, activo) 
            VALUES (?, 1)
        ''', (hora,))
    
    conn.commit()
    conn.close()

# Obtener servicios desde la BD
def obtener_servicios():
    """Obtiene todos los servicios activos desde la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT nombre, precio, descripcion, imagen_url FROM servicios WHERE activo = 1 ORDER BY nombre')
    servicios = []
    for row in c.fetchall():
        servicios.append({
            'nombre': row[0],
            'precio': row[1],
            'desc': row[2],
            'img': row[3]
        })
    conn.close()
    return servicios

def actualizar_servicios(servicios):
    """Actualiza los servicios en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Eliminar todos los servicios existentes
    c.execute('DELETE FROM servicios')
    
    # Insertar los nuevos servicios
    for servicio in servicios:
        c.execute('''
            INSERT INTO servicios (nombre, precio, descripcion, imagen_url, activo) 
            VALUES (?, ?, ?, ?, ?)
        ''', (servicio['nombre'], servicio['precio'], servicio['descripcion'], servicio['imagen_url'], servicio['activo']))
    
    conn.commit()
    conn.close()

def obtener_peluqueros():
    """Obtiene todos los peluqueros activos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, nombre, foto_url, activo FROM peluqueros WHERE activo = 1 ORDER BY nombre')
    peluqueros = []
    for row in c.fetchall():
        peluqueros.append({
            'id': row[0],
            'nombre': row[1],
            'foto_url': row[2],
            'activo': bool(row[3])
        })
    conn.close()
    return peluqueros

def actualizar_peluqueros(peluqueros):
    """Actualiza los peluqueros en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Eliminar todos los peluqueros existentes
    c.execute('DELETE FROM peluqueros')
    
    # Insertar los nuevos peluqueros
    for peluquero in peluqueros:
        c.execute('''
            INSERT INTO peluqueros (nombre, foto_url, activo) 
            VALUES (?, ?, ?)
        ''', (peluquero['nombre'], peluquero['foto_url'], peluquero['activo']))
    
    conn.commit()
    conn.close()

# Consultar horas ocupadas para un día
def horas_ocupadas(dia):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT hora FROM citas WHERE dia = ?', (dia,))
    ocupadas = [row[0] for row in c.fetchall()]
    conn.close()
    return ocupadas

# Guardar una cita
def guardar_cita(nombre, servicio, dia, hora, telefono, peluquero_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO citas (nombre, servicio, dia, hora, telefono, peluquero_id) VALUES (?, ?, ?, ?, ?, ?)',
              (nombre, servicio, dia, hora, telefono, peluquero_id))
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar
init_db()

# Función para generar citas de prueba realistas
def generar_citas_prueba():
    """Genera citas de prueba realistas desde hoy hasta final de agosto"""
    import random
    
    # Nombres realistas de clientes
    nombres = [
        "María García", "Ana López", "Carmen Rodríguez", "Isabel Martínez", "Rosa Sánchez",
        "Elena Pérez", "Laura González", "Sofia Fernández", "Patricia Jiménez", "Mónica Ruiz",
        "Cristina Moreno", "Beatriz Díaz", "Nuria Martín", "Victoria Alonso", "Teresa Gutiérrez",
        "Pilar Romero", "Angeles Navarro", "Dolores Torres", "Concepción Domínguez", "Isabel Vázquez",
        "Lucía Hernández", "Paula Castro", "Adriana Morales", "Claudia Silva", "Valentina Rojas",
        "Camila Mendoza", "Sara Herrera", "Daniela Vega", "Gabriela Fuentes", "Carolina Reyes",
        "Andrea Morales", "Natalia Jiménez", "Valeria Torres", "Mariana Silva", "Fernanda Castro",
        "Sofía Mendoza", "Emma Herrera", "Olivia Vega", "Ava Fuentes",
        "Mia Reyes", "Charlotte Morales", "Amelia Jiménez", "Harper Torres", "Evelyn Silva"
    ]
    
    # Servicios disponibles
    servicios = [
        "Corte de mujer", "Corte de hombre", "Peinado", "Tinte raíz", "Mechas", "Lavado y secado",
        "Corte y color", "Peinado de fiesta", "Tinte completo", "Mechas californianas", "Brushing",
        "Corte degradado", "Peinado recogido", "Color fantasía", "Mechas balayage", "Tratamiento capilar",
        "Corte bob", "Peinado casual", "Tinte natural", "Mechas lowlights", "Secado profesional"
    ]
    
    # Horarios disponibles desde BD
    horas = obtener_horarios_disponibles()
    
    # Calcular fechas desde hoy hasta final de agosto
    hoy = datetime.date.today()
    fin_agosto = datetime.date(2025, 8, 31)  # 31 de agosto de 2025
    
    citas_generadas = []
    fecha_actual = hoy
    
    print(f"🎯 Generando citas desde {hoy.strftime('%d/%m/%Y')} hasta {fin_agosto.strftime('%d/%m/%Y')}")
    
    # Generar citas para cada día desde hoy hasta final de agosto
    while fecha_actual <= fin_agosto:
        fecha_str = fecha_actual.strftime('%Y-%m-%d')
        dia_semana = fecha_actual.weekday()
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana]
        
        # Domingo no hay citas
        if dia_semana == 6:  # Domingo
            fecha_actual += datetime.timedelta(days=1)
            continue
            
        # Generar entre 3-15 citas por día (más ocupado los miércoles, jueves y viernes)
        num_citas = random.randint(3, 10)
        if dia_semana == 2:  # Miércoles más ocupado
            num_citas = random.randint(8, 14)
            print(f"🎯 Miércoles {fecha_str}: {num_citas} citas")
        elif dia_semana == 3:  # Jueves ocupado
            num_citas = random.randint(6, 12)
            print(f"📅 Jueves {fecha_str}: {num_citas} citas")
        elif dia_semana == 4:  # Viernes muy ocupado
            num_citas = random.randint(10, 16)
            print(f"🔥 Viernes {fecha_str}: {num_citas} citas")
        elif dia_semana == 5:  # Sábado ocupado
            num_citas = random.randint(8, 14)
            print(f"🌟 Sábado {fecha_str}: {num_citas} citas")
        else:
            print(f"📅 {nombre_dia} {fecha_str}: {num_citas} citas")
        
        # Seleccionar horas aleatorias para las citas
        horas_disponibles = horas.copy()
        random.shuffle(horas_disponibles)
        horas_seleccionadas = horas_disponibles[:num_citas]
        
        for hora in horas_seleccionadas:
            nombre = random.choice(nombres)
            servicio = random.choice(servicios)
            telefono = f"6{random.randint(10000000, 99999999)}"  # Teléfono móvil español
            
            # Guardar la cita en la base de datos
            guardar_cita(nombre, servicio, fecha_str, hora, telefono)
            citas_generadas.append({
                'fecha': fecha_str,
                'hora': hora,
                'nombre': nombre,
                'servicio': servicio,
                'telefono': telefono
            })
        
        fecha_actual += datetime.timedelta(days=1)
    
    print(f"\n🎉 Total de citas generadas: {len(citas_generadas)}")
    return citas_generadas

# Endpoint para generar citas de prueba
@app.route('/generar_citas_prueba', methods=['POST'])
def generar_citas_prueba_endpoint():
    try:
        citas = generar_citas_prueba()
        return jsonify({
            'ok': True, 
            'mensaje': f'Se han generado {len(citas)} citas de prueba desde hoy hasta final de agosto',
            'citas': citas
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

# Endpoint para limpiar todas las citas (solo para desarrollo)
@app.route('/limpiar_citas', methods=['POST'])
def limpiar_citas():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM citas')
        conn.commit()
        conn.close()
        return jsonify({'ok': True, 'mensaje': 'Todas las citas han sido eliminadas'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

@app.route("/")
def index():
    return render_template("index.html")

# Panel de control de citas
@app.route("/panel")
def panel():
    return render_template("panel.html")

@app.route("/configuracion")
def configuracion():
    return render_template("configuracion.html")

# Endpoint del chatbot eliminado - no se usa en la aplicación actual

# --- ENDPOINT PARA HORAS DISPONIBLES ---
@app.route('/horas_disponibles', methods=['POST'])
def horas_disponibles():
    data = request.get_json()
    dia = normalizar_fecha(data.get('dia'))
    # Obtener horarios desde la BD
    todas = obtener_horarios_disponibles()
    ocupadas = horas_ocupadas(dia)
    libres = [h for h in todas if h not in ocupadas]
    return jsonify({'libres': libres})

# --- ENDPOINT PARA RESERVAR CITA ---
@app.route('/reservar_cita', methods=['POST'])
def reservar_cita():
    data = request.get_json()
    nombre = data.get('nombre')
    servicio = data.get('servicio')
    dia = normalizar_fecha(data.get('dia'))
    hora = data.get('hora')
    telefono = data.get('telefono', '')
    peluquero_id = data.get('peluquero_id')
    # Comprobar si la hora sigue libre
    if hora in horas_ocupadas(dia):
        return jsonify({'ok': False, 'msg': 'La hora ya está ocupada'})
    guardar_cita(nombre, servicio, dia, hora, telefono, peluquero_id)
    return jsonify({'ok': True, 'msg': 'Cita reservada correctamente'})

# --- ENDPOINT PARA CONSULTAR CITAS DE UN DÍA (panel de control) ---
@app.route('/citas_dia', methods=['POST'])
def citas_dia():
    data = request.get_json()
    dia_original = data.get('dia')
    dia = normalizar_fecha(dia_original)
    print(f"🔍 Consultando citas para: {dia_original} -> {dia}")
    
    if not dia:
        print(f"❌ Error: fecha inválida '{dia_original}'")
        return jsonify({'ocupadas': [], 'citas': [], 'error': 'Fecha inválida'})
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar si hay citas para esta fecha
    c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (dia,))
    total_citas = c.fetchone()[0]
    print(f"📊 Total de citas en BD para {dia}: {total_citas}")
    
    c.execute('''
        SELECT c.id, c.hora, c.nombre, c.servicio, c.telefono, c.peluquero_id, p.nombre as peluquero_nombre 
        FROM citas c 
        LEFT JOIN peluqueros p ON c.peluquero_id = p.id 
        WHERE c.dia = ?
    ''', (dia,))
    rows = c.fetchall()
    conn.close()
    
    ocupadas = [row[1] for row in rows]
    citas = [
        {
            'id': row[0], 
            'hora': row[1], 
            'nombre': row[2], 
            'servicio': row[3], 
            'telefono': row[4], 
            'peluquero_id': row[5],
            'peluquero_nombre': row[6] or 'Sin asignar',
            'dia': formatear_fecha_display(dia)
        } for row in rows
    ]
    
    print(f"📅 Encontradas {len(citas)} citas para {dia}: {[c['hora'] for c in citas]}")
    return jsonify({'ocupadas': ocupadas, 'citas': citas})

# --- ENDPOINT: Próximos 20 días laborables y disponibilidad ---
@app.route('/proximos_dias_disponibles', methods=['GET'])
def proximos_dias_disponibles():
    HORAS = obtener_horarios_disponibles()
    dias = []
    hoy = datetime.date.today()
    hasta = hoy + datetime.timedelta(days=31)
    dia = hoy
    while dia <= hasta:
        dia_str = dia.strftime('%Y-%m-%d')
        ocupadas = horas_ocupadas(dia_str)
        libres = [h for h in HORAS if h not in ocupadas]
        dias.append({
            'fecha': dia_str,
            'fecha_display': formatear_fecha_display(dia_str),
            'disponibles': len(libres),
            'weekday': dia.weekday()  # 0=lunes, 6=domingo
        })
        dia += datetime.timedelta(days=1)
    return jsonify({'dias': dias})

@app.route('/enviar_recordatorio', methods=['POST'])
def enviar_recordatorio():
    data = request.get_json()
    email = data.get('email')
    fecha = data.get('fecha')
    hora = data.get('hora')
    servicio = data.get('servicio')
    nombre_peluqueria = 'BarberShop'  # Nombre del negocio
    try:
        # Configuración de email
        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        msg = EmailMessage()
        msg["Subject"] = f"Recordatorio de tu cita en {nombre_peluqueria}"
        msg["From"] = email_user
        msg["To"] = email  # El destinatario es el email del usuario
        cuerpo = f"""
Hola,

Te recordamos tu cita en {nombre_peluqueria}:

- Servicio: {servicio}
- Fecha: {fecha}
- Hora: {hora}

¡Te esperamos!
"""
        msg.set_content(cuerpo)
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})

@app.route('/actualizar_telefono', methods=['POST'])
def actualizar_telefono():
    data = request.get_json()
    dia = data.get('dia')
    hora = data.get('hora')
    telefono = data.get('telefono')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE citas SET telefono = ? WHERE dia = ? AND hora = ?', (telefono, dia, hora))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/citas_por_telefono', methods=['POST'])
def citas_por_telefono():
    data = request.get_json()
    telefono = data.get('telefono')
    hoy = datetime.date.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT servicio, dia, hora, nombre FROM citas WHERE telefono = ? AND dia >= ?', (telefono, hoy))
    rows = c.fetchall()
    conn.close()
    citas = [
        {'servicio': row[0], 'dia': row[1], 'hora': row[2], 'nombre': row[3]} for row in rows
    ]
    return jsonify({'citas': citas})

@app.route('/borrar_cita', methods=['POST'])
def borrar_cita():
    data = request.get_json()
    fecha = normalizar_fecha(data.get('fecha'))
    hora = data.get('hora')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM citas WHERE dia = ? AND hora = ?', (fecha, hora))
        conn.commit()
        conn.close()
        
        if c.rowcount > 0:
            return jsonify({'ok': True, 'msg': 'Cita borrada correctamente'})
        else:
            return jsonify({'ok': False, 'msg': 'No se encontró la cita'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': str(e)})

# --- RUTAS PARA CONFIGURACIÓN DEL NEGOCIO ---

@app.route('/guardar_configuracion', methods=['POST'])
def guardar_configuracion():
    """Guarda la configuración del negocio en la base de datos"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Crear tabla de configuración si no existe
        c.execute('''
            CREATE TABLE IF NOT EXISTS configuracion_negocio (
                id INTEGER PRIMARY KEY,
                hora_apertura TEXT,
                hora_cierre TEXT,
                dias_laborables TEXT,
                duracion_corte INTEGER,
                duracion_barba INTEGER,
                duracion_combo INTEGER,
                duracion_tratamiento INTEGER,
                intervalo_citas INTEGER,
                anticipacion_reserva INTEGER,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar o actualizar configuración
        c.execute('''
            INSERT OR REPLACE INTO configuracion_negocio 
            (id, hora_apertura, hora_cierre, dias_laborables, 
             duracion_corte, duracion_barba, duracion_combo, duracion_tratamiento,
             intervalo_citas, anticipacion_reserva)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('horaApertura'),
            data.get('horaCierre'),
            data.get('diasLaborables'),
            data.get('duracionCorte'),
            data.get('duracionBarba'),
            data.get('duracionCombo'),
            data.get('duracionTratamiento'),
            data.get('intervaloCitas'),
            data.get('anticipacionReserva')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'ok': True, 'msg': 'Configuración guardada exitosamente'})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al guardar configuración: {str(e)}'})

@app.route('/obtener_configuracion', methods=['GET'])
def obtener_configuracion():
    """Obtiene la configuración actual del negocio"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Crear tabla si no existe
        c.execute('''
            CREATE TABLE IF NOT EXISTS configuracion_negocio (
                id INTEGER PRIMARY KEY,
                hora_apertura TEXT,
                hora_cierre TEXT,
                dias_laborables TEXT,
                duracion_corte INTEGER,
                duracion_barba INTEGER,
                duracion_combo INTEGER,
                duracion_tratamiento INTEGER,
                intervalo_citas INTEGER,
                anticipacion_reserva INTEGER,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Obtener configuración actual
        c.execute('SELECT * FROM configuracion_negocio WHERE id = 1')
        row = c.fetchone()
        conn.close()
        
        if row:
            config = {
                'horaApertura': row[1],
                'horaCierre': row[2],
                'diasLaborables': row[3],
                'duracionCorte': row[4],
                'duracionBarba': row[5],
                'duracionCombo': row[6],
                'duracionTratamiento': row[7],
                'intervaloCitas': row[8],
                'anticipacionReserva': row[9]
            }
        else:
            # Configuración por defecto
            config = {
                'horaApertura': '10:00',
                'horaCierre': '19:00',
                'diasLaborables': 'lunes-viernes',
                'duracionCorte': 30,
                'duracionBarba': 20,
                'duracionCombo': 45,
                'duracionTratamiento': 60,
                'intervaloCitas': 30,
                'anticipacionReserva': 2
            }
        
        return jsonify({'ok': True, 'configuracion': config})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al obtener configuración: {str(e)}'})

@app.route('/generar_horas_disponibles', methods=['POST'])
def generar_horas_disponibles():
    """Genera las horas disponibles basadas en la configuración del negocio"""
    try:
        data = request.get_json()
        fecha = data.get('fecha')
        
        # Obtener configuración actual
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT hora_apertura, hora_cierre, intervalo_citas FROM configuracion_negocio WHERE id = 1')
        row = c.fetchone()
        conn.close()
        
        if row:
            hora_apertura = row[0]
            hora_cierre = row[1]
            intervalo = row[2]
        else:
            # Valores por defecto
            hora_apertura = '10:00'
            hora_cierre = '19:00'
            intervalo = 30
        
        # Generar horas disponibles
        horas = []
        hora_actual = datetime.datetime.strptime(hora_apertura, '%H:%M')
        hora_fin = datetime.datetime.strptime(hora_cierre, '%H:%M')
        
        while hora_actual < hora_fin:
            horas.append(hora_actual.strftime('%H:%M'))
            hora_actual += datetime.timedelta(minutes=intervalo)
        
        # Filtrar horas ocupadas
        ocupadas = horas_ocupadas(fecha)
        disponibles = [h for h in horas if h not in ocupadas]
        
        return jsonify({'ok': True, 'horas': disponibles})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al generar horas: {str(e)}'})

# --- ENDPOINTS PARA GESTIONAR HORARIOS DISPONIBLES ---

@app.route('/obtener_horarios_disponibles', methods=['GET'])
def obtener_horarios_disponibles_endpoint():
    """Obtiene todos los horarios disponibles"""
    try:
        horarios = obtener_horarios_disponibles()
        return jsonify({'ok': True, 'horarios': horarios})
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al obtener horarios: {str(e)}'})

@app.route('/actualizar_horarios_disponibles', methods=['POST'])
def actualizar_horarios_disponibles_endpoint():
    """Actualiza los horarios disponibles"""
    try:
        data = request.get_json()
        horarios = data.get('horarios', [])
        
        if not horarios:
            return jsonify({'ok': False, 'msg': 'No se proporcionaron horarios'})
        
        actualizar_horarios_disponibles(horarios)
        return jsonify({'ok': True, 'msg': 'Horarios actualizados correctamente'})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al actualizar horarios: {str(e)}'})

@app.route('/generar_horarios_automaticos', methods=['POST'])
def generar_horarios_automaticos():
    """Genera horarios automáticamente basados en la configuración del negocio"""
    try:
        data = request.get_json()
        hora_apertura = data.get('horaApertura', '10:00')
        hora_cierre = data.get('horaCierre', '19:00')
        intervalo = data.get('intervaloCitas', 30)
        
        # Generar horarios
        horas = []
        hora_actual = datetime.datetime.strptime(hora_apertura, '%H:%M')
        hora_fin = datetime.datetime.strptime(hora_cierre, '%H:%M')
        
        while hora_actual < hora_fin:
            horas.append(hora_actual.strftime('%H:%M'))
            hora_actual += datetime.timedelta(minutes=intervalo)
        
        # Actualizar en BD
        actualizar_horarios_disponibles(horas)
        
        return jsonify({'ok': True, 'msg': f'Se generaron {len(horas)} horarios automáticamente', 'horarios': horas})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al generar horarios: {str(e)}'})

# --- ENDPOINTS PARA GESTIONAR SERVICIOS ---

@app.route('/obtener_servicios', methods=['GET'])
def obtener_servicios_endpoint():
    """Obtiene todos los servicios activos"""
    try:
        servicios = obtener_servicios()
        return jsonify({'ok': True, 'servicios': servicios})
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al obtener servicios: {str(e)}'})

@app.route('/actualizar_servicios', methods=['POST'])
def actualizar_servicios_endpoint():
    """Actualiza los servicios"""
    try:
        data = request.get_json()
        servicios = data.get('servicios', [])
        
        if not servicios:
            return jsonify({'ok': False, 'msg': 'No se proporcionaron servicios'})
        
        actualizar_servicios(servicios)
        return jsonify({'ok': True, 'msg': 'Servicios actualizados correctamente'})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al actualizar servicios: {str(e)}'})

# --- ENDPOINTS PARA GESTIONAR PELUQUEROS ---

@app.route('/obtener_peluqueros', methods=['GET'])
def obtener_peluqueros_endpoint():
    """Obtiene todos los peluqueros activos"""
    try:
        peluqueros = obtener_peluqueros()
        return jsonify({'ok': True, 'peluqueros': peluqueros})
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al obtener peluqueros: {str(e)}'})

@app.route('/actualizar_peluqueros', methods=['POST'])
def actualizar_peluqueros_endpoint():
    """Actualiza los peluqueros"""
    try:
        data = request.get_json()
        peluqueros = data.get('peluqueros', [])
        
        if not peluqueros:
            return jsonify({'ok': False, 'msg': 'No se proporcionaron peluqueros'})
        
        actualizar_peluqueros(peluqueros)
        return jsonify({'ok': True, 'msg': 'Peluqueros actualizados correctamente'})
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Error al actualizar peluqueros: {str(e)}'})

# --- ENDPOINT DE ESTADÍSTICAS ---

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    """Obtiene estadísticas del negocio"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Total de citas
        c.execute('SELECT COUNT(*) FROM citas')
        total_citas = c.fetchone()[0]
        
        # Citas de hoy
        hoy = datetime.date.today().strftime('%Y-%m-%d')
        c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (hoy,))
        citas_hoy = c.fetchone()[0]
        
        # Citas de esta semana
        lunes = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        domingo = lunes + datetime.timedelta(days=6)
        c.execute('SELECT COUNT(*) FROM citas WHERE dia BETWEEN ? AND ?', 
                 (lunes.strftime('%Y-%m-%d'), domingo.strftime('%Y-%m-%d')))
        citas_semana = c.fetchone()[0]
        
        # Citas pendientes (futuras)
        c.execute('SELECT COUNT(*) FROM citas WHERE dia >= ?', (hoy,))
        citas_pendientes = c.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_citas': total_citas,
            'citas_hoy': citas_hoy,
            'citas_semana': citas_semana,
            'citas_pendientes': citas_pendientes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
