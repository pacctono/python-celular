# Agenda: clase para manejar la agenda de los asesores.
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

class Agenda:
  lAge = []    
  dic = {
        "user_id":["Agenda del usuario (asesor)", 's', "", 0],
        "contacto_id":False,
        "fecha":["Fecha del evento", 'f', "", 0],
        "fecEve":False,
        "descripcion":["Descripcion de la cita", 's', "", 0],
        "name":["Nombre de la persona a contactar", 's', "", 0],
        "telefono":["Telefono de la persona a contactar", 's', "", 0],
        "direccion":["Direccion de la persona a contactar", 's', "", 0],
        "email":["Correo de la persona a contactar", 's', "", 0],
        }

  def __init__(self, index):  # En este caso Agenda es una vista y no tiene la llave 'id'.
    if 0 >= len(Agenda.lAge): 
      print('ERROR: No se ha creado la lista de agendas.')
      return None
    if 0 > index or index > len(Agenda.lAge):
      print('ERROR: Esta llave:' + str(index) + 'esta fuera de rango.')
      return None
    reg = Agenda.lAge[index]
    self.user_id     = reg['user_id']
    self.contacto_id = reg['contacto_id']
    self.fecha       = reg['fecha']
    self.fecEve      = reg['fecEve']
    self.descripcion = reg['descripcion']
    self.name        = reg['name']
    self.telefono    = reg['telefono']
    self.direccion   = reg['direccion']
    self.email       = reg['email']
  @staticmethod
  def prepararListaDeAgendas(dir=''):
    lAge = ES.cargaListaJson(dir+'agendas.txt')
    if not lAge: lAge = []           # Lista de agendas.
    Agenda.lAge = lAge
    return
# Funcion prepararListaDeAgendas
  @staticmethod
  def nombre(index):
    if 0 <= index < len(Agenda.lAge):
      reg = Agenda.lAge[index]
      return ASE.nombreAsesor(reg['user_id'])
  def get(self, campo, valorPorDefecto=''):
    if hasattr(self, campo): return getattr(self, campo)
    return valorPorDefecto
  def muestra(self, imp=True):
    dic  = Agenda.dic
    sMsj = ''
    for campo in dic:
      if dic[campo] and hasattr(self, campo):
        if campo == 'user_id':
          val  = getattr(self, campo)    
          sMsj += COM.prepLnCad(dic[campo][0], '[' + str(val) + '] ' +\
                                ASE.nombreAsesor(val))
        else: sMsj += COM.prepLnMsj(dic, self, campo)
    if sMsj: opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
# Fin de class Agenda

if __name__ == '__main__':
  ASE.prepararListaDeAsesores('../data/')
  agenda = Agenda(0)
  Agenda.prepararListaDeAgendas("../data/")
  agenda.muestra()
  agenda = Agenda(1)
  agenda.muestra()
  print(Agenda.nombre(1))