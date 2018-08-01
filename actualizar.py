#-*-coding:utf8;-*-
#qpy:3
#qpy:console
try:
  import androidhelper as android
except:
  import android
import socket, sys
import libConst, libES
from urllib.request import urlopen
from time import time, localtime, strftime

droid = android.Android()
ES    = libES
CO    = libConst

AMARI = CO.color.YELLOW			# Primer titulo. Identifica la fecha de actualizacion de los datos.
CYAN  = CO.color.CYAN			# Identificacion del socio.
AZUL  = CO.color.BLUE			# Identificacion de los datos.
VERDE = CO.color.GREEN			# Linea final (totales).
ROJO  = CO.color.RED			# Error
PURPURA  = CO.color.PURPLE
NEGRITA = CO.color.BOLD
SUBRAYA = CO.color.UNDERLINE
FIN   = CO.color.END

lSitios = ["IPASPUDO", "Portatil", "Casa", "Otro", "Salir"]
lIPs    = ["10.0.0.100", "10.0.0.103", "192.168.1.200", "192.168.0.105"]
IPDIR = "10.0.0.100"
lDATA = [
		 'control.txt',			# Por procesamiento posterior, este archivo, SIEMPRE, debe estar primero.
		 'bancos.txt',
		 'cheques.txt',
		 'conceptos.txt',
		 'disponibilidad.txt',
		 'extension.txt',
		 'heute.txt',
		 'moneda.txt',
		 'persona.txt',
		 'parentesco.txt',
		 'prestamos.txt',
		 'servifun.txt',
		 'nomina.txt',
		 'nominacne.txt',
		 'ubicacion.txt',
		 'egyp.txt',
		 'egypacu.txt',
		 'concNominaN.txt',
		 'concNominaH.txt',
		 'concNominaC.txt',
		 'concNominaCcE.txt',
		 'archsBanco.txt'
		]

def obtenerIP(servidor):		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((servidor, 80))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.

ES.muestraInicio("IPASPUDO: J-30619229-8.")

ind = ES.entradaConLista(droid, 'Busqueda del servidor', 'Seleccione servidor', lSitios)		# Busca el servidor.
if (ind >= len(lSitios)) or (ind < 0) or (ind == (len(lSitios)-1)) or (None == ind):	# Se asegura de tener el indice correcto.
	ES.muestraFin()
	sys.exit()
print("Obteniendo archivo desde %s (%s)." % (lSitios[ind], lIPs[ind]))
dirIP   = lIPs[ind]													# Si el indice es correcto, obtener la direccion IP.
miDirIP = obtenerIP(dirIP)											# Esta rutina fue la unica que encontre para mi IP.
print("Mi direccion IP es: %s" % miDirIP)
try:
	if dirIP[0:dirIP.rindex('.')] != miDirIP[0:miDirIP.rindex('.')]:	# Las tres primeras partes de ambos IPv4 deben ser iguales.
		print("El servidor seleccionado %s es errado." % dirIP)
		ES.muestraFin()
		sys.exit()
except ValueError:						# La funcion rindex (busca indece desde el final de la cadena), no consigue el '.'.
	print("ERROR EXTRA#O DE RED")									# Este error NUNCA deberia ocurrir.
	ES.muestraFin()
	sys.exit()

# Se trata de saber, cuando se actualizo por ultima vez un archivo. En el nuevo control.txt,
# ademas de la informacion del sistema, tambien se guardara la fecha de descarga de cada archivo.
dControl = ES.cargaDicc("control.txt")	# Diccionario de control, antes de recibir el nuevo.

URL = "http://" + dirIP + "/" + 'movil/'
bImpar  = True
lBancosHoy = None
dHoy = strftime("%d/%m/%Y", localtime())
for DATA in lDATA:
	sColor, bImpar = ES.colorLinea(bImpar, VERDE, AZUL)
	print("%sLeyendo%s %s remoto..." % (sColor, FIN, DATA))
	try:
		data = urlopen(URL + DATA, None, 10).read().decode('UTF-8')	# None, ningun parametro es enviado al servidor; 10, timeout.
		bLeido = True												# No hubo error de lectura desde el servidor.
	except:
		print("%sERROR LEYENDO%s %s %sREMOTO.%s" % (ROJO, FIN, DATA, ROJO, FIN))
		bLeido = False
	if bLeido:														# Si no hubo error de lectura desde el servidor.
		if 'control.txt' == DATA:
			lControl = data.rstrip().split('\n')
			if 0 < len(lControl):
				sControl = ''
				bOtroDia = False
				for l in lControl:
					ll = l.strip().split(';')
					if 1 < len(ll) and 'Sinca' == ll[0]:
						lll = ll[1].strip().split(':', 1)
						sFecControl = lll[1].strip()
						if 1 < len(lll): sControl = "%sControl al: %s%s." % (PURPURA, FIN, sFecControl)
						llll = sFecControl.strip().split(' ')
						if (1 < len(llll)) and (dHoy == llll[0]): bOtroDia = False
						else: bOtroDia = True
						break
					# if 1 < len(ll) and 'Sinca' == ll[0]
				# for l in lControl
				if bOtroDia:
					ES.imprime(sControl)
					ind = ES.entradaConLista(droid, 'Continuar', 'Seleccione', ['Si', 'No'])		# Continuar.
					if (2 <= ind) or (0 > ind) or (1 == ind) or (None == ind):	# Se asegura de tener el indice correcto.
						ES.muestraFin()
						sys.exit()
				# FIN if bOtroDia
			# FIN if 0 < len(lControl)
			else:
				ES.muestraFin()
				sys.exit()
		# Fin if 'control.txt' == DATA
		try:
			f = open(ES.DIR + DATA, "w")
			bAbierto = True											# No hubo error al abrir para escribir en archivo local.
		except:
			print("%sERROR AL TRATAR DE ABRIR%s %s %sPARA ESCRITURA.%s" % (ROJO, FIN, DATA, ROJO, FIN))
			bAbierto = False
		if bAbierto:												# Si no hubo error al abrir para escribir en archivo local.
			print("%sEscribiendo%s %s local..." % (sColor, FIN, DATA))
			try:
				f.write(data)
				bEscrito = True										# No hubo error escribiendo en el archivo local.
				if ('control.txt' != DATA) and ('archsBanco.txt' != DATA):
					dControl[DATA] = strftime("%d/%m/%Y %H:%M:%S", localtime())
			except:
				print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (ROJO, FIN, DATA))
				bEscrito = False
			finally:
				f.close()
			if bEscrito:
				if 'heute.txt' == DATA: print("%s %sactualizado con%s %d!" % (DATA, CYAN, FIN, ES.cLineas(DATA)))
				else: print("%s %sactualizado con%s %d!" % (DATA, sColor, FIN, ES.cLineas(DATA)))
				if 'archsBanco.txt' == DATA: lBancosHoy = data.rstrip().split('\n')
				else: lBancosHoy = None
			# Fin if bEscrito
		# Fin if bAbierto
	# Fin if bLeido
	elif 'control.txt' == DATA:
		print("%sPARECIERA QUE EXISTE ALGUN PROBLEMA CON INTERNET O LOS ARCHIVOS NO EXISTEN.%s" % (ROJO, FIN))
		ES.muestraFin()
		sys.exit()
# Fin for

dFecha = ES.cargaDicc("control.txt")	# Nuevo control con solo los valores recibidos del servidor.
for k in dFecha.keys():					# Llaves recibidas en el nuevo control.txt.
	if k in dControl:					# Elimina las llaves recibidas, del diccionario anterior.
		dControl.pop(k)					# Solo quedara en dControl, las fechas de descarga de los archivos.
sfControl = 'control.txt'
try:
	fc = open(ES.DIR + sfControl, "a")	# Se prepara para agregar, las fechas de descarga de cada archivo.
except:
	print("%sERROR AL TRATAR DE ABRIR%s %s %sPARA ESCRITURA.%s" % (ROJO, FIN, sfControl, ROJO, FIN))
#	continue
try:
	if fc:
		for k,v in dControl.items():	# Cada llave, valor de las fechas de descarga de los archivos.
			fc.write(k + ';' + v + '\n')# Agrega a 'fc' la fecha de cada archivo descargado.
except:
	print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (ROJO, FIN, sfControl))
finally:
	fc.close()

#print(lBancosHoy)
if lBancosHoy and (0 < len(lBancosHoy)):
	print('\n' + NEGRITA + SUBRAYA + 'Ahora procederemos a descargar los archivos de cada banco.' + FIN + '\n')
	for DATA in lBancosHoy:
		sColor, bImpar = ES.colorLinea(bImpar, VERDE, AZUL)
		print("%sLeyendo%s %s remoto..." % (sColor, FIN, DATA))
		try:
			data = urlopen(URL + DATA, None, 10).read().decode('UTF-8')	# None, ningun parametro es enviado al servidor; 10, timeout.
			bLeido = True												# No hubo error de lectura desde el servidor.
		except:
			print("%sERROR LEYENDO%s %s %sREMOTO.%s" % (ROJO, FIN, DATA, ROJO, FIN))
			bLeido = False
		if bLeido:														# Si no hubo error de lectura desde el servidor.
			try:
				f = open(ES.DIR + DATA, "w")
				bAbierto = True											# No hubo error al abrir para escribir en archivo local.
			except:
				print("%sERROR AL TRATAR DE ABRIR%s %s %sPARA ESCRITURA.%s" % (ROJO, FIN, DATA, ROJO, FIN))
				bAbierto = False
			if bAbierto:												# Si no hubo error al abrir para escribir en archivo local.
				print("%sEscribiendo%s %s local..." % (sColor, FIN, DATA))
				try:
					f.write(data)
					bEscrito = True										# No hubo error escribiendo en el archivo local.
				except:
					print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (ROJO, FIN, DATA))
					bEscrito = False
				finally:
					f.close()
			# Fin if bAbierto
		# Fin if bLeido
	# Fin for DATA in lBancosHoy
# Fin if
else:
	print('\n' + NEGRITA + SUBRAYA + 'No hay archivos de banco de hoy' + FIN + '\n')
ES.muestraFin()
# Fin del programa
