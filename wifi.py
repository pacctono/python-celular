#-*-coding:utf8;-*-
#qpy:3
#qpy:console
try:
	import androidhelper as android
except:
	import android
import socket
import struct

droid = android.Android()

def obtenerIP(servidor):		# Es la unica rutina que consegui para obtener mi IP.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((servidor, 80))	# servidor puede ser cualquiera, no es necesario usar el seleccionado.
	return s.getsockname()[0]	# el IP es el primer elemento de la tupla devuelta. El 2do elemento parece ser una puerta.

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
print("Mi direccion IP: %s" % socket.inet_ntoa(struct.pack("<L", dirL)))

miDirIP = obtenerIP('10.0.0.100')											# Esta rutina fue la unica que encontre para mi IP.
print("Mi direccion IP (con problemas) es: %s" % miDirIP)
