# ipaIper: Modulo para leer conceptos de IPASPUDO.
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
          SELECT r.Cedula AS ci, UPPER(p.Nombre) AS nmb, CONCAT(r.NUCLEO_1,
                  r.NUCLEO_2) AS nuc, p.Nro_Cuenta AS cta,
                  p.FORMA_PAGO AS bco, r.GENERICO_personal AS gen,
                  r.ESPECIFICO_personal AS esp,
                  r.CATEGORIA_personal AS cat,
		              r.CONDICION_LABORAL AS cond,
                  r.DEDICACION_LABORAL AS ded,
                  DATE_FORMAT(r.Fecha_Ingreso, '%d%m%Y') AS fing,
                  TRUNCATE(100*ROUND(p.Sueldo_integral, 2), 0) AS sdi,
                  SUM(TRUNCATE(100*ROUND(n.Cuota, 2), 0)) AS sdo
          FROM udo.rac_SUFIJO r INNER JOIN udo.personal_SUFIJO p
                  ON (p.Cedula = r.Cedula AND r.Sec_clave = '1')
                INNER JOIN udo.nomina_SUFIJO n
                  ON (n.Cedula = p.Cedula AND n.Concepto IN
                  ('101', '106', '107', '108'))
#                  ('101', '102', '103', '104', '105', '106', '107',
#                   '108', '109', '110'))
          WHERE EXISTS
                (SELECT n1.Cedula FROM nomina n1
                 WHERE n1.Cedula = n.Cedula
                 AND   n1.Concepto = '134')
#                       ('134', '511', '562'))
          GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
          ORDER BY 1
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
            'ci':int(fila[0]), 'nmb':fila[1], 'nuc':fila[2],
            'cta':fila[3], 'bco':fila[4], 'gen':fila[5], 'esp':fila[6],
            'cat':fila[7], 'cond':fila[8], 'ded':fila[9],
            'fing':fila[10], 'sdi':fila[11], 'sdo':fila[12]
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
  print('fila ' + str(0) + ': ', lista[0])
  print('fila ' + str(len(lista)) + ': ', lista[len(lista)-1])