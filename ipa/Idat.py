# libConceptos: Modulo para leer conceptos de IPASPUDO.
#-*- coding:ISO-8859-1 -*-
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

def poblarLista(sufijoNomina):
  lista = []
  if not bMySQL:
    print('NO HAY CONEXIÓN A MySQL.')
    return lista
# Abre la conexion con la base de datos.
  if oMySQL.conectar():
# Prepara un cursor.
    cursor = oMySQL.abreCursor()
# Prepara una consulta SQL para SELECT registros desde la base de datos.
    sql = '''
          SELECT n.Cedula AS ci, n.Concepto AS cct,
                 TRUNCATE(100*ROUND(n.valor_fijo, 2), 0) AS vf,
                 TRUNCATE(100*ROUND(n.valor_variable, 2), 0) AS vv
          FROM   udo.nomina_SUFIJO n INNER JOIN ipaspudo.conceptos c ON
                        (c.Codigo = n.Concepto AND c.id_nomina = 'S')
                  INNER JOIN udo.personal_SUFIJO USING (Cedula)
          WHERE  n.Valor_fijo != 0 OR n.Valor_variable != 0
          ORDER BY n.Cedula, n.Concepto
          '''
    sql = sql.replace('SUFIJO', sufijoNomina)
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      if list == type(resultados):
        for fila in resultados:
# Crea lista de registros.
          lista.append({
            'ci':int(fila[0]), 'cct':fila[1], 'vf':fila[2],
            'vv':fila[3]
          })
      else:
        print("Error: %s, sufijo: %s" % (resultados, sufijoNomina))
    except:
      print("Imposible crear lista de filas. Sufijo: ", sufijoNomina)
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return lista
# FIN funcion poblarLista

if __name__ == '__main__':
  if 1 < len(sys.argv): sufijo = sys.argv[1]
  else: sufijo = '2018_12'
  lista = poblarLista(sufijo)
  for l in lista:
    if 4299801 == l['ci']: print('PC:', l)
  print('fila ' + str(len(lista)) + ': ', lista[len(lista)-1])