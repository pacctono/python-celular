# General: modulo para manejar rutinas generales.
#-*- coding:ISO-8859-1 -*-
from __future__ import print_function # Para poder usar 'print' de version 3.

try:
  if __name__ == '__main__' or 0 > __name__.find('lib'):
    from __init__ import DIR, LINEA, bMovil
    if not bMovil: DIR = '../' + DIR
  else:
    from lib import DIR, LINEA, bMovil
    if not bMovil: DIR = './' + DIR
except:
  DIR = './'
  LINEA = 70
  bMovil = False

if bMovil:
  try:
    import androidhelper as android
  except:
    import android
  droid = android.Android()
else: droid = None

if __name__ == '__main__' or 0 > __name__.find('lib'): import ES
else: from lib import ES

eliminarPuntos = lambda cadena, cad='.': cadena.replace(cad, '') # Cadena (solo digitos) del socio.
cambiarAPunto  = lambda cadena, cad=',': cadena.replace(cad, '.')
formateaNumeroTelefono = lambda cad: (cad if (10!=len(cad)) else
                                "0%s-%s-%s" % (cad[0:3], cad[3:6], cad[6:]))
formateaFecha = lambda cad: (cad if (10>len(cad)) else
                                "%s-%s-%s" % (cad[-2:], cad[5:7], cad[0:4]))
formateaRif = lambda cad: (cad if (10!=len(cad)) else
                                "%s-%s-%s" % (cad[0:1], cad[1:9], cad[-1:]))
def descomponeFecha(fec):
  from datetime import date

  try:
    ano = int(fec[-4:])
    mes = int(fec[3:5])
    dia = int(fec[0:2])
  except ValueError:
    ano = int(fec[0:4])
    mes = int(fec[5:7])
    dia = int(fec[-2:])
  diaSem = date(ano, mes, dia).weekday()
  return ano, mes, dia, diaSem
# funcion formateaFecha

def esEntero(v):
    v = str(v).strip()
    return v=='0' or (v if v.find('..') > -1 else \
                            v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()
# Funcion esEntero
def formateaNumero(cad, dec=0):
  if (not isinstance(cad, str) and not isinstance(cad, float) and \
      not isinstance(cad, int)) and ((None != dec) and not isinstance(dec, int)):
    return None
  if None == dec: dec = 0
  if isinstance(cad, str): cad = cad.strip(' \t\n\r')

  if isinstance(cad, float) or isinstance(cad, int): cad = str(cad)
  try:
    fCad = float(cad)
    fCad = round(fCad, dec)
#    signo = ''
#    if 0 > fCad:
#      signo = '-'
#      fCad  = -fCad
    cad = str(fCad)
  except:
    return None

  x = cad.split('.')		# Divide el numero en parte entera (x[0]) y parte decimal (x[1]).
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
#  x = re.findall(pas0 = "{:,}".format(s)

#  for i in range(0,s0 = "{:,}".format(s)

#    if 4 <= len(x0)s0 = "{:,}".format(s)

#      x1 = '.' + x0s0 = "{:,}".format(s)

#      x0 = x0[0:-3]s0 = "{:,}".format(s)

#    else:
#      x1 = x0 + x1
#  print('fn: ', signo + x1 + x2)

# parte entera (x1) con '.' intercalado cada 3 dec + parte decimal con ',' adelante.
  return x1 + x2
# funcion formateaNumero(sCad, dec)
def selOpcionMenu(lOpciones, sTitulo='Que desea hacer'):	# Devuelve una de las opciones de lOpciones.
  ''' Menu desplegado al inicio. '''
  nOpciones = len(lOpciones)

  lSeleccion = [lOpciones[i][0] for i in range(nOpciones)]	# Opciones a desplegar.
  lFuncion   = [lOpciones[i][1] for i in range(nOpciones)]	# Funciones a ejecutar por cada opcion desplegada.
  indice = ES.entradaConLista(droid, sTitulo, 'Que desea hacer', lSeleccion)
  if None == indice or 0 > indice: return -11
  return lFuncion[indice]
# funcion selOpcionMenu(lOpciones)
def limpiarPantalla():
  import os

  if 'posix' == os.name:
    os.system('clear')
  elif os.name in ('ce', 'nt', 'dos'):
    os.name('cls')
# funcion limpiarPantalla
def numeroPorc(num, dec=0):
  cad = ''
  try:
    if (0 != num): cad = formateaNumero(num, dec) + '%'
  except: pass
  return cad if cad else '0.000%'
# Funcion numeroPorc
def numeroMon(num, dec=0, mon='$'):
  cad = ''
  try:
    if (0 != num): cad = mon + formateaNumero(num, dec)
  except: pass
  return cad
# Funcion numeroMon
