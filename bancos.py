#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
import re
from time import time, localtime, strftime
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

from lib import ES, Const
CO    = Const
ES    = ES
AMARI = CO.color.YELLOW	# Primer titulo. Identifica la fecha de actualizacion de los datos.
CYAN  = CO.color.CYAN		# Identificacion del socio.
AZUL  = CO.color.BLUE		# Identificacion de los datos.
VERDE = CO.color.GREEN	# Linea final (totales).
PURPURA = CO.color.PURPLE	# Linea final (total de prestamos).
NEGRITA = CO.color.BOLD	# Negrita
ROJO  = CO.color.RED		# Linea de error.
SUBRAYADO  = CO.color.UNDERLINE	# Subrayado
FIN   = CO.color.END

patron = re.compile("\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile("\d{1,3}")	# Expresion regular: 1 o mas dec (\d+) y tres dec al final (\d{3}).

sHoy     = strftime("%Y%m%d", localtime())
sHoyAno  = strftime("%Y", localtime())
sHoyMes  = strftime("%m", localtime())
sHoyDia  = strftime("%d", localtime())
sRif     = 'J306192298'
sEmpresa = 'IPASPUDO'

if bMovil:
	def cargarNombres(nombArch='MERCANTIL*.TXT'):
		rutaDatos = DIR

		lFiles = [f for f in listdir(rutaDatos) if isfile(join(rutaDatos, f)) and fnmatch.fnmatch(f, nombArch)]

		if not lFiles:
			ES.alerta(droid, nombArch, "No hubo coincidencias!")
			return None
		lFiles.sort()
		return lFiles
	# FIN funcion cargarNombres
	def buscarArchivo(lFiles):
		if None == lFiles or 1 > len(lFiles): return None
		if 1 == len(lFiles): return(lFiles[0])
		indice = ES.entradaConLista(droid, 'ARCHIVOS ENCONTRADOS', 'Seleccione nombre', lFiles)
		if None == indice or 0 > indice: return None
		return(lFiles[indice])
	# FIN funcion buscarArchivo
def prepara(nbrArchBanco):
  global sBanco

  try:
    (sNbrArch, sTipo) = nbrArchBanco.split('.', 1)
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
          print("%sNombre de archivo pasado como parametro no cumple con los nombres de archivos esperados.%s" %
               (ROJO, FIN))
          sys.exit()
  return sFecha, bMerc, bMProv, bBan, bVzla
# FIN funcion prepara
def mercantil(bMerc, f, sFecha, sCodCta):
  global sRif

# 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
  try:
    if bMerc:
      sNumLote = sFecha
      sFechaValor = sFecha[1:9]
      sHora = sFecha[9:]
    else:
      sFechaValor = sFecha
      sHora = ''
    ln = f.readline()
    ln1 = (ln[0:1], ln[1:13], ln[13:28], ln[28:33], ln[33:43], ln[43:44], ln[44:59], ln[59:67], float(ln[67:84])/100, ln[84:92], ln[92:112], ln[112:119], ln[139:])	# El ultimo campo tiene 261 caracteres (todos zeros).
    if '1' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la primera fila no tiene un '1', pero contiene: '" + ln1[0] + "'.")
    elif 'BAMRVECA' != ln1[1].strip():
      raise ValueError(ROJO + "Error:" + FIN + " identifcacion del banco en 2da columna de 1ra fila errada, deberia ser 'BAMRVECA', pero contiene: '" + ln1[1] + "'.")
    if bMerc:
      if sNumLote != ln1[2]:
        raise ValueError(ROJO + "Error:" + FIN + " Numero de lote errado, en col 14 de 1ra fila, deberia ser : '" + sNumLote + "', pero tiene '" + ln1[2] + "'")
      sTPro = 'NOMIN'
      sTPag = '0000000414'
    else:		# Proveedores
      sNumLote = ln1[2]
      sTPro = 'PROVE'
      sTPag = '0000000062'
    if sTPro != ln1[3]:
      raise ValueError(ROJO + "Error:" + FIN + " Tipo de producto en columna 29 de 1ra fila errada, deberia ser '" + sTPro + "'")
    elif sTPag != ln1[4]:
      raise ValueError(ROJO + "Error:" + FIN + " Tipo de pago en columna 34 de 1ra fila errada, deberia ser '" + sTPag + "' (Prestamo caja de ahorros o Pago proveedores)")
    elif sRif[0:1] != ln1[5] or sRif[1:] != ln1[6].lstrip('0'):
      raise ValueError(ROJO + "Error:" + FIN + " Rif en columna 44 de 1ra fila errada, deberia ser '" + sRif + "'.")
    elif not ln1[7].isdigit():
      raise ValueError(ROJO + "Error:" + FIN + " Numero de registros en columna 60 de 1ra fila errada, deberia ser numerico, pero es: '" + ln1[7] + "'")
    elif sFechaValor != ln1[9]:
      raise ValueError(ROJO + "Error:" + FIN + " Fecha valor errada, en col 85 de 1ra fila, deberia ser : '" + sFechaValor + "', pero tiene '" + ln1[9] + "'")
    elif sCodCta != ln1[10]:
      raise ValueError(ROJO + "Error:" + FIN + " Codigo cuenta errada, en col 93 de 1ra fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[10] + "'.")
    elif '0000000' != ln1[11]:
      raise ValueError(ROJO + "Error:" + FIN + " En columna 113 de 1ra fila errada, deberia ser '0000000', pero tiene '" + ln1[11] + "'")
    nroReg = int(ln1[7])
    fMtoTot = ln1[8]
    lista = [(ln[0:1], ln[1:2], ln[2:17], ln[17:18], ln[18:30], ln[30:60], ln[60:80], float(ln[80:97])/100, ln[97:113], ln[113:123], ln[123:126], ln[126:186], ln[186:201], ln[201:251], ln[285:365], ln[365:]) for ln in f]	# El ultimo campo tiene 35 car's.
    return lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion mercantil
def banesco(f, sFecha, sCodCta):
  global sRif, sEmpresa, sBanco

# 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
  try:
    sFechaValor = sFecha
    ln = f.readline()
    ln1 = (ln[0:3], ln[3:18], ln[18:])	# El ultimo campo tiene 16 caracteres (maximo).
    if 'HDR' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la primera fila no tiene un 'HDR', pero contiene: '" + ln1[0] + "'.")
    elif sBanco != ln1[1].rstrip():
      raise ValueError(ROJO + "Error:" + FIN + " La palabra '" + sBanco + "' deberia estar en la columna 4 de la primera fila, pero contiene: '" + ln1[1] + "'.")
    elif 34 < len(ln):
      raise ValueError(ROJO + "Error:" + FIN + " La longitud de la primera fila no deberia ser mayor de 34, pero es: '" + str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:37], ln[37:38], ln[40:48], ln[75:83], ln[83:89])
    if '01' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la segunda fila no tiene un '01', pero contiene: '" + ln1[0] + "'.")
    elif '9' != ln1[2]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 38 de la segunda fila no tiene un '9', pero contiene: '" + ln1[2] + "'.")
    elif not ln1[3].isdigit():
      raise ValueError(ROJO + "Error:" + FIN + " La columna 41 de la segunda fila deberia contener 8 digitos, pero contiene: '" + ln1[3] + "'.")
    else: sNumLote = ln1[3]
    if sFechaValor != ln1[4]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 76 de la segunda fila deberia contener la fecha valor: '" + sFechaValor + "', pero contiene: '" + ln1[4] + "'.")
    elif not ln1[5].isdigit():
      raise ValueError(ROJO + "Error:" + FIN + " La columna 84 de la segunda fila deberia contener 6 digitos (hora), pero contiene: '" + ln1[5] + "'.")
    else: sHora = ln1[5]
    if 91 < len(ln):
      raise ValueError(ROJO + "Error:" + FIN + " La longitud de la segunda fila no deberia ser mayor de 91, pero es: '" + str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:10], ln[32:42], ln[49:57], float(ln[84:99])/100, ln[103:123], ln[137:144], ln[148:156])
    if '02' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la tercera fila no tiene un '02', pero contiene: '" + ln1[0] + "'.")
    elif sFechaValor != ln1[1] or sFechaValor != ln1[7]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 3 o 149 de la tercera fila deberia contener la fecha valor: '" + sFechaValor + "', pero contiene: '" + ln1[1] + "' o '" + ln1[8] + "'.")
    elif sRif != ln1[2]:
      raise ValueError(ROJO + "Error:" + FIN + " Rif en columna 2 de tercera fila errada, deberia ser '" + sRif + "'")
    elif sEmpresa != ln1[3]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 50 de la tercera fila deberia contener '" + sEmpresa + "', pero contiene: '" + ln1[3] + "'.")
    elif sCodCta != ln1[5]:
      raise ValueError(ROJO + "Error:" + FIN + " Codigo cuenta errada, en col 104 de la tercera fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[5] + "'.")
    elif sBanco != ln1[6].rstrip():
      raise ValueError(ROJO + "Error:" + FIN + " La palabra '" + sBanco + "' deberia estar en la columna 138 de la tercera fila, pero contiene: '" + ln1[6] + "'.")
    if 157 < len(ln):
      raise ValueError(ROJO + "Error:" + FIN + " La longitud de la tercera fila no deberia ser mayor de 157, pero es: '" + str(len(ln)) + "'.")
    fMtoTot = ln1[4]
# Linea de detalle y ultima
    sLnDet = '03'
    lista = []
    for ln in f:
      if sLnDet == ln[0:2]:
# Cualquiera de las tres (3) lineas funcionan.
#        lista.append((ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:]))	# El ultimo campo tiene 215 car's.
#        lista += [(ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:])]	# El ultimo campo tiene 215 car's.
        lista[len(lista):] = [(ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:])]	# El ultimo campo tiene 215 car's.
      elif '06' == ln[0:2]: ln1 = (ln[0:2], ln[16:17], ln[29:32], float(ln[32:47])/100)
      else: raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la fila  de detalle tiene un identificador errado, contiene: '" + ln[0] + "'.")
    if '06' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la tercera fila no tiene un '02', pero contiene: '" + ln1[0] + "'.")
    elif '1' != ln1[1]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 17 de la ultima fila no tiene un '1', pero contiene: '" + ln1[1] + "'.")
    elif not ln1[2].isdigit():
      raise ValueError(ROJO + "Error:" + FIN + " La columna 30 de la ultima fila deberia contener digitos, pero contiene: '" + ln1[2] + "'.")
    else:
      nroReg = int(ln1[2])
    if fMtoTot != ln1[3]:
      raise ValueError(ROJO + "Error:" + FIN + " La columna 33 de la ultima fila deberia contener el mismo valor del monto total de la tercera fila: " + str(fMtoTot) + ", pero contiene: '" + ln1[2] + "'.")
    elif 48 < len(ln):
      raise ValueError(ROJO + "Error:" + FIN + " La longitud de la ultima fila no deberia ser mayor de 48, pero es: '" + str(len(ln)) + "'.")
    return lista, 0, sNumLote, sFechaValor, sHora, nroReg, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion banesco
def vzla(f, sFecha, sCodCta):
  global sRif, sEmpresa, sBanco

  try:
    sDia = sFecha[6:]
    sMes = sFecha[4:6]
    sAno = sFecha[2:4]
    ln = f.readline()
    ln1 = (ln[0:1], ln[1:9], ln[9:41], ln[41:61], ln[61:63], ln[63:65], ln[66:68],
            ln[69:71], float(ln[71:84])/100, ln[84:])	# El ultimo campo tiene 6 caracteres.
    if 'H' != ln1[0]:
      raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la primera fila no tiene una 'H', pero contiene: '" +
                        ln1[0] + "'.")
    elif sEmpresa != ln1[1].strip():
      raise ValueError(ROJO + "Error:" + FIN + " La 2da columna de 1ra fila deberia contener '" +
                        sEmpresa + "'; pero contiene: '" + ln1[1] + "'.")
    elif sCodCta != ln1[3]:
      raise ValueError(ROJO + "Error:" + FIN + " Codigo cuenta errada, en col 42 de 1ra fila, deberia ser : '" +
                        sCodCta + "', pero tiene '" + ln1[3] + "'.")
    elif sDia != ln1[5]:
      print(ROJO + "Error:" + FIN + " dia errado, en col 64 de 1ra fila, deberia ser : '" +
                        sDia + "', pero tiene '" + ln1[5] + "'.")
    elif sMes != ln1[6]:
      print(ROJO + "Error:" + FIN + " Mes errado, en col 67 de 1ra fila, deberia ser : '" +
                        sMes + "', pero tiene '" + ln1[6] + "'.")
    elif sAno != ln1[7]:
      print(ROJO + "Error:" + FIN + " a#o errado, en col 70 de 1ra fila, deberia ser : '" +
                        sAno + "', pero tiene '" + ln1[7] + "'.")
    sFechaValor = ln[63:71]
    fMtoTot = ln1[8]
    lista = [(ln[0:1], ln[1:21], float(ln[21:32])/100, ln[32:36], ln[36:76], ln[76:86], ln[86:])
              for ln in f]	# El ultimo campo tiene 8 car's.
    return lista, 0, '', sFechaValor, '', 0, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion vzla
def colorLinea(bImpar=True, sColor=AZUL, sOtroColor=None):
  global bMovil

  if bMovil: return ES.colorLinea(bImpar, sColor, sOtroColor)
  if bImpar: sColor = CYAN
  return sColor, not bImpar
# FIN funcion colorLinea
def calcTotal(lista, nLnCtrl, sLnDet, iCI, iCC, iNac, sTPag, iMto, iNbr):
  global sCed

  lTot = (0, 0.00)
  nLn  = nLnCtrl
  st   = ''
  for l in lista:
    nLn += 1
    try:
      if sLnDet != l[0]:
        raise ValueError(ROJO + "Error:" + FIN + " La primera columna de la fila " + str(nLn) + ", no tiene un '" + sLnDet + "', tiene: '" + l[0] + "'.")
      elif not l[iCI].isdigit():	# iCI es el indice de la cedula, definido anteriormente.
         raise ValueError(ROJO + "Error:" + FIN + " en el campo de la cedula de identidad del socio en la fila: " + str(nLn) + ", contiene: " + l[iCI])
      elif not l[iCC].isdigit():	# iCC es el indice del codigo cuenta socio, definido anteriormente.
         raise ValueError(ROJO + "Error:" + FIN + " en el campo del codigo de cuenta (2) del socio en la fila: " + str(nLn) + ", contiene: " + l[iCC])
      if bMerc or bBan:
        if l[iNac] not in ('J', 'G', 'V', 'E', 'P'):
          raise ValueError(ROJO + "Error:" + FIN + " La segunda columna de la fila " + str(nLn) + ", no contiene 'J', 'G', 'V', 'E' o 'P', contiene: " + l[1])
      if bMerc or bMProv:
        if l[3] not in ('1', '3'):
          raise ValueError(ROJO + "Error:" + FIN + " La forma de pago en columna 18 en la fila " + str(nLn) + ", no contiene '1' o '3', contiene: " + l[3])
        elif '000000000000' != l[4]:
          raise ValueError(ROJO + "Error:" + FIN + " En columna 19 de la fila " + str(nLn) + " deberia ser '000000000000', pero tiene '" + l[4] + "'")
        elif sTPag != l[9]:
          raise ValueError(ROJO + "Error:" + FIN + " Tipo de pago en columna 114 en la fila " + str(nLn) + ", deberia ser '" + sTPag + "' (Prestamo caja de ahorros o Pago a proveedores), pero contiene: " + l[9])
        elif '000' != l[10]:
          raise ValueError(ROJO + "Error:" + FIN + " En la columna 124 en la fila " + str(nLn) + ", deberia ser '000', pero contiene: '" + l[10] + "'")
        elif '000000000000000' != l[12]:
          if bMerc: raise ValueError(ROJO + "Error:" + FIN + " En la columna 187 en la fila " + str(nLn) + ", deberia ser '000000000000000', pero contiene: '" + l[12] + "'")
  
      lTot = (lTot[0]+1, lTot[1]+l[iMto])	# iMto es el indice del monto, definido anteriormente.
      if '' != sCed:
        try: bCINoEncontrada
        except NameError: bCINoEncontrada = True
        if sCed.lstrip('0') == l[iCI].lstrip('0'):
          st = "%sCedula de identidad:%s %s%s%s" % (CYAN, FIN, AZUL, ES.fgFormateaNumero(sCed), FIN)
          st = "%sNombre:%s %s%s%s" % (CYAN, FIN, AZUL, l[iNbr], FIN)
          st = "%sCuenta:%s %s%s%s" % (CYAN, FIN, AZUL, l[iCC][0:4]+'-'+l[iCC][4:8]+'-'+l[iCC][8:10]+'-'+l[iCC][10:], FIN)
          st = "%sMonto:%s %s%s%s" % (CYAN, FIN, AZUL, ES.fgFormateaNumero(l[iMto], 2), FIN)
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
    st = "%sLa cedula de identidad:%s %s%s%s no fue encontrada." % (ROJO, FIN, AZUL, ES.fgFormateaNumero(sCed), FIN)
  return lTot, st
# FIN funcion calcTotal
def cargarFilas(lTot, nroReg, iNoReg1, iNoReg2, fMtoTot, iMtoTot1, iMtoTot2, sNumLote, sRif, sFechaValor, sCodCta):
  global bMerc, bMProv, bBan, bVzla

  st = ''
  if (bMerc or bMProv or bBan) and int(nroReg) != lTot[0]:
    st += "%sError:%s El numero de registros de la primera(Mercantil)/ultima(Banesco) fila no concuerda con el numero de registros detalle.\n" % (ROJO, FIN)
    st += "%sValor entre columnas " + str(iNoReg1+1) + " y " + str(iNoReg2) + " del primer/ultimo registro:%s %s%s%s.\n" % (AZUL, FIN, ROJO, nroReg, FIN)
    st += "%sNumero total de registros de detalle:%s %s%d%s.\n" % (AZUL, FIN, ROJO, lTot[0], FIN)
  if 0.005 < abs(fMtoTot - lTot[1]):
    st += "%sError:%s El monto total de la primera fila no concuerda con la suma del monto total de depositos.\n" % (ROJO, FIN)
    st += "Valor entre columnas " + str(iMtoTot1) + " y " + str(iMtoTot2) + " del primer registro: " + ES.fgFormateaNumero(fMtoTot, 2) + '.\n'
    st += "Monto total de depositos en registros de detalle: " + ES.fgFormateaNumero(lTot[1], 2) + '.\n'
  if bMerc or bMProv or bBan: st += "%sNumero de lote:%s %s%s%s\n" % (AZUL, FIN, CYAN, sNumLote, FIN)
  if bMerc or bMProv or bBan: st += "%sRif:%s %s%s%s\n" % (AZUL, FIN, CYAN, sRif[0:1]+'-'+sRif[1:], FIN)
  if bMerc or bMProv or bBan: st += "%sFecha valor:%s %s%s%s\n" % (AZUL, FIN, CYAN, sFechaValor[6:] + '/' +\
                                                     sFechaValor[4:6] + '/' + sFechaValor[0:4], FIN)
  elif bVzla: st += "%sFecha valor:%s %s%s%s\n" % (AZUL, FIN, CYAN, sFechaValor, FIN)
  st += "%sCodigo de cuenta bancaria:%s %s%s%s.\n" % (AZUL, FIN, CYAN, sCodCta[0:4]+'-'+sCodCta[4:8]+'-'+sCodCta[8:10]+'-'+sCodCta[10:], FIN)
  st += "%sSe deposita a %d socios, la cantidad de %s bolivares.%s\n" % \
        (VERDE, lTot[0], ES.fgFormateaNumero(lTot[1], 2), FIN)
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
    print("%sNo paso el nombre del archivo como parametro.%s" % (ROJO, FIN))
    sys.exit()
while True:
  if bMovil:
    nbrArchBanco = buscarArchivo(lFiles)
    if None == nbrArchBanco: break
    f = ES.abrir(nbrArchBanco, 'r')
    iCed = ES.entradaNumero(droid, "Cedula de identidad", "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = ''
    else: sCed = str(iCed)
  else:
    try: f = open(nbrArchBancoCompleto, 'r')
    except:
      print("%sEl archivo%s '%s' %sno existe.%s" % (ROJO, FIN, nbrArchBancoCompleto, ROJO, FIN))
      break

  (sFecha, bMerc, bMProv, bBan, bVzla) = prepara(nbrArchBanco)

  if bMerc or bMProv:
    sCodCta = '01050068121068204451'
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) = mercantil(bMerc, f, sFecha, sCodCta)
    nLnCtrl = 1; iNoReg1 = 59; iNoReg2 = 67; iMtoTot1 = 67; iMtoTot2 = 84
    iNac = 1; iCI = 2; iNbr = 11; iCC = 6; iMto = 7; sLnDet = '2'

  elif bBan:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    sCodCta = '01340055500553285809'
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) = banesco(f, sFecha, sCodCta)
    nLnCtrl = 3; iMtoTot1 = 67; iMtoTot2 = 84
    iNac = 3; iCI = 4; iNbr = 5; iCC = 2; iMto = 1; sLnDet = '03'; iNoReg1 = 29; iNoReg2 = 32

  elif bVzla:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    sCodCta = '01020672330000020336'
    (lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot) = vzla(f, sFecha, sCodCta)
    nLnCtrl = 1; iMtoTot1 = 71; iMtoTot2 = 84
    iNac = 0; iCI = 5; iNbr = 4; iCC = 1; iMto = 2; sLnDet = '1'; iNoReg1 = 0; iNoReg2 = 0
#  else:
#    lista = [(ln.rstrip()[9:12], float(ln.rstrip()[12:20])/100, float(ln.rstrip()[20:])/100) for ln in f]
  f.close()

  (lTot, stc) = calcTotal(lista, nLnCtrl, sLnDet, iCI, iCC, iNac, sTPag, iMto, iNbr)
  st = cargarFilas(lTot, nroReg, iNoReg1, iNoReg2, fMtoTot, iMtoTot1, iMtoTot2, sNumLote, sRif, sFechaValor, sCodCta)
  st += stc

  if bMovil:
    ES.imprime(st.rstrip(' \t\n\r'))
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer', ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Programa
