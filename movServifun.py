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

patron = re.compile(r"\d+(\.\d+)?$")	# Valida un numero entero o punto float.
pat = re.compile(r"\d{1,3}")	# Expresion regular: Entre 1 y 3 dec.

if bMovil:
	def cargarNombres(nombArch='IPAS*.TXT'):
		rutaDatos = DIR

		lFiles = [f for f in listdir(rutaDatos) if isfile(join(rutaDatos, f)) and\
                                                fnmatch.fnmatch(f, nombArch)]

		if not lFiles:
			ES.alerta(droid, nombArch, "No hubo coincidencias!")
			return None
		lFiles.sort()
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
def poblarDicc(lidat, dConc, sConc = '563'):
  dicc = {} # Tres elementos: # de socios, suma de saldos, suma de cuotas.
  dicc['AHO']  = (0, 0.00, 0.00)
  dConc['AHO'] = {'des':'AHORROS'}
  dicc['CRE']  = (0, 0.00, 0.00)
  dConc['CRE'] = {'des':'CONCEPTOS CREADOS'}
  dicc['DMD']  = (0, 0.00, 0.00)
  dConc['DMD'] = {'des':'CONCEPTOS MODIFICADOS'}
  dicc['ELI']  = (0, 0.00, 0.00)
  dConc['ELI'] = {'des':'CONCEPTOS ELIMINADOS'}
  for l in lidat:
    if '' != sConc and sConc != l[2]: continue
    try:
      sLlave = l[2]+'-'+l[0]+'-'+l[5]+'-'+l[6]  # Concepto; 6 o 7; Tipo; SC/CF
      if sLlave not in dicc: dicc[sLlave] = (0, 0.00, 0.00)
      dicc[sLlave] = (dicc[sLlave][0]+1, dicc[sLlave][1]+l[3],
                                                        dicc[sLlave][2]+l[4])
      if l[2] in ('511', '562'):		# Ahorro patronal y ahorro personal
        if '3' != l[5]: dicc['AHO'] = (dicc['AHO'][0]+1, dicc['AHO'][1]+l[3],
                                                        dicc['AHO'][2]+l[4])
      if '1' == l[5]: dicc['CRE'] = (dicc['CRE'][0]+1, dicc['CRE'][1]+l[3],
                                                        dicc['CRE'][2]+l[4])
      if '2' == l[5]: dicc['DMD'] = (dicc['DMD'][0]+1, dicc['DMD'][1]+l[3],
                                                        dicc['DMD'][2]+l[4])
      if '3' == l[5]: dicc['ELI'] = (dicc['ELI'][0]+1, dicc['ELI'][1]+l[3],
                                                        dicc['ELI'][2]+l[4])
    except:
      print(l)
      print(dConc[l[2]])
      print(dicc[l[1]])
      sys.exit()

  return dicc, dConc
# FIN funcion poblarDicc
def mostrarConceptos(dicc, dConc):

  lconc = []
  i = 0
  sMax = '000-0-0-0'
  for ld in dicc.items():		# el metodo items(), devuelve una lista de dicc's (llave, valor) tupla pares
    lconc.insert(i, ld[0])
    if ld[0][0:3].isdigit() and ld[0] > sMax: sMax = ld[0]	# Concepto con el maximo valor, para saber donde subrayar.
    i += 1
  lconc.sort()
  bImpar  = True
  st = "%s%s%9s %-20.20s %6.6s %15.15s %15.15s %6.6s%s\n" % \
      (CO.SUBRAYADO, CO.AMARI, 'CLAVE', 'DESCRIPCION', '#MOVI', '     Saldo',
                                            '         Cuota', 'PORCEN', CO.FIN)
  for v in lconc:
    if not ((0.00 == dicc[v][1]) and (0.00 == dicc[v][2])) or ('3' == v[6:7]):
       if v[0:3].isdigit() and v[4:5].isdigit() and v[6:7].isdigit() and \
            v[8:].isdigit():
         if sMax == v: subrayar = CO.SUBRAYADO
         else: subrayar = ''
       else: subrayar = ''
       if ('AHO' == v): sColor = CO.PURPURA
       elif ('ELI' == v): sColor = CO.ROJO
       else: sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
       sConc = v[0:3]
       if '3' == v[6:7]: sObs = CO.ROJO + 'Eli'
       elif '2' == v[6:7]: sObs = 'Mod'
       elif '1' == v[6:7]: sObs = 'Cre'
       else: sObs = ''
       st += "%s%s%9s %-20.20s %6.6s %15.15s %15.15s %s%s\n" % (subrayar,
          sColor, v, dConc.get(sConc, {'des':'NO TENGO DESCRIPCION'})['des'],
          FG.formateaNumero(dicc[v][0]), FG.formateaNumero(dicc[v][1], 2),
          FG.formateaNumero(dicc[v][2], 2), sObs, CO.FIN)

  return st
# FIN funcion mostrarConceptos

# Inicio principal
dConc = CC.creaDicConceptos()
if bMovil:
  lFiles = cargarNombres('[Ii][Pp][Aa][Ss]0*.[Tt][Xx][Tt]')
  if not lFiles: sys.exit()
else:
  if 1 < len(sys.argv):
    mes = sys.argv[1]
    if not mes.isdigit() or 1 > int(mes) or 12 < int(mes):
      print("%sEl primer prametro deberia ser el mes y esta errado.%s" %
            (CO.ROJO, CO.FIN))
      sys.exit()
    if 2 < len(sys.argv):
      nombArchivo = sys.argv[2]
    else:
      nombArchivo = 'IPAS'
    if 3 < len(sys.argv) and sys.argv[2].isdigit():
      ano = sys.argv[3]
    else:
      ano = '2018'
  else:
    print("%sEjecutar: movServifun mm ipas aaaa%s" % (CO.ROJO, CO.FIN))
    sys.exit()
  nombArch = basename(nombArchivo)

while True:
  if bMovil:
    nombArch = buscarArchivo(lFiles)
    if None == nombArch: break
    f = ES.abrir(nombArch, 'r')
    iCed = ES.entradaNumero(droid, "Cedula o Concepto"
                                        "Cedula del socio o Concepto", sCed)
    if None == iCed or 0 == iCed: sCed = ''
    else: sCed = str(iCed)
  else:
    sNuc = '01'
    nombArchivoCompleto = nombArchivo + sNuc + ano + mes + '.TXT'
    try:
      f = open(nombArchivoCompleto, 'r')
    except:
      f = False
  if not f:
    print("%sNombre de archivo%s '%s' %serrado.%s" % (CO.ROJO, CO.FIN,
                                        nombArchivoCompleto, CO.ROJO, CO.FIN))
    break

# 0:Mov (6:retroact o 7:fijo); 1:CI; 2:Conc; 3:Saldo; 4:Cuota;
# 5:Ctrl (1:Crea, 2:Mod, 3:eli); 6:Tipo (1:Saldo-cuota, 2:Cuota fija).
  lista = [(linea.rstrip()[0:1], linea.rstrip()[1:9], linea.rstrip()[10:13],
            float(linea.rstrip()[26:38])/100, float(linea.rstrip()[38:49])/100,
            linea.rstrip()[52:53], linea.rstrip()[76:77]) for linea in f]
  if f: f.close()

  dicc, dConc = poblarDicc(lista, dConc)
  st = mostrarConceptos(dicc, dConc)

  if bMovil:
    ES.imprime(st.rstrip(' \t\n\r'))
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer',
                                                    ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Principal
