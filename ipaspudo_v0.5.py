#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys, time, types

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

from lib import IPASPUDO as IP
from lib import ES, Cuota as CU

esperar = 'Espere un momento, por favor...'
if droid:
  droid.dialogCreateHorizontalProgress('IPASPUDO', esperar, 100)
  droid.dialogShow()
  droid.dialogSetCurrentProgress(15)
else: print(esperar)
IP.prepararListasDeTrabajo()
if droid: droid.dialogSetCurrentProgress(60)
else: print('Listas listas!')
IP.prepararDiccionariosDeTrabajo()
if droid: droid.dialogSetCurrentProgress(90)
else: print('Diccionarios listos!')

IP.colocarDroid(droid)
ES.muestraInicio("IPASPUDO: J-30619229-8.")
if droid: droid.dialogSetCurrentProgress(95)

sUXD, sCXD = IP.leeValXDefecto()
if droid:
  droid.dialogSetCurrentProgress(100)
  droid.dialogDismiss()

nOp = 11
while True:
  sOpcion = IP.selFuncionInicial(nOp)

  if 'cuota' == sOpcion: CU.cuota(droid)
  elif 'salir' == sOpcion or None == sOpcion: break
  elif isinstance(sOpcion, int) and 0 > int(sOpcion): break
  elif 'cedula' == sOpcion:
    IP.cigIgualMenosUno()
    ci, sNombre = IP.valSocio()
    if (0 < ci):
      IP.mSocio(sNombre)
      bSF = True
      while bSF:
        bSF = IP.selFuncion(nOp)
  elif 'nombre' == sOpcion:
    IP.hacercigAntIgualAcig()
    ci, sNombre = IP.buscarNombre()
    if (0 < ci):
      IP.mSocio(sNombre)
      if not IP.escigAntIgualAcig():
        bSF = True
        while bSF:
          bSF = IP.selFuncion(nOp)
        IP.cigAntIgualA(ci)
  else:
    func = eval('IP.' + sOpcion)	# Evaluar contenido de sOpcion; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType): func()	# Si la cadena evaluada es una funcion, ejecutela.
    else: break
# Fin while True

IP.escValXDefecto(sUXD, sCXD)
ES.muestraFin()
# Fin del programa
