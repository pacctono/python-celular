#!/usr/bin/python
# conceptos: Modulo para leer conceptos de IPASPUDO.
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
AMARI = CO.color.YELLOW	# Primer titulo. Identifica la fecha de actualizacion de los datos.
CYAN  = CO.color.CYAN		# Identificacion del socio.
AZUL  = CO.color.BLUE		# Identificacion de los datos.
VERDE = CO.color.GREEN	# Linea final (totales).
PURPURA = CO.color.PURPLE	# Linea final (total de prestamos).
NEGRITA = CO.color.BOLD	# Negrita
ROJO  = CO.color.RED		# Linea de error.
SUBRAYADO  = CO.color.UNDERLINE	# Subrayado
FIN   = CO.color.END

bMySQL = MySQL.bMySQL
oMySQL = MySQL.cMySQL()

if not bMovil:
  def abre(aNb, modo='r', codigo = 'latin-1', bImprimir = False):
    'Abre para leer, el archivo cuyo nombre es el valor de aNb'
    global DIR
    aNb = DIR + aNb
    try:
#      f = open(aNb, mode=modo, encoding=codigo)
      f = open(aNb, mode=modo)
      if (bImprimir): print(aNb + " archivo abierto.")
      return f
    except:
      if (bImprimir):
        print(AMARI + "ERROR ABRIENDO: " + FIN + aNb)
        print(AMARI + "os.path.abspath(aNb): " + FIN + abspath(aNb))
      return False
# FIN funcion abre
def poblarDicConc(co, de, cm='', nu='', no='', au=''):
  return {'cod':co, 'des':de, 'com':cm, 'nus':nu, 'nom':no, 'aut':au}	# Codigo, desc,
# com: 2 primeros digitos comprobante, nu: cod tabla_prestamo,
# no: es concepto de nomina (S/N), au: automatico (S/N).
# FIN funcion poblarDic
def creaDicConceptos():
  dConc = {}
  if not bMySQL:
    try:
      if bMovil:
        dConcepto = ES.cargaDicc("conceptos.txt")
        for k,v in dConcepto.items():
       	  dConc[k] = poblarDicConc(k, v)
      else:
#        f = abre("conceptos.txt", bImprimir = True)
        f = abre("conceptos.txt")
        if not f:
          print('Problemas para abrir el archivo de texto.\n')
          return {}
        for linea in f:
          try:
            k, v,  cm, nu, no, au = linea.rstrip().split(';')
            dConc[k] = poblarDicConc(k, v,  cm, nu, no, au)
          except:
            print('Problemas para leer el archivo.\n')
            continue
        else: f.close()
      return dConc
    except:
      if not bMovil: print('Problemas con el archivo de texto.\n')
      return {}
# Abre la conexion con la base de datos.
  if oMySQL.conectar():
# Prepara un cursor.
    cursor = oMySQL.abreCursor()
# Prepara una consulta SQL para SELECT registros desde la base de datos.
    sql = '''SELECT codigo, descripcion, tx_comprobante, nu_sinca, 
                  id_nomina, id_automatico 
           FROM conceptos'''
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de conceptos.
        dConc[fila[0]] = poblarDicConc(fila[0], fila[1], fila[2], fila[3],
                                       fila[4], fila[5])
    except:
      print("Imposible crear diccionario de conceptos.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dConc
# FIN funcion creaDicConceptos

if __name__ == '__main__':
  dConc = creaDicConceptos()
  print(dConc[u'511'])