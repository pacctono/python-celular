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

def obtenerIP():		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.

if droid:
	print(droid.wifiGetConnectionInfo())
	print(droid.wifiGetConnectionInfo().result)
	decip = droid.wifiGetConnectionInfo().result['ip_address']
	print("Direccion IP en decimal: %d" % decip)
	hexip = hex(decip).split('x')[1]
	print("Direccion IP en hexadecimal: %x" % decip)
	print(hex(decip).split('x'))
	dirL = int(hexip, 16)
	print(hex(dirL))
	print(struct.pack("<L", dirL))			# Little indian
	print(struct.pack(">L", dirL))			# Big indian
	miDirIP = "%s" % socket.inet_ntoa(struct.pack("<L", dirL))
else:
	miDirIP = obtenerIP()

print("Mi direccion IP es: %s" % miDirIP)
