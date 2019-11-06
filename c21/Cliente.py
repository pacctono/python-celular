# Cliente: clase para manejar clientes de la inmobiliaria.
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

lMenu = [
          ['Todas los clientes', 'Cli.todosClientes'],
          ['Listar clientes por ...', 'Cli.LstCliPor'],
          ['Buscar un cliente', 'Cli.buscCli'],
          ['Estadisticas ...', 'Cli.totPor'],
	      ]

class Cliente:
  lCli = []    
  dic = {
        "id":False,
        "cedula":["Cedula de identidad", 'n', "", 0],               # Datos del asesor, como diccionario.
        "rif":["Numero de rif", 's', '', 0],
        "name":["Nombre", 's', "", 0],
        "telefono":["Telefono", 't', "", 0],
        "email":["Correo electronico", 's', "", 0],
        "fecNac":["Fecha de nacimiento", 'f', "", 0],
        "direccion":["Direccion", 's', "", 0],
        "observaciones":["Observaciones", 's', "", 0],
        }

  def __init__(self, id):
    if 0 >= len(Cliente.lCli): 
      print('ERROR: No se ha creado la lista de clientes.')
      return None
    for reg in Cliente.lCli:
      if id == reg['id']: break
    else:
      print('ERROR: No se ha encontrado la llave:' + str(id) +\
            ' en la lista de clientes.')
      return None
    for campo in reg:
      if (campo in ('actualizado', 'borrado')):
        setattr(self, 'fecha_' + campo, reg[campo])
      else: setattr(self, campo, reg[campo])
    '''
    self.id = reg['id']
    self.cedula   = reg['cedula']
    self.rif      = reg['rif']
    self.name     = reg['name']
    self.telefono = reg['telefono']
    self.email    = reg['email']
    self.fecNac   = reg['fecNac']
    self.direccion = reg['direccion']
    self.observaciones = reg['observaciones']
    self.user_id = reg['user_id']
    self.fecha_creado = reg['creado']
    self.user_actualizo = reg['user_actualizo']
    self.fecha_actualizado = reg['actualizado']
    self.user_borro = reg['user_borro']
    self.fecha_borrado = reg['borrado']
    '''
  @staticmethod
  def prepararListaDeClientes(dir=''):
    lCli = ES.cargaListaJson(dir+'clientes.txt')
    if not lCli: lCli = []           # Lista de clientes.
    Cliente.lCli = lCli
    return
# Funcion prepararListaDeClientes
  @staticmethod
  def nombre(id):
    for reg in Cliente.lCli:
      if (id == reg['id']):
        return reg['name']
  def gCedula(self):
    return FG.formateaNumero(self.cedula)
  def gTelefono(self):
    return FG.formateaNumeroTelefono(self.telefono)
  def gRif(self):
    return FG.formateaRif(self.rif)
  def get(self, campo, valorPorDefecto=''):
    if hasattr(self, campo): return getattr(self, campo)
    return valorPorDefecto
  def muestra(self, imp=True):
    dic  = Cliente.dic
    sMsj = ''
    for campo in dic:
        if dic[campo] and hasattr(self, campo):
            sMsj += COM.prepLnMsj(dic, self, campo)
    if sMsj: opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
  @staticmethod
  def todosClientes():
    return
  # Metodo todosClientes
  @staticmethod
  def LstCliPor():
    return
  # Metodo LstCliPor
  @staticmethod
  def buscCli():
    return
  # Metodo buscCli
  @staticmethod
  def totPor():
    return
  # Metodo totPor
  @staticmethod
  def clientes():
    global lMenu
    op = ''
    while ('' == op): op = COM.selOpcion(lMenu, 'Menu de clientes')
  # Funcion clientes
# Fin de class Cliente

if __name__ == '__main__':
  Cliente.prepararListaDeClientes("../data/")
#  PRO.prepararListaDePropiedades("../data/")
  cliente = Cliente(0)
  cliente.muestra()
  cliente = Cliente(1)
  cliente.muestra()
  print(Cliente.nombre(2))