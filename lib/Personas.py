#!/usr/bin/python
# personas: Modulo para leer socios de IPASPUDO.
#-*-coding:utf8;-*-
from __future__ import print_function # Para poder usar 'print' de version 3.

try:
  from lib import DIR, LINEA, bMovil
except:
  DIR = './'
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

def poblarDicPersona(ci, nb, nu='', fnac='P', ds='No', ex='N'):
      return {'ci':ci, 'nb':nb, 'nu':nu, 'fnac':fnac, 'dsp':ds, 'ex':ex}	# Codigo, desc,
# nu: primera letra del nucleo (socios) o digito (personal).
# fnac: fecha de nacimiento, P: datos desde 'personal';
# dsp: disponibilidad en numero o 'No', si los datos son tomados desde 'personal'.
# ex: extension alta ('A'), baja ('a') o No ('N').
# FIN funcion poblarDic
def creaDicPersonas():
  dPersona = {}
  archTexto = "persona.txt"
  if not bMySQL:
    try:
      c = -1
      dPer = ES.cargaDicc(archTexto)
      for k,v in dPer.items():
        c = k    
        (nb, nu, fnac, ds, ex) = v.split('|')
        dPersona[k] = poblarDicPersona(k, nb, nu, fnac, ds, ex)
      return dPersona
    except:
      if not bMovil:
        print('Problemas con el archivo de texto: ' + archTexto + '(' + c +
                                                                        ').\n')
      return {}
# Abre la conexion con la base de datos.
  if oMySQL.conectar():
# Prepara una consulta SQL para SELECT registros desde la base de datos.
    sql = '''
          SELECT s.Cedula AS ci, s.Nombre as nb, SUBSTRING(s.Nucleo, 1, 1)
                    as nu,
                 DATE_FORMAT(IFNULL(s.Fecha_nacimiento, '00000000'), '%d%m%Y')
                    as fnac,
                 IFNULL(a.Monto, '0.00') as ds,
                 IF(IFNULL(e.nu_suma_asegurada, 'N')=1250, 'A', 'a') as ex
			    FROM   socios s LEFT JOIN ahorros a ON (a.Cedula = s.Cedula AND
                                                  a.Concepto = '999')
                          LEFT JOIN extension e ON (e.nu_cedula = s.Cedula AND
                                                  e.nu_cedula_carga = s.Cedula)
#			    WHERE  Estatus = 1
			    UNION
			    SELECT p.Cedula AS ci,
                 TRIM(TRAILING '.' FROM TRIM(TRAILING ',' FROM p.Nombre))
                    as nb,
                 Nucleo_1 as nu, 'P' as fnac, 'No' as ds, 'N' as ex
			    FROM   personal p INNER JOIN rac r ON
                    (r.Cedula = p.Cedula AND r.Sec_clave = '1')
			    WHERE  p.Cedula NOT IN
                    (SELECT s.Cedula FROM socios s WHERE s.Cedula = p.Cedula)
			    ORDER BY 1
          '''
# Prepara un cursor.
    cursor = oMySQL.abreCursor()
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de conceptos.
        dPersona[int(fila[0])] = poblarDicPersona(int(fila[0]), fila[1],
                                            fila[2], fila[3], fila[4], fila[5])
    except:
      print("Imposible crear diccionario de personas.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dPersona
# FIN funcion creaDicPersonas

if __name__ == '__main__':
  dPersona = creaDicPersonas()
  print(dPersona[3874555]['ci'], dPersona[3874555]['nb'],
        dPersona[3874555]['fnac'], sep=';')   # Prof. Orlando De La Cruz
  print(dPersona[4299801]['ci'], dPersona[4299801]['nu'],
        dPersona[4299801]['fnac'], dPersona[4299801]['dsp'],
        dPersona[4299801]['ex'], sep=';')
  print(dPersona[4299956]['nu'], dPersona[4299956]['dsp'],
        dPersona[4299956]['ex'], sep=';')     # RUIZ MORENO CARMEN DEL VALLE