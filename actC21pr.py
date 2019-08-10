#!/usr/bin/python3
#-*- coding:ISO-8859-1 -*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
PY3 = 3 == sys.version_info.major
if PY3:
  unicode = str
else:
  input = raw_input

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
else: droid = None

import socket
import struct

from lib import ES, Const as CO, General as FG
from urllib.request import urlopen
from time import time, localtime, strftime, ctime
from os import stat
from datetime import datetime

lSitios = ["Puente Real", "Portatil", "Casa", "Otro", "Salir"]
lIPs    = ["192.168.0.100", "192.168.0.200", "192.168.1.200", ""]
lDATA = [
		 'control.txt',			# Por procesamiento posterior, este archivo, SIEMPRE, debe estar primero.
		 'asesores.txt',
		 'propiedades.txt',
		 'totales.txt',
		 'estatus.txt',
		 'negociacion.txt',
		 'moneda.txt',
		 'estatus_century_21.txt',
		]

def getNetworkIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))
	return s.getsockname()[0]
def obtenerIP(servidor):		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((servidor, 80))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.

ES.muestraInicio("Century21 Puente Real: J-40589955-7.")

ind = ES.entradaConLista(droid, 'Busqueda del servidor',
								'Seleccione servidor', lSitios)		# Busca el servidor.
if (None == ind) or (ind == (len(lSitios)-1)) or (len(lSitios) <= ind) or \
					(0 > ind):	# Se asegura de tener el indice correcto.
	ES.muestraFin()
	sys.exit()
IPServ = lIPs[ind]
if ((ind == (len(lSitios)-2)) or ('' == IPServ)):
	IPServ = ES.entradaNombre(droid, 'IP del servidor',
								'Introduzca IP del servidor', '192.168.0.')
print("Obteniendo archivo desde %s (%s)." % (lSitios[ind], IPServ))
if droid:
	decip = droid.wifiGetConnectionInfo().result['ip_address']
	hexip = hex(decip).split('x')[1]
	dirL = int(hexip, 16)
	miDirIP = socket.inet_ntoa(struct.pack("<L", dirL))
else:
	miDirIP = obtenerIP(IPServ)	# Esta rutina fue la unica que encontre para mi IP.

print("Mi direccion IP es: %s" % miDirIP)
try:
	if IPServ[0:IPServ.rindex('.')] != miDirIP[0:miDirIP.rindex('.')]:	# Las tres primeras partes de ambos IPv4 deben ser iguales.
		print("El servidor seleccionado %s es errado." % IPServ)
		ES.muestraFin()
		sys.exit()
except ValueError:						# La funcion rindex (busca indece desde el final de la cadena), no consigue el '.'.
	print("ERROR EXTRA#O DE RED")									# Este error NUNCA deberia ocurrir.
	ES.muestraFin()
	sys.exit()

# Se trata de saber, cuando se actualizo por ultima vez un archivo. En el nuevo control.txt,
# ademas de la informacion del sistema, tambien se guardara la fecha de descarga de cada archivo.
dControl = ES.cargaDicc("control.txt")	# Diccionario de control, antes de recibir el nuevo.

URL = "http://" + IPServ + '/public/storage/'
bImpar  = True
dHoy = strftime("%Y%m%d", localtime())
try:
	f = open(DIR + 'control.txt', "r")
	data = f.read()
	lControl = [linea.strip().split(';')
									for linea in data.rstrip().split('\n')]
except:
	lControl = [['0', nombArch] for nombArch in lDATA]
dControl = {linea[1].strip():[linea[0].strip(), linea[0].strip()]
					for linea in lControl if FG.esEntero(linea[0].strip())}
for DATA in lDATA:
	if 'control.txt' != DATA:
		(timeAnterior, timeNuevo) = dControl.get(DATA, ['0', '-1'])
	else: timeAnterior = timeNuevo = 0
	segsDiferencia = int(timeNuevo) - int(timeAnterior)
	sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE, CO.AZUL)
	print("%sLeyendo%s %s remoto. Local modificado hace: %d seg del remoto" %
						(sColor, CO.FIN, DATA, segsDiferencia))
	if 'control.txt' != DATA and 0 >= segsDiferencia:
		if 0 == segsDiferencia:
			print("%s, %slocal; ya esta actualizado con%s %d lineas! El %s" % \
								(DATA, sColor, CO.FIN, ES.cLineas(DATA),
													ctime(int(timeAnterior))))
			continue
	try:
		data = urlopen(URL + DATA, None, 10).read().decode('ISO-8859-1')	# None, ningun parametro es enviado al servidor; 10, timeout.
		bLeido = True												# No hubo error de lectura desde el servidor.
	except:
		print("%sERROR LEYENDO%s %s %sREMOTO.%s" % (CO.ROJO, CO.FIN, DATA,
															CO.ROJO, CO.FIN))
		bLeido = False
	if bLeido:														# Si no hubo error de lectura desde el servidor.
		if 'control.txt' == DATA:
			lControl = [linea.strip().split(';')
									for linea in data.rstrip().split('\n')]
			if 0 < len(lControl):
				sControl = ''
				bOtroDia = False
				for l in lControl:
					if 'Sinca' == l[0]:
						fechaControl = datetime.strptime(l[1],
								'ACTUALIZADO Al: %d/%m/%Y %H:%M:%S')
						sControl = "%sControl al: %s%s." % (CO.PURPURA, CO.FIN,
																fechaControl)
						if (dHoy != fechaControl.strftime('%Y%m%d')):
							bOtroDia = True
						break
					# if 1 < len(ll) and 'Sinca' == ll[0]
				# for l in lControl
				if bOtroDia:
					ES.imprime(sControl)
					ind = ES.entradaConLista(droid, 'Continuar', 'Seleccione',
												['Si', 'No'])		# Continuar.
					if (1 <= ind) or (0 > ind) or (None == ind):	# Se asegura de tener el indice correcto.
						ES.muestraFin()
						sys.exit()
				# FIN if bOtroDia
				for linea in lControl:
					if ES.esEntero(linea[0]):	# linea[0] sera el nuevo tiempo.
						dControl[linea[1]] = [
							dControl.get(linea[1], ['0', 0])[0], linea[0]
						]	# el tiempo anterior es el primer item de dControl o -1.
#						if linea[1] in dControl:
#							dControl[linea[1]] = [dControl[linea[1]][0],
#																	linea[0]]
#						else: dControl[linea[1]] = ['-1', linea[0]]
			# FIN if 0 < len(lControl)
			else:
				ES.muestraFin()
				sys.exit()
		# Fin if 'control.txt' == DATA
		try:
			f = open(DIR + DATA, "w")
			bAbierto = True											# No hubo error al abrir para escribir en archivo local.
		except:
			print("%sERROR AL TRATAR DE ABRIR%s %s%s %sPARA ESCRITURA.%s" % \
								(CO.ROJO, CO.FIN, DIR, DATA, CO.ROJO, CO.FIN))
			bAbierto = False
		if bAbierto:												# Si no hubo error al abrir para escribir en archivo local.
			print("%sEscribiendo%s %s local..." % (sColor, CO.FIN, DATA))
			try:
				f.write(data)
				bEscrito = True										# No hubo error escribiendo en el archivo local.
			except:
				print("%sERROR AL TRATAR DE ESCRIBIR%s %s." % (CO.ROJO, CO.FIN,
																		DATA))
				bEscrito = False
			finally:
				f.close()
			if bEscrito:
				print("%s %sactualizado con%s %d lineas!" % (DATA,
								(CO.CYAN if 'heute.txt' == DATA else sColor),
													CO.FIN, ES.cLineas(DATA)))
			# Fin if bEscrito
		# Fin if bAbierto
	# Fin if bLeido
	elif 'control.txt' == DATA:		# El primer archivo a leer, no se pudo descargar.
		print(("%sPARECIERA QUE EXISTE ALGUN PROBLEMA CON INTERNET O LOS "
				"ARCHIVOS NO EXISTEN.%s") % (CO.ROJO, CO.FIN))
		ES.muestraFin()
		sys.exit()
# Fin for
ES.muestraFin()
# Fin del programa
