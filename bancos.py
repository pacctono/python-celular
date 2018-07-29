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

def abrir(aNb, modo='r', codigo = 'latin-1', bImprimir = False):
  'Abre para leer, el archivo cuyo nombre es el valor de aNb'
  global DIR
  aNb = DIR + aNb
  try:
#    f = open(aNb, mode=modo, encoding=codigo)
    f = open(aNb, mode=modo)
    if (bImprimir): print(aNb + " archivo abierto.")
    return f
  except:
    if (bImprimir):
      print(color.YELLOW + "ERROR ABRIENDO: " + color.END + aNb)
      print(color.YELLOW + "os.path.abspath(aNb): " + color.END + os.path.abspath(aNb))
    return False
# funcion abrir
def poblarDicConc(co, de, cm='', nu='', no='', au=''):
  return {'cod':co, 'des':de, 'com':cm, 'nus':nu, 'nom':no, 'aut':au}	# Codigo, desc,
		# com: 2 primeros digitos comprobante, nu: cod tabla_prestamo,
		# no: es concepto de nomina (S/N), au: automatico (S/N).
# funcion poblarDic
def creaDicConceptos():
  if not bMySQL:
    try:
#      f = abrir("conceptos.txt", bImprimir = True)
      f = abrir("conceptos.txt")
      if not f:
        print('Problemas para abrir el archivo\n')
        return {}
      dConc = {}
      for linea in f:
        try:
          k, v,  cm, nu, no, au = linea.rstrip().split(';')
          dConc[k] = poblarDicConc(k, v,  cm, nu, no, au)
        except:
          print('Problemas para leer el archivo\n')
          continue
      else: f.close()
      return dConc
    except:
      print('Problemas con el archivo\n')
      return {}
# Open database connection
  db = MySQLdb.connect("localhost","ipaspudo","qazwsxedc","ipaspudo" )
# prepare a cursor object using cursor() method
  cursor = db.cursor()
# Prepare SQL query to SELECT records from the database.
  sql = "SELECT codigo, descripcion, tx_comprobante, nu_sinca, id_nomina, id_automatico \
         FROM conceptos"
  try:
# Execute the SQL command
    cursor.execute(sql)
# Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    dConc = {}
    for row in results:
# Crear diccionari de conceptos.
      dConc[row[0]] = {
                       'cod':row[0],
                       'des':row[1],
                       'com':row[2],
                       'nus':row[3],
                       'nom':row[4],
                       'aut':row[5]
                      }
  except:
    print("Imposible crear diccionario de conceptos")
  return dConc
# disconnect from server
  db.close()
# funcion creaDicConceptos
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
dConc = creaDicConceptos()

sHoy = strftime("%Y%m%d", localtime())
nbrArchBanco = sys.argv[1]
f = open(nbrArchBanco, 'r')
try:
  ln = f.readline()
  if 'MERCANTILF' == nbrArchBanco[0:10]:	# 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
    sNumLote = nbrArchBanco[11:26]
    sFecha = nbrArchBanco[12:20]
    sCodCta = '01050068121068204451'
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
    elif 'J' != ln1[5] or '000000306192298' != ln1[6]:
      raise ValueError("Error: Rif en columna 44 de 1ra fila errada, deberia ser 'J000000306192298'")
    else: sRif = ln1[5] + '-' + ln1[6].lstrip('0')
    if not ln1[7].isdigit():
      raise ValueError("Error: Numero de registros en columna 60 de 1ra fila errada, deberia ser numerico, pero es: '" + ln1[7] + "'")
    elif sFecha != ln1[9]:
      raise ValueError("Error: Fecha valor errada, en col 85 de 1ra fila, deberia ser : '" + sFecha + "', pero tiene '" + ln1[9] + "'")
    elif sCodCta != ln1[10]:
      raise ValueError("Error: Codigo cuenta errada, en col 93 de 1ra fila, deberia ser : '" + sCodCta + "', pero tiene '" + ln1[10] + "'.")
    elif '0000000' != ln1[11]:
      raise ValueError("Error: En columna 113 de 1ra fila errada, deberia ser '0000000', pero tiene '" + ln1[11] + "'")
    nroReg = ln1[7]
    iNoReg1 = 59
    iNoReg2 = 67
    fMtoTot = ln1[8]
    iMtoTot1 = 67
    iMtoTot2 = 84
    lista = [(ln[0:1], ln[1:2], ln[2:17], ln[17:18], ln[18:30], ln[30:60], ln[60:80], float(ln[80:97])/100, ln[97:113], ln[113:123], ln[123:126], ln[126:186], ln[186:201], ln[201:251], ln[285:365], ln[365:]) for ln in f]	# El ultimo campo tiene 35 car's.
    iCI = 2
    iCC = 6
    iMto = 7
    sLnDet = '2'
  elif 'GLOBAL' == nbrArchBanco[0:6]:	# 42,20:CtaDebito; 72,13:MntTot. Detalle: 77,10:CI; 22,11:Monto; 2,20:CtaCliente
    sDia = nbrArchBanco[13:15]
    sMes = nbrArchBanco[11:13]
    sAno = nbrArchBanco[9:11]
    sCodCta = '01020672330000020336'
    ln1 = (ln[0:1], ln[1:9], ln[9:41], ln[41:61], ln[61:63], ln[63:65], ln[66:68], ln[69:71], float(ln[71:84])/100, ln[84:])	# El ultimo campo tiene 6 caracteres (todos zeros).
    if 'H' != ln1[0]:
      raise ValueError("Error: La primera columna de la primera fila no tiene una 'H', pero contiene: '" + ln1[0] + "'.")
    elif 'IPASPUDO' != ln1[1].strip():
      raise ValueError("Error: identifcacion del banco en 2da columna de 1ra fila errada, deberia ser 'IPASPUDO', pero contiene: '" + ln1[1] + "'.")
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
  else:
    lista = [(ln.rstrip()[9:12], float(ln.rstrip()[12:20])/100, float(ln.rstrip()[20:])/100) for ln in f]
except ValueError as er:
  print(er)
  sys.exit()
except Exception as er:
  print(er)
  sys.exit()
f.close()

lTot = (0, 0.00)
nLn  = 1
for l in lista:
  nLn += 1
  try:
    if sLnDet != l[0]:
      raise ValueError("Error: La primera columna de la fila " + str(nLn) + ", no tiene un '" + sLnDet + "', tiene: '" + l[0] + "'.")
    elif not l[iCI].isdigit():	# iCI es el indice de la cedula, definido anteriormente.
       raise ValueError("Error en el campo de la cedula de identidad del socio en la fila: " + str(nLn) + ", contiene: " + l[iCI])
    elif not l[iCC].isdigit():	# iCC es el indice del codigo cuenta socio, definido anteriormente.
       raise ValueError("Error en el campo del codigo de cuenta (2) del socio en la fila: " + str(nLn) + ", contiene: " + l[iCC])
    if 'MERCANTILF' == nbrArchBanco[0:10]:	# 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
      if l[1] not in ('V', 'E', 'P'):
        raise ValueError("Error: La segunda columna de la fila " + str(nLn) + ", no contiene 'V', 'E' o 'P', contiene: " + l[1])
      elif l[3] not in ('1', '3'):
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
if 'MERCANTILF' == nbrArchBanco[0:10] and int(ln1[7]) != lTot[0]:
  print("%sError:%s El numero de registros de la primera fila no concuerda con el numero de registros detalle" % (ROJO, FIN))
  print("%sValor entre columnas " + str(iNoReg1+1) + " y " + str(iNoReg2) + " del primer registro:%s %s%s%s" % (AZUL, FIN, ROJO, ln1[7], FIN))
  print("%sNumero total de registros de detalle:%s %s%d%s" % (AZUL, FIN, ROJO, lTot[0], FIN))
if fMtoTot != lTot[1]:
  print("%sError:%s El monto total de la primera fila no concuerda con la suma del monto total de depositos" % (ROJO, FIN))
  print("%sValor entre columnas " + str(iMtoTot1) + " y " + str(iMtoTot1) + " del primer registro:%s %s%s%s" % (AZUL, FIN, ROJO, fgFormateaNumero(fMtoTot, 2), FIN))
  print("%smonto total de depossitos en registros de detalle:%s %s%s%s" % (AZUL, FIN, ROJO, fgFormateaNumero(lTot[1], 2), FIN))
if 'MERCANTILF' == nbrArchBanco[0:10]: print("%sNumero de lote:%s %s%s%s" % (AZUL, FIN, CYAN, sNumLote, FIN))
if 'MERCANTILF' == nbrArchBanco[0:10]: print("%sRif:%s %s%s%s" % (AZUL, FIN, CYAN, sRif, FIN))
print("%sFecha valor:%s %s%s%s" % (AZUL, FIN, CYAN, sFecha, FIN))
print("%sCodigo de cuenta bancaria:%s %s%s%s" % (AZUL, FIN, CYAN, sCodCta, FIN))
print("%sSe deposita a %d socios, la cantidad de %s bolivares.%s" % \
      (VERDE, lTot[0], fgFormateaNumero(lTot[1], 2), FIN))

# FIN Programa
