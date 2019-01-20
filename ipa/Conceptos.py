# libConceptos: Modulo para leer conceptos de IPASPUDO.
#-*-coding:utf8;-*-
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys
PY3 = 3 == sys.version_info.major
if PY3:
  unicode = str
else:
  input = raw_input

try:
  if __name__ == '__main__': 
    import os
    sys.path.append(os.path.join(os.path.dirname(
                                  os.path.abspath(__file__)), '..'))
  from lib import DIR, bMovil
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
  droid = False

from lib import ES, Const as CO, MySQL

bMySQL = MySQL.bMySQL
oMySQL = MySQL.cMySQL()

def poblarDicConc(co, de, cm='', nu='', no='', au=''):
  return {'cod':co, 'des':de, 'com':cm, 'nus':nu, 'nom':no, 'aut':au}	# Codigo, desc,
# com: 2 primeros digitos comprobante, nu: cod tabla_prestamo,
# no: es concepto de nomina (S/N), au: automatico (S/N).
# FIN funcion poblarDic
def creaDicConceptos():
  dConcepto = {}
  if not bMySQL:
    if __name__ != '__main__' or bMovil: archTexto = "conceptos.txt"
    else: archTexto = "../data/conceptos.txt"
    try:
      c = -1
      dConc = ES.cargaDicc(archTexto)
      for k,v in dConc.items():
        c = k    
        dConcepto[k] = poblarDicConc(k, v)
      return dConcepto
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
          SELECT codigo, descripcion, tx_comprobante, nu_sinca, id_nomina,
                  id_automatico 
          FROM conceptos
          '''
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de conceptos.
        dConcepto[fila[0]] = poblarDicConc(fila[0], fila[1], fila[2],
                                        fila[3], fila[4], fila[5])
    except:
      print("Imposible crear diccionario de conceptos.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dConcepto
# FIN funcion creaDicConceptos

if __name__ == '__main__':
  dConcepto = creaDicConceptos()
  print('dConcepto[511]: ', dConcepto['511'])