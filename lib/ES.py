# libES: modulo para entrada y salida.
#-*- coding:UTF-8 -*-
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
# raw_input desaparece en ver 3 y se convierte en input.
# Ver: https://blog.teamtreehouse.com
if 2 == sys.version_info.major:
  input = raw_input
import os

try:
  if __name__ == '__main__' or 0 > __name__.find('lib'):
    from __init__ import DIR, LINEA, bMovil
    if not bMovil: DIR = '../' + DIR
  else:
    from lib import DIR, LINEA, bMovil
    if not bMovil: DIR = './' + DIR
except:
  DIR = './'
  bMovil = False

import re
patron = re.compile(r"\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
#pat = re.compile(r"\d{1,3}")	        # Expresion regular: 1 o mas dig (\d+) y tres dig al final (\d{3}).
import json

from time import time, localtime, strftime, sleep
if 0 > __name__.find('lib'): import Const as CO
else: from lib import Const as CO

par = lambda x: (0 == (x%2))	# Es un numero par.
def abrir(aNb, modo='r', codigo = 'ISO-8859-1', bImprimir = False):
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
      print(CO.AMARI + "[ES]ERROR ABRIENDO (DIR): " + CO.FIN + aNb + ' (' +\
              DIR + ')')
      print(CO.AMARI + "os.path.abspath(aNb): " + CO.FIN + abspath(aNb))
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
def alerta(droid, titulo, mensaje=''):

  if droid:
    droid.dialogCreateAlert(titulo, mensaje)
    droid.dialogSetPositiveButtonText('Aceptar')
    droid.dialogSetNegativeButtonText('Cancelar')
    droid.dialogShow()
    resultado = droid.dialogGetResponse().result
    droid.dialogDismiss()
  else:
    print(titulo, mensaje, sep=':')
    resultado = True
  return resultado
# funcion alerta
def siNo(droid, titulo, mensaje='', neutral=True, si='Si', no='No'):

  if droid:
    droid.dialogCreateAlert(titulo, mensaje)
    droid.dialogSetPositiveButtonText(si)
    droid.dialogSetNegativeButtonText(no)
    if (neutral): droid.dialogSetNeutralButtonText('Cancelar')
    droid.dialogShow()
    resultado = droid.dialogGetResponse().result['which']
    droid.dialogDismiss()
    if (resultado in ('positive', 'negative', 'neutral')):
      if ('positive' == resultado): resp = 'S'    # Boton si.
      elif ('negative' == resultado): resp = 'N'  # Boton no.
      else: resp = 'C'                            # Boton 'Cancelar'.
    else: resp = 'C'
  else:
    print(titulo)
    print(mensaje)
    lst = ['Si', 'No', 'Cancelar']
    i = 0
    for item in lst:
      print(i, item, sep='.-')
      i += 1
    indice = -1
    while (0 > indice) or (len(lst) <= indice):
      indice = entradaNumero(droid, '', 'Introduzca un número', 0, True, True)
    resp = lst[indice][0]
  return resp
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
      resultado = input(mensaje + '[' + str(porDefecto) + ']: ')
      if '' == resultado or None == resultado: resultado = str(porDefecto)
      if patron.match(resultado): break
  if None == resultado: return None
# resultado = resultado.replace('.', '')
  bMatch = patron.match(resultado)
  if None == bMatch: return None
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
    resultado = input(mensaje + '[' + porDefecto + ']: ')
    if ('' == resultado) or (None == resultado): resultado = porDefecto
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
    from datetime import datetime
    fechaDefecto = str(dia) + '-' + str(mes) + '-' + str(ano)
    while True:
      try:
        fecha = input('Introduzca la fecha en formato DD-MM-YYYY [' +
                                                        fechaDefecto + ']: ' )
        if None == fecha or '' == fecha: fecha = fechaDefecto
        resultado = datetime.strptime(fecha, "%d-%m-%Y")
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
  print(resultado)
  resAno = "%04d" % (resultado['year'] if droid else resultado.year)
  resMes = "%02d" % (resultado['month'] if droid else resultado.month)
  resDia = "%02d" % (resultado['day'] if droid else resultado.day)
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
def cargaJson(aNb):
  '''Lee una cadena de caracteres desde un archivo que es una
      representacion Json y devuelve la instancia correspondiente.'''
  f = abrir(aNb)
  if not f: return False
  try:
    cad = f.read()
    obj = json.loads(cad)
  except: pass
  finally: f.close()
  if 'obj' in locals(): return obj
  else: return False      # Si 'obj' no esta entre las variables locales de la funcion, no ha sido definida.
# funcion cargaJson
def cargaListaJson(aNb):
  '''Lee una cadena de caracteres, en cada archivo de un archivo; la
      cual, es una representacion Json y devuelve la lista de la
      instancia correspondiente.'''
  f = abrir(aNb)
  if not f: return []
  try:
    lst = [json.loads(linea) for linea in f] # List comprehension
  except IOError as err:
    print("[ES]Error E/S: {0}".format(err))
  except UnicodeDecodeError as err:
    print("[ES]Error decodificando unicode: {0}".format(err))
  except:
    print("[ES]Error inesperado:", sys.exc_info()[0])
    raise
  finally: f.close()
  if 'lst' in locals(): return lst
  else: return []      # Si 'lst' no esta entre las variables locales de la funcion, no ha sido definida.
# funcion cargaListaJson
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
  finally: f.close()
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
# print(st)
  lineas = st.split('\n')
  nLineas = len(lineas)
  n, maxLong = 0, 0
  try:
    nLineasPant = CO.LINEAS         # Numero de lineas a mostrar cada vez, por pantalla.
  except NameError:
    nLineasPant = 25                # Numero de lineas a mostrar cada vez, por pantalla.
  nLinTecladoVirtual = 5            # # de lineas, aprox. que quita el teclado virtual en el celular.
  if bMovil: nLineasPant -= nLinTecladoVirtual
  for linea in lineas:
    n += 1
    print(linea)
    nCarEsp = len(linea.split('\033'))        # Numero de caracteres especiales (color) en la linea.
    if maxLong < (len(linea) - nCarEsp): maxLong = len(linea) - nCarEsp
    if (nLineasPant < n and nLineas > n):
      tecla = input('Presione <ENTER> para continuar o <s><ENTER> para terminar ...')
      if (0 < len(tecla)): break
      n = 0
  maxLong = maxLong if maxLong < (CO.leenCarMostrar() - 1)\
                    else CO.leenCarMostrar() - 1
  sFin     = ' F I N '										# 7 caracteres.
  sFinLin  = '-->'											# 3 caracteres.
  nCarJust = int(maxLong - len(sFin) - len(sFinLin) - 1)	# ' F I N ' = 7 cars + '-->' = 3 cars. Queda 1 espacio al final.
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
def colorLinea(bImpar=True, sColor=CO.VERDE, sOtroColor=''):
  if bImpar: sColor = sOtroColor
  return sColor, not bImpar
# funcion colorLinea
def muestraInicio(sEmp):
  nCar = len(sEmp)
  if not par(nCar): nCar += 1
  sLinea = llenarCadena(int(nCar/2), '-+')
  print(sLinea)
  print(CO.AMARI + sEmp + CO.FIN + ' ' + strftime("%d/%m/%Y %H:%M:%S",
                                                                localtime()))
  print(sLinea)
# funcion muestraInicio
def muestraFin():
  print(CO.AMARI + 'PC 2015 y posterior' + CO.FIN + ' ' +\
                                    strftime("%d/%m/%Y %H:%M:%S", localtime()))
  print("-+-+-+-+-+-+-+-+-+-+")
  print("Listo!")
# funcion muestraFin
