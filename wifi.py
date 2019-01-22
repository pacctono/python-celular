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

from lib import Const as CO

def obtenerIP():		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.

if droid:
	print("%sdroid.wifiGetConnectionInfo(): %s" % (CO.AZUL, CO.FIN),
																																end='')
	print(droid.wifiGetConnectionInfo())
	print("%sdroid.wifiGetConnectionInfo().result: %s" % \
																						(CO.AZUL, CO.FIN), end='')
	print(droid.wifiGetConnectionInfo().result)
	decip = droid.wifiGetConnectionInfo().result['ip_address']
	print("%sdroid.wifiGetConnectionInfo().result['ip_address']; %s" % \
																						(CO.AZUL, CO.FIN), end='')
	print("%sDec:%s %d; " % (CO.AZUL, CO.FIN, decip), end='')
	print("%sHex:%s %x" % (CO.AZUL, CO.FIN, decip))
	hexip = hex(decip).split('x')[1]
	print("%shex(%s%d%s).split('x')[1]:%s %s" % \
							(CO.AZUL, CO.FIN, decip, CO.AZUL, CO.FIN, hexip))
	print("%shex(%s%d%s).split('x'):%s " % \
							(CO.AZUL, CO.FIN, decip, CO.AZUL, CO.FIN), end='')
	print(hex(decip).split('x'))
	dirL = int(hexip, 16)
	print("%sint(%s%s%s, 16):%s " % \
										(CO.AZUL, CO.FIN, hexip, CO.AZUL, CO.FIN), end='')
	print(hex(dirL))
	print("%sstruct.pack(\"<L\", int(%s%s%s, 16))[Little indian]:%s " % \
										(CO.AZUL, CO.FIN, hexip, CO.AZUL, CO.FIN), end='')
	print(struct.pack("<L", dirL))			# Little indian
	print("%sstruct.pack(\">L\", int(%s%s%s, 16))[Big indian]:%s " % \
										(CO.AZUL, CO.FIN, hexip, CO.AZUL, CO.FIN), end='')
	print(struct.pack(">L", dirL))			# Big indian
	print("%ssocket.inet_ntoa(struct.pack(\"<L\", int(%s%s%s, 16)):%s " \
									% (CO.AZUL, CO.FIN, hexip, CO.AZUL, CO.FIN), end='')
	miDirIP = "%s" % socket.inet_ntoa(struct.pack("<L", dirL))
	print(miDirIP)
else:
	miDirIP = obtenerIP()

print("Mi direccion IP es: %s" % miDirIP)
