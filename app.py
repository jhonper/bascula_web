from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_required
import serial
import time
import random
import threading
import sys
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for

import os # para poder acceder a lso directorios
import database as db
from math import ceil

# adicional
from flask_mysqldb import MySQL
import MySQLdb.cursors

from werkzeug.security import check_password_hash, generate_password_hash

from flask_wtf.csrf import CSRFProtect


# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'

# adicional
csrf = CSRFProtect(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # acceder la carpeta de proyecto CRUD_FLASK_MYSQL
# unir src a la carpeta de proyecto CRUD_FLASK_MYSQL
# template_dir = os.path.join(template_dir, 'src', 'templates')

# app = Flask(__name__, template_folder = template_dir) # para que busque el index html y lo renderice


#region cambio
# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     # db = get_db_connection()
#     cursor = db.database.cursor()
#     return ModelUser.get_by_id(cursor, user_id)
#     # return ModelUser.get_by_id(db, user_id)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # db = get_db_connection()
#         cursor = db.database.cursor()
#         user = User(None, username, password)
#         user = ModelUser.login(cursor, user)
#         print(f'account: {user}')
#         if user and user.password:
#             session['loggedin'] = True
#             session['id'] = user.id
#             session['username'] = user.username
#             print(f'Antes de redirección:::')
#             return redirect(url_for('home'))
#         else:
#             msg = 'Incorrect username/password!'
#     # return render_template('login.html', msg='')
#     return render_template('auth/login.html', msg='')              

#endregion


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'basculax'

mysql = MySQL(app)

@app.before_request
def make_session_permanent():
    session.permanent = True

#region login - chat
# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # if 'loggedin' in session:
    #     # Si el usuario ya está autenticado, redirige a la página adecuada
    #     if len(session.get('codigoprov', '')) == 0:
    #         return redirect(url_for('entransito'))
    #     else:
    #         return redirect(url_for('entra'))

    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    #     account = cursor.fetchone()
    #     if account and check_password_hash(account['password'], password):
    #         session['loggedin'] = True
    #         session['id'] = account['id']
    #         session['username'] = account['username']
    #         session['codigoprov'] = account['codigoprov']
    #         if len(account['codigoprov']) == 0:
    #             return redirect(url_for('entransito'))
    #         else:
    #             return redirect(url_for('entra'))
    #     else:
    #         msg = 'Incorrect username/password!'
    #         return render_template('auth/login.html', msg=msg)

    # return render_template('auth/login.html', msg='')    
#region login - chat

#region - login original
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()

        print(f"Usuario logueado: {account}")
        print(f"account['username']: {account['username']}")
        print(f"account['productospermitidos']: {account['productospermitidos']}")
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session.permanent = True # nueva linea
            session['id'] = account['id']
            session['username'] = account['username']
            session['codigoprov'] = account['codigoprov']
            session['editarpesos'] = account['editarpesos']
            session['productospermitidos'] = account['productospermitidos']
            print(f"session['productospermitidos']: {session['productospermitidos']}")
            if len(account['codigoprov']) == 0: # linea nueva
                return redirect(url_for('entransito'))
            else:
                return redirect(url_for('entra'))          
        else:
            msg = 'Incorrect username/password!'
    return render_template('auth/login.html', msg='')       
# endregion - login original

         


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         print(f"username: {username}")
#         print(f"password: {password}")
#         # db = get_db_connection()
#         # cursor = db.cursor(MySQLdb.cursors.DictCursor)
#         cursor = db.database.cursor()
#         cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
#         account = cursor.fetchone()
#         print(f'account: {account}')
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             print(f'Antes de redirección:::')
#             return redirect(url_for('home'))
#         else:
#             msg = 'Incorrect username/password!'
#     #return render_template('login.html', msg='')
#     return render_template('auth/login.html', msg='')        

@app.route('/logout')
def logout():
   # Elimina la sesión del usuario al hacer logout
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('codigoprov', None)
    session.pop('editarpesos', None)
    session.pop('productospermitidos', None)
    return redirect(url_for('login'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # print(request.form['username'])
#         # print(request.form['password'])
#         user = User(0, request.form['username'], request.form['password'])
#         logged_user = ModelUser.login(db, user)
#         if logged_user != None:
#             if logged_user.password:
#                 login_user(logged_user)
#                 return redirect(url_for('home'))
#             else:
#                 flash("Invalid password...")
#                 return render_template('auth/login.html')
#         else:
#             flash("User not found...")
#             return render_template('auth/login.html')
#     else:
#         return render_template('auth/login.html')


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


# @app.route('/protected')
# @login_required
# def protected():
#     return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

#endregion


#region - código con serialport
#socketio = SocketIO(app)

#peso = 0


# Abre una conexión al puerto COM2 (ajusta según tu configuración)
# puerto_com2 = "COM5"
# ser = serial.Serial('COM5', baudrate=9600, timeout=1)

# class SerialPort:
#     def __init__(self):
#         self.comportName = ""
#         self.baud = 0
#         self.timeout = None
#         self.ReceiveCallback = None
#         self.isopen = False
#         self.receivedMessage = None
#         self.serialport = serial.Serial()

#     def IsOpen(self):
#         return self.isopen

#     def Open(self,portname="COM5",baudrate=9600):
#         if not self.isopen:
#             # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
#             self.serialport.port = portname
#             self.serialport.baudrate = baudrate
#             try:
#                 self.serialport.open()
#                 self.isopen = True
#             except:
#                 print("Error opening COM port: ", sys.exc_info()[0])

# @app.route('/opens')
# def simular_bascula(puerto = 'COM5'):
#     global peso
#     try:
#         #with serial.Serial(port=puerto, baudrate=9600, timeout=1) as ser:
#             print(f"Simulando báscula en el puerto {puerto}. Presiona Ctrl+C para detener.")
#             while True:
#                 # Genera un peso aleatorio entre 0 y 100 kg
#                 # peso = round(random.uniform(0, 100), 2)
#                 peso = random.randint(0, 100)
                
#                 # Convierte el peso a una cadena y lo envía al puerto serie
#                 peso_str = f"{peso:.2f}\n"
#                 ser.write(peso_str.encode('utf-8'))

#                 print(f"Peso enviado: {peso} kg")
#                 socketio.emit('peso', {'peso': peso})
#                 # time.sleep(1)  # Espera 1 segundo antes de enviar el próximo peso
#                 time.sleep(0.5) # medio segundo

#     except serial.SerialException as e:
#         print(f"Error al abrir el puerto {puerto}: {e}")

#endregion - Código con serialport

@csrf.exempt 
@app.route('/addEntrada')
def addEntrada():
    cursor = db.database.cursor()
    cursor.execute(f"SELECT id, documento, nombre FROM Proveedores")
    proveedores = cursor.fetchall() 
    dataProveedor = [dict(zip([column[0] for column in cursor.description], record)) for record in proveedores]
    
    # Consulta a tabla Productos
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    dataProductos = [dict(zip([column[0] for column in cursor.description], record)) for record in productos]
    #print(f"dataProductos: {dataProductos}")

    # Consulta a tabla Conductores
    cursor.execute("SELECT * FROM conductores")
    conductores = cursor.fetchall()
    dataConductores = [dict(zip([column[0] for column in cursor.description], record)) for record in conductores]
    print(f"dataVehiculo:::::: {dataConductores}")

    # Consulta a tabla Vehiculo
    cursor.execute("SELECT * FROM vehiculo")
    vehiculos = cursor.fetchall()
    dataVehiculo = [dict(zip([column[0] for column in cursor.description], record)) for record in vehiculos]
    print(f"dataVehiculo:::::: {dataVehiculo}")

    # Consulta a tabla Origenes
    cursor.execute("SELECT * FROM origenes")
    origenes = cursor.fetchall()
    dataOrigenes = [dict(zip([column[0] for column in cursor.description], record)) for record in origenes]

    # Consulta a tabla Destinos
    cursor.execute("SELECT * FROM destinos")
    destinos = cursor.fetchall()
    dataDestinos = [dict(zip([column[0] for column in cursor.description], record)) for record in destinos]

    cursor.close()

    return render_template('addmovimiento.html', dataProveedor=dataProveedor, dataProductos=dataProductos,
                           dataConductores=dataConductores, dataVehiculo=dataVehiculo,
                           dataOrigenes=dataOrigenes, dataDestinos=dataDestinos)
# simulaciongpt2.html - addmovimiento.html
@csrf.exempt 
@app.route('/addoperaciones', methods=['POST'])
def addoperaciones():
    tipomovimiento = request.form['tipomovimiento']
    idProveedor = request.form['idProveedor']
    idConductor = request.form['idConductor']
    print(f"tipomovimiento: {tipomovimiento}")
    print(f"tipomovimiento tipo: {type(tipomovimiento)}")
    # placa = request.form['placa']
    idvehiculo = request.form['idvehiculo']
    print(f"idvehiculo: {idvehiculo}")
    idProducto = request.form['idProducto']
    idorigen = request.form['idorigen']
    iddestino = request.form['iddestino']
    observaciones = request.form['observaciones']
    fechaentrada = request.form['fechaentrada'] 
    print(f"Fecha entrada: {fechaentrada}")
    horaentrada = request.form['horaentrada'] 
    print(f"Hora entrada: {horaentrada}")
    pesoentrada = request.form['pesoentrada']
    pesosalida = request.form['pesosalida']
    pesoneto = request.form['pesoneto']
    fechasalida = datetime.now().strftime('%d-%m-%Y') 
    horasalida = datetime.now().strftime('%H:%M')
    
    cursor = db.database.cursor()

    if (idProveedor and idConductor and idvehiculo and idProducto and idorigen and iddestino and observaciones
        and fechaentrada and horaentrada and pesoentrada):

        cursor.execute(""" INSERT INTO Movimiento (tipomovimiento, idproveedor, idconductor, idvehiculo, idproducto, idorigen, 
                       iddestino, observaciones, fechaentrada, horaentrada, pesoentrada) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                    (tipomovimiento, idProveedor, idConductor, idvehiculo, idProducto, idorigen, iddestino, observaciones,
                    fechaentrada, horaentrada, pesoentrada))

    # Obtener el ID del movimiento insertado
    ultimo_movimiento_insertado = cursor.lastrowid
    print(f"Último movimiento insertado: {ultimo_movimiento_insertado}")    
        
    db.database.commit()
    return redirect(url_for('entransito'))
    # Llamar a la función reporteentrada y pasar el último ID insertado como argumento
    #return reporteentrada(ultimo_movimiento_insertado)
    #return  get_movimiento_completo_por_id(ultimo_movimiento_insertado)




# @app.route('/reporte-entrada', methods=['POST'])
# def reporteentrada(idmovimiento=None):
#     if idmovimiento is None:
#         # Si no se proporcionó un ID de movimiento, tratar de obtenerlo del formulario
#         idmovimiento = request.form.get('idmovimiento')
#     else:
#         # Si se proporcionó un ID de movimiento, imprímelo
#         print("ID del último movimiento insertado:", idmovimiento)



@app.route('/buscar-entrada')
def buscarentrada():
    return render_template('buscarentrada.html')
    
@csrf.exempt 
@app.route('/reporte-entrada', methods=['POST'])
def reporteentrada():
    idmovimiento = request.form['idmovimiento']
    print("idmovimiento: {idmovimiento}")
    dataMovimiento = get_movimiento_completo_por_id(idmovimiento)
    print(f"REPORTE DE ENTRADA: {dataMovimiento}")
    print(f"Type Respuesta: {type(dataMovimiento)}")
    if dataMovimiento:
        print(f"DATA MOVIMIENTO: {dataMovimiento}")
        return render_template('reporteentrada.html', dataMovimiento=dataMovimiento)
    else:
        return '<h1>Movimiento no encontrado</h1>'


@csrf.exempt 
@app.route('/updateoperaciones', methods=['POST'])
def updateoperaciones():
    idmovimiento = request.form['idmovimiento']
    observaciones = request.form['observaciones']
    pesoentrada = request.form['pesoentrada']
    pesosalida = request.form['pesosalida']
    pesoneto = request.form['pesoneto']
    fechasalida = request.form['fechasalida'] 
    horasalida = request.form['horasalida'] 
    
    cursor = db.database.cursor()

    if (idmovimiento and pesoentrada and observaciones and pesosalida and pesoneto and fechasalida and horasalida):

        cursor.execute(''' UPDATE movimiento SET pesoentrada=%s, observaciones=%s, fechasalida=%s, horasalida=%s, pesosalida=%s, pesoneto=%s 
                   WHERE idmovimiento=%s ''', (pesoentrada, observaciones, fechasalida, horasalida, pesosalida, pesoneto, idmovimiento)) 
        
    db.database.commit()
    return redirect(url_for('entransito'))


def permisos_requeridos(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        # Verificar si 'codigoprov' no es None, lo que significa que el usuario no tiene permisos
        if session.get('codigoprov') is None:
            # Si 'codigoprov' no es None, redireccionar a una página de error o a una ruta que tenga sentido en tu aplicación
            return redirect(url_for('login'))
        else:
            # Si 'codigoprov' es None, permitir el acceso a la función original
            return func(*args, **kwargs)
    return decorador


# @app.route('/')
@csrf.exempt 
#@login_required
@app.route('/entransito')
#@permisos_requeridos
def entransito():
    cursor = db.database.cursor()
    # cursor.execute(f"SELECT * FROM Movimiento WHERE fechasalida is null") # ORDER BY fechaentrada DESC
    cursor.execute(''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, 
                              Proveedores.nombre as proveedor, Vehiculo.placa as placa
                            FROM Movimiento
                            JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id
                            JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                        WHERE fechasalida is null;  
                ''')
    movimientos = cursor.fetchall() 
    dataMovimientos = [dict(zip([column[0] for column in cursor.description], record)) for record in movimientos]
    cursor.close()

    return render_template('transitos.html', dataMovimientos=dataMovimientos)


# # Función para obtener un movimiento por su ID
def get_movimiento_por_id(idmovimiento):
    cursor = db.database.cursor()

#region CONSULTA CON JOIN   
    consulta = ''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, Movimiento.observaciones,
                            Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, Movimiento.pesoentrada,
                            Conductores.nombre AS nombreconductor,
                            Vehiculo.placa AS placa,
                            Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                            Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                            Destinos.codigo AS codigodestino, Destinos.destino AS destino
                            FROM Movimiento
                            JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                            JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                            JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                            JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                            JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                            JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                            WHERE idmovimiento = %s '''
#endregion        
    cursor.execute(consulta, (idmovimiento,))
    movimiento = cursor.fetchone()

    movimiento = dict(zip([column[0] for column in cursor.description], movimiento)) if movimiento else {}

    print(f"Encontrado: {movimiento}")
    print(f"Type Encontrado: {type(movimiento)}")

    # # Convertir la fecha de entrada a un objeto datetime
    movimiento['fechaentrada'] = movimiento['fechaentrada'].strftime('%d/%b/%Y')
    return movimiento


# Función para obtener un movimiento por su ID
def get_movimiento_completo_por_id(idmovimiento):
    cursor = db.database.cursor()

#region CONSULTA CON JOIN   
    consulta = ''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, Movimiento.fechasalida, Movimiento.horasalida,
                            Movimiento.observaciones,
                            Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, 
                            Movimiento.pesoentrada, Movimiento.pesosalida, Movimiento.pesoneto,
                            Conductores.nombre AS nombreconductor,
                            Vehiculo.placa AS placa,
                            Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                            Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                            Destinos.codigo AS codigodestino, Destinos.destino AS destino
                            FROM Movimiento
                            JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                            JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                            JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                            JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                            JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                            JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                            WHERE idmovimiento = %s '''
#endregion        
    cursor.execute(consulta, (idmovimiento,))
    movimiento = cursor.fetchone()

    movimiento = dict(zip([column[0] for column in cursor.description], movimiento)) if movimiento else {}

    # print(f"Encontrado: {movimiento}")
    # print(f"Type Encontrado: {type(movimiento)}")

    # # Convertir la fecha de entrada a un objeto datetime
    movimiento['fechaentrada'] = movimiento['fechaentrada'].strftime('%d/%b/%Y')
    movimiento['fechasalida'] = movimiento['fechasalida'].strftime('%d/%b/%Y')
    return movimiento





# @app.route('/editMovimiento/<int:idmovimiento>')
@csrf.exempt 
@app.route('/editMovimiento', methods=['POST'])
def editMovimiento():
    # Realiza la consulta por el ID de movimiento en tu base de datos
    # Supongamos que tienes una función get_movimiento_por_id en tu base de datos
    idmovimiento = request.form['idmovimiento']
    # idmovimiento = request.form.get('idmovimiento')
    dataMovimiento = get_movimiento_por_id(idmovimiento)
    dataProductos = getProductos()
    dataProveedor =  getProveedores()
    dataOrigenes = getOrigenes()
    dataDestinos = getDestinos()
    dataVehiculo = getVehiculos()
    dataConductores = getConductores()

    print(f"Respuesta: {dataMovimiento}")
    print(f"Type Respuesta: {type(dataMovimiento)}")
    if dataMovimiento:
        # Renderiza una plantilla HTML con los datos del movimiento
        return render_template('editmovimiento.html', dataMovimiento=dataMovimiento, dataProductos=dataProductos, dataProveedor=dataProveedor,
                                                        dataOrigenes=dataOrigenes, dataDestinos=dataDestinos, dataVehiculo=dataVehiculo,
                                                        dataConductores=dataConductores)
        # return render_template('edit.html', dataMovimiento=dataMovimiento)
    else:
        return '<h1>Movimiento no encontrado</h1>'





#region - FUNCIÓN PARA RECUPERAR PROVEEDORES    
# def getProveedores():
#     cursor = db.database.cursor()
#     cursor.execute(f"SELECT id, documento, nombre FROM Proveedores")
#     proveedores = cursor.fetchall() 
#     dataProveedor = [dict(zip([column[0] for column in cursor.description], record)) for record in proveedores]  
#     return dataProveedor

def getProveedores():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT id, documento, nombre FROM Proveedores")
        proveedores = cursor.fetchall()
        dataProveedor = [dict(zip([column[0] for column in cursor.description], record)) for record in proveedores]
        return dataProveedor
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los proveedores: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion        

#region - FUNCIÓN PARA RECUPERAR ORIGENES    
def getOrigenes():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT idorigen, codigo, origen FROM Origenes")
        origenes = cursor.fetchall()
        dataOrigen = [dict(zip([column[0] for column in cursor.description], record)) for record in origenes]
        return dataOrigen
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los origenes: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion       

#region - FUNCIÓN PARA RECUPERAR DESTINOS    
def getDestinos():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT iddestino, codigo, destino FROM Destinos")
        destinos = cursor.fetchall()
        dataDestino = [dict(zip([column[0] for column in cursor.description], record)) for record in destinos]
        return dataDestino
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los destinos: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion    

#region - FUNCIÓN PARA RECUPERAR PRODUCTOS       
def getProductos():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT IDproducto, Codigo, Nombre FROM Productos")
        productos = cursor.fetchall()
        dataProducto = [dict(zip([column[0] for column in cursor.description], record)) for record in productos]
        # print(f"dataProducto: {dataProducto}")
        return dataProducto
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los destinos: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion 
            
#region - FUNCIÓN PARA RECUPERAR VEHICULOS       
def getVehiculos():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT id, placa, nombre FROM Vehiculo")
        vechiculos = cursor.fetchall()
        dataVehiculos = [dict(zip([column[0] for column in cursor.description], record)) for record in vechiculos]
        return dataVehiculos
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los vehiculos: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion             


#region - FUNCIÓN PARA RECUPERAR CONDUCTORES       
def getConductores():
    cursor = None
    try:
        cursor = db.database.cursor()
        cursor.execute("SELECT id, documento, nombre FROM Conductores")
        conductores = cursor.fetchall()
        dataConductores = [dict(zip([column[0] for column in cursor.description], record)) for record in conductores]
        return dataConductores
    except Exception as e:
        print(f"Ha ocurrido un error al obtener los conductores: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
#endregion 


#region - Filtros Múltiples
@app.route('/filtrosmultiples')
def filtrosmultiples():
    dataProveedor = getProveedores()
    dataOrigen = getOrigenes()
    dataDestino = getDestinos()
    dataVehiculo = getVehiculos()
    dataProducto = getProductos()
    print(f"dataProveedor: {dataProveedor}")
    return render_template('filtrosmultiples.html', dataProveedor=dataProveedor, dataOrigen=dataOrigen, dataDestino=dataDestino, dataVehiculo = dataVehiculo,
                           dataProducto=dataProducto)    


@csrf.exempt
@app.route('/consultasmultiples', methods=['POST'])
def consultasmultiples():
    tipomovimiento = request.form.get('tipomovimiento')
    fecha_desde = request.form.get('fecha_desde') # request.form['fecha_desde']
    fecha_hasta = request.form.get('fecha_hasta') # request.form['fecha_hasta']
    nombre_producto = request.form.get('nombre_producto')  # Nuevo campo
    idmovimiento = request.form.get('idmovimiento')  # Nuevo campo
    origen = request.form.get('origen')  # Nuevo campo
    destino = request.form.get('destino')
    codigoprov = request.form.get('codigoprov')
    nombreprov = request.form.get('nombreproveedor')
    placa = request.form.get('placa')

    cursor = db.database.cursor()

    query = ''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, 
                Movimiento.fechasalida, Movimiento.horasalida, Movimiento.observaciones,
                Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, Movimiento.pesoentrada,
                Movimiento.pesosalida, Movimiento.pesoneto,
                Conductores.nombre AS nombreconductor,
                Vehiculo.placa AS placa,
                Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                Destinos.codigo AS codigodestino, Destinos.destino AS destino
                FROM Movimiento
                JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                WHERE 1=1 AND Movimiento.pesosalida IS NOT NULL''' # WHERE fechaentrada BETWEEN %s AND %s AND fechasalida IS NOT NULL AND Proveedores.documento = %s '''

    # Agregamos las condiciones adicionales si los campos están presentes
    params = [] # params = [fecha_desde, fecha_hasta, codigoprov]
    if tipomovimiento:
        query += ' AND Movimiento.tipomovimiento = %s'
        params.append(tipomovimiento)
    if fecha_desde and not fecha_hasta:
        query += ' AND fechaentrada = %s'
        params.append(fecha_desde)
    elif fecha_hasta and not fecha_desde:
        query += ' AND fechasalida = %s'
        params.append(fecha_hasta)
    elif fecha_desde and fecha_hasta:
        query += ' AND fechaentrada BETWEEN %s AND %s'
        params.extend([fecha_desde, fecha_hasta])
    if nombre_producto:
        query += ' AND Productos.nombre = %s'
        params.append(nombre_producto)
    if idmovimiento:
        query += ' AND Movimiento.idmovimiento = %s'
        params.append(idmovimiento)
    if origen:
        query += ' AND Origenes.origen = %s'
        params.append(origen)
    if destino:
        query += ' AND Destinos.destino = %s'
        params.append(destino)    
    if codigoprov:
        query += ' AND Proveedores.documento = %s'
        params.append(codigoprov)
    if nombreprov:
        query += ' AND Proveedores.nombre = %s'
        params.append(nombreprov)  
    if placa:
        query += ' AND Vehiculo.placa LIKE %s'
        params.append("%" + placa + "%")   

    cursor.execute(query, params)
    movimientos = cursor.fetchall()
    dataMovimientos = [dict(zip([column[0] for column in cursor.description], record)) for record in movimientos]

    return render_template('multiplesresultados.html', dataMovimientos=dataMovimientos)


@app.route('/entra')
def entra():
    dataProveedor = getProveedores()
    dataOrigen = getOrigenes()
    dataDestino = getDestinos()
    dataVehiculo = getVehiculos()
    dataProducto = getProductos()
    #print(f"dataProveedor: {dataProveedor}")
    return render_template('consultaentradas.html', dataProveedor=dataProveedor, dataOrigen=dataOrigen, dataDestino=dataDestino, dataVehiculo = dataVehiculo,
                           dataProducto=dataProducto) 
#endregion - Filtro Múltiples


@csrf.exempt 
@app.route('/consultaentradas', methods=['POST'])
def consultaentradas():
    tipomovimiento = request.form.get('tipomovimiento')
    fecha_desde = request.form.get('fecha_desde') # request.form['fecha_desde']
    fecha_hasta = request.form.get('fecha_hasta') # request.form['fecha_hasta']
    nombre_producto = request.form.get('nombre_producto')  # Nuevo campo
    idmovimiento = request.form.get('idmovimiento')  # Nuevo campo
    origen = request.form.get('origen')  # Nuevo campo
    destino = request.form.get('destino')
    codigoprov = request.form.get('codigoprov')
    nombreprov = request.form.get('nombreproveedor')
    placa = request.form.get('placa')

    cursor = db.database.cursor()
        
    codigoprov = session['codigoprov']
    
    print(f"Usuario actual::: {session['codigoprov']}")
        # Consultar la base de datos por movimientos en el rango de fechas especificado
        # cursor.execute(''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, Movimiento.observaciones,
    query = ''' SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, 
                Movimiento.fechasalida, Movimiento.horasalida, Movimiento.observaciones,
                Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, Movimiento.pesoentrada,
                Movimiento.pesosalida, Movimiento.pesoneto,
                Conductores.nombre AS nombreconductor,
                Vehiculo.placa AS placa,
                Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                Destinos.codigo AS codigodestino, Destinos.destino AS destino
                FROM Movimiento
                JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                WHERE Proveedores.documento=%s AND Movimiento.pesosalida IS NOT NULL'''
    # Agregamos las condiciones adicionales si los campos están presentes
    params = [codigoprov] # params = [fecha_desde, fecha_hasta, codigoprov]
    if tipomovimiento:
        query += ' AND Movimiento.tipomovimiento = %s'
        params.append(tipomovimiento)
    if fecha_desde and not fecha_hasta:
        query += ' AND fechaentrada = %s'
        params.append(fecha_desde)
    elif fecha_hasta and not fecha_desde:
        query += ' AND fechasalida = %s'
        params.append(fecha_hasta)
    elif fecha_desde and fecha_hasta:
        query += ' AND fechaentrada BETWEEN %s AND %s'
        params.extend([fecha_desde, fecha_hasta])
    if nombre_producto:
        query += ' AND Productos.nombre = %s'
        params.append(nombre_producto)
    if idmovimiento:
        query += ' AND Movimiento.idmovimiento = %s'
        params.append(idmovimiento)
    if origen:
        query += ' AND Origenes.origen = %s'
        params.append(origen)
    if destino:
        query += ' AND Destinos.destino = %s'
        params.append(destino)    
    if codigoprov:
        query += ' AND Proveedores.documento = %s'
        params.append(codigoprov)
    if nombreprov:
        query += ' AND Proveedores.nombre = %s'
        params.append(nombreprov)  
    if placa:
        query += ' AND Vehiculo.placa LIKE %s'
        params.append("%" + placa + "%")   

    cursor.execute(query, params)
    movimientos = cursor.fetchall()
    dataMovimientos = [dict(zip([column[0] for column in cursor.description], record)) for record in movimientos]
        
    return render_template('resultado.html', dataMovimientos=dataMovimientos)




#region Proveedores :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/proveedores')
def proveedores():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM Proveedores LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM Proveedores")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('proveedores.html', data=insertObject, num_pages=total_pages, current_page=page)

@csrf.exempt 
@app.route('/addproveedor', methods=['POST'])
def addproveedor():
    documento = request.form['documento'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if documento and nombre:
        cursor = db.database.cursor()
        sql = "INSERT INTO Proveedores (documento, nombre) VALUES (%s, %s)"
        data = (documento, nombre)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('proveedores'))

@csrf.exempt 
@app.route('/deleteproveedor/<string:id>')
def deleteproveedor(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM Proveedores WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('proveedores'))

@csrf.exempt 
@app.route('/editproveedor/<string:id>', methods=['POST'])
def editproveedor(id):
    documento = request.form['documento'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if documento and nombre:
        cursor = db.database.cursor()
        sql = "UPDATE Proveedores SET documento = %s, nombre = %s WHERE id = %s"
        data = (documento, nombre, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('proveedores'))

#endregion


#region Productos
@csrf.exempt 
@app.route('/productos')
def productos():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM Productos LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM Productos")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('index.html', data=insertObject, num_pages=total_pages, current_page=page)

# Ruta para guardar productos en la base de datos # @app.route('/', methods=['GET','POST'])
@csrf.exempt 
@app.route('/addproductos', methods=['POST'])
def addproductos():
    codigo = request.form['codigo']
    nombre = request.form['nombre']

    if codigo and nombre:
        cursor = db.database.cursor()
        # sql = "INSERT INTO Productos (codigo, nombre) VALUES ('$codigo', '$nombre')"
        sql = "INSERT INTO Productos (codigo, nombre) VALUES (%s, %s)"
        data = (codigo, nombre)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('productos'))

@csrf.exempt 
@app.route('/deleteproducto/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM Productos WHERE IDproducto = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('productos'))

# @app.route('/', methods=['GET','POST'])
@csrf.exempt 
@app.route('/editproducto/<string:id>', methods=['POST'])
def edit(id):
    codigo = request.form['codigo']
    nombre = request.form['nombre']

    if codigo and nombre:
        cursor = db.database.cursor()
        sql = "UPDATE Productos SET codigo = %s, nombre = %s WHERE IDproducto = %s"
        data = (codigo, nombre, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('productos'))   
#endregion    

#region Conductores :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/conductores')
def conductores():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM Conductores LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM Conductores")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('conductores.html', data=insertObject, num_pages=total_pages, current_page=page)

@csrf.exempt 
@app.route('/addconductor', methods=['POST'])
def addconductor():
    documento = request.form['documento'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if documento and nombre:
        cursor = db.database.cursor()
        sql = "INSERT INTO Conductores (documento, nombre) VALUES (%s, %s)"
        data = (documento, nombre)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('conductores'))

@csrf.exempt 
@app.route('/deleteconductor/<string:id>')
def deleteconductor(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM Conductores WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('conductores'))

@csrf.exempt 
@app.route('/editconductor/<string:id>', methods=['POST'])
def editconductor(id):
    documento = request.form['documento'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if documento and nombre:
        cursor = db.database.cursor()
        sql = "UPDATE Conductores SET documento = %s, nombre = %s WHERE id = %s"
        data = (documento, nombre, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('conductores'))

#endregion    

#region Vehiculos :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/vehiculos')
def vehiculos():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM Vehiculo LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM Vehiculo")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('vehiculos.html', data=insertObject, num_pages=total_pages, current_page=page)

@csrf.exempt 
@app.route('/addvehiculo', methods=['POST'])
def addvehiculo():
    placa = request.form['placa'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if placa and nombre:
        cursor = db.database.cursor()
        sql = "INSERT INTO Vehiculo (placa, nombre) VALUES (%s, %s)"
        data = (placa, nombre)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('vehiculos'))

@csrf.exempt 
@app.route('/deletevehiculo/<string:id>')
def deletevehiculo(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM Vehiculo WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('vehiculos'))

@csrf.exempt 
@app.route('/editvehiculo/<string:id>', methods=['POST'])
def editvehiculo(id):
    #id = request.form['id'] # id, documento, nombre
    nombre = request.form['nombre'] # 

    if nombre:
        cursor = db.database.cursor()
        sql = "UPDATE Vehiculo SET nombre = %s WHERE id = %s"
        data = (nombre, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('vehiculos'))

#endregion 

# region Origenes :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/origenes')
def origenes():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM origenes LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM origenes")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('origenes.html', data=insertObject, num_pages=total_pages, current_page=page)

# Ruta para guardar origenes en la base de datos # @app.route('/', methods=['GET','POST'])
@csrf.exempt 
@app.route('/addorigen', methods=['POST'])
def addorigen():
    codigo = request.form['codigo']
    origen = request.form['origen']

    if codigo and origen:
        cursor = db.database.cursor()
        sql = "INSERT INTO origenes (codigo, origen) VALUES (%s, %s)"
        data = (codigo, origen)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('origenes'))

@csrf.exempt 
@app.route('/deleteorigen/<string:id>')
def deleteorigen(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM origenes WHERE idorigen = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('origenes'))

@csrf.exempt 
@app.route('/editorigen/<string:id>', methods=['POST'])
def editorigen(id):
    codigo = request.form['codigo']
    origen = request.form['origen']

    if codigo and origen:
        cursor = db.database.cursor()
        sql = "UPDATE origenes SET codigo = %s, origen = %s WHERE idorigen = %s"
        data = (codigo, origen, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('origenes'))   
#endregion Origenes 

# region Destinos :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/destinos')
def destinos():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM destinos LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM destinos")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]

    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    cursor.close()

    return render_template('destinos.html', data=insertObject, num_pages=total_pages, current_page=page)

# Ruta para guardar destinos en la base de datos # @app.route('/', methods=['GET','POST'])
@csrf.exempt 
@app.route('/adddestino', methods=['POST'])
def adddestino():
    codigo = request.form['codigo']
    destino = request.form['destino']

    if codigo and destino:
        cursor = db.database.cursor()
        sql = "INSERT INTO destinos (codigo, destino) VALUES (%s, %s)"
        data = (codigo, destino)
        cursor.execute(sql, data)
        db.database.commit()

    return redirect(url_for('destinos'))

@csrf.exempt 
@app.route('/deletedestino/<string:id>')
def deletedestino(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM destinos WHERE iddestino = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('destinos'))

@csrf.exempt 
@app.route('/editdestino/<string:id>', methods=['POST'])
def editdestino(id):
    codigo = request.form['codigo']
    destino = request.form['destino']

    if codigo and destino:
        cursor = db.database.cursor()
        sql = "UPDATE destinos SET codigo = %s, destino = %s WHERE iddestino = %s"
        data = (codigo, destino, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('destinos'))   

#endregion Destinos     




# region User :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@csrf.exempt 
@app.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de registros por página

    offset = (page - 1) * per_page  # Offset para la consulta SQL

    cursor = db.database.cursor()
    cursor.execute(f"SELECT * FROM user LIMIT {per_page} OFFSET {offset}")
    mysqlresult = cursor.fetchall() 
    insertObject = []  # Lista para almacenar los registros convertidos a diccionarios
    columnName = [column[0] for column in cursor.description]
    for record in mysqlresult:
        insertObject.append(dict(zip(columnName, record)))

    cursor.execute("SELECT COUNT(*) FROM user")  # Contar el número total de registros
    total_records = cursor.fetchone()[0]
    #print(f"insertObject Usuarios::: {insertObject}")
    total_pages = ceil(total_records / per_page)  # Calcular el número total de páginas

    # cursor.close()

    return render_template('users.html', data=insertObject, num_pages=total_pages, current_page=page)

# Ruta para guardar origenes en la base de datos # @app.route('/', methods=['GET','POST'])
@csrf.exempt 
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        descripcion = request.form['descripcion']
        codigoprov = request.form['codigoprov']
        editarpesos = request.form['permiteeditarpesos']
        productospermitidos = request.form['productospermitidos']

        print(f"editarpesos: {editarpesos}")
        print(f"productospermitidos: {productospermitidos}")

        # Obtener el valor del checkbox y convertirlo a un booleano
        editarpesos = True if request.form.get('permiteeditarpesos') == 'on' else False

        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s, %s)', (username, hashed_password, descripcion, codigoprov, 
                                                                          editarpesos, productospermitidos,))
        mysql.connection.commit()
        # msg = '¡Te has registrado exitosamente!'
        # return render_template('auth/register.html', msg=msg)
    return redirect(url_for('users'))

@csrf.exempt 
@app.route('/deleteuser/<string:id>')
def deleteuser(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM user WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('users'))

@csrf.exempt 
@app.route('/editusers/<string:id>', methods=['POST'])
def editusers(id):
    codigo = request.form['codigo']
    origen = request.form['origen']

    if codigo and origen:
        cursor = db.database.cursor()
        sql = "UPDATE origenes SET codigo = %s, origen = %s WHERE idorigen = %s"
        data = (codigo, origen, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('origenes'))   
#endregion User 


#region rutas anteriores
# @app.route('/stop')
# def stop_simulation():
#     try:
#         ser.close()
#         return "Puerto COM cerrado."
#     except serial.SerialException as e:
#         return f"Error al cerrar el puerto COM: {e}"

# @app.route('/open')
# def open_simulation():
#     try:
#         ser.open()
#         return "Puerto COM abierto."
#     except serial.SerialException as e:
#         return f"Error al abrir el puerto COM: {e}"

#endregion


if __name__ == "__main__":
    app.run("0.0.0.0",7000,threaded=True,debug=True)    

    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    #puerto_com2 = "COM3"  # Puedes cambiar esto según tu configuración de puertos
    #threading.Thread(target=simular_bascula, args=(puerto_com2,)).start()
    #socketio.run(app, port=7000)

    #app.config.from_object(config['development'])
    #csrf.init_app(app)
    
