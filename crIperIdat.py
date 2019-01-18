#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
# Cedula=0:10; Nombre (corto=11:40/largo=11:83); Nucleo (42:44/83:85);
# Cuenta bancaria (45:65/86:106); formaDePago=107:108;
# generico=109:110; especifico=111:112; categoria=113:114;
# condicion=115:116; dedicacion=117:118; sueldo=119:129;
# fechaIngreso=130:138; sueldoIntegral=139:149; espacios=149-199.
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
PY3 = 3 == sys.version_info.major
if PY3:
  unicode = str
else:
  input = raw_input

from time import strftime
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
  droid = False

from lib import ES, Const as CO
from ipa import Iper, Idat

print(strftime("%Y/%m/%d %H:%M:%S"))
prefijoIper = ''
anoNomina = strftime("%Y")
mesNomina = strftime("%m")
if 1 < len(sys.argv):
  if sys.argv[1].isdigit() and 1 <= int(sys.argv[1]) <= 12:
    mesNomina = "%02d" % int(sys.argv[1])
  else:
    print("%sDebe suministrar un numero de mes valido:%s %s" % \
          (CO.ROJO, CO.FIN, sys.argv[1]))
    sys.exit()
  if 2 < len(sys.argv):
#    if 4 == len(sys.argv[2]) and sys.argv[2].isdigit():
    if 4 == len(sys.argv[2]) and sys.argv[2].isdigit() and \
       sys.argv[2] in (anoNomina, str(int(anoNomina)-1)):
      anoNomina = sys.argv[2]
      if 3 < len(sys.argv):
        prefijoIper = sys.argv[3]
    else:
      print("%sDebe suministrar un numero de año valido:%s %s" % \
            (CO.ROJO, CO.FIN, sys.argv[2]))
      sys.exit()
sufijoNomina = anoNomina + '_' + mesNomina
nombArchIper = prefijoIper + 'IPER' + anoNomina + mesNomina + '.TXT'
nombArchIdat = prefijoIper + 'IDAT' + anoNomina + mesNomina + '.TXT'

# Inicio principal
try:
  fIper = ES.abrir(nombArchIper, 'w')
  fIdat = ES.abrir(nombArchIdat, 'w')
except:
  fIper = False
  fIdat = False
Iper = Iper.poblarLista(sufijoNomina)
Idat = Idat.poblarLista(sufijoNomina)
if fIper and fIdat:
  for l in Iper:
    fIper.write("%08d %-70.70s  %2.2s %20.20s %1.1s %1.1s %1.1s %1.1s "
                "%1.1s %1.1s %010d %8.8s %010d\n" %
            (l['ci'], l['nmb'], l['nuc'], l['cta'], l['bco'], l['gen'],
              l['esp'], l['cat'], l['cond'], l['ded'],
              100*int(l['sdo']), l['fing'], 0))
  print('%d filas en %s.' % (len(Iper), nombArchIper))
  for l in Idat:
    fIdat.write("%010d %-3.3s%010d%010d\n" %
            (l['ci'], l['cct'], 100*int(l['vf']), 100*int(l['vv'])))
  print('%d filas en %s.' % (len(Idat), nombArchIdat))
else:
  print("%sNombre de archivo de salida%s '%s'/'%s' %serrado.%s" % \
        (CO.ROJO, CO.FIN, nombArchIper, nombArchIdat, CO.ROJO, CO.FIN))
  if not bMovil:
    n = 0    
    for l in Iper:
      print(l)
      n += 1
      if 10 <= n: break
    n = 0    
    for l in Idat:
      print(l)
      n += 1
      if 10 <= n: break
  sys.exit()
print(strftime("%Y/%m/%d %H:%M:%S"))
# FIN Principal