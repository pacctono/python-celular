#!/usr/bin/python3
#-*- coding:ISO-8859-1 -*-
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

from c21 import Propiedades as PRO
from c21 import Comun as COM
from c21 import Asesores as ASE
from c21.Contacto import Contacto as Con
from c21.Cliente import Cliente as Cli
from c21.Turno import Turno as Tur
from c21.Agenda import Agenda as Age
from c21 import Comisiones as CMS
from lib import ES, Cuota as CU, General as FG

lMenu = [
          ['Calcular cuota', 'cuota'],                  # 0
          ['Calcular comision', 'comisiones'],          # 1
          ['Actualizar datos', 'COM.actualizar'],
          ['Cumpleaneros', 'ASE.cumpleanos'],           # 3
          ['Asesor', 'ASE.asesor'],
          ['Propiedades', 'PRO.propiedades'],
          ['Contactos', 'Con.contactos'],
          ['Clientes', 'Cli.clientes'],
          ['Turnos', 'Tur.turnos'],
          ['Agenda', 'Age.agendas'],
#          ['Todas las propiedades', 'PRO.propiedades'],
#          ['Listar propiedades por ...', 'PRO.LstPropPor'],
#          ['Buscar una propiedad', 'PRO.buscProp'],
#          ['Estadisticas ...', 'PRO.totPor'],
          ['Salir', 'salir']
	      ]

def leeValXDefecto():

  fC21 = ES.abrir("c21pr.txt")
  if not fC21:
    cog    = 0				  # Codigo inicial
    sUXD   = 'c21pr'		# Usuario por defecto
    sCXD   = 'c21pr'		# Contraseña por defecto
  else:
    try:
      sC21 = fC21.read()
      lC21 = json.loads(sC21)
      sUXD = lC21[0]		# Usuario por defecto
      sCXD = lC21[1]		# Contraseña por defecto
      cog  = lC21[2]		# Codigo por defecto. Esta linea es solo para mejorar la vista.
    except: pass
    finally: fC21.close()
  return cog, sUXD, sCXD
# funcion leeValXDefecto
def escValXDefecto(sUXD, sCXD, cog):

  lC21 = [sUXD, sCXD, cog]
  fC21 = ES.abrir("c21pr.txt", 'w')
  if fC21:
    try: fC21.write(json.dumps(lC21))
    except: pass
    finally: fC21.close()
  else: print("No se grabaron los valores por defecto!")
# funcion escValXDefecto
def selFuncionInicial(nOpciones=7):		# nOpciones: Primeras opciones de lMenu a desplegar.
  ''' Menu desplegado al inicio. nOpciones = 6: <Cuota>, <Comisiones>,
    <Nombre> ..... y <Salir>. '''

  return FG.selOpcionMenu(
            lMenu[0:nOpciones] + lMenu[(len(lMenu)-1):], 'Inicio')
# Funcion selFuncionInicial(nOpciones)
#def selFuncion(ci, nOpcion=6):
#  ''' Menu desplegado al suministrar un codigo o al encontrar el codigo de una
#      parte de un nombre suministrado.
#  '''
#  lNuevoMenu = lMenu[nOpcion:(len(lMenu)-1)]+[['Volver', '-11']]	# lMenu sin las opciones generales + la opcion 'Volver'.
#  sTitulo    = str(ci) + ':' + COM.nombreProp(COM.mNombre(ci))	# Titulo a desplegar con las opciones.
#  while True:
#    try:
#      func = eval(FG.selOpcionMenu(lNuevoMenu, sTitulo))	# Evaluar contenido de res['name']; el cual, debe ser una funcion conocida.
#    except:
#      return False
#    while True:
#      if isinstance(func, types.FunctionType):
#        opc = func(ci)	    # Si la cadena evaluada es una funcion, ejecutela.
#        if FG.esEntero(opc): opc = str(opc)
#        if '' == opc or None == opc or not opc.isdigit() or (opc.isdigit() and
#                        (0 > int(opc) or len(lNuevoMenu) <= int(opc))): break
#        func = eval(lNuevoMenu[int(opc)][1])
#      else: return False
# Funcion selFuncion
def cargar(mostrar=False, esperar='Espere un momento, por favor...'):
  global control

  if mostrar:    
    if droid:
      droid.dialogCreateHorizontalProgress('Century21 Puente Real', esperar, 100)
      droid.dialogShow()
      droid.dialogSetCurrentProgress(15)
    else: print(esperar)
  Con.prepararListaDeContactos()
  Cli.prepararListaDeClientes()
  Age.prepararListaDeAgendas()
  Tur.prepararListaDeTurnos()
  ASE.prepararListaDeAsesores()
  PRO.prepararListaDePropiedades()
  PRO.prepararListas()      # totales en propiedades.
  if mostrar:    
    if droid: droid.dialogSetCurrentProgress(60)
    else: print('Listas listas!')
  COM.prepararDiccionarios()
  fc = open(DIR + COM.CONTROL, 'r')
  if fc: control = fc.read()
  else: control = ''
  if mostrar:    
    if droid: droid.dialogSetCurrentProgress(95)
    else: print('Diccionarios listos!')
  if droid and mostrar: FG.limpiarPantalla()
# Funcion cargar

cargar(True)
ES.muestraInicio("Century21 Puente Real: J-40589955-7.")
print(control)
if droid: droid.dialogSetCurrentProgress(98)

cog, sUXD, sCXD = leeValXDefecto()
if droid:
  droid.dialogSetCurrentProgress(100)
  droid.dialogDismiss()

nOp = len(lMenu) - 1
while True:
  sOpcion = selFuncionInicial(nOp)

  if 'cuota' == sOpcion: CU.cuota(droid)
  elif 'comisiones' == sOpcion: CMS.comisiones(droid)
  elif 'salir' == sOpcion or None == sOpcion: break
  elif isinstance(sOpcion, int) and 0 > int(sOpcion): break
  else:
    func = eval(sOpcion)	# Evaluar contenido de sOpcion; el cual, debe ser una funcion conocida.
    if isinstance(func, types.FunctionType):
      if bMovil: FG.limpiarPantalla()     # Solo limpia pantalla, si se ejecuta desde un movil.
      tecla = func()	# Si la cadena evaluada es una funcion, ejecutela.
      if (0 <= sOpcion.find('actualizar')): cargar()
      try:
        if type(tecla) in (list, tuple): tecla = tecla[0]
      except IndexError:
        print(type(tecla), tecla)
        break
      if ('s' == tecla): break
    else: break
# Fin while True

escValXDefecto(sUXD, sCXD, cog)
ES.muestraFin()
# Fin del programa
