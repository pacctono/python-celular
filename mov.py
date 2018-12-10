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
def poblarDicc(lidat, dConc, sConc = ''):
  if 3 != len(sConc): sConc = ''    # Mostrar solo un concepto especifico.
  dicc = {} # Tres elementos: # de socios, suma de saldos, suma de cuotas.
  dicc['AHO']  = (0, 0.00, 0.00)
  dConc['AHO'] = {'des':'AHORROS'}
  dicc['CRE']  = (0, 0.00, 0.00)
  dConc['CRE'] = {'des':'CONCEPTOS CREADOS'}
  dicc['DMD']  = (0, 0.00, 0.00)
  dConc['DMD'] = {'des':'CONCEPTOS MODIFICADOS'}
  dicc['ELI']  = (0, 0.00, 0.00)
  dConc['ELI'] = {'des':'CONCEPTOS ELIMINADOS'}
  dicc['OTR']  = (0, 0.00, 0.00)
  dConc['OTR'] = {'des':'561,563,570 sin Eli'}
  dicc['TOT']  = (0, 0.00, 0.00)
  dConc['TOT'] = {'des':'TOT GENERAL sin Eli'}
  for l in lidat:
    if '' != sConc and sConc != l[2]: continue
    try:
      sLlave = l[2]+'-'+l[0]+'-'+l[5]+'-'+l[6]  # Concepto; 6 o 7; Tipo; SC/CF
      if sLlave not in dicc: dicc[sLlave] = (0, 0.00, 0.00)
      dicc[sLlave] = (dicc[sLlave][0]+1, dicc[sLlave][1]+l[3],
                                                        dicc[sLlave][2]+l[4])
      if '3' != l[5]: dicc['TOT'] = (dicc['TOT'][0]+1, dicc['TOT'][1]+l[3],
                                                        dicc['TOT'][2]+l[4])
      if l[2] in ('511', '562'):		# Ahorro patronal y ahorro personal
        if '3' != l[5]: dicc['AHO'] = (dicc['AHO'][0]+1, dicc['AHO'][1]+l[3],
                                                        dicc['AHO'][2]+l[4])
      if '1' == l[5]: dicc['CRE'] = (dicc['CRE'][0]+1, dicc['CRE'][1]+l[3],
                                                        dicc['CRE'][2]+l[4])
      if '2' == l[5]: dicc['DMD'] = (dicc['DMD'][0]+1, dicc['DMD'][1]+l[3],
                                                        dicc['DMD'][2]+l[4])
      if '3' == l[5]: dicc['ELI'] = (dicc['ELI'][0]+1, dicc['ELI'][1]+l[3],
                                                        dicc['ELI'][2]+l[4])
      if l[2] in ('561', '563', '570'):	# Cuota mensual, ServiFun, Fondo Salud
        if '3' != l[5]: dicc['OTR'] = (dicc['OTR'][0]+1, dicc['OTR'][1]+l[3],
                                                        dicc['OTR'][2]+l[4])
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
       if ('TOT' == v): sColor = CO.VERDE
       elif ('AHO' == v): sColor = CO.PURPURA
       elif ('ELI' == v): sColor = CO.ROJO
       elif ('OTR' == v): sColor = CO.PURPURA
       else: sColor, bImpar = ES.colorLinea(bImpar, CO.AZUL, CO.CYAN)
       if 0 == dicc['TOT'][1]: fPorc = 0.00
       else: fPorc = 100.00*dicc[v][1]/dicc['TOT'][1]
       sConc = v[0:3]
       if '3' == v[6:7]: sObs = CO.ROJO + 'Eli'
       elif '2' == v[6:7]: sObs = 'Mod'
       elif '1' == v[6:7]: sObs = 'Cre'
       else: sObs = ''
       st += "%s%s%9s %-20.20s %6.6s %15.15s %15.15s %6.6s %s%s\n" % (subrayar,
          sColor, v, dConc.get(sConc, {'des':'NO TENGO DESCRIPCION'})['des'],
          FG.formateaNumero(dicc[v][0]), FG.formateaNumero(dicc[v][1], 2),
          FG.formateaNumero(dicc[v][2], 2), FG.formateaNumero(fPorc, 2),
          sObs, CO.FIN)

  return st
# FIN funcion mostrarConceptos

# Inicio principal
dConc = CC.creaDicConceptos()
sCed = ''
if bMovil:
  lFiles = cargarNombres('[Ii][Pp][Aa][Ss]0*.[Tt][Xx][Tt]')
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
    iCed = ES.entradaNumero(droid, "Cedula o Concepto"
                                        "Cedula del socio o Concepto", sCed)
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

# 0:Mov (6:retroact o 7:fijo); 1:CI; 2:Conc; 3:Saldo; 4:Cuota;
# 5:Ctrl (1:Crea, 2:Mod, 3:eli); 6:Tipo (1:Saldo-cuota, 2:Cuota fija).
  lista = [(linea.rstrip()[0:1], linea.rstrip()[1:9], linea.rstrip()[10:13],
            float(linea.rstrip()[26:38])/100, float(linea.rstrip()[38:49])/100,
            linea.rstrip()[52:53], linea.rstrip()[76:77]) for linea in f]
  if f: f.close()

  dicc, dConc = poblarDicc(lista, dConc, sCed)
  st = mostrarConceptos(dicc, dConc)

  if 4 > len(sCed): sCed = ''   # Solo se va a listar un concepto.
  if '' != sCed:
    bCINoEncontrada = True
    for l in lista:
      if sCed.lstrip('0') == l[1].lstrip('0'):
        if bCINoEncontrada: st += "\n%sCI:%s%s%s%s" % (CO.CYAN, CO.FIN,
                                    CO.AZUL, FG.formateaNumero(sCed), CO.FIN)
        st += "\n%sCLV:%s%s%s-%-20.20s%s " % (CO.CYAN, CO.FIN, CO.AZUL, l[2],
                dConc.get(l[2], {'des':'NO TENGO DESCRIPCION'})['des'], CO.FIN)
        st += "%sSdo:%s%s%s%s; Cta:%s%s%s%s" %\
              (CO.CYAN, CO.FIN, CO.AZUL, FG.formateaNumero(l[3], 2), CO.CYAN,
                        CO.FIN, CO.AZUL, FG.formateaNumero(l[4], 2), CO.FIN)
        st += "%s; Ct:%s%s%s%s; Tp:%s%s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL, l[5],
                                        CO.CYAN, CO.FIN, CO.AZUL, l[6], CO.FIN)
        bCINoEncontrada = False
  if '' != sCed and bCINoEncontrada:
    st += "\n%sLa cedula de identidad:%s %s%s%s no fue encontrada.\n" % \
                (CO.ROJO, CO.FIN, CO.AZUL, FG.formateaNumero(sCed), CO.FIN)
  else: st += '\n'

  if bMovil:
    ES.imprime(st.rstrip(' \t\n\r'))
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer',
                                                    ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Principal
