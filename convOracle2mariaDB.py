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

import re
def ireplace(self, viejo, nuevo, count=0):
  ''' Se comporta como string.replace(), pero lo hace
      sin importar minusculas o mayusculas. '''
  
# Las dos lineas siguientes pueden ser sustituidas por:
#  return re.sub('(?i)'+re.escape(viejo), nuevo, self)
  patron = re.compile(re.escape(viejo), re.I) # re.I:ignora minus/mayus
  return re.sub(patron, nuevo, self, count)
# FIN funcion ireplace
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
def obtenerFecha(fechaConFormato):
  fecha, formato = fechaConFormato.split(',')
  fecha = fecha.strip("' \"")
  formato = formato.strip("' \"")
  iDia = formato.find('d')
  if 0 <= iDia: nDia = formato.count('d')
  iMes = formato.find('m')
  if 0 <= iMes: nMes = formato.count('m')
  iAno = formato.find('y')
  if 0 <= iAno: nAno = formato.count('y')
  if 0 > iDia or 0 > iMes or 0 > iAno: return "'" + fecha + "'"
  else:
    return "'" + fecha[iAno:iAno+nAno] + '-' + fecha[iMes:iMes+nMes] + \
            '-' + fecha[iDia:iDia+nDia] + " 00:00:00'"
# FIN funcion fechaFormateada
def tipoNumber(linea):
  if '(' in linea: return ireplace(linea, 'NUMBER', 'DECIMAL')
  else: return ireplace(linea, 'NUMBER', 'DOUBLE')
# FIN funcion tipoNumber
def tipoVarchar2(linea):
  linea = ireplace(linea, 'VARCHAR2', 'VARCHAR')    
  if ' char' in linea.lower():
    iChar = linea.lower().index(' char')
    linea = linea[0:iChar] + linea[iChar+5:]
  return linea
# FIN funcion tipoVarchar2
def tipoDate(linea):
  return ireplace(linea, 'date', 'DATETIME')
# FIN funcion tipoDate

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
        if 4 <= len(sufijoEntrada) <= 6:
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
  salida  = []
  salida.append('SET GLOBAL max_allowed_packet=128*1024*1024;')
  nLineas = 1       # Numero de lineas
  nInsert = False   # No se ha encontrado un 'insert into'.
  crearTabla = False
  linUltValue = []
  for linea in f:
    linea = linea[0:linea.index('\n')]
    if 'set feed' in linea.lower(): continue  # set feedback
    if 'alter' in linea.lower() and \
      'triggers' in linea.lower(): continue   # set alter.*triggers
    if 'set define' in linea.lower(): continue   # set define
    if 'prompt' in linea.lower(): continue       # prompt
    if 'commit' in linea.lower(): continue    # commit
    if 'NOMINA' in linea: linea = linea.replace('NOMINA', 'nomina')
    if 'PERSONAL' in linea:
          linea = linea.replace('PERSONAL', 'personal')
    if 'RAC' in linea: linea = linea.replace('RAC', 'rac')
    if crearTabla:
      if ';' in linea: crearTabla = False
      if 'number' in linea.lower(): linea = tipoNumber(linea.rstrip())
      if 'date' in linea.lower(): linea = tipoDate(linea.rstrip())
      if 'varchar2' in linea.lower():
        linea = tipoVarchar2(linea.rstrip())
    if 'create table' in linea.lower():
      linea = linea.replace(sufijoEntrada, sufijoSalida)
      salida.append('DROP TABLE IF EXISTS ' + \
          linea[linea.lower().find('create')+13:] + ';')
      nLineas += 1
      linea = linea.replace('create table', 'CREATE TABLE')
      crearTabla = True
    if 'create unique index' in linea.lower():
      linea = linea.replace(sufijoEntrada, sufijoSalida)
      linea = linea.replace('create unique index', \
                            'CREATE UNIQUE INDEX')
    if 'insert into' in linea.lower():
      if not nInsert: # Mantener y cambiar primera linea con 'insert into'
        linea = linea.replace(sufijoEntrada, sufijoSalida)
        linea = linea.lower().replace('insert into', 'INSERT INTO')
        linea = linea[0:linea.index('(')] + 'VALUES'
        nInsert = True
      else:
        continue
    if nInsert and 'values ' in linea.lower():
      if 0 == linea.lower().find('values '):
        if 0 < linea.rfind(';'): linea = linea[0:linea.rfind(';')] + ','
        linea = ireplace(linea, 'values ', '')    
        if 'to_date' in linea.lower():
          iDate = linea.lower().index('to_date')
          iParentesisAbre = linea.index('(', iDate)
          iParentesisCierra = linea.index(')', iParentesisAbre)
          fechaConFormato = \
            linea[iParentesisAbre+1:iParentesisCierra].lstrip().rstrip()
          fecha = obtenerFecha(fechaConFormato)
          linea = linea[0:iDate] + fecha + \
                  linea[iParentesisCierra+1:].lstrip().rstrip()
      else:
        nInsert = False
        linUltValue.append(nLineas)
    nLineas += 1
    salida.append(linea)
  # FIN del for linea in f:
  if 0 >= len(linUltValue): linUltValue.append(nLineas - 1)
  for l in linUltValue:
    salida[l] = salida[l][0:salida[l].rfind(',')] + ';'
  for linea in salida:
    print(linea)
#  print(linUltValue)
#  print(nLineas)

  break

# FIN Principal