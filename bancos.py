#!/usr/bin/python
import sys
import re
import os
from time import time, localtime, strftime
try:
  import MySQLdb
  bMySQL = True
except:
  bMySQL = False

DIR = '../'
class color:
	PURPLE   = '\033[95m'
	HEADER   = '\033[95m'
	CYAN     = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE     = '\033[94m'
	OKBLUE   = '\033[94m'
	GREEN    = '\033[92m'
	OKGREEN  = '\033[92m'
	YELLOW   = '\033[93m'
	WARNING  = '\033[93m'
	RED      = '\033[91m'
	BOLD     = '\033[1m'
	UNDERLINE = '\033[4m'
	END      = '\033[0m'
	FAIL     = '\033[91m'
AMARI = color.YELLOW	# Primer titulo.
CYAN  = color.CYAN	# Identificacion del socio.
AZUL  = color.BLUE	# Identificacion de los datos.
PURPURA = color.PURPLE	# Linea final (total de prestamos).
VERDE = color.GREEN	# Linea final (totales).
ROJO  = color.RED	# Linea de error.
FIN   = color.END

patron = re.compile("\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile("\d{1,3}")	# Expresion regular: 1 o mas dec (\d+) y tres dec al final (\d{3}).

def colorLinea(bImpar=True, sColor=AZUL):
  if bImpar: sColor = CYAN
  return sColor, not bImpar
# funcion colorLinea
def fgFormateaNumero(sCad, dec=0):
  if (not isinstance(sCad, str) and not isinstance(sCad, float) and not isinstance(sCad, int)) and \
     ((None != dec) and not isinstance(dec, int)): return None

  if isinstance(sCad, float) or isinstance(sCad, int): sCad = str(sCad)
#  print('fn entrada: ', sCad)
  try:
    fCad = float(sCad)
    fCad = round(fCad, dec)
    signo = ''
    if 0 > fCad:
      signo = '-'
      fCad  = -fCad
    sCad = str(fCad)
  except:
    return None

  x = sCad.split('.');		# Divide el numero en parte entera (x[0]) y parte decimal (x[1]).
  x0 = x[0];				# x1 es la parte entera
  if 1 < len(x):
    x2 = x[1]
  if 0 < dec: x2 = ',' + x2.ljust(dec, '0')
  else: x2 = ''
  dec = dec + 1			# Crece en 1 al agregar la coma "," decimal.
  if dec < len(x2): x2 = x2[0:dec]

  x1 = ''
  x = re.findall(pat, x0)
  for i in range(0, len(x)):
    if 4 <= len(x0):
      x1 = '.' + x0[-3:] + x1
      x0 = x0[0:-3]
    else:
      x1 = x0 + x1
#  print('fn salida: ', signo + x1 + x2)

  return signo + x1 + x2	#parte entera (x1) con '.' intercalado cada 3 dec + parte decimal con ',' adelante.
# funcion fgFormateaNumero(sCad, dec)

# Inicio principal
sHoy = strftime("%Y%m%d", localtime())
nbrArchBanco = sys.argv[1]
f = open(nbrArchBanco, 'r')
try:
  ln = f.readline()
  if 'MERCANTILF' == nbrArchBanco[0:10]:	# 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
    sNumLote = nbrArchBanco[11:26]
    sFecha = nbrArchBanco[12:20]
    sCodCta = '01050068121068204451'
    nLnCtrl = 1
    ln1 = (ln[0:1], ln[1:13], ln[13:28], ln[28:33], ln[33:43], ln[43:44], ln[44:59], ln[59:67], float(ln[67:84])/100, ln[84:92], ln[92:112], ln[112:119], ln[139:])	# El ultimo campo tiene 261 caracteres (todos zeros).
    if '1' != ln1[0]:
      raise ValueError("Error: La primera columna de la primera fila no tiene un '1', pero contiene: '" + ln1[0] + "'.")
    elif 'BAMRVECA' != ln1[1].strip():
      raise ValueError("Error: identifcacion del banco en 2da columna de 1ra fila errada, deberia ser 'BAMRVECA', pero contiene: '" + ln1[1] + "'.")
    elif sNumLote != ln1[2]:
      raise ValueError("Error: Numero de lote errado, en col 14 de 1ra fila, deberia ser : '" + sNumLote + "', pero tiene '" + ln1[2] + "'")
    elif 'NOMIN' != ln1[3]:
      raise ValueError("Error: Tipo de producto en columna 29 de 1ra fila errada, deberia ser 'NOMIN'")
    elif '0000000414' != ln1[4]:
      raise ValueError("Error: Tipo de pago en columna 34 de 1ra fila errada, deberia ser '0000000414' (Prestamo caja de ahorros)")
    elif 'J' != ln1[5] or '306192298' != ln1[6].lstrip('0'):
      raise ValueError("Error: Rif en columna 44 de 1ra fila errada, deberia ser 'J306192298'")
    else: sRif = ln1[5] + '-' + ln1[6].lstrip('0')
    if not ln1[7].isdigit():
      raise ValueError("Error: Numero de registros en columna 60 de 1ra fila errada, deberia ser numerico, pero es: '" + ln1[7] + "'")
    elif sFecha != ln1[9]:
      raise ValueError("Error: Fecha valor errada, en col 85 de 1ra fila, deberia ser : '" + sFecha + "', pero tiene '" + ln1[9] + "'")
    elif sCodCta != ln1[10]:
      raise ValueError("Error: Codigo cuenta errada, en col 93 de 1ra fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[10] + "'.")
    elif '0000000' != ln1[11]:
      raise ValueError("Error: En columna 113 de 1ra fila errada, deberia ser '0000000', pero tiene '" + ln1[11] + "'")
    nroReg = int(ln1[7])
    iNoReg1 = 59
    iNoReg2 = 67
    fMtoTot = ln1[8]
    iMtoTot1 = 67
    iMtoTot2 = 84
    lista = [(ln[0:1], ln[1:2], ln[2:17], ln[17:18], ln[18:30], ln[30:60], ln[60:80], float(ln[80:97])/100, ln[97:113], ln[113:123], ln[123:126], ln[126:186], ln[186:201], ln[201:251], ln[285:365], ln[365:]) for ln in f]	# El ultimo campo tiene 35 car's.
    iNac = 1
    iCI = 2
    iCC = 6
    iMto = 7
    sLnDet = '2'
  elif 'BANESCO' == nbrArchBanco[0:7]:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    sFecha = nbrArchBanco[8:16]
    sCodCta = '01340055500553285809'
    nLnCtrl = 3
    ln1 = (ln[0:3], ln[3:18], ln[18:])	# El ultimo campo tiene 16 caracteres (maximo).
    if 'HDR' != ln1[0]:
      raise ValueError("Error: La primera columna de la primera fila no tiene un 'HDR', pero contiene: '" + ln1[0] + "'.")
    elif 'BANESCO' != ln1[1].rstrip():
      raise ValueError("Error: La palabra 'BANESCO' deberia estar en la columna 4 de la primera fila, pero contiene: '" + ln1[1] + "'.")
    elif 34 < len(ln):
      raise ValueError("Error: La longitud de la primera fila no deberia ser mayor de 34, pero es: '" + str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:37], ln[37:38], ln[40:48], ln[75:83], ln[83:89])
    if '01' != ln1[0]:
      raise ValueError("Error: La primera columna de la segunda fila no tiene un '01', pero contiene: '" + ln1[0] + "'.")
    elif '9' != ln1[2]:
      raise ValueError("Error: La columna 38 de la segunda fila no tiene un '9', pero contiene: '" + ln1[2] + "'.")
    elif not ln1[3].isdigit():
      raise ValueError("Error: La columna 41 de la segunda fila deberia contener 8 digitos, pero contiene: '" + ln1[3] + "'.")
    else: sNumLote = ln1[3]
    if sFecha != ln1[4]:
      raise ValueError("Error: La columna 76 de la segunda fila deberia contener la fecha valor: '" + sFecha + "', pero contiene: '" + ln1[4] + "'.")
    elif not ln1[5].isdigit():
      raise ValueError("Error: La columna 84 de la segunda fila deberia contener 6 digitos (hora), pero contiene: '" + ln1[5] + "'.")
    else: sHora = ln1[5]
    if 91 < len(ln):
      raise ValueError("Error: La longitud de la segunda fila no deberia ser mayor de 91, pero es: '" + str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:10], ln[32:42], ln[49:57], float(ln[84:99])/100, ln[103:123], ln[137:144], ln[148:156])
    if '02' != ln1[0]:
      raise ValueError("Error: La primera columna de la tercera fila no tiene un '02', pero contiene: '" + ln1[0] + "'.")
    elif sFecha != ln1[1] or sFecha != ln1[7]:
      raise ValueError("Error: La columna 3 o 149 de la tercera fila deberia contener la fecha valor: '" + sFecha + "', pero contiene: '" + ln1[1] + "' o '" + ln1[8] + "'.")
    elif 'J306192298' != ln1[2]:
      raise ValueError("Error: Rif en columna 2 de tercera fila errada, deberia ser 'J306192298'")
    else: sRif = ln1[2][0:1] + '-' + ln1[2][1:]
    if 'IPASPUDO' != ln1[3]:
      raise ValueError("Error: La columna 50 de la tercera fila deberia contener 'IPASPUDO', pero contiene: '" + ln1[3] + "'.")
    elif sCodCta != ln1[5]:
      raise ValueError("Error: Codigo cuenta errada, en col 104 de la tercera fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[5] + "'.")
    elif 'BANESCO' != ln1[6].rstrip():
      raise ValueError("Error: La palabra 'BANESCO' deberia estar en la columna 138 de la tercera fila, pero contiene: '" + ln1[6] + "'.")
    if 157 < len(ln):
      raise ValueError("Error: La longitud de la tercera fila no deberia ser mayor de 157, pero es: '" + str(len(ln)) + "'.")
    fMtoTot = ln1[4]
    iMtoTot1 = 67
    iMtoTot2 = 84
# Linea de detalle y ultima
    iNac = 3
    iCI = 4
    iCC = 2
    iMto = 1
    sLnDet = '03'
    index = 0
    lista = []
    for ln in f:
      if sLnDet == ln[0:2]:
# Cualquiera de las tres (3) lineas funcionan.
#        lista.append((ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:]))	# El ultimo campo tiene 215 car's.
#        lista += [(ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:])]	# El ultimo campo tiene 215 car's.
        lista[len(lista):] = [(ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:])]	# El ultimo campo tiene 215 car's.
        index += 1
      elif '06' == ln[0:2]: ln1 = (ln[0:2], ln[16:17], ln[29:32], float(ln[32:47])/100)
      else: raise ValueError("Error: La primera columna de la fila tiene un identificador errado, contiene: '" + ln[0] + "'.")
    if '06' != ln1[0]:
      raise ValueError("Error: La primera columna de la tercera fila no tiene un '02', pero contiene: '" + ln1[0] + "'.")
    elif '1' != ln1[1]:
      raise ValueError("Error: La columna 17 de la ultima fila no tiene un '1', pero contiene: '" + ln1[1] + "'.")
    elif not ln1[2].isdigit():
      raise ValueError("Error: La columna 30 de la ultima fila deberia contener digitos, pero contiene: '" + ln1[2] + "'.")
    else:
      nroReg = int(ln1[2])
      iNoReg1 = 29
      iNoReg2 = 32
    if fMtoTot != ln1[3]:
      raise ValueError("Error: La columna 33 de la ultima fila deberia contener el mismo valor del monto total de la tercera fila: " + str(fMtoTot) + ", pero contiene: '" + ln1[2] + "'.")
    elif 48 < len(ln):
      raise ValueError("Error: La longitud de la ultima fila no deberia ser mayor de 48, pero es: '" + str(len(ln)) + "'.")
  elif 'GLOBAL' == nbrArchBanco[0:6]:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    sDia = nbrArchBanco[13:15]
    sMes = nbrArchBanco[11:13]
    sAno = nbrArchBanco[9:11]
    sCodCta = '01020672330000020336'
    nLnCtrl = 1
    ln1 = (ln[0:1], ln[1:9], ln[9:41], ln[41:61], ln[61:63], ln[63:65], ln[66:68], ln[69:71], float(ln[71:84])/100, ln[84:])	# El ultimo campo tiene 6 caracteres.
    if 'H' != ln1[0]:
      raise ValueError("Error: La primera columna de la primera fila no tiene una 'H', pero contiene: '" + ln1[0] + "'.")
    elif 'IPASPUDO' != ln1[1].strip():
      raise ValueError("Error: La 2da columna de 1ra fila deberia contener 'IPASPUDO', pero contiene: '" + ln1[1] + "'.")
    elif sCodCta != ln1[3]:
      raise ValueError("Error: Codigo cuenta errada, en col 42 de 1ra fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[3] + "'.")
    elif sDia != ln1[5]:
      raise ValueError("Error: dia errado, en col 64 de 1ra fila, deberia ser : '" + sDia + "', pero tiene '" + ln1[5] + "'.")
    elif sMes != ln1[6]:
      raise ValueError("Error: Mes errado, en col 67 de 1ra fila, deberia ser : '" + sMes + "', pero tiene '" + ln1[6] + "'.")
    elif sAno != ln1[7]:
      raise ValueError("Error: a#o errado, en col 70 de 1ra fila, deberia ser : '" + sAno + "', pero tiene '" + ln1[7] + "'.")
    sFecha = ln[63:71]
    fMtoTot = ln1[8]
    iMtoTot1 = 71
    iMtoTot2 = 84
    lista = [(ln[0:1], ln[1:21], float(ln[21:32])/100, ln[32:36], ln[36:76], ln[76:86], ln[86:]) for ln in f]	# El ultimo campo tiene 8 car's.
    iCI = 5
    iCC = 1
    iMto = 2
    sLnDet = '1'
#  else:
#    lista = [(ln.rstrip()[9:12], float(ln.rstrip()[12:20])/100, float(ln.rstrip()[20:])/100) for ln in f]
except ValueError as er:
  print(er)
  sys.exit()
#except Exception as er:
#  print(er)
#  sys.exit()
f.close()

lTot = (0, 0.00)
nLn  = nLnCtrl
for l in lista:
  nLn += 1
  try:
    if sLnDet != l[0]:
      raise ValueError("Error: La primera columna de la fila " + str(nLn) + ", no tiene un '" + sLnDet + "', tiene: '" + l[0] + "'.")
    elif not l[iCI].isdigit():	# iCI es el indice de la cedula, definido anteriormente.
       raise ValueError("Error en el campo de la cedula de identidad del socio en la fila: " + str(nLn) + ", contiene: " + l[iCI])
    elif not l[iCC].isdigit():	# iCC es el indice del codigo cuenta socio, definido anteriormente.
       raise ValueError("Error en el campo del codigo de cuenta (2) del socio en la fila: " + str(nLn) + ", contiene: " + l[iCC])
    if 'MERCANTILF' == nbrArchBanco[0:10] or 'BANESCO' == nbrArchBanco[0:7]:
      if l[iNac] not in ('V', 'E', 'P'):
        raise ValueError("Error: La segunda columna de la fila " + str(nLn) + ", no contiene 'V', 'E' o 'P', contiene: " + l[1])
    if 'MERCANTILF' == nbrArchBanco[0:10]:
      if l[3] not in ('1', '3'):
        raise ValueError("Error: La forma de pago en columna 18 en la fila " + str(nLn) + ", no contiene '1' o '3', contiene: " + l[3])
      elif '000000000000' != l[4]:
        raise ValueError("Error: En columna 19 de la fila " + str(nLn) + " deberia ser '000000000000', pero tiene '" + l[4] + "'")
      elif '0000000414' != l[9]:
        raise ValueError("Error: Tipo de pago en columna 114 en la fila " + str(nLn) + ", deberia ser '0000000414' (Prestamo caja de ahorros), pero contiene: " + l[9])
      elif '000' != l[10]:
        raise ValueError("Error: Tipo de pago en columna 124 en la fila " + str(nLn) + ", deberia ser '000', pero contiene: " + l[10])
      elif '000000000000000' != l[12]:
        raise ValueError("Error: Tipo de pago en columna 124 en la fila " + str(nLn) + ", deberia ser '000000000000000', pero contiene: " + l[12])

    lTot = (lTot[0]+1, lTot[1]+l[iMto])	# iMto es el indice del monto, definido anteriormente.
  except ValueError as er:
    print(er)
    sys.exit()
  except Exception as er:
    print(str(nLn) + ': ')
    print(l)
    print(er)
    sys.exit()
# FIN for

#lTot = (0, 0.00)
if ('MERCANTILF' == nbrArchBanco[0:10] or 'BANESCO' == nbrArchBanco[0:7]) and int(nroReg) != lTot[0]:
  print("%sError:%s El numero de registros de la primera(Mercantil)/ultima(Banesco) fila no concuerda con el numero de registros detalle" % (ROJO, FIN))
  print("%sValor entre columnas " + str(iNoReg1+1) + " y " + str(iNoReg2) + " del primer/ultimo registro:%s %s%s%s" % (AZUL, FIN, ROJO, nroReg, FIN))
  print("%sNumero total de registros de detalle:%s %s%d%s" % (AZUL, FIN, ROJO, lTot[0], FIN))
if 0.005 < abs(fMtoTot - lTot[1]):
  print("%sError:%s El monto total de la primera fila no concuerda con la suma del monto total de depositos" % (ROJO, FIN))
  print("Valor entre columnas " + str(iMtoTot1) + " y " + str(iMtoTot2) + " del primer registro: " + fgFormateaNumero(fMtoTot, 2))
  print("Monto total de depossitos en registros de detalle: " + fgFormateaNumero(lTot[1], 2))
if 'MERCANTILF' == nbrArchBanco[0:10]: print("%sNumero de lote:%s %s%s%s" % (AZUL, FIN, CYAN, sNumLote, FIN))
if 'MERCANTILF' == nbrArchBanco[0:10]: print("%sRif:%s %s%s%s" % (AZUL, FIN, CYAN, sRif, FIN))
print("%sFecha valor:%s %s%s%s" % (AZUL, FIN, CYAN, sFecha, FIN))
print("%sCodigo de cuenta bancaria:%s %s%s%s" % (AZUL, FIN, CYAN, sCodCta, FIN))
print("%sSe deposita a %d socios, la cantidad de %s bolivares.%s" % \
      (VERDE, lTot[0], fgFormateaNumero(lTot[1], 2), FIN))

# FIN Programa
