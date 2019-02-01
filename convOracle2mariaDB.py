#!/usr/bin/python3
#-*- coding:UTF-8 -*-
#qpy:3
#qpy:console
#from __future__ import print_function # Para usar 'print' de version 3.
import sys
# unicode desaparece en ver 3 y se convierte en str.
# Ver: https://blog.teamtreehouse.com/python-2-vs-python-3
# Tambien: https://nbviewer.jupyter.org/github/rasbt/python_reference/blob/master/tutorials/key_differences_between_python_2_and_3.ipynb
if 3 == sys.version_info.major:
  unicode = str
from time import time, localtime, strftime, sleep
print(strftime("%Y/%m/%d %H:%M:%S"))
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
  droid = False
  from os.path import abspath, basename

from lib import ES, Const as CO

crearControlPersonal = """
DROP TABLE IF EXISTS controlpersonal;
CREATE TABLE controlpersonal
(
  FECHA             VARCHAR(8),
  LISTOMOVIMIENTO   VARCHAR(1),
  QUINCENA          VARCHAR(1),
  NUMSEM            VARCHAR(1),
  PROCESO           VARCHAR(2),
  ACT_GENERAL       VARCHAR(1),
  ACT_ISLR          VARCHAR(1),
  ACT_HISTORICO     VARCHAR(1),
  PERMISO           VARCHAR(1),
  CEDULA_RAC        DECIMAL(9,0),
  DESCRIPCION       VARCHAR(60),
  NOMBRE_TABLAS     VARCHAR(15)
)
;
"""
valoresControlPersonal = [
  '',                # FECHA
  '0',               # LISTOMOVIMIENTO
  '3',               # QUINCENA
  '4',               # NUMSEM
  '50',              # PROCESO
  '0',               # ACT_GENERAL
  '0',               # ACT_ISLR
  '0',               # ACT_HISTORICO
  '0',               # PERMISO
  '999000399',       # CEDULA_RAC
  'NOMINA ',         # DESCRIPCION
  '_1016'            # NOMBRE_TABLAS
]

import calendar   # calendar.mdays[mm]: numero de dias del mes 'mm'.
def numeroDiaSemana(ano, mes, diaSemana = calendar.MONDAY): # 0: lunes
  return len([1 for i in calendar.monthcalendar(ano, mes) \
              if i[diaSemana] != 0])
# FIN funcion numeroDiaSemana
def numeroLunes(ano, mes):
  return numeroDiaSemana(ano, mes, calendar.MONDAY) # 0:lunes, ...
# FIN funcion numeroLunes
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
  if 0 <= iDia and 0 <= iMes and 0 <= iAno:
    fecha = fecha[iAno:iAno+nAno] + '-' + fecha[iMes:iMes+nMes] + \
            '-' + fecha[iDia:iDia+nDia]
  return "CAST('" + fecha + "' AS DATETIME)"
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
        prefijoNombArch = sys.argv[3]   # nomina_, personal_ o rac_.
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

if bMovil:
  nombArchEnt = buscarArchivo(lFiles)
  if None == nombArchEnt: exit
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
  sys.exit()
#print("%sNombre de archivos, entrada:%s '%s'%s, salida:%s '%s'" % \
#      (CO.AMARI, CO.FIN, nombArchEntCompleto, CO.AMARI, CO.FIN, \
#        nombArchSalCompleto))
bControlPersonal = False
salida  = []
salida.append('SET GLOBAL max_allowed_packet=128*1024*1024;')
nLineas = 1       # Numero de lineas
nInsert = False   # No se ha encontrado un 'insert into'.
crearTabla = False
linUltValue = []
restar = 0        # Restar lineas sumadas con anticipacion.
for linea in f:
  linea = linea.rstrip('\n\r ')
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
    linea = ireplace(linea, '_ipaspudo', '')
    salida.append('DROP TABLE IF EXISTS ' + \
        linea[linea.lower().find('create')+13:] + ';')
    nLineas += 1
    restar += 1
    linea = ireplace(linea, 'create table', 'CREATE TABLE')
    bControlPersonal = 'controlpersonal' in linea
    crearTabla = True
  if 'create unique index' in linea.lower():
    linea = linea.replace(sufijoEntrada, sufijoSalida)
    linea = ireplace(linea, '_ipaspudo', '')
    linea = ireplace(linea, 'create unique index', \
                          'CREATE UNIQUE INDEX')
  if 'insert into' in linea.lower():
    if not nInsert: # Mantener y cambiar primera linea con 'insert into'
      linea = linea.replace(sufijoEntrada, sufijoSalida)
      linea = ireplace(linea, '_ipaspudo', '')
      linea = ireplace(linea, 'insert into', 'INSERT INTO')
      linea = linea[0:linea.index('(')] + 'VALUES'
      nInsert = True
      nLineas += 1    # El primer 'insert' por el continue
      restar += 1
      salida.append(linea)
    continue
  if nInsert:
    if 0 == linea.lower().find('values '):
      if 0 < linea.rfind(';'): linea = linea[0:linea.rfind(';')] + ','
      linea = ireplace(linea, 'values ', '')
      while 'to_date' in linea.lower():
        iDate = linea.lower().index('to_date')
        iParentesisAbre = linea.index('(', iDate)
        iParentesisCierra = linea.index(')', iParentesisAbre)
        fechaConFormato = \
          linea[iParentesisAbre+1:iParentesisCierra].lstrip().rstrip()
        fecha = obtenerFecha(fechaConFormato)
        linea = linea[0:iDate] + fecha + \
                linea[iParentesisCierra+1:].lstrip().rstrip()
      # Eliminar la cadena '...chr(...)...'
      while 'chr(' in linea.lower():
        iChr = linea.lower().index('chr')
        lInd = linea.rfind("'", 0, iChr)
        rInd = linea.find("'", iChr, linea.find(',', iChr))
        if lInd < iChr and 0 < lInd and \
            rInd > iChr and len(linea)-1 > rInd:
          linea = linea[0:lInd] + linea[rInd+1:]
    else:
      nInsert = False
      linUltValue.append(nLineas-1-restar) # El primer ele de lista es 0.
  nLineas += 1
  restar = 0
  salida.append(linea)
# FIN del for linea in f:
if nInsert or 0 >= len(linUltValue): linUltValue.append(nLineas - 1)
for l in linUltValue:
  salida[l] = salida[l][0:salida[l].rfind(',')] + ';'

#for linea in salida:
#  print(linea.encode('utf-8'))
# Escribir archivo de salida.
try:
  f = ES.abrir(nombArchSalCompleto, 'w')
except:
  f = False
if f:
  for linea in salida:
    f.write(unicode(linea + '\n'))
else:
  if bMovil:
    print("%sNombre de archivo de salida%s '%s' %serrado.%s" % \
              (CO.ROJO, CO.FIN, nombArchSalCompleto, CO.ROJO, CO.FIN))
  else:
    for linea in salida:
      print(linea.encode('utf-8'))
  sys.exit()
#print(linUltValue)
#print(nLineas)
#print(linUltValue)

print(strftime("%Y/%m/%d %H:%M:%S"))
if not bControlPersonal and 'nomina_' == prefijoNombArch:
  ind = ES.entradaConLista(droid, 'Desea preparar la creación'
            ' de controlpersonal', 'Seleccione', ['Si', 'No'])
  if not ((1 <= ind) or (0 > ind) or (None == ind)):	# Se asegura de tener el indice correcto.
    ind = 0
  if 0 == ind:
    crearControlPersonal = crearControlPersonal.replace(\
                  'controlpersonal', 'controlpersonal_' + sufijoSalida)
    f.write(unicode(crearControlPersonal))
    f.write(unicode('INSERT INTO controlpersonal' + '_' + sufijoSalida \
                + ' VALUES\n'))
    partes = sufijoSalida.split('_')
    if 2 < len(partes): nExtra = partes[0].upper() + ' '
    else: nExtra = ''
    ano = partes[len(partes)-2]
    mes = partes[len(partes)-1]
    valoresControlPersonal[0] = str(calendar.mdays[int(mes)]) + mes + ano
    valoresControlPersonal[3] = str(numeroLunes(int(ano), int(mes)))
    valoresControlPersonal[10] += nExtra + CO.meses[int(mes)] + ' ' + ano
    valoresInsert = '('
    for valor in valoresControlPersonal:
      valoresInsert += "'" + valor + "', "
    valoresInsert = valoresInsert.rstrip(', ') + ');\n'
    f.write(unicode(valoresInsert))
    print('Se preparó la creación de controlpersonal_' + sufijoSalida)
  print(strftime("%Y/%m/%d %H:%M:%S"))
# FIN Principal