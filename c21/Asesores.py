# libPersonas: Modulo para leer socios de IPASPUDO.
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

# Preparar lista de asesores
# id
# cedula
# name
# telefono
# email
# email_c21
# licencia_mls
# fecha_ingreso
# fecha_nacimiento
# sexo
# estado_civil
# profesion
# direccion
# is_admin
# socio
# created_at
# updated_at
def prepararListaDeAsesores(dir=''):
  global lAse, lNAs

  lAse = ES.cargaJson(dir+'asesores.txt')
  if not lAse:
    lAse = []           # Lista de asesores.
    return

  lNAs = []
  for l in lAse:
    if (1 == l['id']): continue    
    lNAs.append([l['name'], l['id']])    
  return
# Funcion prepararListaDeAsesores

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

def asesor(bImp=True):
  global droid    
  global lNAs

  id = FG.selOpcionMenu(lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  resp = ES.siNo(droid, 'propiedades', 'Desea mostrar las propiedades'
                ' de '+ lAse[id-1]['name'], False)
  #print(resp)
  tCap = tCer = 0.00
  nF = nV = tLados = 0
  bImpar = True
  if ('S' == resp): st = PRO.titulo('Captado', 10, 'Cerrado', 10)
  else: st = ''
  for l in PRO.lPro:
    if (40 < len(l)):
      if not (isinstance(l[iIdCap], int)) or not (isinstance(l[iIdCer], int)):
        continue    
      if (id != l[iIdCap]) and (id != l[iIdCer]): continue
      if ('S' != l[iStatu]) and (id == l[iIdCap]):
        try:
          tCap += float(l[iCoCap])    
        except: pass
      if ('S' != l[iStatu]) and (id == l[iIdCer]):
        try:
          tCer += float(l[iCoCer])    
        except: pass
      nF += 1
      if ('S' != l[iStatu]):
        nV += 1
        tLados += l[iLados]
      if ('S' == resp):
        sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
        st += PRO.detalles(l, sColor, True, iCoCap, 10, 27, id,
                            iCoCer, 10, 33, id)
  # Fin for
  st += CO.AMARI + FG.formateaNumero(nF) + ' negociaciones [' +\
        FG.formateaNumero(nV) + ' validas].' + CO.FIN + '\n'

  dic = {'tCap':tCap, 'tCer':tCer, 'tCaptCer':tCap+tCer}
  if bImp:
    if __name__ == '__main__':
      sMsj = ("%sID:%s %2d\n") % (CO.AZUL, CO.FIN, id)
    else: sMsj = ''
    ind  = id - 1
#   sMsj += ("%sCedula de identidad:%s %s\n") % (CO.AZUL, CO.FIN,
#           FG.formateaNumero(lAse[ind]['cedula']))
    sMsj += COM.prepLnMsj(lAse[ind], 'cedula', 1)
    sMsj += COM.prepLnMsj(lAse[ind], 'name')
    sMsj += COM.prepLnMsj(lAse[ind], 'telefono', 3)
    sMsj += COM.prepLnMsj(lAse[ind], 'email')
    sMsj += COM.prepLnMsj(lAse[ind], 'email_c21')
    sMsj += COM.prepLnMsj(lAse[ind], 'licencia_mls')
    sMsj += COM.prepLnMsj(lAse[ind], 'fecha_ingreso', 2)
    sMsj += COM.prepLnMsj(lAse[ind], 'fecha_nacimiento', 2)
    sMsj += COM.prepLnMsj(lAse[ind], 'sexo')
    sMsj += COM.prepLnMsj(lAse[ind], 'estado_civil')
    sMsj += COM.prepLnMsj(lAse[ind], 'profesion')
    sMsj += COM.prepLnMsj(lAse[ind], 'direccion')
    if (lAse[ind]['socio']):
      sMsj += ("%sAsesor socio%s\n") % (CO.AMARI, CO.FIN)

    if (0 < nF): sMsj += st    # Las propiedades donde ha participado el asesor.

    sMsj += COM.prepLnMsj(dic, 'tCap', 1, '22', 2)
    sMsj += COM.prepLnMsj(dic, 'tCer', 1, '22', 2)
    sMsj += COM.prepLnMsj(dic, 'tCaptCer', 1, '12', 2)
    opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
  return ind, opc
# FIN funcion asesor

#Variables globales
iCodCN = COM.iCodCN
iFeRes = COM.iFeRes
iFeFir = COM.iFeFir
iNegoc = COM.iNegoc
iNombr = COM.iNombr
iStatu = COM.iStatu
iMoned = COM.iMoned
iPreci = COM.iPreci
iComis = COM.iComis
iIVA   = COM.iIVA
iLados = COM.iLados
iFRsIv = COM.iFRsIv
iFRcIv = COM.iFRcIv
iPoFra = COM.iPoFra
iFraPR = COM.iFraPR
iPoRCN = COM.iPoRCN
iPoReg = COM.iPoReg
iRegal = COM.iRegal
iIdCap = COM.iIdCap
iNbCap = COM.iNbCap
iPoCap = COM.iPoCap
iCoCap = COM.iCoCap
iPoGer = COM.iPoGer
iCoGer = COM.iCoGer
iIdCer = COM.iIdCer
iNbCer = COM.iNbCer
iPoCer = COM.iPoCer
iCoCer = COM.iCoCer
iNetos = COM.iNetos
iStC21 = COM.iStC21
iRepCN = COM.iRepCN
if __name__ == '__main__':
  prepararListaDeAsesores("../data/")
  PRO.prepararListaDePropiedades("../data/")
  asesor()