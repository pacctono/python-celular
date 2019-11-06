# Comun: Rutinas comunes para la inmobiliaria.
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

lSitios = ["Puente Real", "Portatil Barcelona", "Portatil Casa", "Virtualbox",
			"Otro", "Volver"]
lIPs    = ["192.168.0.220", "192.168.0.200", "192.168.0.200", "192.168.0.205", ""]
CONTROL = 'control.txt'

def muestraError(func, desc, cad, ln, dec=0):
  print('ERROR en ' + func + ': ' + desc + ':' + type(desc))
  print('ERROR en ' + func + ': ' + cad + ':' + type(cad))
  print('ERROR en ' + func + ': ' + ln + ':' + type(ln))
  print('ERROR en ' + func + ': ' + dec + ':' + type(dec))
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
  except TypeError:
    muestraError('prepLnBool', desc, condAsesor, condArreglo)
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
  except TypeError:
    muestraError('prepLnCad', desc, cad, ln)
    return ''
# Funcion prepLnCad
def prepLnNum(desc, num, dec=0, ln=''):
#  print(CO.ROJO + 'DESC EN <prepLnNum>:' + CO.FIN, desc, num, dec, ln)
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, FG.formateaNumero(num, dec))
    else: return ''
  except TypeError:
    muestraError('prepLnNum', desc, num, ln, dec)
    return ''
# Funcion prepLnNum
def prepLnFec(desc, fec, ln=''):
  try:
    if ln:
      lng = int(ln) if isinstance(ln, str) else ln
      if (0 < ln): fec = fec[0:int(ln)]
    if ('' != fec): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, fec)
    else: return ''
  except TypeError:
    muestraError('prepLnFec', desc, fec, ln)
    return ''
# Funcion prepLnFec
def prepLnTel(desc, tel, ln=''):
  try:
    if ('' != tel): return ("%s%s:%s %" + ln + "s\n")\
                % (CO.AZUL, desc, CO.FIN, FG.formateaNumeroTelefono(tel))
    else: return ''
  except TypeError:
    muestraError('prepLnTel', desc, tel, ln)
    return ''
# Funcion prepLnTel
def prepLnMon(desc, num, dec=0, ln='', mon='$'):
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                  % (CO.AZUL, desc, CO.FIN, FG.numeroMon(num, dec, mon))
    else: return ''
  except TypeError:
    muestraError('prepLnMon', desc, num, ln, dec)
    return ''
# Funcion prepLnMon
def prepLnPorc(desc, num, dec=0, ln=''):
  try:
    if (0 != num): return ("%s%s:%s %" + ln + "s\n")\
                        % (CO.AZUL, desc, CO.FIN, FG.numeroPorc(num, dec))
    else: return ''
  except TypeError:
    muestraError('prepLnPorc', desc, num, ln, dec)
    return ''
# Funcion prepLnPorc
def prepLnMsj(dMsj, dic, campo, *opcion):
  '''
    Prepara la linea a imprimir:
    dic: Diccionario desde donde se tomara el valor a imprimir.
    campo: llave en el diccionario del campo a imprimir. Tambien, para dMsj.
    tipo: tipo de campo. 0:cadena, 1:numero, 2:fecha, 3:telefono, 4:moneda, 5:porcentaje
    lng: longitud de caracteres, minimo, a mostrar del campo.
    dec: numero de decimales, si el campo a imprimir es numerico.
  '''

  # print(CO.AMARI + 'CAMPO EN <prepLnMsj>:' + CO.FIN, campo)
  # print('dMsj:', dMsj[campo])
  # print('dic:', dic[campo])
  # print('opcion:', opcion)
  var = dMsj.get(campo, 'Ninguno')
  # if 'pcCom' == campo: print('dic:', dic[campo])
  if 'Ninguno' == var: return campo + ' no esta en el diccionario de mensajes (COM.dMsj).\n'
  # if 'pcCom' == campo: print('dic:', dic[campo])
  if not var: return ''
  valor = dic.get(campo, 'NoExiste')
  # if 'pcCom' == campo: print('campo:', campo, dic[campo], valor)
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
    msj = prepLnBool(desc, valor, str(lng))
  elif ('s' == tipo):
    msj = prepLnCad(desc, valor, str(lng))
  elif ('n' == tipo):
    msj = prepLnNum(desc, valor, dec, str(lng))
  elif ('f' == tipo):
    msj = prepLnFec(desc, valor, str(lng))
  elif ('t' == tipo):
    msj = prepLnTel(desc, valor, str(lng))
  elif ('m' == tipo):
    if 'moneda' in dic:
      msj = prepLnMon(desc, valor, dec, str(lng), dic['moneda'])
    else: msj = prepLnMon(desc, valor, dec, str(lng))
  elif ('p' == tipo):
    msj = prepLnPorc(desc, valor, dec, str(lng))
  else:
    msj = ''
  return msj
# Funcion prepLnMsj
def descNegociacion(llave):
  global dNeg
  return dNeg.get(llave, 'Negociacion no existe:'+llave)[0:22]
# Funcion descNegociacion
def descEstatus(llave):
  global dEst
  return dEst.get(llave, 'Estatus no existe:'+llave)[0:30]
# Funcion descEstatus
def descEstatusC21(llave):
  global dSC21
  return dSC21.get(llave, 'Estatus sistema C21 no existe:'+llave)[0:31]
# Funcion descEstatusC21
def descTipo(llave):
  global dTip
  return dTip.get(llave, 'Tipo no existe:'+llave)[0:30]
# Funcion descTipo
def descCaracteristica(llave):
  global dCar
  return dCar.get(llave, 'Caracteristica no existe:'+llave)[0:30]
# Funcion descCaracteristica
def descCiudad(llave):
  global dCiu
  return dCiu.get(llave, 'Ciudad no existe:'+llave)[0:30]
# Funcion descCiudad
def descMunicipio(llave):
  global dMun
  return dMun.get(llave, 'Municipio no existe:'+llave)[0:30]
# Funcion descMunicipio
def descEstado(llave):
  global dEdo
  return dEdo.get(llave, 'Estado no existe:'+llave)[0:30]
# Funcion descEstado
def descDeseo(llave):
  global dDes
  return dDes.get(llave, 'Deseo no existe:'+llave)[0:30]
# Funcion descDeseo
def descZona(llave):
  global dZon
  return dZon.get(llave, 'Zona no existe:'+llave)[0:30]
# Funcion descZona
def descPrecio(llave):
  global dPre
  return dPre.get(llave, 'Precio no existe:'+llave)[0:30]
# Funcion descPrecio
def descOrigen(llave):
  global dOri
  return dOri.get(llave, 'Origen no existe:'+llave)[0:30]
# Funcion descOrigen
def descResultado(llave):
  global dRes
  return dRes.get(llave, 'Resultado no existe:'+llave)[0:30]
# Funcion descResultado
def selEstatus():
  global dEst

  lEst = [(dEst[key], key) for key in dEst]
  st = FG.selOpcionMenu(lEst + [['Volver', 'v']], 'Estatus')

  return st
# Funcion selEstatus
def selMes(lTMe, incluirTodos=False):

  if incluirTodos: nvaLst = [['Todos', 't']]
  else: nvaLst = []
  for l in lTMe:
    nvaLst.append([l[0][0:4]+' '+CO.meses[int(l[0][5:])], l[0]])
  mes = FG.selOpcionMenu(nvaLst + [['Volver', 'v']], 'Mes')
  if ('v' == mes): return 'v', 'v'
  if ('t' == mes): return 't', 't'

  return mes[0:4], mes[5:]
# Funcion selMes
def selOpcion(Menu, descr):
  menu = Menu

  opc = FG.selOpcionMenu(menu + [['Volver', -1]], descr)
  if isinstance(opc, int) and 0 > int(opc): return opc
  else:
    if (0 == opc.find('PRO')): from c21 import Propiedades as PRO
    elif (0 == opc.find('Con')): from c21.Contacto import Contacto as Con
    elif (0 == opc.find('Cli')): from c21.Cliente import Cliente as Cli
    elif (0 == opc.find('Tur')): from c21.Turno import Turno as Tur
    elif (0 == opc.find('Age')): from c21.Agenda import Agenda as Age
    func = eval(opc)	# Evaluar contenido de opc; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType): return func()	# Si la cadena evaluada es una funcion, ejecutela.
    else: return opc
# Funcion BuscProp

# Definir variables globales
def prepararDiccionarios(dir=''):
  global dNeg, dTip, dCar, dCiu, dMun, dEdo, dEst, dMon, dSC21, dDes,\
          dZon, dPre, dOri, dRes

  dNeg = ES.cargaJson(dir+'negociacion.txt')
  if not dNeg: dNeg = {}
  dTip = ES.cargaJson(dir+'tipos.txt')
  if not dTip: dTip = {}
  dCar = ES.cargaJson(dir+'caracteristicas.txt')
  if not dCar: dCar = {}
  dCiu = ES.cargaJson(dir+'ciudads.txt')
  if not dCiu: dCiu = {}
  dMun = ES.cargaJson(dir+'municipios.txt')
  if not dMun: dMun = {}
  dEdo = ES.cargaJson(dir+'estados.txt')
  if not dEdo: dEdo = {}
  dEst = ES.cargaJson(dir+'estatus.txt')
  if not dEst: dEst = {}
  dMon = ES.cargaJson(dir+'moneda.txt')
  if not dMon: dMon = {}
  dSC21 = ES.cargaJson(dir+'estatus_sistema_c21.txt')
  if not dSC21: dSC21 = {}
  dDes = ES.cargaJson(dir+'deseos.txt')
  if not dDes: dDes = {}
  dZon = ES.cargaJson(dir+'zonas.txt')
  if not dZon: dZon = {}
  dPre = ES.cargaJson(dir+'precios.txt')
  if not dPre: dPre = {}
  dOri = ES.cargaJson(dir+'origens.txt')
  if not dOri: dOri = {}
  dRes = ES.cargaJson(dir+'resultados.txt')
  if not dRes: dRes = {}
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
    return ES.muestraFin()
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
      return ES.muestraFin()
      sys.exit()
  except ValueError:						# La funcion rindex (busca indece desde el final de la cadena), no consigue el '.'.
    print("ERROR EXTRA#O DE RED")									# Este error NUNCA deberia ocurrir.
    return ES.muestraFin()
    sys.exit()

# Se trata de saber, cuando se actualizo por ultima vez un archivo. En el nuevo control.txt,
# ademas de la informacion del sistema, tambien se guardara la fecha de descarga de cada archivo.
# dControl = ES.cargaDicc("control.txt")	# Diccionario de control, antes de recibir el nuevo. No implementado 27/08/2019.

  URL = "http://" + IPServ + ':8080/storage/'
  bImpar  = True
  data = urlopen(URL + CONTROL, None, 10).read().decode('ISO-8859-1')	# None, ningun parametro es enviado al servidor; 10, timeout.
  if None == data:
    print('ERROR. No hubo carga.')
    sys.exit()
  f = open(DIR + CONTROL, "w")
  if f:
    archivos = data.split('\n')
    fechaGrabado = archivos.pop(0)
    f.write('Datos grabados: ' + fechaGrabado)
    ahora = strftime("\nDatos descargados: %a, %d/%m/%Y %-l:%M:%S %p\n", localtime())
    f.write(ahora)
    f.close()
  else:
    print('ERROR. No se pudo escribir en el archivo.')
    sys.exit()
  for nombreArchivo in archivos:
#    if nombreArchivo[5:6].isdigit(): continue      # La primera linea es una fecha. El primer caracter es un digito.    
    nombreArchivo = nombreArchivo.rstrip(' \t\n\r')
    if not nombreArchivo: continue
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE, CO.AZUL)
    print("%sLeyendo%s %s remoto." % (sColor, CO.FIN, nombreArchivo))
    try:
      data = urlopen(URL + nombreArchivo, None, 10).read().decode('ISO-8859-1')	# None, ningun parametro es enviado al servidor; 10, timeout.
      bLeido = True												# No hubo error de lectura desde el servidor.
    except:
      print("%sERROR LEYENDO%s %s %sREMOTO.%s" % (CO.ROJO, CO.FIN, nombreArchivo,
                                CO.ROJO, CO.FIN))
      bLeido = False
    if bLeido:														# Si no hubo error de lectura desde el servidor.
      try:
        f = open(DIR + nombreArchivo, "w")
        bAbierto = True											# No hubo error al abrir para escribir en archivo local.
      except:
        print("%sERROR AL TRATAR DE ABRIR%s %s%s %sPARA ESCRITURA.%s" % \
                  (CO.ROJO, CO.FIN, DIR, nombreArchivo, CO.ROJO, CO.FIN))
        bAbierto = False
      if bAbierto:												# Si no hubo error al abrir para escribir en archivo local.
        print("%sEscribiendo%s %s local..." % (sColor, CO.FIN, nombreArchivo))
        try:
          f.write(data)
          bEscrito = True										# No hubo error escribiendo en el archivo local.
        except:
          print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (CO.ROJO, CO.FIN,
                                      nombreArchivo))
          bEscrito = False
        finally:
          f.close()
        if bEscrito:
          print("%s %sactualizado con%s %d lineas!" % (nombreArchivo,
                  (CO.CYAN if 'heute.txt' == nombreArchivo else sColor),
                            CO.FIN, ES.cLineas(nombreArchivo)))
        # Fin if bEscrito
      # Fin if bAbierto
    # Fin if bLeido
  # Fin for
  return ES.muestraFin()
# Funcion actualizar