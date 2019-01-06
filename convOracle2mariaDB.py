#!/usr/bin/python
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para usar 'print' de version 3.
import sys
from time import time, localtime, strftime, sleep
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
  def cargarNombres(nombArchEnt='nomina*.sql'):
    rutaDatos = DIR

    lFiles = [f for f in listdir(rutaDatos) 
                if isfile(join(rutaDatos, f)) and 
                    fnmatch.fnmatch(f, nombArchEnt)]
    lFiles.sort()

    if not lFiles:
      ES.alerta(droid, nombArchEnt, "No hubo coincidencias!")
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
  lFiles = cargarNombres('nomina*.sql')
  if not lFiles: sys.exit()
else:
  if 1 < len(sys.argv):
    sufijoEntrada = sys.argv[1]
    prefijoNombArch = 'nomina_'
    sufijoSalida = strftime("%Y_%m")
    if 2 < len(sys.argv):
      sufijoSalida = sys.argv[2]
      if 3 < len(sys.argv):
        prefijoNombArch = sys.argv[3]
    else:
      if sufijoEntrada.isdigit():
        if 4 <= len(sufijoEntrada) and 6 >= len(sufijoEntrada):
          if 4 == len(sufijoEntrada):
            sufijoSalida = '20' + sufijoEntrada[2:] + '_' + \
                            sufijoEntrada[0:2]
          elif 5 == len(sufijoEntrada):
            sufijoSalida = '2' + sufijoEntrada[2:] + '_' + \
                            sufijoEntrada[0:2]
          elif 6 == len(sufijoEntrada):
            sufijoSalida = sufijoEntrada[2:] + '_' + \
                            sufijoEntrada[0:2]
    nombArchEntCompleto = prefijoNombArch + sufijoEntrada + '.sql'
    nombArchEnt = basename(nombArchEntCompleto)
    nombArchSalCompleto = prefijoNombArch + sufijoSalida + '.sql'
    nombArchSal = basename(nombArchSalCompleto)
  else:
    print("%sNo suministro el sufijo de entrada.%s" % (CO.ROJO, CO.FIN))
    sys.exit()

while True:
  if bMovil:
    nombArchEnt = buscarArchivo(lFiles)
    if None == nombArchEnt: break
    f = ES.abrir(nombArchEnt, 'r', 'latin-1')
    iCed = ES.entradaNumero(droid, "Cedula de identidad",
                                  "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = None
    else: sCed = str(iCed)
  else:
    try:
      f = ES.abrir(nombArchEntCompleto, 'r', 'latin-1')
    except:
      f = False
  if not f:
    print("%sNombre de archivo%s '%s' %serrado.%s" % (CO.ROJO, CO.FIN,
                                nombArchEntCompleto, CO.ROJO, CO.FIN))
    break
#  print("%sNombre de archivos, entrada:%s '%s'%s, salida:%s '%s'" % \
#        (CO.AMARI, CO.FIN, nombArchEntCompleto, CO.AMARI, CO.FIN, \
#          nombArchSalCompleto))
  nInsert = False   # No se ha encontrado un 'insert into'.
  salida  = []
  salida.append('SET GLOBAL max_allowed_packet=128*1024*1024;')
  nLineas = 1       # Numero de lineas
  for linea in f:
    linea = linea[0:linea.index('\n')]
    if 0 <= linea.lower().find('set feed'): continue  # set feedback
    if 0 <= linea.lower().find('alter') and \
      0 <= linea.lower().find('triggers'): continue   # set alter.*triggers
    if 0 <= linea.lower().find('set define'): continue  # set define
    if 0 <= linea.lower().find('prompt'): continue    # prompt
    if 0 <= linea.lower().find('commit'): continue    # commit
    if 0 <= linea.find('NOMINA'):
      linea = linea.replace('NOMINA', 'nomina')
    if 0 <= linea.find('PERSONAL'):
      linea = linea.replace('PERSONAL', 'personal')
    if 0 <= linea.find('RAC'):
      linea = linea.replace('RAC', 'rac')
    if 0 <= linea.lower().find('create table'):
      linea = linea.replace(sufijoEntrada, sufijoSalida)
      salida.append('DROP TABLE IF EXISTS ' + \
          linea[linea.lower().find('create')+13:] + ';')
      nLineas += 1
      linea = linea.replace('create table', 'CREATE TABLE')
    if 0 <= linea.lower().find('create unique index'):
      linea = linea.replace(sufijoEntrada, sufijoSalida)
      linea = linea.replace('create unique index', \
                            'CREATE UNIQUE INDEX')
    if 0 <= linea.lower().find('insert into'):
      if not nInsert: # Mantener y cambiar primera linea con 'insert into'
        linea = linea.replace(sufijoEntrada, sufijoSalida)
        nInsert = True
        linea = linea.lower().replace('insert into', 'INSERT INTO')
        linea = linea[0:linea.index('(')] + 'VALUES'
        linUltValue = nLineas + 1   # El '1' representa la linea actual.
      else:
        continue
    if nInsert and 0 == linea.lower().find('values '):
      if 0 < linea.rfind(';'): linea = linea[0:linea.rfind(';')] + ','
      linea = linea.replace('values ', '')    
      linea = linea.replace('VALUES ', '')    
      if 0 < linea.lower().find('to_date'):
        iDate = linea.lower().index('to_date')
        iParentesisAbre = linea.index('(', iDate)
        iParentesisCierra = linea.index(')', iParentesisAbre)
        fecha = \
            linea[iParentesisAbre+1:iParentesisCierra].lstrip().rstrip()
        linea = linea[0:iDate] + fecha + \
                linea[iParentesisCierra+1:].lstrip().rstrip()
      linUltValue += 1
    nLineas += 1
    salida.append(linea)
  linUltValue -= 1
  salida[linUltValue] = \
            salida[linUltValue][0:salida[linUltValue].rfind(',')] + ';'
  for linea in salida:
    print(linea)
#  print(linUltValue)
#  print(nLineas)

  break

# FIN Principal