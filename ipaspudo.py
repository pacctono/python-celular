#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys, time, types
import json

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
from ipa import ExtensionYServiFun as ESF
from ipa import Nomina as NOM
from ipa import Comun as COM
from lib import ES, Cuota as CU, General as FG

def leeValXDefecto():

  fIpa = ES.abrir("ipaspudo.txt")
  if not fIpa:
    sUXD   = 'ipas'				# Usuario por defecto
    sCXD   = 'ipas'				# Contraseña por defecto
  else:
    try:
      sIpa = fIpa.read()
      lIpa = json.loads(sIpa)
      sUXD = lIpa[0]		# Usuario por defecto
      sCXD = lIpa[1]		# Contraseña por defecto
      cig  = lIpa[2]		# Cedula por defecto. Esta linea es solo para mejorar la vista.
    except: pass
    finally: fIpa.close()
  return cig, sUXD, sCXD
# funcion leeValXDefecto
def escValXDefecto(sUXD, sCXD, cig):

  lIpa = [sUXD, sCXD, cig]
  fIpa = ES.abrir("ipaspudo.txt", 'w')
  if fIpa:
    try: fIpa.write(json.dumps(lIpa))
    except: pass
    finally: fIpa.close()
  else: print("No se grabaron los valores por defecto!")
# funcion escValXDefecto
def selFuncionInicial(nOpciones=6):		# nOpciones: Primeras opciones de lMenu a desplegar.
  ''' Menu desplegado al inicio. nOpciones = 6: <Cuota>, <Cedula>,
    <Nombre> ..... y <Salir>. '''

  return FG.selOpcionMenu(
            COM.lMenu[0:nOpciones] + COM.lMenu[(len(COM.lMenu)-1):], 'Inicio')
# Funcion selFuncionInicial(nOpciones)
def selFuncion(ci, nOpcion=6):
  ''' Menu desplegado al suministrar una cedula o al encontrar la cedula de una
      parte de un nombre suministrado.
      Eliminados: ['Calcular cuota', 'cuota'], ['Cedula del socio', 'cedula'],
      ['Buscar cedula del socio', 'nombre'], ['Cheques', 'cheque'],
      ['Deposito por fecha', 'depositos'] '''

  lNuevoMenu = COM.lMenu[nOpcion:(len(COM.lMenu)-1)]+[['Volver', '-11']]	# lMenu sin las opciones generales + la opcion 'Volver'.
  sTitulo    = str(ci) + ':' + COM.nombreSocio(COM.mNombre(ci))	# Titulo a desplegar con las opciones.
  while True:
    try:
      func = eval(FG.selOpcionMenu(lNuevoMenu, sTitulo))	# Evaluar contenido de res['name']; el cual, debe ser una funcion conocida.
    except:
      return False
    while True:
      if isinstance(func, types.FunctionType):
        opc = func(ci)	    # Si la cadena evaluada es una funcion, ejecutela.
        if FG.esEntero(opc): opc = str(opc)
        if '' == opc or None == opc or not opc.isdigit() or (opc.isdigit() and
                        (0 > int(opc) or len(lNuevoMenu) <= int(opc))): break
        func = eval(lNuevoMenu[int(opc)][1])
      else: return False
# Funcion selFuncion

esperar = 'Espere un momento, por favor...'
if droid:
  droid.dialogCreateHorizontalProgress('IPASPUDO', esperar, 100)
  droid.dialogShow()
  droid.dialogSetCurrentProgress(15)
else: print(esperar)
AP.prepararListasDeTrabajo()
ESF.prepararListasDeTrabajo()
if droid: droid.dialogSetCurrentProgress(60)
else: print('Listas listas!')
COM.prepararDiccionariosDeTrabajo()
if droid: droid.dialogSetCurrentProgress(90)
else: print('Diccionarios listos!')

ES.muestraInicio("IPASPUDO: J-30619229-8.")
if droid: droid.dialogSetCurrentProgress(95)

cig, sUXD, sCXD = leeValXDefecto()
if droid:
  droid.dialogSetCurrentProgress(100)
  droid.dialogDismiss()

nOp = 11
while True:
  sOpcion = selFuncionInicial(nOp)

  if 'cuota' == sOpcion: CU.cuota(droid)
  elif 'salir' == sOpcion or None == sOpcion: break
  elif isinstance(sOpcion, int) and 0 > int(sOpcion): break
  elif 'cedula' == sOpcion:
    ci, sNombre = COM.valSocio(cig)
    if (0 < ci):
      cig = ci
      COM.mSocio(sNombre, ci)
      selFuncion(ci, nOp)
  elif 'nombre' == sOpcion:
    ci, sNombre = COM.buscarNombre()
    if (0 < ci):
      if ci != cig:
        COM.mSocio(sNombre, ci)
        cig = ci
      selFuncion(ci, nOp)
  else:
    func = eval(sOpcion)	# Evaluar contenido de sOpcion; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType): func()	# Si la cadena evaluada es una funcion, ejecutela.
    else: break
# Fin while True

escValXDefecto(sUXD, sCXD, cig)
ES.muestraFin()
# Fin del programa