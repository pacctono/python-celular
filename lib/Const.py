# libConst: modulo para entrada y salida.
#-*-coding:utf8;-*-
try:
  from lib import DIR, LINEA, bMovil
except:
  DIR = './'
  LINEA = 70
  bMovil = False

meses = [
	'',
	'ENERO',
	'FEBRERO',
	'MARZO',
	'ABRIL',
	'MAYO',
	'JUNIO',
	'JULIO',
	'AGOSTO',
	'SEPTIEMBRE',
	'OCTUBRE',
	'NOVIEMBRE',
	'DICIEMBRE'
]

UT  = 1000	# Valor actual de la unidad tributaria
UTA = 1000	# valor de la unidad tributaria del a#o anterior.
anoDividendo = '2.016'

UGENERAL = 'ipaspudo'	# Usuario general, devuelve info restringida: Cedula, Nombre, Nucleo, etc.
SUPERUSU = 'ipas'		# Superusuario.
USUAREC  = 'ipasrec'	# Usuario del Rectorado.
USUAANZ  = 'ipasanz'	# Usuario nucleo de Anzoategui.
USUABOL  = 'ipasbol'	# Usuario nucleo de Bolivar.
USUAMON  = 'ipasmon'	# Usuario nucleo de Monagas.
USUANVAE = 'ipasnva'	# Usuario nucleo de Nueva Esparta.
USUASUC  = 'ipasns'		# Usuario nucleo de Sucre.
USUAADM  = 'ipasadm'	# Usuario administrativo.

NMAXITEM = 50			# Numero maximo de items (cheques) a mostrar en una lista de seleccion. Usado: lCheques.
# Vivienda
MMADQV = 3000000 # Monto maximo para adquisicion de vivienda.
NMADQV = 300     # Numero maximo de meses para adquisicion de vivienda.
MMREMV = 2000000 # Monto maximo para remodelacion de vivienda.
NMREMV = 240     # Numero maximo de meses para remodelacion de vivienda.
MMCTPV = 2000000 # Monto maximo para construccion de vivienda.
NMCTPV = 240     # Numero maximo de meses para construccion de vivienda.
MMCIV  = 150000  # Monto maximo para cuota inicial de vivienda.
NMCIV  = 120     # Numero maximo de meses para cuota inicial de vivienda.
MMCDTV = 1000000 # Monto maximo para compra de terreno.
NMCDTV = 240     # Numero maximo de meses para compra de terreno.
IAV    = 10.00   # Interes anual para vivienda.
# Vehiculos
#lTipoAuto   = ['Nuevo', 'Usado']
MMA    = 3000000 # Monto maximo para vehiculo.
#lNumeroUT  = [3200, 3200]
IAA    = 12.00		# Interes anual para vehiculos.
NMA    = 180			# Numero maximo de meses para vehiculos.
MMLBM  = 250000	# Monto maximo para linea blanca/marron.
IAC    = 12.00		# Interes anual para linea blanca/marron.
NMC    = 60			# Numero maximo de meses para linea blanca/marron.
MMMN   = 1000000 # Monto maximo para moto nueva.
MMMU   = 400000  # Monto maximo para moto usada.
NMM    = 180			# Numero maximo de meses para motos.

MFS    = 70000	# Monto del Fondo de salud.
MFSM   = 40000	# Monto del Fondo de salud por maternidad.

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
AMARI   = color.YELLOW	# Primer titulo. Identifica la fecha de actualizacion de los datos.
CYAN    = color.CYAN	# Identificacion del socio.
AZUL    = color.BLUE	# Identificacion de los datos.
VERDE   = color.GREEN	# Linea final (totales).
PURPURA = color.PURPLE	# Linea final (total de prestamos).
NEGRITA = color.BOLD	# Negrita
SUBRAYA = color.UNDERLINE
ROJO    = color.RED		# Linea de error.
SUBRAYADO  = color.UNDERLINE	# Subrayado
FIN     = color.END

lMonto = ['10000', '20000', '30000', '40000', '50000', '75000', '100000',
			'150000', '250000', '500000', '600000', '700000', '1000000',
			'1500000', '2000000', 'Otro']
lNuMes = ['12', '18', '24', '30', '36', '48', '60', '72', '84', '96', '120',
			'144', '150', '180', '240', '300', 'Otro']
lInter = ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', 'Otro']

lEstado = ['HECHO', 'LISTO', 'ENTREG', 'PAGADO']	# Estado del cheque
# Maximo 20 caracteres para cada uno.
dConceptos = {
  '0':'FEC INGRESO IPASPUDO',
  '1':'APORTE PATRONAL',
  '2':'AHORRO SOCIO',
  '3':'AHORROS NO RECIBIDOS',
  '4':'RETIRO PARCIAL',
  '5':'TOT AHORROS ACUMUDOS',
  '6':'TOT AHORROS ACUM 80%',
  '7':'FIANZAS',
  '8':'RETENCS NO RECIBIDAS',
  '9':'TOTAL PRESTAMOS',
  'A':'DEUDA VIEJA ABONADA',
  'B':'DISPONIBILIDAD',
  'C':'TOTAL CUOTAS',
  'D':'NORMAL',
  'E':'COMPLETA',
  'F':'EXTRAS'
}
dNucleo = {
  'R':'Rectorado',
  'S':'Sucre',
  'A':'Anzoategui',
  'M':'Monagas',
  'B':'Bolivar',
  'N':'Nueva Esparta'
}
dExtension = {
  'A':'ACTIVO',
  'a':'activo',
  'N':'No activo'
}

# ServiFun
CI    = 398.25		# Cuota individual
CCC   = 597.75		# Cuota con carga hasta 8 (incluyendo al socio)
CO    = 398.25		# Cuota de servifun para incluir otra carga
CHM25 = 398.25		# Cuota para hermanos mayores de 25.
CM70  = 199.50		# Cuota para cada carga mayor de 70.
CM75  = 399.00		# Cuota para cada carga mayor de 75.
CM80  = 598.25		# Cuota para cada carga mayor de 80.
CEM70 = 199.50		# Cuota especial para cada carga mayor de 70.
CEM75 = 399.00		# Cuota especial para cada carga mayor de 75.
CEM80 = 598.25		# Cuota especial para cada carga mayor de 80.

lTitulo = [
			'Cedula de identidad', 'Nombre', 'Nucleo',
			'Fecha de nacimiento', 'Disponibilidad', 'Extension',
			'Fecha ingreso IPASPUDO', 'Neto de nomina', 'Servifun'
		  ]
lTH = [['', 'AHORRO SOCIOS', '511', '211010101', '', ''],
       ['', 'AHORRO PATRONO', '562', '211020101', '', ''],
       ['', 'RETIRO PARCIAL', '', '211030101', '', '']
      ]

lCB = [['Mercantil', 'AHORRO       ', '01050068140068276745',
			'112-02-01-02-6'],		# Mercantil
       ['Mercantil', 'CORRIENTE    ', '01050068120068204451',
			'112-02-01-01-1'],		# Mercantil
       ['Mercantil', 'AHO VEBONOS  ', '01050068127068036899',
	   		'112-02-01-02-8'],		# Mercantil
       ['BANESCO  ', 'CTE SERVIFUN ', '01340055570553285769',
	   		'112-02-01-01-9'],		# Banesco
       ['BANESCO  ', 'CTE OPERACION', '01340055500553285809',
	   		'112-02-01-01-9'],		# Banesco
       ['Caribe   ', 'CORRIENTE    ', '01140521575217000264',
	   		'112-02-01-01-7'],		# Bancaribe
       ['Venezuela', 'CORRIENTE    ', '01020672330000020336',
	   		'112-01-01-01-11'],		# Venezuela
       ['Venezuela', 'CTE C/INTERES', '01020673110000025784',
	   		'112-01-01-01-12'],		# Venezuela
       ['BNC      ', 'CORRIENTE    ', '01910048122148032454',
	   		'112-02-01-01-13'],		# BNC
       ['BNC      ', 'AHORRO       ', '01910048171048003569',
	   		'112-02-01-02-13'],		# BNC
       ['Pueblo   ', 'CORRIENTE    ', '01490025020300047193',
	   		'112-01-01-01-14'],		# Banco del Pueblo
       ['Pueblo   ', 'AHORRO       ', '01490025050400310589',
	   		'112-01-01-02-12'],		# Banco del Pueblo
       ['Del Sur  ', 'CORRIENTE    ', '01570029783729204036',
	   		'112-01-01-02-12'],		# Del Sur Banco Universal
       ['Caroni   ', 'CORRIENTE    ', '01280044454401000890',
	   		'112-01-01-02-12'],		# Banco Caroni CA
      ]

def getTerminalSize():
	""" getTerminalSize()
	 - get width and height of console
	"""

	import os
	def ioctl_GWINSZ(fd):
		try:
			import fcntl, termios, struct
			cr = struct.unpack('hh', fcntl.ioctl(fd,
												termios.TIOCGWINSZ,'1234'))
		except:
			return None
		return cr
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		return 0, 0
	return int(cr[1]), int(cr[0])
# Fin funcion getTerminalSize
try:
	nCarLin, LINEAS = getTerminalSize()		# Columnas, lineas de la pantalla.
	if (0 == nCarLin): nCarLin = LINEA		# Numero de caracteres por linea del terminal.
except:
	nCarLin = 42					# Valor por defecto en caso de no poderse calcular o de no estar definido.
  
if nCarLin > 60: bPantAmplia = True
else: bPantAmplia = False

def maxLongitudCadena(lista=[], ind=0):
	maxLongCad = 0
	for l in lista:
		if len(l[ind]) > maxLongCad: maxLongCad = len(l[ind])
	return maxLongCad
# Fin maxLongitudCadena(lista=[], ind=0)
def carPorCampo(lista=[], ind=0, nOffset=0):
	global nCarLin, nCarMostrar
	
	nCarCampo = nCarLin - nOffset - 1					# Numero de caracteres (espacio total), donde se mostrara el campo.
	maxLongCad = maxLongitudCadena(lista, ind)			# numero maximo de caracteres del campo especificado.
	if maxLongCad < nCarCampo: nCarCampo = maxLongCad	# > longitud maxima de la cadena a mostrar en el campo.
	nCarMostrar = nOffset + nCarCampo					# Numero de caracteres, maximo, a mostrar por linea.
	return nCarMostrar, nCarCampo, maxLongCad
# Fin carPorCampo(lista=[], ind=0, offset=0)
def nCarJustIzq(sCadena='', nCarMostrar=0):
	nCarCC = len(sCadena)								# Numero de caracteres del campo.
	if (0 == nCarMostrar): nCarMostrar = nCarCC
	return int((nCarMostrar - nCarCC + 1)/2) + nCarCC	# Numero de caracteres para justificar a la izquierda el campo.
# Fin nCarIzqCampo(sCadena='', nCarMostrar=nCarLin)
def justIzqTituloCol(sTitCol='', nCarCol=0):			# Centra el titulo de una columna en su espacio maximo.
#	nCarIzCC = nCarJustIzq(sTitCol, nCarCol)			# Numero de cars en blanco a la izquierda del titulo de la columna.
	sTitCol  = sTitCol.ljust(nCarCol + 1)
	return sTitCol
# funcion justIzqTituloCol
def escnCarMostrar(n):									# Modifica el numero de caracteres a mostrar por linea.
	global nCarMostrar
	nCarMostrar = n
	return nCarMostrar
# funcion escnCarCampo
def leenCarMostrar():									# Devuelve el numero de caracteres a mostrar por linea.
	global nCarMostrar
	return nCarMostrar
# funcion leenCarCampo

nCarMostrar = nCarLin									# Numero de caracteres a mostrar por linea.