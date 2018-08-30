#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
from time import localtime, strftime
from os import listdir
from os.path import isfile, join, basename
import fnmatch

try:
  from lib import DIR, bMovil
except:
  DIR = './'
  bMovil = False
if bMovil:
  try:
    import androidhelper as android
  except:
    import android
  droid = android.Android()
else:
  droid = None

from ipa import BBanesco as BB
from ipa import BMercantil as BM
from ipa import BVenezuela as BV
from lib import ES, Const as CO, General as FG

sHoy     = strftime("%Y%m%d", localtime())
sHoyAno  = strftime("%Y", localtime())
sHoyMes  = strftime("%m", localtime())
sHoyDia  = strftime("%d", localtime())
sRif     = 'J306192298'
sEmpresa = 'IPASPUDO'

if bMovil:
	def cargarNombres(nombArch='MERCANTIL*.TXT'):
		rutaDatos = DIR

		lFiles = [f for f in listdir(rutaDatos) if isfile(join(rutaDatos, f)) and
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
		indice = ES.entradaConLista(droid, 'ARCHIVOS ENCONTRADOS', "Seleccione "
                                                            "nombre", lFiles)
		if None == indice or 0 > indice: return None
		return(lFiles[indice])
	# FIN funcion buscarArchivo
def prepara(nbrArchBanco):
  global sBanco

  try:
    sNbrArch = nbrArchBanco[0:nbrArchBanco.find('.')]
  except:
    sNbrArch = nbrArchBanco
  try:
    (sNbrBanco, sFecha) = sNbrArch.split('_', 1)
  except:
    sNbrBanco = sNbrArch
    sFecha    = sHoy
  bMerc = bMProv = bBan = bVzla = False
  sBanco = 'MERCANTILF'
  if 0 == sNbrBanco.find(sBanco, 0, len(sBanco)): bMerc = True
  else:
    bMerc = False
    sBanco = 'MERCANTILP'
    if 0 == sNbrBanco.find(sBanco, 0, len(sBanco)): bMProv = True
    else:
      bMProv = False
      sBanco = 'BANESCO'
      if 0 == sNbrBanco.find(sBanco, 0, len(sBanco)): bBan = True
      else:
        bBan = False
        if 0 == sNbrBanco.find('GLOBAL', 0, len(sBanco)):
          bVzla = True
          sBanco = 'VENEZUELA'
        else:
          bVzla = False
          print("%sNombre de archivo pasado como parametro no cumple con "
                    "los nombres de archivos esperados.%s" %
               (CO.ROJO, CO.FIN))
          sys.exit()
  return sFecha, bMerc, bMProv, bBan, bVzla
# FIN funcion prepara
def calcTotal(lista, nLnCtrl, sLnDet, iCI, iCC, iNac, sTPag, iMto, iNbr):
  global sCed

  lTot = (0, 0.00)
  nLn  = nLnCtrl
  st   = ''
  for l in lista:
    nLn += 1
    try:
      if sLnDet != l[0]:
        raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna"
                          "de la fila " + str(nLn) + ", no tiene un '" +
                          sLnDet + "', tiene: '" + l[0] + "'.")
      elif not l[iCI].isdigit():	# iCI es el indice de la cedula, definido anteriormente.
         raise ValueError(CO.ROJO + "Error:" + CO.FIN + " en el campo de la"
                          "cedula de identidad del socio en la fila: " +
                          str(nLn) + ", contiene: " + l[iCI])
      elif not l[iCC].isdigit():	# iCC es el indice del codigo cuenta socio, definido anteriormente.
         raise ValueError(CO.ROJO + "Error:" + CO.FIN + " en el campo del"
                          "codigo de cuenta (2) del socio en la fila: " +
                          str(nLn) + ", contiene: " + l[iCC])
      if bMerc or bBan:
        if l[iNac] not in ('J', 'G', 'V', 'E', 'P'):
          raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La segunda columna"
                            "de la fila " + str(nLn) + ", no contiene 'J', 'G'"
                            ", 'V', 'E' o 'P', contiene: " + l[1])
      if bMerc or bMProv:
        if l[3] not in ('1', '3'):
          raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La forma de pago"
                            "en columna 18 en la fila " + str(nLn) + 
                            ", no contiene '1' o '3', contiene: " + l[3])
        elif '000000000000' != l[4]:
          raise ValueError(CO.ROJO + "Error:" + CO.FIN + " En columna 19 de"
                            "la fila " + str(nLn) + " deberia ser "
                            "'000000000000', pero tiene '" + l[4] + "'")
        elif sTPag != l[9]:
          raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Tipo de pago en"
                            "columna 114 en la fila " + str(nLn) +
                            ", deberia ser '" + sTPag + "' (Prestamo caja de"
                            "ahorros o Pago a proveedores), pero contiene: " +
                            l[9])
        elif '000' != l[10]:
          raise ValueError(CO.ROJO + "Error:" + CO.FIN + " En la columna 124"
                            "en la fila " + str(nLn) + ", deberia ser '000'"
                            ", pero contiene: '" + l[10] + "'")
        elif '000000000000000' != l[12]:
          if bMerc: raise ValueError(CO.ROJO + "Error:" + CO.FIN + " En la"
                                      "columna 187 en la fila " + str(nLn) +
                                      ", deberia ser '000000000000000', pero"
                                      "contiene: '" + l[12] + "'")
  
      lTot = (lTot[0]+1, lTot[1]+l[iMto])	# iMto es el indice del monto, definido anteriormente.
      if '' != sCed:
        try: bCINoEncontrada
        except NameError: bCINoEncontrada = True
        if sCed.lstrip('0') == l[iCI].lstrip('0'):
          st = "%sCedula de identidad:%s %s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL,
                (FG.formateaNumero(sCed) if FG.formateaNumero(sCed) else sCed),
                                                                        CO.FIN)
          st = "%sNombre:%s %s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL, l[iNbr],
                                                                      CO.FIN)
          st = "%sCuenta:%s %s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL,
                  [iCC][0:4]+'-'+l[iCC][4:8]+'-'+l[iCC][8:10]+'-'+l[iCC][10:],
                                                                      CO.FIN)
          st = "%sMonto:%s %s%s%s" % (CO.CYAN, CO.FIN, CO.AZUL,
                (FG.formateaNumero(l[iMto], 2) if FG.formateaNumero(l[iMto], 2)
                 else str(l[iMto])), CO.FIN)
          bCINoEncontrada = False
    except ValueError as er:
      print(er)
      sys.exit()
    except Exception as er:
      print(str(nLn) + ': ')
      print(l)
      print(er)
      sys.exit()
# FIN for
  if '' != sCed and bCINoEncontrada:
    st = "%sLa cedula de identidad:%s %s%s%s no fue encontrada." % (CO.ROJO,
            CO.FIN, CO.AZUL,
            (FG.formateaNumero(sCed) if FG.formateaNumero(sCed) else sCed),
            CO.FIN)
  return lTot, st
# FIN funcion calcTotal
def cargarFilas(lTot, nroReg, iNoReg1, iNoReg2, fMtoTot, iMtoTot1, iMtoTot2,
                sNumLote, sRif, sFechaValor, sCodCta):
  global bMerc, bMProv, bBan, bVzla

  st = ''
  if (bMerc or bMProv or bBan) and int(nroReg) != lTot[0]:
    st += ("%sError:%s El numero de registros de la primera(Mercantil)/"
            "ultima(Banesco) fila no concuerda con el numero de registros "
            "detalle.\n") % (CO.ROJO, CO.FIN)
    st += ("%sValor entre columnas %s y %s "
            "del primer/ultimo registro:%s %s%s%s.\n") % (CO.AZUL,
            str(iNoReg1+1), str(iNoReg2), CO.FIN, CO.ROJO, nroReg, CO.FIN)
    st += "%sNumero total de registros de detalle:%s %s%d%s.\n" % (CO.AZUL,
                                            CO.FIN, CO.ROJO, lTot[0], CO.FIN)
  if 0.005 < abs(fMtoTot - lTot[1]):
    st += ("%sError:%s El monto total de la primera fila no concuerda con la "
              "suma del monto total de depositos.\n") % (CO.ROJO, CO.FIN)
    st += "Valor entre columnas " + str(iMtoTot1) + " y " + str(iMtoTot2) + \
            " del primer registro: " + \
           (FG.formateaNumero(fMtoTot, 2) if FG.formateaNumero(fMtoTot, 2) 
            else str(fMtoTot)) + '.\n'
    st += "Monto total de depositos en registros de detalle: " + \
            (FG.formateaNumero(lTot[1], 2) if FG.formateaNumero(lTot[1], 2) 
             else str(lTot[1])) + '.\n'
  if bMerc or bMProv or bBan: st += "%sNumero de lote:%s %s%s%s\n" % (CO.AZUL,
                                            CO.FIN, CO.CYAN, sNumLote, CO.FIN)
  if bMerc or bMProv or bBan: st += "%sRif:%s %s%s%s\n" % (CO.AZUL, CO.FIN,
                                      CO.CYAN, sRif[0:1]+'-'+sRif[1:], CO.FIN)
  if bMerc or bMProv or bBan: st += "%sFecha valor:%s %s%s%s\n" % (CO.AZUL,
                                    CO.FIN, CO.CYAN, sFechaValor[6:] + '/' +\
                                    sFechaValor[4:6] + '/' +sFechaValor[0:4],
                                    CO.FIN)
  elif bVzla: st += "%sFecha valor:%s %s%s%s\n" % (CO.AZUL, CO.FIN, CO.CYAN,
                                                          sFechaValor, CO.FIN)
  st += "%sCodigo de cuenta bancaria:%s %s%s%s.\n" % (CO.AZUL, CO.FIN, CO.CYAN,
      sCodCta[0:4]+'-'+sCodCta[4:8]+'-'+sCodCta[8:10]+'-'+sCodCta[10:], CO.FIN)
  st += "%sSe deposita a %d socios, la cantidad de %s bolivares.%s\n" % \
        (CO.VERDE, lTot[0],
         (FG.formateaNumero(lTot[1], 2) if FG.formateaNumero(lTot[1], 2) 
          else lTot[1]), CO.FIN)
  return st
# FIN funcion cargarFilas

# Inicio principal
sCed = ''
if bMovil:
  lFiles = cargarNombres('[BGM][ALE][NOR][EBC][SA][CLN]*.[Tt][Xx][Tt]')
  if not lFiles: sys.exit()
else:
  if 1 < len(sys.argv):
    nbrArchBancoCompleto = sys.argv[1]
    nbrArchBanco = basename(nbrArchBancoCompleto)
    if 2 < len(sys.argv) and sys.argv[2].isdigit():
      sCed = sys.argv[2]
  else:
    print("%sNo paso el nombre del archivo como parametro.%s" % (CO.ROJO,
                                                                      CO.FIN))
    sys.exit()
while True:
  if bMovil:
    nbrArchBanco = buscarArchivo(lFiles)
    if None == nbrArchBanco: break
    f = ES.abrir(nbrArchBanco, 'r')
    iCed = ES.entradaNumero(droid, "Cedula de identidad",
                                        "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = ''
    else: sCed = str(iCed)
  else:
    try: f = open(nbrArchBancoCompleto, 'r')
    except:
      print("%sEl archivo%s '%s' %sno existe.%s" % (CO.ROJO, CO.FIN,
                                      nbrArchBancoCompleto, CO.ROJO, CO.FIN))
      break

  (sFecha, bMerc, bMProv, bBan, bVzla) = prepara(nbrArchBanco)

  if bMerc or bMProv:
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) =\
                                        BM.mercantil(bMerc, f, sFecha, sRif)
    nLnCtrl = 1; iNoReg1 = 59; iNoReg2 = 67; iMtoTot1 = 67; iMtoTot2 = 84
    iNac = 1; iCI = 2; iNbr = 11; iCC = 6; iMto = 7; sLnDet = '2'
    sCodCta = BM.sCodCta

  elif bBan:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) =\
                                  BB.banesco(f, sFecha, sRif, sEmpresa, sBanco)
    nLnCtrl = 3; iMtoTot1 = 67; iMtoTot2 = 84
    iNac = 3; iCI = 4; iNbr = 5; iCC = 2; iMto = 1; sLnDet = '03'
    iNoReg1 = 29; iNoReg2 = 32
    sCodCta = BB.sCodCta

  elif bVzla:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) =\
                                    BV.vzla(f, sFecha, sRif, sEmpresa, sBanco)
    nLnCtrl = 1; iMtoTot1 = 71; iMtoTot2 = 84
    iNac = 0; iCI = 5; iNbr = 4; iCC = 1; iMto = 2; sLnDet = '1'
    iNoReg1 = 0; iNoReg2 = 0
    sCodCta = BV.sCodCta

  f.close()

  (lTot, stc) = \
          calcTotal(lista, nLnCtrl, sLnDet, iCI, iCC, iNac, sTPag, iMto, iNbr)
  st = cargarFilas(lTot, nroReg, iNoReg1, iNoReg2, fMtoTot, iMtoTot1, iMtoTot2,
                    sNumLote, sRif, sFechaValor, sCodCta)
  st += stc

  if bMovil:
    ES.imprime(st.rstrip(' \t\n\r'))
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer',
                                ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Programa