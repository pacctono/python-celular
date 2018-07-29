#!/usr/bin/python
import sys
import re
try:
  import MySQLdb
  bMySQL = True
except:
  bMySQL = False

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
FIN   = color.END

patron = re.compile("\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile("\d{1,3}")	# Expresion regular: 1 o mas dec (\d+) y tres dec al final (\d{3}).

def creaDicConceptos():
  if not bMySQL: return {}
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
#  print('fn: ', signo + x1 + x2)

  return signo + x1 + x2	#parte entera (x1) con '.' intercalado cada 3 dec + parte decimal con ',' adelante.
# funcion fgFormateaNumero(sCad, dec)

dConc = creaDicConceptos()

f = open(sys.argv[1], 'r')
lista = [(linea.rstrip()[9:12], float(linea.rstrip()[12:20])/100, float(linea.rstrip()[20:])/100) for linea in f]
dicc = {}
dicc['AHO']  = (0, 0.00, 0.00, 0.00)
dConc['AHO'] = {'des':'AHORROS'}
dicc['PR0']  = (0, 0.00, 0.00, 0.00)
dConc['PR0'] = {'des':'PRESTAMOS x COMPRO'}
dicc['PR1']  = (0, 0.00, 0.00, 0.00)
dConc['PR1'] = {'des':'PRESTAMOS x COD Sinca'}
dicc['PRE']  = (0, 0.00, 0.00, 0.00)
dConc['PRE'] = {'des':'TOTAL PRESTAMOS'}
dicc['TOT']  = (0, 0.00, 0.00, 0.00)
dConc['TOT'] = {'des':'TOTAL GENERAL'}
for l in lista:
  try:
    if not dicc.has_key(l[0]): dicc[l[0]] = (0, 0.00, 0.00, 0.00)
    dicc[l[0]] = (dicc[l[0]][0]+1, dicc[l[0]][1]+l[1], dicc[l[0]][2]+l[2], dicc[l[0]][3]+l[1]+l[2])
    dicc['TOT'] = (dicc['TOT'][0]+1, dicc['TOT'][1]+l[1], dicc['TOT'][2]+l[2], dicc['TOT'][3]+l[1]+l[2])
    if l[0] in ('511', '562'):
      dicc['AHO'] = (dicc['AHO'][0]+1, dicc['AHO'][1]+l[1], dicc['AHO'][2]+l[2], dicc['AHO'][3]+l[1]+l[2])
    if dConc.get(l[0], {'com':''})['com'] and \
       dConc.get(l[0], {'com':''})['com'].isdigit() and \
       '94' == dConc.get(l[0], {'com':''})['com']:
      dicc['PR0'] = (dicc['PR0'][0]+1, dicc['PR0'][1]+l[1], dicc['PR0'][2]+l[2], dicc['PR0'][3]+l[1]+l[2])
    if dConc.get(l[0], {'nus':''})['nus'] and \
       dConc.get(l[0], {'nus':''})['nus'].isdigit():
      dicc['PR1'] = (dicc['PR1'][0]+1, dicc['PR1'][1]+l[1], dicc['PR1'][2]+l[2], dicc['PR1'][3]+l[1]+l[2])
    if l[0] not in ('511','561', '562', '563', '570'):
      dicc['PRE'] = (dicc['PRE'][0]+1, dicc['PRE'][1]+l[1], dicc['PRE'][2]+l[2], dicc['PRE'][3]+l[1]+l[2])
  except:
    print(l)
    print(dConc[l[0]])
    sys.exit()
#
lconc = []
i = 0
iMax = '000'
for ld in dicc.items():
  lconc.insert(i, ld[0])
  if ld[0].isdigit() and ld[0] > iMax: iMax = ld[0]
  i += 1
lconc.sort()
bImpar  = True
print("%s%s%3s %-20.20s %6.6s %15.15s %15.15s %15.15s%s" % \
      (color.UNDERLINE, AMARI, 'CLV', 'DESCRIPCION', '#SOCI', 'VALOR FIJO', 'VALOR VARIABLE', 'TOTALES', FIN))
#print("%s%3s %6.6s %15.15s %15.15s %15.15s%s" % (AMARI, '---', '-----', '----------', '--------------', '-------', FIN))
for v in lconc:
    if not ((0.00 == dicc[v][1]) and (0.00 == dicc[v][2]) and (0.00 == dicc[v][3])):
       if v.isdigit():
         if iMax > v: subrayar = ''
         else: subrayar = color.UNDERLINE
       else: subrayar = ''
       if ('TOT' == v): sColor = VERDE
       elif v in ('AHO', 'PRE', 'PR0', 'PR1'): sColor = PURPURA
       else: sColor, bImpar = colorLinea(bImpar)
       print("%s%s%3s %-20.20s %6.6s %15.15s %15.15s %15.15s%s" %\
             (subrayar, sColor, v, dConc.get(v, {'des':'NO TENGO DESCRIPCION'})['des'], \
              fgFormateaNumero(dicc[v][0]), fgFormateaNumero(dicc[v][1], 2), \
              fgFormateaNumero(dicc[v][2], 2), fgFormateaNumero(dicc[v][3], 2), FIN))
#
f.close()
