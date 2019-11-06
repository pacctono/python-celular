# Turno: clase para manejar turnos de los asesores.
#-*- coding:ISO-8859-1 -*-
from __future__ import print_function # Para poder usar 'print' de version 3.

try:
  if __name__ == '__main__': from . import bMovil
  else: from lib import bMovil
except:
  bMovil = False

if bMovil:
  try:
    import androidhelper as android
  except:
    import android
  droid = android.Android()
else:
  droid = None

import sys
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG
from c21 import Comun as COM
from c21 import Asesores as ASE

lMenu = [
          ['Todas los turnos', 'Tur.todosTurnos'],
          ['Listar turnos por ...', 'Tur.LstTurPor'],
          ['Buscar un turno', 'Tur.buscTur'],
          ['Estadisticas ...', 'Tur.totPor'],
	      ]

class Turno:
  lTur = []    
  dic = {
        "id":False,
        "user_id":["Turno del usuario (asesor)", 's', "", 0],
        "fecha":["Fecha del turno", 'f', "", 0],
        "user_creo":["Usuario (asesor) creador del turno", 's', "", 0],
        "user_actualizo":["Usuario (asesor) modifico el turno", 's', "", 0],
        "user_borro":["Usuario (asesor) borro el turno", 's', "", 0],
        "turnoFecha":False,
        "creado":["Fecha de creacion", 's', '', 0],
        }

  def __init__(self, id):
    if 0 >= len(Turno.lTur): 
      print('ERROR: No se ha creado la lista de turnos.')
      return None
    for reg in Turno.lTur:
      if id == reg['id']: break
    else:
      print('ERROR: No se ha encontrado la llave:' + str(id) +\
            ' en la lista de turnos.')
      return None
    for campo in reg:
      if (campo in ('actualizado', 'borrado')):
        setattr(self, 'fecha_' + campo, reg[campo])
      else: setattr(self, campo, reg[campo])
    '''
    self.id = reg['id']
    self.user_id        = reg['user_id']
    self.fecha          = reg['fecha']
    self.user_creo      = reg['user_creo']
    self.creado         = reg['creado']
    self.user_actualizo = reg['user_actualizo']
    self.user_borro     = reg['user_borro']
    '''
  @staticmethod
  def prepararListaDeTurnos(dir=''):
    lTur = ES.cargaListaJson(dir+'turnos.txt')
    if not lTur: lTur = []           # Lista de turnos.
    Turno.lTur = lTur
    return
# Funcion prepararListaDeTurnos
  @staticmethod
  def nombre(id):
    for reg in Turno.lTur:
      if (id == reg['id']):
        return ASE.nombreAsesor(reg['user_id'])
  def get(self, campo, valorPorDefecto=''):
    if hasattr(self, campo): return getattr(self, campo)
    return valorPorDefecto
  def muestra(self, imp=True):
    dic  = Turno.dic
    sMsj = ''
    for campo in dic:
      if dic[campo] and hasattr(self, campo):
        if (campo in ('user_id', 'user_creo')):
          val  = getattr(self, campo)    
          sMsj += COM.prepLnCad(dic[campo][0], '[' + str(val) + '] ' +\
                                ASE.nombreAsesor(val))
        else: sMsj += COM.prepLnMsj(dic, self, campo)
    if sMsj: opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
  @staticmethod
  def todosTurnos():
    return
  # Metodo todosTurnos
  @staticmethod
  def LstTurPor():
    return
  # Metodo LstTurPor
  @staticmethod
  def buscTur():
    return
  # Metodo buscTur
  @staticmethod
  def totPor():
    return
  # Metodo totPor
  @staticmethod
  def turnos():
    global lMenu
    op = ''
    while ('' == op): op = COM.selOpcion(lMenu, 'Menu de turnos')
  # Funcion turnos
# Fin de class Turno

if __name__ == '__main__':
  ASE.prepararListaDeAsesores('../data/')
  Turno.prepararListaDeTurnos("../data/")
  turno = Turno(0)
  turno.muestra()
  turno = Turno(1)
  turno.muestra()
  print(Turno.nombre(1))