# Contacto: clase para manejar los contactos iniciales de la inmobiliaria.
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
          ['Todas los contactos', 'Con.todosContactos'],
          ['Listar contactos por ...', 'Con.LstContPor'],
          ['Buscar un contacto', 'Con.buscCont'],
          ['Estadisticas ...', 'Con.totPor'],
	      ]

class Contacto:
  lCon = []    
  dic = {
        "id":False,
        "cedula":["Cedula de identidad", 'n', "", 0],               # Datos del asesor, como diccionario.
        "name":["Nombre", 's', "", 0],
        "veces_name":["Nombre", 'n', "", 0],
        "user_id":["Contactado por el usuario (asesor)", 's', "", 0],
        "creado":["Fecha contactado, inicialmente", 's', '', 0],
        "telefono":["Telefono", 't', "", 0],
        "veces_telefono":["Telefono", 'n', "", 0],
        "email":["Correo electronico", 's', "", 0],
        "veces_email":["Correo electronico", 'n', "", 0],
        "direccion":["Direccion", 's', "", 0],
        "deseo_id":["El contacto inicial desea", 's', "", 0],
        "tipo_id":["El contacto inicial busca", 's', "", 0],
        "zona_id":["El contacto inicial desea la zona de", 's', "", 0],
        "precio_id":["El precio aprox. del contacto inicial", 's', "", 0],
        "origen_id":["El contacto inicial se entero por", 's', "", 0],
        "resultado_id":["El resultado de este contacto inicial fue", 's', "", 0],
        "fecEve":False,
        "fecha":["Fecha de proximo contacto", 's', "", 0],
        "observaciones":["Observaciones", 's', "", 0],
        "user_actualizo":["Usuario que modifico este contacto", 's', "", 0],
        "fecha_actualizado":["Este contacto incial fue modificado", 's', "", 0],
        "user_borro":["Usuario que borro este contacto", 's', "", 0],
        "fecha_borrado":["Este contacto incial fue borrado", 's', "", 0],
        }

  def __init__(self, id):
    if 0 >= len(Contacto.lCon): 
      print('ERROR: No se ha creado la lista de contactos.')
      return None
    for reg in Contacto.lCon:
      if id == reg['id']: break
    else:
      print('ERROR: No se ha encontrado la llave:' + str(id) +\
            ' en la lista de contactos.')
      return None
    for campo in reg:
      if (campo in ('actualizado', 'borrado')):
        setattr(self, 'fecha_' + campo, reg[campo])
      else: setattr(self, campo, reg[campo])
    '''
    self.id = reg['id']
    self.cedula   = reg['cedula']
    self.name     = reg['name']
    self.veces_name     = reg['veces_name']
    self.user_id = reg['user_id']
    self.creado = reg['creado']
    self.telefono = reg['telefono']
    self.veces_telefono = reg['veces_telefono']
    self.email    = reg['email']
    self.veces_email    = reg['veces_email']
    self.direccion = reg['direccion']
    self.deseo_id = reg['deseo_id']
    self.tipo_id = reg['tipo_id']
    self.zona_id = reg['zona_id']
    self.precio_id = reg['precio_id']
    self.origen_id = reg['origen_id']
    self.resultado_id = reg['resultado_id']
    self.fecEve = reg['fecEve']
    self.observaciones = reg['observaciones']
    self.user_actualizo = reg['user_actualizo']
    self.fecha_actualizado = reg['actualizado']
    self.user_borro = reg['user_borro']
    self.fecha_borrado = reg['borrado']
    '''
  @staticmethod
  def prepararListaDeContactos(dir=''):
    lCon = ES.cargaListaJson(dir+'contactos.txt')
    if not lCon: lCon = []           # Lista de contactos.
    Contacto.lCon = lCon
    return
# Funcion prepararListaDeContactos
  @staticmethod
  def nombre(id):
    for reg in Contacto.lCon:
      if (id == reg['id']):
        return reg['name']
  def gCedula(self):
    return FG.formateaNumero(self.cedula)
  def gTelefono(self):
    return FG.formateaNumeroTelefono(self.telefono)
  def get(self, campo, valorPorDefecto=''):
    return getattr(self, campo, valorPorDefecto)
    #if hasattr(self, campo): return getattr(self, campo)
    #return valorPorDefecto
  def muestra(self, imp=True):
    dic  = Contacto.dic
    sMsj = ''
    for campo in dic:
      if dic[campo] and hasattr(self, campo):
        val  = getattr(self, campo)    
        if ('user_id' == campo):
          sMsj += COM.prepLnCad(dic[campo][0], '[' + str(val) + '] ' +\
                                ASE.nombreAsesor(val))
        elif (campo in ('deseo_id', 'tipo_id', 'zona_id', 'precio_id',\
                        'origen_id', 'resultado_id')):
          func = 'COM.desc'+campo[0:campo.find('_id')].capitalize() # Puedo usar'_', pero '_id' es mas descriptivo.
          func += '(str('+str(val)+'))'
          sMsj += COM.prepLnCad(dic[campo][0], '[' + str(val) + '] ' +\
                                eval(func))
        else: sMsj += COM.prepLnMsj(dic, self, campo)
    if sMsj: opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
  @staticmethod
  def todosContactos():
    return
  # Metodo todosContactos
  @staticmethod
  def LstContPor():
    return
  # Metodo LstContPor
  @staticmethod
  def buscCont():
    return
  # Metodo buscCont
  @staticmethod
  def totPor():
    return
  # Metodo totPor
  @staticmethod
  def contactos():
    global lMenu
    op = ''
    while ('' == op): op = COM.selOpcion(lMenu, 'Menu de contactos')
  # Funcion contactos
# Fin de class Contacto

if __name__ == '__main__':
  Contacto.prepararListaDeContactos("../data/")
  ASE.prepararListaDeAsesores('../data/')
  COM.prepararDiccionarios('../data/')
  print("=> contacto = Contacto(0)")
  contacto = Contacto(0)
  print("=> contacto.muestra()")
  contacto.muestra()
  print("=> contacto = Contacto(1)")
  contacto = Contacto(1)
  print("=> contacto.muestra()")
  contacto.muestra()
  print(Contacto.nombre(2))