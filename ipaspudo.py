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

from ipa import AhorroYPrestamo as AP
from ipa import GanYPer as GyP
from ipa import Nomina as NOM
from ipa import Comun as COM
from lib import ES, Cuota as CU

esperar = 'Espere un momento, por favor...'
if droid:
  droid.dialogCreateHorizontalProgress('IPASPUDO', esperar, 100)
  droid.dialogShow()
  droid.dialogSetCurrentProgress(15)
else: print(esperar)
AP.prepararListasDeTrabajo()
if droid: droid.dialogSetCurrentProgress(60)
else: print('Listas listas!')
if droid: droid.dialogSetCurrentProgress(90)
else: print('Diccionarios listos!')

ES.muestraInicio("IPASPUDO: J-30619229-8.")
if droid: droid.dialogSetCurrentProgress(95)

sUXD, sCXD = AP.leeValXDefecto()
if droid:
  droid.dialogSetCurrentProgress(100)
  droid.dialogDismiss()

nOp = 11
while True:
  sOpcion = AP.selFuncionInicial(nOp)

  if 'cuota' == sOpcion: CU.cuota(droid)
  elif 'salir' == sOpcion or None == sOpcion: break
  elif isinstance(sOpcion, int) and 0 > int(sOpcion): break
  elif 'cedula' == sOpcion:
    ci, sNombre = COM.valSocio(AP.cig)
    if (0 < ci):
      AP.cig = ci
      COM.mSocio(sNombre, ci)
      bSF = True              # Función seleccionada.
      while bSF:
        bSF = AP.selFuncion(nOp)
  elif 'nombre' == sOpcion:
    ci, sNombre = AP.buscarNombre()
    if (0 < ci):
      if ci != AP.cig:
        COM.mSocio(sNombre, ci)
        AP.cig = ci
      bSF = True            # Función seleccionada.
      while bSF:
        bSF = AP.selFuncion(nOp)
  else:
    func = eval(sOpcion)	# Evaluar contenido de sOpcion; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType): func()	# Si la cadena evaluada es una funcion, ejecutela.
    else: break
# Fin while True

AP.escValXDefecto(sUXD, sCXD)
ES.muestraFin()
# Fin del programa
