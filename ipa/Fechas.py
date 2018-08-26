# libFechas: Modulo para leer fechas de control de IPASPUDO.
#-*-coding:utf8;-*-
from __future__ import print_function # Para poder usar 'print' de version 3.

try:
  if __name__ == '__main__': from . import bMovil
  else: from lib import bMovil
except:
  bMovil = False

from datetime import datetime
from time import strftime
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

def poblarDicFechas(md, fec, hor='00:00:00'):
  return {'mod':md, 'fec':fec, 'hor':hor}         # Codigo, fecha, hora.
# mod: Modulo ('Sinca', 'Actualizacion', 'Prestamos', ...)
# fec y hor: Fecha y hora de actualización del módulo.
# FIN funcion poblarDic
def creaDicFechas():
  dFecha = {}
  archTexto = "control.txt"
  if not bMySQL:
    try:
      c = -1
      dFec = ES.cargaDicc(archTexto)
      for k,v in dFec.items():
        c = k    
        hor = '00:00:00'
        if 'Sinca' == k:
          fecha = datetime.strptime(v, 'ACTUALIZADO Al: %d/%m/%Y %H:%M:%S')
          hor = fecha.strftime('%H:%M:%S')
        elif 'Actualizacion' == k:
          fecha = datetime.strptime(v, '%Y-%m-%d')
        elif 'Prestamos' == k:
          fecha = datetime.strptime(v, '1 %Y-%m-%d')
        elif 'Extension' == k:
          fecha = datetime.strptime(v.split(' ')[3], '%Y-%m-%d')
        elif 'Nomina' == k:
          fecha = datetime.strptime(v, 'ACTUALIZADA AL: %d/%m/%Y')
        else: continue
        fec = fecha.strftime('%Y%m%d')
        dFecha[k] = poblarDicFechas(k, fec, hor)
      return dFecha
    except Exception as er:
      if not bMovil:
        print('Problemas con el archivo de texto: ' + archTexto + '(' + c +
                                                                        ').\n')
        print('ERROR: ', er)
      return {}
# Abre la conexion con la base de datos.
  if oMySQL.conectar():
# Prepara un cursor.
    cursor = oMySQL.abreCursor()
# Prepara una consulta SQL para SELECT registros desde la base de datos.
    sql = '''
          SELECT tx_modulo AS md, DATE_FORMAT(fe_fecha, '%d%m%Y') AS fec,
                  fe_hora AS hor
			    FROM   control
			    UNION
			    SELECT 'Nomina' AS md, CONCAT(SUBSTRING(Fecha FROM 5 FOR 4),
                                  SUBSTRING(Fecha FROM 3 FOR 2),
                                  SUBSTRING(Fecha FROM 1 FOR 2)) AS fec,
                                  '00:00:00' AS hor
			    FROM   controlpersonal
          '''
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de bancos.
        dFecha[fila[0]] = poblarDicFechas(fila[0], fila[1], fila[2])
    except:
      print("Imposible crear diccionario de bancos.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dFecha
# FIN funcion creaDicFechas

if __name__ == '__main__':
  dFecha = creaDicFechas()
  print("dFecha['Sinca']: ", dFecha['Sinca'])