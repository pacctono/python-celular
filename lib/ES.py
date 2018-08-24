# libES: modulo para entrada y salida.
#-*-coding:utf8;-*-
from __future__ import print_function # Para poder usar 'print' de version 3.

try:
  if __name__ == '__main__' or 0 > __name__.find('lib'):
    from __init__ import DIR, LINEA, bMovil
    if not bMovil: DIR = '..' + DIR
  else:
    from lib import DIR, LINEA, bMovil
    if not bMovil: DIR = '.' + DIR
except:
  DIR = './'
  bMovil = False

import sys
import os
import re
from time import time, localtime, strftime, sleep
if 0 > __name__.find('lib'): import Const as CO
else: from lib import Const as CO

AMARI = CO.color.YELLOW	  # Primer titulo. Identifica la fecha de actualizacion de los datos.
CYAN  = CO.color.CYAN			# Identificacion del socio.
AZUL  = CO.color.BLUE			# Identificacion de los datos.
VERDE = CO.color.GREEN		# Linea final (totales).
ROJO  = CO.color.RED			# Error.
FIN  = CO.color.END

patron = re.compile(r"\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile(r"\d{1,3}")	        # Expresion regular: 1 o mas dig (\d+) y tres dig al final (\d{3}).

par = lambda x: (0 == (x%2))	# Es un numero par.
def abrir(aNb, modo='r', codigo = 'UTF-8', bImprimir = False):
  'Abre para leer, el archivo cuyo nombre es el valor de aNb'
  import io
  from os.path import abspath, basename
  global DIR

  if basename(aNb) == aNb: aNb = DIR + aNb
  try:
    if bMovil: f = open(aNb, mode=modo, encoding=codigo)
    else: f = io.open(aNb, mode=modo, encoding=codigo)
    if (bImprimir): print('[ES]' + aNb + " archivo abierto.")
    return f
  except:
    if (bImprimir):
      print(AMARI + "[ES]ERROR ABRIENDO (DIR): " + FIN + aNb + ' (' + DIR + ')')
      print(AMARI + "os.path.abspath(aNb): " + FIN + abspath(aNb))
    return False
# funcion abrir
def abrirErr(aNb, bImprimir = False):
  'Abre para escribir, el archivo cuyo nombre es el valor de aNb'
  aNb = DIR + aNb
  try:
    f = open(aNb, 'w')
    if (bImprimir): print('[ES]' + aNb + " archivo abierto.")
    return f
  except:
    if (bImprimir): print("[ES]ERROR ABRIENDO: " + aNb)
    return False
# funcion abrirErr
def esEntero(v):
    v = str(v).strip()
    return v=='0' or (v if v.find('..') > -1 else \
                            v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()
# Funcion esEntero
def fgFormateaNumero(sCad, dec=0):
  if (not isinstance(sCad, str) and not isinstance(sCad, float) and \
      not isinstance(sCad, int)) and ((None != dec) and not dec.isinteger()):
    return None
  if None == dec: dec = 0
  if isinstance(sCad, str): sCad = sCad.strip(' \t\n\r')

  if isinstance(sCad, float) or isinstance(sCad, int): sCad = str(sCad)
  try:
    fCad = float(sCad)
    fCad = round(fCad, dec)
#    signo = ''
#    if 0 > fCad:
#      signo = '-'
#      fCad  = -fCad
    sCad = str(fCad)
  except:
    return None

  x = sCad.split('.')		# Divide el numero en parte entera (x[0]) y parte decimal (x[1]).
  x0 = int(x[0])	      # x0 es la parte entera
  if 1 < len(x):        # Esta y las prox 6 lineas parecen innecesarias por 'round' arriba.
    x2 = x[1]           # x2 es la parte decimal.
  if 0 < dec:
    x2 = ',' + x2.ljust(dec, '0')
    dec += 1			      # Crece en 1 al agregar la coma "," decimal.
  else: x2 = ''
  if dec < len(x2): x2 = x2[0:dec]

# Agrupa de 3 en 3 y separa con ',', luego la remplaza con '.'.
  x1 = "{:,}".format(x0).replace(',','.')
#  x1 = ''
#  x = re.findall(pat, x0)
#  for i in range(0, len(x)):
#    if 4 <= len(x0):
#      x1 = '.' + x0[-3:] + x1
#      x0 = x0[0:-3]
#    else:
#      x1 = x0 + x1
#  print('fn: ', signo + x1 + x2)

# parte entera (x1) con '.' intercalado cada 3 dec + parte decimal con ',' adelante.
  return x1 + x2
# funcion fgFormateaNumero(sCad, dec)
def fgEliminarPuntos(sCadena, sP='.'):
  lCadDig = sCadena.rstrip().split(sP)
  return ''.join(lCadDig)		# Cadena (solo digitos) del socio.
# funcion fgEliminarPuntos
def fgCambiarAPunto(sCad):
	return sCad.replace(',', '.')
# funcion fgCambiarAPunto(sCad)
def formateaNumeroTelefono(sNum):
	if 10 != len(sNum): return sNum
	else: return "%s-%s-%s" % (sNum[0:3], sNum[3:6], sNum[6:])
# funcion formateaNumeroTelefono
def alerta(droid, titulo, valor=''):

  if droid:
    droid.dialogCreateAlert(titulo, valor)
    droid.dialogSetPositiveButtonText('Aceptar')
    droid.dialogSetNegativeButtonText('Cancelar')
    droid.dialogShow()
    resultado = droid.dialogGetResponse().result
    droid.dialogDismiss()
  else:
    print(titulo, valor, sep=':')
    resultado = True
  return resultado
# funcion alerta
def mostrarValor(droid, valor):
  
  sValor = repr(valor)
  return alerta(droid, 'EL VALOR SUMINISTRADO', sValor)
# funcion mostrarValor
def entradaNumero(droid, titulo = 'Entrada de un valor numerico',
                  mensaje = 'Introduzca numero', porDefecto='-1', bEntero=True,
                  bZero=False, bNegativo=False):
  '''Permite la entrada manual de un valor numerico.
     bEntero=True: Solo se permite numero entero.
     bZero=True: Permite el valor zero.
     bNegativo=True: Permite valores negativos.'''

  if droid:
    resultado = droid.dialogGetInput(titulo, mensaje, porDefecto).result
    droid.dialogDismiss()
  else:
    while True:
      print(titulo)    
      resultado = input(mensaje + ': ')
      if resultado.isdigit() or None == resultado: break
  if None == resultado: return None
  resultado = fgEliminarPuntos(resultado)
  bMatch = patron.match(resultado)
  if None == bMatch: return bMatch
  elif (not bZero) and (0 == float(resultado)): return None
  elif (not bNegativo) and (0 > float(resultado)): return None
  elif bEntero:
    try:
      nRes = int(resultado)
      return nRes
    except:
      return None
  else: return float(resultado)
# funcion entradaNumero
def entradaNombre(droid, titulo = 'Entrada de datos',
                  mensaje = 'Introduzca texto', porDefecto = ''):
  '''Permite la entrada manual de texto.'''

  if droid:
    resultado = droid.dialogGetInput(titulo, mensaje, porDefecto).result
    droid.dialogDismiss()
  else:
    print(titulo)    
    resultado = porDefecto
    resultado = input(mensaje + ': ')
  return resultado
# funcion entradaNombre
def entradaContrasena(droid, titulo = 'Contrasena',
                      mensaje = 'Introduzca contrasena', porDefecto = ''):
  '''Permite la entrada manual de texto.'''

  if droid:
    resultado = droid.dialogGetPassword(titulo, mensaje).result
    droid.dialogDismiss()
  else:
    import getpass
    print(titulo)    
    resultado = porDefecto
    resultado = getpass.getpass(mensaje)
  return resultado
# funcion entradaNombre
def entradaFecha(droid, ano, mes, dia):
  if droid:    
    droid.dialogCreateDatePicker(ano, mes, dia)
    droid.dialogShow()
    resultado = droid.dialogGetResponse().result
    droid.dialogDismiss()
  else:
#    import datetime    
    while True:    
      try:
        fecha = input('Introduzca la fecha en formato DD-MM-YYYY:' )
#        fech1 = datetime.datetime.strptime(fecha, "%d-%m-%y")
        dia, mes, ano = map(int, fecha.split('-'))
        resultado = str(ano).rjust(4, '0') + str(mes).rjust(2, '0') + \
                                                        str(dia).rjust(2, '0')
        break
      except:
        print('Oh! Oh! Fecha Errada.')
  return resultado
# funcion entradaFecha
def entradaFechaLocal(droid, ano='', mes='', dia=''):
  if ('' == ano): ano = strftime("%Y")
  if ('' == mes): mes = strftime("%m")
  if ('' == dia): dia = strftime("%d")
  resultado = entradaFecha(droid, ano, mes, dia)
  resAno = "%04d" % resultado['year']
  resMes = "%02d" % resultado['month']
  resDia = "%02d" % resultado['day']
  sFecha = resDia + '/' + resMes + '/' + resAno
  return sFecha
# funcion entradaFechaLocal
def entradaConLista(droid, titulo, mensaje, lista):
  '''Muestra una Lista para escoger un valor.'''

  if droid:
    droid.dialogCreateAlert(titulo)
    droid.dialogSetItems(lista)
    droid.dialogShow()
    try:
      indice = droid.dialogGetResponse().result['item']
      droid.dialogDismiss()
    except:
      droid.dialogDismiss()
      return None
  else:
    print(titulo)    
    print(mensaje)    
    i = 0
    for item in lista:
      print(i, item, sep='.-')
      i += 1
    indice = entradaNumero(droid, '', 'Introduzca un número', 0, True, True)
  if None == indice or 0 > indice or (len(lista) <= indice): return None
  else: return indice
# funcion entradaConLista
def entradaNumeroConLista(droid, titulo, mensaje, lista, bEntero=True,
                          bZero=False, bNegativo=False):
  '''Muestra una Lista para escoger un valor. El ultimo sirve para la entrada
     manual (entradaNumero). bEntero, bZero=True, bNegativo: Son usados por la
     funcion entradaManual.'''

  indice  = entradaConLista(droid, titulo, mensaje, lista)
  if None == indice: return None
  iUltimo = len(lista) - 1
  if iUltimo == indice:
    porDefecto = str(lista[iUltimo-1])
    rValor = entradaNumero(droid, titulo, mensaje, porDefecto, bEntero, bZero,
                                                                    bNegativo)
    while None == rValor:
      rValor = entradaNumero(droid, titulo + ' Error!',
                'Debe introducir un valor valido', porDefecto, bEntero, bZero,
                bNegativo)
    return rValor
  else:
    return float(lista[indice])
# funcion entradaNumeroConLista
def cLineas(aNb):
  'Abre un archivo de texto y cuenta sus lineas'
  f = abrir(aNb)
  if not f: return -1
  lineas = f.readlines()
  nLineas = len(lineas)
  f.close()
  return nLineas
# funcion cLineas
def cargaLista(aNb):
  'Abre para leer, el archivo cuyo nombre es el valor de aNb y crea una lista'
  f = abrir(aNb)
  if not f: return []
  try:
    lista = [linea.rstrip().split(';') for linea in f if 3 < len(linea)] # List comprehension. Evita lineas en blanco
  except IOError as err:
    print("[ES]Error E/S: {0}".format(err))
  except UnicodeDecodeError as err:
    print("[ES]Error decodificando unicode: {0}".format(err))
  except:
    print("[ES]Error inesperado:", sys.exc_info()[0])
    raise
  finally:
    f.close()
  if 'lista' in locals(): return lista
  else: return []
# funcion cargaLista
def cargaDicc(aNb):
  '''Abre para leer, el archivo cuyo nombre es el valor de aNb y crea un
     diccionario'''
  f = abrir(aNb)
  dicc = {}
  if not f: return dicc
  for linea in f:
    try:
      k, v = linea.rstrip().split(';', 1)
      if ';' in v: v = v[0:v.find(';')]
      dicc[k.strip()] = v.strip()
    except: continue
  f.close()
  return dicc
# funcion cargaDicc
def cargaDiccLista(aNb):
  '''Abre para leer, el archivo cuyo nombre es el valor de aNb y crea un
     diccionario, cuya data es una lista'''
  f = abrir(aNb)
  dicc = {}
  if not f: return dicc
  for linea in f:
    try:
      list = linea.rstrip().split(';')
      lista = [list[i].strip() for i in range(len(list))]
      dicc[lista[0].strip()] = lista
    except: continue
  f.close()
  return dicc
# funcion cargaDiccLista
def llenarCadena(nCar, sCad='-+'):
  sCadena = ''
  for _ in range(nCar): sCadena += sCad
  return sCadena
# funcion llenarCadena(nCar, sCad='-+')
def imprime(st):
  print(st)
  sFin     = ' F I N '										# 7 caracteres.
  sFinLin  = '-->'											# 3 caracteres.
  nCarJust = int(CO.leenCarMostrar() - len(sFin+sFinLin) - 1)	# ' F I N ' = 7 cars + '-->' = 3 cars. Queda 1 espacio al final.
  if par(nCarJust): nEspIzq  = ''							# Si es par no agregar espacio a la izquierda.
  else:
    nEspIzq   = ' '
    nCarJust -= 1
  nCarJust   /= 2											# Numero de cars da cada lado.
  if par(nCarJust): sRellenar = ''
  else:
    sRellenar = '-'
    nCarJust -= 1
  nCarJust   /= 2											# Numero de cars da cada lado.
  sRellenar = llenarCadena(int(nCarJust), '-+') + sRellenar		# Cadena a imprimir de cada lado.
  s = input(sRellenar + nEspIzq + sFin + sRellenar + sFinLin)	# Muestra la cadena final.
  return s
# funcion imprime
def colorLinea(bImpar=True, sColor=VERDE, sOtroColor=''):
  if bImpar: sColor = sOtroColor
  return sColor, not bImpar
# funcion colorLinea
def muestraInicio(sEmp):
  nCar = len(sEmp)
  if not par(nCar): nCar += 1
  sLinea = llenarCadena(int(nCar/2), '-+')
  print(sLinea)
  print(AMARI + sEmp + FIN + ' ' + strftime("%d/%m/%Y %H:%M:%S", localtime()))
  print(sLinea)
# funcion muestraInicio
def muestraFin():
  print(AMARI + 'PC 2015 y posterior' + FIN + ' ' + \
                                    strftime("%d/%m/%Y %H:%M:%S", localtime()))
  print("-+-+-+-+-+-+-+-+-+-+")
  print("Listo!")
# funcion muestraFin
