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
        if dic[campo]:
            sMsj += COM.prepLnMsj(dic, self, campo)
    opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
# Fin de class Cliente

if __name__ == '__main__':
  Cliente.prepararListaDeClientes("../data/")
#  PRO.prepararListaDePropiedades("../data/")
  lCli = Cliente.lCli
  cliente = Cliente(0)
  if None != cliente: cliente.muestra()
  print(Cliente.nombre(1))