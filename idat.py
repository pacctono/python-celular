#!/usr/bin/python
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
import re

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

from lib import ES, Const as CO, General as FG
from ipa import Conceptos as CC

from lib import MySQL
bMySQL = MySQL.bMySQL
oMySQL = MySQL.cMySQL()

patron = re.compile(r"\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile(r"\d{1,3}")	# Expresion regular: 1 o mas dec (\d+) y tres dec al final (\d{3}).

if bMovil:
  def cargarNombres(nombArch='IDAT*.TXT'):
    rutaDatos = DIR

    lFiles = [f for f in listdir(rutaDatos) if isfile(join(rutaDatos, f)) and \
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
def poblarDicc(lidat, dConc):
  dicc = {}
  dicc['AHO']  = (0, 0.00, 0.00, 0.00)
  dConc['AHO'] = {'des':'AHORROS'}
  dicc['PR0']  = (0, 0.00, 0.00, 0.00)
  dConc['PR0'] = {'des':'PRESTAMOS x COMPRO'}
  dicc['PR1']  = (0, 0.00, 0.00, 0.00)
  dConc['PR1'] = {'des':'PRESTAMOS x COD Sinca'}
  dicc['PRE']  = (0, 0.00, 0.00, 0.00)
  dConc['PRE'] = {'des':'PRESTAMOS'}
  dicc['OTR']  = (0, 0.00, 0.00, 0.00)
  dConc['OTR'] = {'des':'OTROS CONCEPTOS'}
  dicc['TOT']  = (0, 0.00, 0.00, 0.00)
  dConc['TOT'] = {'des':'TOTAL GENERAL'}
  for l in lidat:
    try:
#    if not dicc.has_key(l[1]): dicc[l[1]] = (0, 0.00, 0.00, 0.00)
      if l[1] not in dicc: dicc[l[1]] = (0, 0.00, 0.00, 0.00)
      dicc[l[1]] = (dicc[l[1]][0]+1, dicc[l[1]][1]+l[2],
                                  dicc[l[1]][2]+l[3], dicc[l[1]][3]+l[2]+l[3])
      dicc['TOT'] = (dicc['TOT'][0]+1, dicc['TOT'][1]+l[2],
                                dicc['TOT'][2]+l[3], dicc['TOT'][3]+l[2]+l[3])
      if l[1] in ('511', '562'):	# Ahorro patronal y ahorro personal
         dicc['AHO'] = (dicc['AHO'][0]+1, dicc['AHO'][1]+l[2],
                                dicc['AHO'][2]+l[3], dicc['AHO'][3]+l[2]+l[3])
      if dConc.get(l[1], {'com':''})['com'] and \
         dConc.get(l[1], {'com':''})['com'].isdigit() and \
         '94' == dConc.get(l[1], {'com':''})['com']:
         dicc['PR0'] = (dicc['PR0'][0]+1, dicc['PR0'][1]+l[2],
                                dicc['PR0'][2]+l[3], dicc['PR0'][3]+l[2]+l[3])
      if dConc.get(l[1], {'nus':''})['nus'] and \
         dConc.get(l[1], {'nus':''})['nus'].isdigit():
         dicc['PR1'] = (dicc['PR1'][0]+1, dicc['PR1'][1]+l[2],
                                dicc['PR1'][2]+l[3], dicc['PR1'][3]+l[2]+l[3])
      if l[1] not in ('511','561', '562', '563', '570'):
         dicc['PRE'] = (dicc['PRE'][0]+1, dicc['PRE'][1]+l[2],
                                dicc['PRE'][2]+l[3], dicc['PRE'][3]+l[2]+l[3])
      if l[1] in ('561', '563', '570'):	# Cuota mensual, ServiFun y Fondo.
         dicc['OTR'] = (dicc['OTR'][0]+1, dicc['OTR'][1]+l[2],
                                dicc['OTR'][2]+l[3], dicc['OTR'][3]+l[2]+l[3])
    except:
      print(l)
      print(dConc[l[1]])
      print(dicc[l[1]])
      sys.exit()
  return dicc, dConc
# FIN funcion poblarDicc
def mostrarConceptos(dicc, dConc):
  lconc = []
  i = 0
  iMax = '000'
  for ld in dicc.items():
  	lconc.insert(i, ld[0])
  	if ld[0].isdigit() and ld[0] > iMax: iMax = ld[0]	# Concepto con el maximo valor, para saber donde subrayar.
  	i += 1
  lconc.sort()
  bImpar  = True
  st = "%s%s%3s %-20.20s %6.6s %15.15s %15.15s %15.15s %6.6s%s\n" % \
  		(CO.SUBRAYADO, CO.AMARI, 'CLV', 'DESCRIPCION', '#SOCI', 'VALOR FIJO',
                                'VALOR VARIABLE', 'TOTALES', 'PORCEN', CO.FIN)
  for v in lconc:
     if not ((0.00 == dicc[v][1]) and (0.00 == dicc[v][2]) and \
                                                        (0.00 == dicc[v][3])):
       if 'AHO' == v and dicc['AHO'][3] == dicc['TOT'][3]: continue
       if v.isdigit():
         if iMax > v: subrayar = ''
         else: subrayar = CO.SUBRAYADO
       else: subrayar = ''
       if ('TOT' == v): sColor = CO.VERDE
       elif v in ('AHO', 'OTR', 'PRE', 'PR0', 'PR1'): sColor = CO.PURPURA
       else: sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
       fPorc = 100.00*dicc[v][3]/dicc['TOT'][3]
       st += "%s%s%3s %-20.20s %6.6s %15.15s %15.15s %15.15s %6.6s%s\n" %\
  				(subrayar, sColor, v, dConc.get(v,
            {'des':'NO TENGO DESCRIPCION'})['des'],
  				  FG.formateaNumero(dicc[v][0]),
            FG.formateaNumero(dicc[v][1], 2), 
  				  FG.formateaNumero(dicc[v][2], 2),
            FG.formateaNumero(dicc[v][3], 2),
  				  FG.formateaNumero(fPorc, 2), CO.FIN)
  return st
# FIN funcion mostrarConceptos

# Inicio principal
dConc = CC.creaDicConceptos()
sCed = ''
if bMovil:
  lFiles = cargarNombres('[Ii][Dd][Aa][Tt]*.[Tt][Xx][Tt]')
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
    f = ES.abrir(nombArch, 'r')
    iCed = ES.entradaNumero(droid, "Cedula de identidad",
                                        "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = ''
    else: sCed = str(iCed)
  else:
    try:
      f = open(nombArchCompleto, 'r')
    except:
      f = False
  if not f:
    print("%sNombre de archivo%s '%s' %serrado.%s" % (CO.ROJO, CO.FIN,
                                            nombArchCompleto, CO.ROJO, CO.FIN))
    break

  try:
    lista = [(linea.rstrip()[0:8], linea.rstrip()[9:12],
              float(linea.rstrip()[12:22])/100,
              float(linea.rstrip()[22:])/100) for linea in f]
  except:
    nL = 0
    f.seek(0, 0)
    for linea in f:
      if not (linea.rstrip()[0:8].isdigit()) or \
        not (linea.rstrip()[9:12].isdigit()) or \
        not (linea.rstrip()[12:22].isdigit()) or \
        not (linea.rstrip()[22:].isdigit()):
        print("%sLinea %d con caracteres extra#os: %s%s" % (CO.ROJO, nL, 
                                                      linea.rstrip(), CO.FIN))
        print("%sCI:%s; CLV:%s; MtoFijo:%s; MtoVar:%s%s" % (CO.ROJO, 
                          linea.rstrip()[0:8], linea.rstrip()[9:12], 
                          linea.rstrip()[12:22], linea.rstrip()[22:], CO.FIN))
        sys.exit()
      nL += 1
# Fin del 'else', del 'for' y del 'except'.
  f.close()

  dicc, dConc = poblarDicc(lista, dConc)
  st = mostrarConceptos(dicc, dConc)

  if '' != sCed:
    bCINoEncontrada = True
    for l in lista:
      if sCed.lstrip('0') == l[0].lstrip('0'):
        if bCINoEncontrada: st += "\n%sCI:%s %s%s%s" % (CO.CYAN, CO.FIN,
                                  CO.AZUL, FG.formateaNumero(sCed), CO.FIN)
        st += "\n%sCLV:%s %s%s-%-20.20s%s " % (CO.CYAN, CO.FIN, CO.AZUL, l[1],
              dConc.get(l[1], {'des':'NO TENGO DESCRIPCION'})['des'], CO.FIN)
        st += "%sFijo:%s %s%s%s; Var:%s %s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL,
                      FG.formateaNumero(l[2], 2), CO.CYAN, CO.FIN, CO.AZUL,
                      FG.formateaNumero(l[3], 2), CO.FIN)
        bCINoEncontrada = False
  if '' != sCed and bCINoEncontrada:
    st += "\n%sLa cedula de identidad:%s %s%s%s no fue encontrada.\n" % \
                (CO.ROJO, CO.FIN, CO.AZUL, FG.formateaNumero(sCed), CO.FIN)
  else: st += '\n'

  if bMovil:
    st += CO.NEGRITA + 'TOTALES EN ' + nombArch + ': ' + \
                        FG.formateaNumero(dicc['TOT'][0]) + ' regs; Bs. ' + \
		                    FG.formateaNumero(dicc['TOT'][3], 2) + CO.FIN
    ES.imprime(st.rstrip(' \t\n\r'))

    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer',
                                                    ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Principal