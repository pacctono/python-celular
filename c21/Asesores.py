# Asesores: Modulo para manejar los asesores de la inmobiliaria.
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
  from os.path import abspath

import sys
import json
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG, MySQL
from c21 import Comun as COM
from c21 import Propiedades as PRO

bMySQL = MySQL.bMySQL
oMySQL = MySQL.cMySQL()

dMsj = {
        "id":False,
        "cedula":["Cedula de identidad", 'n', "", 0],               # Datos del asesor, como diccionario.
        "name":["Nombre", 's', "", 0],
        "telefono":["Telefono", 't', "", 0],
        "email":["Correo electronico", 's', "", 0],
        "email_c21":["Correo electronico Century 21", 's', "", 0],
        "licencia_mls":["Licencia MLS", 's', "", 0],
        "fecha_ingreso":False,
        "fecIng":["Fecha de ingreso", 'f', "", 0],
        "fecha_nacimiento":False,
        "fecNac":["Fecha de nacimiento", 'f', "", 0],
        "sexo":False,
        "genero":["Sexo", 's', "", 0],
        "estado_civil":False,
        "edoCivil":["Estado civil", 's', "", 0],
        "profesion":["Profesion", 's', "", 0],
        "direccion":["Direccion", 's', "", 0],
        'is_admin':['Este usuario es administrador del sistema', 'b', True, 0],
        'socio':['Este asesor es Socio', 'b', True, 0],
        'activo':['Este asesor no esta activo en la oficina', 'b', False, 0],
        "ladosCaptador":["Total lados captado", 'n', "5", 0],
        "ladosCerrador":["Total lados cerrado", 'n', "5", 0],
        "lados":["Total lados", 'n', "13", 0],
        "pvrCaptador":["Total pvr captador", 'n', "23", 2],
        "pvrCerrador":["Total pvr cerrador", 'n', "23", 2],
        "precioVentaReal":["Total precio de venta real", 'n', "15", 2],
        "comisionCaptador":["Comision total captado", 'n', "22", 2],
        "comisionCerrador":["Comision total cerrado", 'n', "22", 2],
        "comision":["Comision total captado y cerrado", 'n', "12", 2],
        "puntosCaptador":["Total puntos captado", 'n', "22", 2],
        "puntosCerrador":["Total puntos cerrado", 'n', "22", 2],
        "puntos":["Total puntos captado y cerrado", 'n', "12", 2],
        'borrado':False,
        'updated_at':False,
        'actualizado':['Datos del asesor modificados', 's', "", 0],
        'created_at':False,
        'creado':False,
        "tCap":["Total captado", 'n', "22", 2],
        "tCer":["Total cerrado", 'n', "22", 2],
        "tCaptCer":["Total captado y cerrado", 'n', "22", 2],
      }

def prepararListaDeAsesores(dir=''):
  global lAse, lNAs

  lAse = ES.cargaListaJson(dir+'asesores.txt')
  if not lAse:
    lAse = []           # Lista de asesores.
    return

  lNAs = []
  for l in lAse:
    if (1 == l['id']): continue
    lNAs.append([l['name'], l['id']])
  return
# Funcion prepararListaDeAsesores
def nombreAsesor(i, restar=0):
  global lAse

  try: i = int(i) - restar
  except: return 'Indice no es numero'
  if (0 > i) or (len(lAse) <= i):
    return 'Indice(' + str(i) + ') nombr err'
  return lAse[int(i)].get('name', 'Nombre no encontrado')
# Funcion nombreAsesor
def poblarLstAsesores(ci, nb, nu='', fnac='P', ds='No', ex='N'):
      return {'ci':ci, 'nb':nb, 'nu':nu, 'fnac':fnac, 'dsp':ds, 'ex':ex}	# Codigo, desc,
# nu: primera letra del nucleo (socios) o digito (personal).
# fnac: fecha de nacimiento, P: datos desde 'personal';
# dsp: disponibilidad en numero o 'No', si los datos son tomados desde 'personal'.
# ex: extension alta ('A'), baja ('a') o No ('N').
# FIN funcion poblarLstAsesores
def creaLstAsesores():
  dPersona = {}
  archTexto = "persona.txt"
  if not bMySQL:
    try:
      c = -1
      dPer = ES.cargaDicc(archTexto)
      for k,v in dPer.items():
        c = k
        (nb, nu, fnac, ds, ex) = v.split('|')
        dPersona[k] = poblarLstAsesores(k, nb, nu, fnac, ds, ex)
      return dPersona
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
    try:
# Ejecuta el comando SQL.
      cursor.execute(sql)
# Alimneta todas las filas en una lista de listas.
      resultados = cursor.fetchall()
      for fila in resultados:
# Crea diccionario de conceptos.
        dPersona[str(int(fila[0]))] = poblarLstAsesores(str(int(fila[0])),
                                  fila[1], fila[2], fila[3], fila[4], fila[5])
    except:
      print("Imposible crear diccionario de personas.")
# disconnect from server
    oMySQL.cierraCursor(cursor)
    oMySQL.cierraConexion()
  else: print("No se pudo conectar a la Base de Datos.")
  return dPersona
# FIN funcion creaLstAsesores

def calcProxMes(fec=None):
  from datetime import date, timedelta
  from calendar import mdays

  if not fec: fec = date.today()
  enUnMes = fec + timedelta(mdays[fec.month])
  return enUnMes.day, enUnMes.month, enUnMes.year, enUnMes
# FIN funcion proxFecha

def cumpleanos(mostrar=True):
  from datetime import date
  global lAse

  hoy = date.today()
  proxDia, proxMes, proxAno, enUnMes = calcProxMes()
  bImpar = True
  titulo = CO.CYAN + 'Proximos cumpleaneros' + CO.FIN + '\n'
  st = ''
  indices = []
  for l in lAse:
    if not l['fecNac']: continue
    fecNac = l['fecNac']
    anoNac, mesNac, diaNac, dSemNac =\
                              FG.descomponeFecha(l['fecNac'])
    fecCump = date(proxAno, mesNac, diaNac)
    diaSem  = CO.semana[fecCump.weekday()]
    if fecCump == hoy:
      indices.append([l['name'], fecCump])
      if mostrar:
        st += CO.AMARI + l['name'] + ': ' + 'HOY, ' + diaSem + ' ' +\
              fecNac[0:2] + ' de ' + CO.meses[mesNac] + CO.FIN + '\n'
    elif hoy < fecCump <= enUnMes:
      if mostrar:
        sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
        st += sColor + l['name'] + ': ' + diaSem + ' ' +\
              fecNac[0:2] + ' de ' + CO.meses[mesNac] + CO.FIN + '\n'
  if mostrar:
    if (st): st = titulo + st
    else: st = CO.CYAN + 'No hay cumpleaneros proximamente.' +\
                CO.FIN + '\n'
    return ES.imprime(st.rstrip(' \t\n\r'))
  else: return indices
# FIN funcion cumpleanos

def asesor(bImp=True):
  global droid
  global lNAs

  id = FG.selOpcionMenu(lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  if __name__ != '__main__':    # No se ha creado la lista de Propiedades lPro. No he podido.
    resp = ES.siNo(droid, 'propiedades', 'Desea mostrar las propiedades'
                ' de '+ lAse[id-1]['name'], False)
    tCap = tCer = 0.00
    nF = nV = tLados = 0
    bImpar = True
    if ('S' == resp):
      st = PRO.titulo('Comision', 11)
      for l in PRO.lPro:
        if (40 < len(l)):
          if not (isinstance(l['asCapId'], int)) or\
              not (isinstance(l['asCerId'], int)):
            continue
          if (id != l['asCapId']) and (id != l['asCerId']): continue
          if (l['estatus'] in ('P', 'C')) and (id == l['asCapId']):
            try:
              tCap += float(l['capPrbr'])
            except: pass
          if (l['estatus'] in ('P', 'C')) and (id == l['asCerId']):
            try:
              tCer += float(l['cerPrbr'])
            except: pass
          nF += 1
          if (l['estatus'] in ('P', 'C')):
            nV += 1
            tLados += l['lados']
      #    if ('S' == resp):
          sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
          st += PRO.detalles(l, sColor, True, 'capPrbr', 'asCapId',
                                'cerPrbr', 'asCerId', id, 11)
      # Fin for
      st += CO.AMARI + 'Tiene ' + FG.formateaNumero(nF) +\
            ' negociaciones [' + FG.formateaNumero(nV) + ' validas].' +\
            CO.FIN + '\n'
    # Fin if ('S' == resp):
    else: st = ''
  # Fin if __name__ != '__main__':

  if bImp:
    if __name__ == '__main__':
      sMsj = ("%sID:%s %2d\n") % (CO.AZUL, CO.FIN, id)
    else: sMsj = ''
    ind  = id - 1
    dic = lAse[ind]
    for ll in dMsj:
      if not dMsj[ll]: continue
      if 'tCap' == ll: break      # De aqui en adelante no son 'propiedades' (variables) del asesor.
      if 'pvrCaptador' == ll and __name__ != '__main__':    # No se ha creado la lista de Propiedades lPro. No he podido.
        if (0 < nF): sMsj += st    # Si la respuesta sobre las propiedades fue 'Si', Despliega las propiedades donde ha participado el asesor.
      if ll in ('tCap', 'tCer', 'tCapCer'): continue  # Solo para verificar valores.
      sMsj += COM.prepLnMsj(dMsj, dic, ll)

    if not bMovil and __name__ != '__main__':
      dic = {'tCap':tCap, 'tCer':tCer, 'tCaptCer':tCap+tCer}
      sMsj += COM.prepLnMsj(dMsj, dic, 'tCap', 'n', '22', 2)
      sMsj += COM.prepLnMsj(dMsj, dic, 'tCer', 'n', '22', 2)
      sMsj += COM.prepLnMsj(dMsj, dic, 'tCaptCer', 'n', '12', 2)
    opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
  return opc, ind
# FIN funcion asesor

if __name__ == '__main__':
  prepararListaDeAsesores("../data/")
#  PRO.prepararListaDePropiedades("../data/")
  asesor()
#  st = ''
#  i  = 0
#  for k in lAse[0].keys():
#    i += 1
#    st += str(i) + ') ' + k + '\n'
#  ES.imprime(st.rstrip(' \t\n\r'))