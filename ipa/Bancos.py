# libBancos: Modulo para leer bancos de IPASPUDO.
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
  from os.path import abspath

if __name__ == '__main__': import ES, Const as CO, MySQL
else: from lib import ES, Const as CO, MySQL

bMySQL = MySQL.bMySQL
oMySQL = MySQL.cMySQL()

def poblarDicBancos(co, de, act='', cta='', sdo=''):
  return {'cod':co, 'des':de, 'act':act, 'cta':cta, 'sdo':sdo}	# Codigo, desc,
# com: 2 primeros digitos comprobante, nu: cod tabla_prestamo,
# no: es concepto de nomina (S/N), au: automatico (S/N).
def creaDicBancos():
  dBanco = {}
  archTexto = "bancos.txt"
  if not bMySQL:
    try:
      c = -1
      dBanc = ES.cargaDicc(archTexto)
      for k,v in dBanc.items():
        c = k    
        dBanco[k] = poblarDicBancos(k, v)
      return dBanco
    except:
      if not bMovil:
        print('Problemas con el archivo de texto: ' + archTexto + '(' + c +
                                                                        ').\n')
      return {}
# Abre la conexion con la base de datos.
  if oMySQL.conectar():
# Prepara un cursor.
    cursor = oMySQL.abreCursor()
# Prepara una consulta SQL para SELECT registros desde la base de datos.
    sql = '''
          SELECT nu_banco, tx_descripcion, id_activo, tx_cuenta, nu_saldo_final
          FROM bancos
          '''
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de bancos.
        dBanco[str(fila[0])] = poblarDicBancos(str(fila[0]), fila[1],
                                                  fila[2], fila[3], fila[4])
    except:
      print("Imposible crear diccionario de bancos.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dBanco
# FIN funcion creaDicBancos

if __name__ == '__main__':
  dBanco = creaDicBancos()
  print('dBanco[1]: ', dBanco['1'])
