# libComun: Rutinas comunes para ipaspudo.
#-*- coding:ISO-8859-1 -*-
import sys
import types
import json
import socket
import struct
from urllib.request import urlopen
from time import time, localtime, strftime, ctime

from lib import ES, Const as CO, General as FG

try:
  from lib import DIR, LINEA, bMovil
except:
  DIR = './'
  bMovil = False

if bMovil:
  try:
    import androidhelper as android
  except:
    import android
  droid = android.Android()
else: droid = None

'''lClasCheques = [
          "Cheque", "Codigo", "Nombre", "Monto", "Estado", "Fecha", "Concepto"
               ]
'''
lMenuLstPro = [
          ['Propiedades X Estatus', 'PRO.lstXEstatus'],
          ['Propiedades X Asesor', 'PRO.lstXAsesor'],
          ['Propiedades X Mes', 'PRO.lstXMes'],
        ]
lMenuProEsp = [
          ['Propiedades X Estatus', 'PRO.xEstatus'],
          ['Propiedades X Nombre', 'PRO.xNombre'],
          ['Propiedades X Asesor', 'PRO.xAsesor'],
          ['Codigo de casa nacional', 'PRO.xCodigo'],
          ['Reporte en casa nacional', 'PRO.xReporte'],
        ]
lMenuTot = [
          ['Totales X Asesor', 'PRO.totAsesor'],
          ['Totales X Mes', 'PRO.totMes'],
          ['Totales X Estatus', 'PRO.totEst'],
          ['Totales X Asesor X Mes', 'PRO.totAsesorMes'],
          ['Totales X Mes X Asesor', 'PRO.totMesAsesor'],
          ['Totales generales', 'PRO.totales'],
        ]
lMenu = [
          ['Calcular cuota', 'cuota'],                  # 0
          ['Calcular comision', 'comisiones'],          # 1
          ['Actualizar datos', 'COM.actualizar'],
          ['Cumpleaneros', 'ASE.cumpleanos'],           # 3
          ['Asesor', 'ASE.asesor'],
          ['Todas las propiedades', 'PRO.propiedades'],
          ['Listar propiedades por ...', 'PRO.LstPropPor'],
          ['Buscar una propiedad', 'PRO.buscProp'],
          ['Totalizar por ...', 'PRO.totPor'],
          ['Salir', 'salir']
	      ]

lSitios = ["Puente Real", "Portatil Barcelona", "Portatil Casa",
			"Otro", "Salir"]
lIPs    = ["192.168.0.101", "192.168.0.200", "192.168.1.200", ""]
lDATA = [
		 'control.txt',			# Por procesamiento posterior, este archivo, SIEMPRE, debe estar primero.
		 'asesores.txt',
		 'estatus.txt',
		 'estatus_sistema_c21.txt',
		 'moneda.txt',
		 'negociacion.txt',
		 'propiedades.txt',
		 'totales.txt',
		]

dMsj = {
          "id":False,
          "cedula":["Cedula de identidad", 'n', "", 0],               # Datos del asesor, como diccionario.
          "name":["Nombre", 's', "", 0],
          "telefono":["Telefono", 't', "", 0],
          "email":["Correo electronico", 's', "", 0],
          "email_c21":["Correo electronico Century 21", 's', "", 0],
          "licencia_mls":["Licencia MLS", 's', "", 0],
          "fecha_ingreso":["Fecha de ingreso", 'f', "", 0],
          "fecha_nacimiento":["Fecha de nacimiento", 'f', "", 0],
          "sexo":False,
          "genero":["Sexo", 's', "", 0],
          "estado_civil":False,
          "edocivil":["Estado civil", 's', "", 0],
          "profesion":["Profesion", 's', "", 0],
          "direccion":["Direccion", 's', "", 0],
          'is_admin':['Este usuario es administrador del sistema', 'b', True, 0],
          'socio':['Este asesor es Socio', 'b', True, 0],
          'activo':['Este asesor no esta activo en la oficina', 'b', False, 0],
          'updated_at':['Datos del asesor modificados', 's', "", 0],
#          'created_at':['Datos del asesor modificados', 's', "", 0],
          'created_at':False,
          "tCap":["Total captado", 'n', "22", 2],
          "tCer":["Total cerrado", 'n', "22", 2],
          "tCaptCer":["Total captado y cerrado", 'n', "22", 2],
          "0":"Numero incremental",                     # Datos de la propiedad, como lista.
          "1":"Codigo casa nacional",
          "2":"fecha de reserva",
          "3":"fecha de firma",
          "4":"Negociacion:",
          "5":"Nombre de la propiedad",
          "6":"Status",
          "7":"Moneda",
          "8":"Precio",
          "9":"Comision",
          "10":"Monto de la reserva sin IVA",
          "11":"IVA",
          "12":"Monto de la reserva con IVA",
          "13":"Monto compartido con otra oficina con IVA",
          "14":"Monto compartido con otra oficina sin IVA",
          "15":"Lados",
          "16":"Franquicia de reserva sin IVA",
          "17":"Franquicia de reserva con IVA",
          "18":"Porcentaje Franquicia",
          "19":"Franquicia a pagar reportada",
          "20":"Porcentaje reportado a casa nacional",
          "21":"Porcentaje Regalia",
          "22":"Regalia",
          "23":"Sanaf - 5%",
          "24":"Bruto real de la oficina",
          "25":"Base para honorario de los socios",
          "26":"Base para honorario",
          "27":"Id del asesor captador",
          "28":"Nombre del asesor captador",
          "29":"Porcentaje Comision del captador",
          "30":"Comision del captador PrBr",
          "31":"Porcentaje Comision del gerente",
          "32":"Comision del gerente",
          "33":"Id del asesor cerrador",
          "34":"Nombre del asesor cerrador",
          "35":"Porcentaje Comision del cerrador PrBr",
          "36":"Comision del cerrador",
          "37":"Porcentaje Bonificacion",
          "38":"Bonificacion",
          "39":"Comision bancaria",
          "40":"Ingreso neto de la oficina",
          "41":"Numero de recibo",
          "42":"Forma de pago al gerente",
          "43":"Factura gerente",
          "44":"Forma de pago a los asesores",
          "45":"Factura asesores",
          "46":"Pago otra oficina",
          "47":"Pagado a Casa Nacional",
          "48":"Status C21",
          "49":"Reporte Casa Nacional",
          "50":"Factura A&S",
          "51":"Comentarios"
        }

def prepLnBool(desc, condAsesor, condArreglo=True):
  # print(CO.ROJO + 'DESC EN <prepLnMsj>:' + CO.FIN, desc)
  try:
    if condAsesor:
      color = CO.AMARI
      desc = desc if condArreglo else ''
    else:
      color = CO.ROJO
      desc = '' if condArreglo else desc
    if '' == desc: return ''
    return ("%s%s%s\n") % (color, desc, CO.FIN)
  except:
    print('ERROR en prepLnBool. Desc: ' + desc)
    return ''
# Funcion prepLnBool
def prepLnCad(desc, cad, ln=''):
  try:
    if ln:
      lng = int(ln) if isinstance(ln, str) else ln
      if (0 < lng): cad = cad[0:int(lng)]
    if ('' != cad): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, cad)
    else: return ''
  except:
    print('ERROR en prepLnCad: ' + desc)
    return ''
# Funcion prepLnCad
def prepLnNum(desc, num, dec=0, ln=''):
  # print(CO.ROJO + 'DESC EN <prepLnNum>:' + CO.FIN, desc, num, dec, ln)
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, FG.formateaNumero(num, dec))
    else: return ''
  except:
    print('ERROR en prepLnNum: ' + desc)
    return ''
# Funcion prepLnNum
def prepLnFec(desc, fec, ln=''):
  try:
    if ln:
      lng = int(ln) if isinstance(ln, str) else ln
      if (0 < ln): fec = fec[0:int(ln)]
    if ('' != fec): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, FG.formateaFecha(fec))
    else: return ''
  except:
    print('ERROR en prepLnFec: ' + desc)
    return ''
# Funcion prepLnFec
def prepLnTel(desc, tel, ln=''):
  try:
    if ('' != tel): return ("%s%s:%s %" + ln + "s\n")\
                % (CO.AZUL, desc, CO.FIN, FG.formateaNumeroTelefono(tel))
    else: return ''
  except:
    print('ERROR en prepLnTel: ' + desc)
    return ''
# Funcion prepLnTel
def prepLnMon(desc, num, dec=0, mon='$', ln=''):
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                  % (CO.AZUL, desc, CO.FIN, FG.numeroMon(num, dec, mon))
    else: return ''
  except:
    print('ERROR en prepLnMon: ' + desc)
    return ''
# Funcion prepLnMon
def prepLnPorc(desc, num, dec=0, ln=''):
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, FG.numeroPorc(num, dec))
    else: return ''
  except:
    print('ERROR en prepLnPorc: ' + desc)
    return ''
# Funcion prepLnPorc
def prepLnMsj(dic, campo, *opcion):
  '''
    Prepara la linea a imprimir:
    dic: Diccionario desde donde se tomara el valor a imprimir.
    campo: llave en el diccionario del campo a imprimir. Tambien, para dMsj.
    tipo: tipo de campo. 0:cadena, 1:numero, 2:fecha, 3:telefono, 4:moneda, 5:porcentaje
    lng: longitud de caracteres, minimo, a mostrar del campo.
    dec: numero de decimales, si el campo a imprimir es numerico.
  '''

  # print(CO.AMARI + 'CAMPO EN <prepLnMsj>:' + CO.FIN, campo)
  # print('dic:', dic)
  # print('opcion:', opcion)
  var = dMsj.get(campo, 'Ninguno')
  if 'Ninguno' == var: return campo + ' no esta en el diccionario de mensajes (COM.dMsj).\n'
  if not var: return ''
  valor = dic.get(campo, 'NoExiste')
  # print('campo:', campo, dic[campo], valor)
  if 'NoExiste' == valor: return campo + ' no esta en el diccionario de este asesor.\n'
  elif None == valor or '' == valor: return ''
  try:
    if isinstance(var, list):
      desc = var[0]
      tipo = opcion[0] if 0 < len(opcion) and opcion[0] else var[1]
      lng  = opcion[1] if 1 < len(opcion) and opcion[1] else var[2]
      dec  = opcion[2] if 2 < len(opcion) and opcion[2] else var[3]
    else:
      desc = var
      tipo = tipo if tipo else 's'
      lng  = lng if lng else ''
      dec  = dec if dec else 0
  except:
    print('asesor:', dic)
    print('campo: ' + campo, 'valor:', valor)
    print('lista del diccionario:', var)
    print('arreglo opcion:', opcion)
    print('Descripcion:', desc, 'Tipo:', tipo, 'Lng:', lng, 'Decimales:', dec)
    return
  if ('b' == tipo):
    msj = prepLnBool(desc, valor, lng)
  elif ('s' == tipo):
    msj = prepLnCad(desc, valor, lng)
  elif ('n' == tipo):
    msj = prepLnNum(desc, valor, dec, lng)
  elif ('f' == tipo):
    msj = prepLnFec(desc, valor, lng)
  elif ('t' == tipo):
    msj = prepLnTel(desc, valor, lng)
  elif ('m' == tipo):
    msj = prepLnMon(desc, valor, lng)
  elif ('p' == tipo):
    msj = prepLnPorc(desc, valor, lng)
  else:
    msj = ''
  return msj
# Funcion prepLnMsj
def descEstatus(llave):
  global dEst

  return dEst.get(llave, 'Estatus no existe:'+llave)[0:20]
# Funcion nombreAsesor
def selEstatus():
  global dEst

  lEst = [(dEst[key], key) for key in dEst]
  st = FG.selOpcionMenu(lEst + [['Volver', 'v']], 'Estatus')
  return st

# Funcion selEstatus
def selMes(lTMe):

  nvaLst = []
  for l in lTMe:
    nvaLst.append([l[0][0:4]+' '+CO.meses[int(l[0][5:])], l[0]])
  mes = FG.selOpcionMenu(nvaLst + [['Volver', 'v']], 'Mes')
  if ('v' == mes): return 'v', 'v'

  return mes[0:4], mes[5:]
# Funcion selMes
def nombreProp(fila):
  ''' Retorna el nombre de una propiedad.
      fila[0]: numero incremental.
      fila[1]: Codigo casa nacional.
      fila[2]: fecha de reserva.
      fila[3]: fecha de firma.
      fila[4]: Negociacion: Venta o Alquiler.
      fila[5]: Nombre de la propiedad.
  '''
  return fila[5].strip(' "\t\n\r')
# Funcion nombreProp
def selOpcion(Menu, descr):
  menu = Menu

  opc = FG.selOpcionMenu(menu + [['Volver', -1]], descr)
  if isinstance(opc, int) and 0 > int(opc): return opc
  else:
    from c21 import Propiedades as PRO
    func = eval(opc)	# Evaluar contenido de opc; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType): func()	# Si la cadena evaluada es una funcion, ejecutela.
    else: return opc
# Funcion BuscProp

# Definir variables globales
def prepararDiccionarios(dir=''):
  global dNeg, dMon, dEst, dSC21

  dNeg = ES.cargaJson(dir+'negociacion.txt')
  if not dNeg: dNeg = {}
  dMon = ES.cargaJson(dir+'moneda.txt')
  if not dMon: dMon = {}
  dEst = ES.cargaJson(dir+'estatus.txt')
  if not dEst: dEst = {}
  dSC21 = ES.cargaJson(dir+'estatus_sistema_c21.txt')
  if not dSC21: dSC21 = {}
# Funcion prepararDiccionarios
def getNetworkIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))
	return s.getsockname()[0]
# Funcion getNetworkIP
def obtenerIP(servidor):		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((servidor, 80))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.
# Funcion obtenerIP
def actualizar():

  ind = ES.entradaConLista(droid, 'Busqueda del servidor',\
                  'Seleccione servidor', lSitios)		# Busca el servidor.
  if (None == ind) or (ind == (len(lSitios)-1)) or (len(lSitios) <= ind) or \
            (0 > ind):	# Se asegura de tener el indice correcto.
    ES.muestraFin()
    sys.exit()
  IPServ = lIPs[ind]
  if ((ind == (len(lSitios)-2)) or ('' == IPServ)):
    IPServ = ES.entradaNombre(droid, 'IP del servidor',
                  'Introduzca IP del servidor', IPServ[0:10])
  print("Obteniendo archivo desde %s (%s)." % (lSitios[ind], IPServ))
  if droid:
    decip = droid.wifiGetConnectionInfo().result['ip_address']
    hexip = hex(decip).split('x')[1]
    dirL = int(hexip, 16)
    miDirIP = socket.inet_ntoa(struct.pack("<L", dirL))
  else:
    miDirIP = obtenerIP(IPServ)	# Esta rutina fue la unica que encontre para mi IP.

  print("Mi direccion IP es: %s" % miDirIP)
  try:
    if IPServ[0:IPServ.rindex('.')] != miDirIP[0:miDirIP.rindex('.')]:	# Las tres primeras partes de ambos IPv4 deben ser iguales.
      print("El servidor seleccionado %s es errado." % IPServ)
      ES.muestraFin()
      sys.exit()
  except ValueError:						# La funcion rindex (busca indece desde el final de la cadena), no consigue el '.'.
    print("ERROR EXTRA#O DE RED")									# Este error NUNCA deberia ocurrir.
    ES.muestraFin()
    sys.exit()

# Se trata de saber, cuando se actualizo por ultima vez un archivo. En el nuevo control.txt,
# ademas de la informacion del sistema, tambien se guardara la fecha de descarga de cada archivo.
# dControl = ES.cargaDicc("control.txt")	# Diccionario de control, antes de recibir el nuevo. No implementado 27/08/2019.

  URL = "http://" + IPServ + '/c21pr/storage/'
  bImpar  = True
  dHoy = strftime("%Y%m%d", localtime())
  for DATA in lDATA:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE, CO.AZUL)
    print("%sLeyendo%s %s remoto." % (sColor, CO.FIN, DATA))
    try:
      data = urlopen(URL + DATA, None, 10).read().decode('ISO-8859-1')	# None, ningun parametro es enviado al servidor; 10, timeout.
      bLeido = True												# No hubo error de lectura desde el servidor.
    except:
      print("%sERROR LEYENDO%s %s %sREMOTO.%s" % (CO.ROJO, CO.FIN, DATA,
                                CO.ROJO, CO.FIN))
      bLeido = False
    if bLeido:														# Si no hubo error de lectura desde el servidor.
      try:
        f = open(DIR + DATA, "w")
        bAbierto = True											# No hubo error al abrir para escribir en archivo local.
      except:
        print("%sERROR AL TRATAR DE ABRIR%s %s%s %sPARA ESCRITURA.%s" % \
                  (CO.ROJO, CO.FIN, DIR, DATA, CO.ROJO, CO.FIN))
        bAbierto = False
      if bAbierto:												# Si no hubo error al abrir para escribir en archivo local.
        print("%sEscribiendo%s %s local..." % (sColor, CO.FIN, DATA))
        try:
          f.write(data)
          bEscrito = True										# No hubo error escribiendo en el archivo local.
        except:
          print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (CO.ROJO, CO.FIN,
                                      DATA))
          bEscrito = False
        finally:
          f.close()
        if bEscrito:
          print("%s %sactualizado con%s %d lineas!" % (DATA,
                  (CO.CYAN if 'heute.txt' == DATA else sColor),
                            CO.FIN, ES.cLineas(DATA)))
        # Fin if bEscrito
      # Fin if bAbierto
    # Fin if bLeido
  # Fin for
  ES.muestraFin()
# Funcion actualizar

#Variables globales
iCodCN = 1                # Indice del codigo a Casa Nacional.
iFeRes = 2                # Indice de la fecha de reserva.
iFeFir = 3                # Indice de la fecha firma.
iNegoc = 4                # Indice de la negociacion.
iNombr = 5                # Indice del nombre de la propiedad.
iStatu = 6                # Indice del estatus.
iMoned = 7                # Indice de la moneda.
iPreci = 8                # Indice del precio.
iComis = 9                # Indice de la comision de la negociacion.
iIVA   = 11               # Indice del IVA usado en la negociacion.
iLados = 15               # Indice de lados.
iFRsIv = 16               # Indice de la Franquicia de Reserva sin IVA.
iFRcIv = 17               # Indice de la Franquicia de Reserva con IVA.
iPoFra = 18               # Indice del porcentaje de franquicia.
iFraPR = 19               # Indice de la Franquicia a Pagar Reportada.
iPoRCN = 20               # Indice del porcentaje de Reporte a Casa Nacional.
iPoReg = 21               # Indice del porcentaje de Regalia.
iRegal = 22               # Indice de la regalia.
iIdCap = 27               # Indice del userId del asesor captador.
iNbCap = 28               # Indice del nombre del asesor captador. Inicialmente, cuando es de otra oficina.
iPoCap = 29               # Indice del porcentaje del asesor captador.
iCoCap = 30               # Indice de la comision del asesor captador.
iPoGer = 31               # Indice del porcentaje del asesor gerente.
iCoGer = 32               # Indice de la comision del gerente.
iIdCer = 33               # Indice del userId del asesor cerrador.
iNbCer = 34               # Indice del nombre del asesor cerrador. Inicialmente, cuando es de otra oficina.
iPoCer = 35               # Indice del porcentaje del asesor cerrador.
iCoCer = 36               # Indice de la comision del asesor cerrador.
iNetos = 40               # Indice del neto.
iStC21 = 48               # Indice del estatus del sistema Century 21.
iRepCN = 49               # Indice del reporte a Casa Nacional.

# Descripcion de las filas de propiedades.txt
# fila[0]: numero incremental.
# fila[1]: Codigo casa nacional.
# fila[2]: fecha de reserva.
# fila[3]: fecha de firma.
# fila[4]: Negociacion: Venta o Alquiler.
# fila[5]: Nombre de la propiedad.
# fila[6]: Status.
# fila[7]: Moneda.
# fila[8]: Precio.
# fila[9]: Comision.
# fila[10]: Monto de la reserva sin IVA.
# fila[11]: IVA.
# fila[12]: Monto de la reserva con IVA.
# fila[13]: Monto de compartido con otra oficina con IVA.
# fila[14]: Monto de compartido con otra oficina sin IVA.
# fila[15]: Lados.
# fila[16]: Franquicia de reserva sin IVA.
# fila[17]: Franquicia de reserva con IVA.
# fila[18]: % Franquicia.
# fila[19]: Franquicia a pagar reportada.
# fila[20]: % reportado a casa nacional.
# fila[21]: % Regalia.
# fila[22]: Regalia.
# fila[23]: Sanaf - 5%.
# fila[24]: Bruto real de la oficina.
# fila[25]: Base para honorario de los socios.
# fila[26]: Base para honorario.
# fila[27]: Id del asesor captador.
# fila[28]: Nombre del asesor captador otra oficina.
# fila[29]: % Comision del captador.
# fila[30]: Comision del captador PrBr.
# fila[31]: % Comision del gerente.
# fila[32]: Comision del gerente.
# fila[33]: Id del asesor cerrador.
# fila[34]: Nombre del asesor cerrador otra oficina.
# fila[35]: % Comision del cerrador PrBr.
# fila[36]: Comision del cerrador.
# fila[37]: % Bonificacion.
# fila[38]: Bonificacion.
# fila[39]: Comision bancaria.
# fila[40]: Ingreso neto de la oficina.
# fila[41]: Numero de recibo.
# 42 y 43:  Pago y factura gerente.
# 44 y 45:  Pago y factura asesores.
# fila[46]: Pago otra oficina.
# fila[47]: Pagado a Casa Nacional.
# fila[48]: Status C21.
# fila[49]: Reporte Casa Nacional.
# fila[50]: Factura A&S.
# fila[51]: Comentarios.
