# libES: modulo para entrada y salida.
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

eliminarPuntos = lambda sCadena, sCad='.': sCadena.replace(sCad, '') # Cadena (solo digitos) del socio.
cambiarAPunto  = lambda sCadena, sCad=',': sCadena.replace(sCad, '.')
formateaNumeroTelefono = lambda sNum: (sNum if (10!=len(sNum)) else
                                "0%s-%s-%s" % (sNum[0:3], sNum[3:6], sNum[6:]))
formateaFecha = lambda sNum: (sNum if (10>len(sNum)) else
                                "%s-%s-%s" % (sNum[8:10], sNum[5:7], sNum[0:4]))
#def formateaNumeroTelefono(sNum):
#	if 10 != len(sNum): return sNum
#	else: return "%s-%s-%s" % (sNum[0:3], sNum[3:6], sNum[6:])
# funcion formateaNumeroTelefono

def esEntero(v):
    v = str(v).strip()
    return v=='0' or (v if v.find('..') > -1 else \
                            v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()
# Funcion esEntero
def formateaNumero(sCad, dec=0):
  if (not isinstance(sCad, str) and not isinstance(sCad, float) and \
      not isinstance(sCad, int)) and ((None != dec) and not isinstance(dec, int)):
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
