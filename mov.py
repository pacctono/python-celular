#!/usr/bin/python
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import sys
import re
try:
  from lib import DIR
  bMovil = True
except:
  DIR = './'
  bMovil = False
if bMovil:
  from os import listdir
  from os.path import isfile, join
else:
  from os.path import abspath
try:
  import MySQLdb
  bMySQL = True
except:
  bMySQL = False

if bMovil:
  import fnmatch
  import sl4a
  import libES, libConst

  CO    = libConst
  ES    = libES
  droid = sl4a.Android()

  AMARI = CO.color.YELLOW	# Primer titulo. Identifica la fecha de actualizacion de los datos.
  CYAN  = CO.color.CYAN		# Identificacion del socio.
  AZUL  = CO.color.BLUE		# Identificacion de los datos.
  VERDE = CO.color.GREEN	# Linea final (totales).
  PURPURA = CO.color.PURPLE	# Linea final (total de prestamos).
  NEGRITA = CO.color.BOLD	# Negrita
  ROJO  = CO.color.RED		# Linea de error.
  SUBRAYADO  = CO.color.UNDERLINE	# Subrayado
  FIN   = CO.color.END
else:
  AMARI = '\033[93m'	# Primer titulo.
  CYAN  = '\033[96m'	# Identificacion del socio.
  AZUL  = '\033[94m'	# Identificacion de los datos.
  PURPURA = '\033[95m'	# Linea final (total de prestamos).
  VERDE = '\033[92m'	# Linea final (totales).
  ROJO  = '\033[91m'	# Linea de error.
  SUBRAYADO = '\033[4m'
  FIN   = '\033[0m'

patron = re.compile("\d+(\.\d+)?$")	# Valida un numero entero o de punto flotante.
pat = re.compile("\d{1,3}")	# Expresion regular: 1 o mas dec (\d+) y tres dec al final (\d{3}).

if not bMovil:
  def abre(aNb, modo='r', codigo = 'latin-1', bImprimir = False):
    'Abre para leer, el archivo cuyo nombre es el valor de aNb'
    global DIR
    aNb = DIR + aNb
    try:
#      f = open(aNb, mode=modo, encoding=codigo)
      f = open(aNb, mode=modo)
      if (bImprimir): print(aNb + " archivo abierto.")
      return f
    except:
      if (bImprimir):
        print(AMARI + "ERROR ABRIENDO: " + FIN + aNb)
        print(AMARI + "os.path.abspath(aNb): " + FIN + abspath(aNb))
      return False
  # FIN funcion abre
else:
	def cargarNombres(nombArch='IPAS*.TXT'):
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
def poblarDicConc(co, de, cm='', nu='', no='', au=''):
  return {'cod':co, 'des':de, 'com':cm, 'nus':nu, 'nom':no, 'aut':au}	# Codigo, desc,
# com: 2 primeros digitos comprobante, nu: cod tabla_prestamo,
# no: es concepto de nomina (S/N), au: automatico (S/N).
# FIN funcion poblarDic
def creaDicConceptos():
  if not bMySQL:
    try:
      if bMovil:
        dConcepto = ES.cargaDicc("conceptos.txt")
        dConc = {}
        for k,v in dConcepto.items():
       	  dConc[k] = poblarDicConc(k, v)
      else:
#        f = abre("conceptos.txt", bImprimir = True)
        f = abre("conceptos.txt")
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
      if not bMovil: print('Problemas con el archivo\n')
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
      dConc[row[0]] = poblarDicConc(row[0], row[1], row[2], row[3], row[4], row[5])
  except:
    print("Imposible crear diccionario de conceptos")
# disconnect from server
  db.close()
  return dConc
# FIN funcion creaDicConceptos
def poblarDicc(lidat, dConc):
  dicc = {}
  dicc['AHO']  = (0, 0.00, 0.00)
  dConc['AHO'] = {'des':'AHORROS'}
  dicc['CRE']  = (0, 0.00, 0.00)
  dConc['CRE'] = {'des':'CONCEPTOS CREADOS'}
  dicc['DMD']  = (0, 0.00, 0.00)
  dConc['DMD'] = {'des':'CONCEPTOS MODIFICADOS'}
  dicc['ELI']  = (0, 0.00, 0.00)
  dConc['ELI'] = {'des':'CONCEPTOS ELIMINADOS'}
  dicc['OTR']  = (0, 0.00, 0.00)
  dConc['OTR'] = {'des':'OTROS CONCEPTOS'}
  dicc['TOT']  = (0, 0.00, 0.00)
  dConc['TOT'] = {'des':'TOTAL GENERAL'}
  for l in lidat:
    try:
      sLlave = l[2]+'-'+l[0]+'-'+l[5]+'-'+l[6]
      if sLlave not in dicc: dicc[sLlave] = (0, 0.00, 0.00)
      dicc[sLlave] = (dicc[sLlave][0]+1, dicc[sLlave][1]+l[3], dicc[sLlave][2]+l[4])
      if '3' != l[5]: dicc['TOT'] = (dicc['TOT'][0]+1, dicc['TOT'][1]+l[3], dicc['TOT'][2]+l[4])
      if l[2] in ('511', '562'):		# Ahorro patronal y ahorro personal
        if '3' != l[5]: dicc['AHO'] = (dicc['AHO'][0]+1, dicc['AHO'][1]+l[3], dicc['AHO'][2]+l[4])
      if '1' == l[5]: dicc['CRE'] = (dicc['CRE'][0]+1, dicc['CRE'][1]+l[3], dicc['CRE'][2]+l[4])
      if '2' == l[5]: dicc['DMD'] = (dicc['DMD'][0]+1, dicc['DMD'][1]+l[3], dicc['DMD'][2]+l[4])
      if '3' == l[5]: dicc['ELI'] = (dicc['ELI'][0]+1, dicc['ELI'][1]+l[3], dicc['ELI'][2]+l[4])
      if l[2] in ('561', '563', '570'):	# Cuota mensual, ServiFun, Fondo de Salud
        if '3' != l[5]: dicc['OTR'] = (dicc['OTR'][0]+1, dicc['OTR'][1]+l[3], dicc['OTR'][2]+l[4])
    except:
      print(l)
      print(dConc[l[2]])
      print(dicc[l[1]])
      sys.exit()

  return dicc, dConc
# FIN funcion poblarDicc
def colorLinea(bImpar=True, sColor=AZUL, sOtroColor=None):
  global bMovil

  if bMovil: return ES.colorLinea(bImpar, sColor, sOtroColor)
  if bImpar: sColor = CYAN
  return sColor, not bImpar
# FIN funcion colorLinea
def fgFormateaNumero(sCad, dec=0):
  global bMovil

  if bMovil: return ES.fgFormateaNumero(sCad, dec)
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
# FIN funcion fgFormateaNumero(sCad, dec)
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
      (SUBRAYADO, AMARI, 'CLAVE', 'DESCRIPCION', '#MOVI', '     Saldo', '         Cuota', 'PORCEN', FIN)
  for v in lconc:
    if not ((0.00 == dicc[v][1]) and (0.00 == dicc[v][2])) or ('3' == v[6:7]):
       if v[0:3].isdigit() and v[4:5].isdigit() and v[6:7].isdigit() and v[8:].isdigit():
         if sMax == v: subrayar = SUBRAYADO
         else: subrayar = ''
       else: subrayar = ''
       if ('TOT' == v): sColor = VERDE
       elif ('AHO' == v): sColor = PURPURA
       elif ('ELI' == v): sColor = ROJO
       elif ('OTR' == v): sColor = PURPURA
       else: sColor, bImpar = colorLinea(bImpar, AZUL, CYAN)
       fPorc = 100.00*dicc[v][1]/dicc['TOT'][1]
       sConc = v[0:3]
       if '3' == v[6:7]: sObs = ROJO + 'Eli'
       elif '2' == v[6:7]: sObs = 'Mod'
       elif '1' == v[6:7]: sObs = 'Cre'
       else: sObs = ''
       st += "%s%s%9s %-20.20s %6.6s %15.15s %15.15s %6.6s %s%s\n" %\
             (subrayar, sColor, v, dConc.get(sConc, {'des':'NO TENGO DESCRIPCION'})['des'], \
              fgFormateaNumero(dicc[v][0]), fgFormateaNumero(dicc[v][1], 2), \
              fgFormateaNumero(dicc[v][2], 2), fgFormateaNumero(fPorc, 2), sObs, FIN)
              
  return st
# FIN funcion mostrarConceptos

# Inicio principal
dConc = creaDicConceptos()
sCed = ''
if bMovil:
  lFiles = cargarNombres('[Ii][Pp][Aa][Ss]0*.[Tt][Xx][Tt]')
  if not lFiles: sys.exit()
else:
  if 1 < len(sys.argv):
    nombArch = sys.argv[1]
    if 2 < len(sys.argv) and sys.argv[2].isdigit():
      sCed = sys.argv[2]
  else:
    print("%sNo paso el nombre del archivo como parametro.%s" % (ROJO, FIN))
    sys.exit()

while True:
  if bMovil:
    nombArch = buscarArchivo(lFiles)
    if None == nombArch: break
    f = ES.abrir(nombArch, 'r')
    iCed = ES.entradaNumero(droid, "Cedula de identidad", "Cedula de identidad del socio", sCed)
    if None == iCed or 0 == iCed: sCed = ''
    else: sCed = str(iCed)
  else:
    try:
      f = open(nombArch, 'r')
    except:
      f = False
  if not f:
    print("%sNombre de archivo%s '%s' %serrado.%s" % (ROJO, FIN, nombArch, ROJO, FIN))
    break

# 0:Mov (6:retroact o 7:fijo); 1:CI; 2:Conc; 3:Saldo; 4:Cuota; 5:Ctrl (1:Crea, 2:Mod, 3:eli); 6:Tipo (1:Saldo-cuota, 2:Cuota fija).
  lista = [(linea.rstrip()[0:1], linea.rstrip()[1:9], linea.rstrip()[10:13], float(linea.rstrip()[28:38])/100, float(linea.rstrip()[38:46])/100, linea.rstrip()[52:53], linea.rstrip()[76:77]) for linea in f]
  if f: f.close()

  dicc, dConc = poblarDicc(lista, dConc)
  st = mostrarConceptos(dicc, dConc)

  if '' != sCed:
    bCINoEncontrada = True
    for l in lista:
      if sCed.lstrip('0') == l[1].lstrip('0'):
        if bCINoEncontrada: st += "\n%sCI:%s%s%s%s" % (CYAN, FIN, AZUL, fgFormateaNumero(sCed), FIN)
        st += "\n%sCLV:%s%s%s-%-20.20s%s " % (CYAN, FIN, AZUL, l[2], dConc.get(l[2], {'des':'NO TENGO DESCRIPCION'})['des'], FIN)
        st += "%sSdo:%s%s%s%s; Cta:%s%s%s%s" %\
              (CYAN, FIN, AZUL, fgFormateaNumero(l[3], 2), CYAN, FIN, AZUL, fgFormateaNumero(l[4], 2), FIN)
        st += "%s; Ct:%s%s%s%s; Tp:%s%s%s%s" %\
              (CYAN, FIN, AZUL, l[5], CYAN, FIN, AZUL, l[6], FIN)
        bCINoEncontrada = False
  if '' != sCed and bCINoEncontrada: st += "\n%sLa cedula de identidad:%s %s%s%s no fue encontrada.\n" % (ROJO, FIN, AZUL, fgFormateaNumero(sCed), FIN)
  else: st += '\n'

  if bMovil:
    ES.imprime(st.rstrip(' \t\n\r'))
    indice = ES.entradaConLista(droid, 'Que desea hacer', 'Que desea hacer', ['Otro archivo', 'Salir'])
    if None == indice or 0 > indice or 1 <= indice: break
  else:
    print(st.rstrip(' \t\n\r'))
    break

# FIN Principal
