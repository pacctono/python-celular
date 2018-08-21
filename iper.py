#!/usr/bin/python
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
import io
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
  from os import listdir
  from os.path import isfile, join, basename
  import fnmatch
else:
  from os.path import abspath, basename

from lib import ES, Const as CO

if bMovil:
  def cargarNombres(nombArch='IPER*.TXT'):
    rutaDatos = DIR

    lFiles = [f for f in listdir(rutaDatos) if isfile(join(rutaDatos, f)) and 
                                                fnmatch.fnmatch(f, nombArch)]
    lFiles.sort()

    if not lFiles:
      ES.alerta(droid, nombArch, "No hubo coincidencias!")
      return None
    return lFiles
  # FIN funcion cargarNombres
  def buscarArchivo(lFiles):
    if None == lFiles or 1 > len(lFiles): return None
    if 1 == len(lFiles): return(lFiles[0])
    indice = ES.entradaConLista(droid, 'ARCHIVOS ENCONTRADOS',
                                        'Seleccione nombre', lFiles)
    if None == indice or 0 > indice: return None
    return(lFiles[indice])
  # FIN funcion buscarArchivo

sCed = None
if bMovil:
  lFiles = cargarNombres('[Ii][Pp][Ee][Rr]*.[Tt][Xx][Tt]')
  if not lFiles: sys.exit()
else:
  if 1 < len(sys.argv):
    nombArchCompleto = sys.argv[1]
    nombArch = basename(nombArchCompleto)
    if 2 < len(sys.argv) and sys.argv[2].isdigit():
      sCed = sys.argv[2]
  else:
    print("%sNo paso el nombre del archivo como parametro.%s" % (CO.ROJO,
                                                                  CO.FIN))
    sys.exit()

while True:
  if bMovil:
    nombArch = buscarArchivo(lFiles)
    if None == nombArch: break
    f = ES.abrir(nombArch, 'r', 'latin-1')
    iCed = ES.entradaNumero(droid, "Cedula de identidad",
                                        "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = None
    else: sCed = str(iCed)
  else:
    try:
      f = ES.abrir(nombArchCompleto, 'r', 'latin-1', True)
    except:
      f = False
  if not f:
    print("%sNombre de archivo%s '%s' %serrado.%s" % (CO.ROJO, CO.FIN,
                                          nombArchCompleto, CO.ROJO, CO.FIN))
    break

# List comprehensions:
# Cedula; Nombre (corto=11:40/largo=11:83); Nucleo (42:44/83:85) y Cuenta bancaria (45:65/86:106).
#  lista = [(linea.rstrip()[0:10], linea.rstrip()[11:83], linea.rstrip()[42:44], \
#          linea.rstrip()[45:65], linea.rstrip()[83:85], linea.rstrip()[86:106]) for linea in f]
#  dicc = {}
#  lCed = []
#  i = 0
#  for l in lista:
#    if not dicc.has_key(l[0]):
#    if l[0] not in dicc:
#      dicc[l[0]] = (l[0], l[1], l[2], l[3], l[4], l[5])
#      lCed.append(l[0])
#      lCed.insert(i, l[0])
#      i += 1
# dict comprehensions:
# Cedula; Nombre (corto=11:40/largo=11:83); Nucleo (42:44/83:85) y Cuenta bancaria (45:65/86:106).
  dicc = {linea.rstrip()[0:10]:(linea.rstrip()[0:10], linea.rstrip()[11:83],
          linea.rstrip()[42:44], linea.rstrip()[45:65], linea.rstrip()[83:85],
          linea.rstrip()[86:106]) for linea in f}
  if bMovil: lCed = [k for k in dicc]   # dicc.keys no funciona en celular.
# el metodo 'items' de diccionarios devuelve un 'view object' del tipo "dict_items" que contiene una lista de key-value.
# el metodo 'keys' de diccionarios devuelve un 'view object' del tipo "dict_keys" que contiene una lista de keys.
# el metodo 'values' de diccionarios devuelve un 'view object' del tipo "dict_values" que contiene una lista de values.
  else: lCed = list(dicc.keys())        # Ambos funcionan en PC. Solo para mostrar ambas maneras. Tambien, en 3.5: [*dicc] porque dict devuelve keys cuando iterate.
  lCed.sort()

  iL = 0		# Numero de linea leida.
  nC = 0		# Numero de linea corta.
  nL = 0		# Numero de linea larga.
  bImpar = False
  for v in lCed:
    iL += 1
    if '' == v or '' == v.strip() or None == v or not v or \
                                                not v.lstrip('0').isdigit():
      print('Linea: ' + str(iL) + ', v: ' + v)
      break
    try:
      if dicc[v][2].isdigit() and dicc[v][3].isdigit():	# Linea corta
        if 0 == (iL%100): print("%8d %30.30s Nuc==>> %s Cta==>> %s" % \
                (int(dicc[v][0]), dicc[v][1], dicc[v][2], dicc[v][3]))
        nC += 1
      elif dicc[v][4].isdigit() and dicc[v][5].isdigit():	# Linea larga
        if sCed:
          if sCed.lstrip('0') == v.lstrip('0'):
            sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
            print("%s%5d: %8d %30.30s Nuc==>> %s Cta==>> %s%s" % (sColor,
              iL, int(dicc[v][0]), dicc[v][1], dicc[v][4], dicc[v][5], CO.FIN))
        elif 0 == (iL%500):
          sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
          print("%s%5d: %8d %30.30s Nuc==>> %s Cta==>> %s%s" % (sColor, iL,
                int(dicc[v][0]), dicc[v][1], dicc[v][4], dicc[v][5], CO.FIN))
        nL += 1
      else:
        print(("%sERROR: (Linea:%d{Corta:%d/Larga:%d})%s;%s(%d):%25.25s\n"
                "Nucleo: {Corta:%s|Larga:%s}; Cuenta: {Corta:%s|Larga:%s}") % \
                (CO.ROJO, iL, nC, nL, CO.FIN, dicc[v][0], len(dicc[v][0]),
                dicc[v][1], dicc[v][2], dicc[v][4], dicc[v][3], dicc[v][5]))
        break
    except:
      print(CO.ROJO + 'PROBABLEMENTE HAY UN ERROR (Linea:' + str(iL) + \
              '{Corta:' + str(nC) + '/Larga:' + str(nL) + '}' + ': ' + v + \
              '|' + dicc[v][1] + '|' + dicc[v][2] + '|' + dicc[v][3] + '|' + \
              dicc[v][4] + '|' + dicc[v][5] + '|' + ') CON EL ARCHIVO: ' + \
              nombArch + CO.FIN)
      break

  if 0 < nC: print("%5d: %8d %30.30s Nuc==>> %s Cta==>> %s" % \
                 (iL, int(dicc[v][0]), dicc[v][1], dicc[v][2], dicc[v][3]))
  else:
    sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
    print("%s%5d: %8d %30.30s Nuc==>> %s Cta==>> %s%s" % (sColor, iL, \
                int(dicc[v][0]), dicc[v][1], dicc[v][4], dicc[v][5], CO.FIN))
  print("%s%d lineas; %d lineas cortas y %d lineas largas%s" % (CO.VERDE, iL, \
                                                            nC, nL, CO.FIN))
  f.close()
  if bMovil:
    ES.imprime('')
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer',
                                                    ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    break

# FIN Principal