# libMySQL: modulo para manipular la conexion a MySQL.
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function   # Para poder usar 'print' de version 3.
if __name__ == '__main__' or 0 > __name__.find('lib'): from config import HOST, USUARIO, PASSWD, BDEDATOS
else: from lib.config import HOST, USUARIO, PASSWD, BDEDATOS

try:
  import MySQLdb	# Este driver solo funciona en python 2.
  bMySQL = True
  bMySQLdb = True
except:
  try:
    import mysql.connector	# Este driver funciona en python 2 y 3.
    from mysql.connector import errorcode
    MySQLdb  = mysql.connector
    bMySQL   = True
    bMySQLdb = False
  except:
    bMySQL = False

class cMySQL(object):
  def __init__(self, servidor=HOST, usuario=USUARIO, passwd=PASSWD, bDeDatos=BDEDATOS):
    self.servidor = servidor
    self.usuario  = usuario
    self.passwd   = passwd
    self.bDeDatos = bDeDatos
# FIN de __init__

  def create_database(self):
    try:
      cursor = self.abreCursor()
      cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.bDeDatos))
    except mysql.connector.Error as err:
      print("Hubo un error creando la base de datos: {}".format(err))
      return False
    else:     # Si no hay una exception. Me parece innecesario, pero, asi no busco al respecto.
      self.cierraCursor(cursor)
      return True

  def conectar(self):
# Open database connection
    if not bMySQL:
      if __name__ == "__main__": print("La libreria de MySQL no esta instalada.")
      return False
    if bMySQLdb:
      try:
        self.cnx = MySQLdb.connect(self.servidor, self.usuario, self.passwd, self.bDeDatos)
        return True
      except:
        print("Error al tratar de conectarse a MySQL usando MySQLdb.")
        print("Servidor: " + self.servidor + ", usuario: " + self.usuario)
        print("Contrasena: " + self.passwd + ", bd: " + self.bDeDatos)
        return False
    else:
      try:
        self.cnx = MySQLdb.connect(host=self.servidor, user=self.usuario,
                                    password=self.passwd)
      except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Error con tu usuario o contraseña.")
        else:
          print(err)
        return False

      try:
        self.cnx.database = self.bDeDatos  
      except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
          if not self.create_database(): return False
          self.cnx.database = self.bDeDatos
        else:
          print(err)
        return False
      else: return True
# FIN de conectar.
  def abreCursor(self):
# prepara un cursor.
    return self.cnx.cursor()
# FIN de abreCursor.
  def cierraCursor(self, cursor):
    cursor.close()
# FIN de cierraCursor.
  def cierraConexion(self):
    self.cnx.close()
# FIN de cierraConexion.

# FIN de la clase cMySQL.

if __name__ == '__main__':
  oMySQL = cMySQL()
  if oMySQL.conectar():
    cursor = oMySQL.abreCursor()
# Prepara la consulta SQL para SELECT registros de la base de datos.
    sql = "SELECT codigo, descripcion, tx_comprobante, nu_sinca, id_nomina, id_automatico \
           FROM conceptos"
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimenta la primera fila en una lista de listas.
      fila = cursor.fetchone()
      print("Primera fila de la tabla conceptos: ",
            fila[0], fila[1], fila[2], fila[3], fila[4], fila[5],
            sep=';', end='\n')
    except:
      print("Problemas accediendo la base de datos de MySQL.")
# desconectarse del servidor
    oMySQL.cierraConexion()
  else: print("Problemas de conexion")

# FIN de la libreria
