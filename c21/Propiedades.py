# Propiedades: Modulo de Propiedades para inmobiliaria.
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

import sys, types
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG
from c21 import Comun as COM
from c21 import Asesores as ASE
from c21 import Cliente as Cli

lMenu = [
          ['Todas las propiedades', 'PRO.todasPropiedades'],
          ['Listar propiedades por ...', 'PRO.LstPropPor'],
          ['Buscar una propiedad', 'PRO.buscProp'],
          ['Estadisticas ...', 'PRO.totPor'],
	      ]
lMenuLstPro = [
          ['Propiedades X Estatus', 'PRO.lstXEstatus'],
          ['Propiedades X Asesor', 'PRO.lstXAsesor'],
          ['Propiedades X Mes', 'PRO.lstXMes'],
        ]
lMenuProEsp = [
          ['Propiedades X Estatus', 'PRO.xEstatus'],
          ['Propiedades X Nombre', 'PRO.xNombre'],
          ['Propiedades X Asesor', 'PRO.xAsesor'],
          ['Codigo de casa nacional', 'PRO.xCodigo'],
          ['Reporte en casa nacional', 'PRO.xReporte'],
        ]
lMenuTot = [
          ['Totales X Asesor', 'PRO.totAsesor'],
          ['Totales X Mes', 'PRO.totMes'],
          ['Totales X Estatus', 'PRO.totEst'],
          ['Totales X Asesor X Mes', 'PRO.totAsesorMes'],
          ['Totales X Mes X Asesor', 'PRO.totMesAsesor'],
          ['Totales generales', 'PRO.totales'],
        ]
dMsj = {
        'id':False,
        'codigo':['Codigo MLS', 's', '', 0],
        'nombre':["Nombre", 's', "", 0],
        'negoc':['Tipo de negociacion', 's', '', 0],
        'fecRes':['Fecha de reserva', 'f', '', 0],
        'fecFir':['Fecha de la firma', 'f', '', 0],
        'estatus':['Estatus', 's', '', 0],
        'exclu':['Exclusividad', 'b', True, 0],
        'tipo_id':['Tipo', 's', '', 0],
        'metraje':['Metraje', 'n', 7, 2],
        'habits':['Habitaciones', 'n', 3, 0],
        'banos':['Ba#os', 'n', 2, 0],
        'niveles':['Niveles', 'n', 3, 0],
        'puestos':['Puestos de estacionamiento', 'n', 3, 0],
        'anoc':['A#o de construccion', 'n', 4, 0],
        'caracteristica_id':['Caracteristicas', 's', '', 0],
        'descr':['Descripcion', 's', '', 0],
        'direc':['Direccion', 's', '', 0],
        'ciudad_id':['Ciudad', 's', '', 0],
        'codPos':['Codigo postal', 's', '', 0],
        'municipio_id':['Municipio', 's', '', 0],
        'estado_id':['Estado', 's', '', 0],
        'cliente_id':['Cliente', 's', '', 0],
        'user_id':['Usuario creador', 's', '', 0],
        'moneda':False,
        'precio':['Precio', 'm', 10, 2],
        'comision':['Porcentaje de la comision', 'p', 5, 2],
        'iva':['Impuesto al valor agregado', 'p', 5, 2],
        'lados':['Lados', 'n', 1, 0],
        'user_actualizo':False,
        'user_borro':False,
        'pcFrq':['Porcentaje para franquicia', 'p', 5, 3],
        'pcReCaNa':['Porcentaje reportado a Casa Nacional', 'p', 5, 3],
        'pcRega':['Porcentaje de Regalia', 'p', 5, 3],
        'pcCom':['Porcentaje a Compartir entre Captador y Cerrador', 'p', 5, 3],
        'pcCap':['Porcentaje del asesor Captador', 'p', 5, 3],
        'pcGer':['Porcentaje del Gerente', 'p', 5, 3],
        'pcCer':['Porcentaje del asesor Cerrador', 'p', 5, 3],
        'pcBonif':['Porcentaje de bonificacion', 'p', 5, 3],
        'comBanc':['Comision bancaria', 'n', 7, 2],
        'nroRec':['Numero de recibo', 's', '', 0],
        'asCapId':False,
        'asCap':['Asesor Captador', 's', '', 0],
        'asCerId':False,
        'asCer':['Asesor Cerrador', 's', '', 0],
        'pagGer':['Pago al Gerente', 's', '', 0],
        'factGer':['Factura del Gerente', 's', '', 0],
        'pagAses':['Pago a asesores', 's', '', 0],
        'factAse':['Factura asesores', 's', '', 0],
        'pagOtOf':['Pago a otra oficina', 's', '', 0],
        'PagCaNa':['Pagado a Casa Nacional', 'b', True, 0],
        'estaC21':['Estatus en el sistema Century 21', 's', '', 0],
        'repCaNa':['Reporte de Casa Nacional', 's', '', 0],
        'comens':['Comentarios', 's', '', 0],
        'factAyS':['Factura A&S', 's', '', 0],
        'resSIva':['Monto de reserva sin IVA', 'm', 8, 2],
        'resCIva':['Monto de reserva con IVA', 'm', 8, 2],
        'comCIva':['Monto compartido con IVA', 'm', 8, 2],
        'comSIva':['Monto compartido sin IVA', 'm', 8, 2],
        'frqSIva':['Monto de reserva de la franquicia sin IVA', 'm', 8, 2],
        'frqCIva':['Monto de reserva de la franquicia con IVA', 'm', 8, 2],
        'frqPaRe':['Monto de la franquicia a pagar reservada', 'm', 7, 2],
        'regalia':['Monto de Regalia', 'm', 8, 2],
        'sanaf5pc':['Sanaf 5%', 'm', 15, 2],
        'ofBrRe':['Monto de la Oficina Bruto Real', 'm', 8, 2],
        'baHoSoc':['Base para honorarios de socio', 'm', 9, 2],
        'baPaHon':['Base para pagar honorarios', 'm', 12, 2],
        'bonific':['Monto de bonificacion', 'm', 17, 2],
        'capPrbr':['Monto de comision al Captador Prbr', 'm', 8, 2],
        'cerPrbr':['Monto de comision al Cerrador Prbr', 'm', 8, 2],
        'gerente':['Monto de comision al Gerente', 'm', 14, 2],
        'ingNeOf':['Monto del ingreso neto de la oficina', 'm', 6, 2],
        'pvrCap':['Precio de Venta Real para el Captador', 'm', 10, 2],
        'pvrCer':['Precio de Venta Real para el Cerrador', 'm', 10, 2],
        'prVeRe':['Precio de Venta Real para la Oficina', 'm', 11, 2],
        'ptsCap':['Puntos del captador', 'n', 9, 2],
        'ptsCer':['Puntos del cerrador', 'n', 9, 2],
        'puntos':['Puntos de la oficina', 'n', 8, 2],
        'borrado':False,
        'creado':False,
        'actualizado':False
      }

def prepararListaDePropiedades(dir='', mostrarSalida=False):
  global lPro

  lPro = ES.cargaListaJson(dir+'propiedads.txt')
  if not lPro: lPro = []
  lAse = ASE.lAse
  for i in range(0, len(lPro)):
    if not (isinstance(lPro[i]['asCapId'], int)) or\
       not (isinstance(lPro[i]['asCerId'], int)):
      continue
# En las proximas cuatro lineas, me aseguro de que la llave ascap/ascer contenga el nombre correcto.
    if (1 < lPro[i]['asCapId']):                         # El asesor captador es de la oficina.
      lPro[i]['asCap'] = lAse[lPro[i]['asCapId']-1]['name']   # Colocar el nombre del asesor captador de la oficina.
    if (1 < lPro[i]['asCerId']):                         # El asesor cerrador es de la oficina.
      lPro[i]['asCer'] = lAse[lPro[i]['asCerId']-1]['name']   # Colocar el nombre del asesor cerrador de la oficina.
  if mostrarSalida: print('**** Salida prepararListaDePropiedades() *')
# Funcion prepararListaDePropiedades
def titulo(*par):
  tCol = ''
  if (2 <= len(par)):
    for n in range(0, len(par), 2):
      tCol += par[n].rjust(par[n+1])
  return CO.AZUL + "Codigo".ljust(7) + "Fechas Res Firma".ljust(18) +\
            " Nombre".ljust(21) + "L".rjust(2) +\
            "Precio".rjust(11) + "P Venta Real".rjust(14) +\
            tCol + CO.FIN + "\n"
# Funcion titulo
def detalles(l, sColor, bCaidas=True, *col):
#  print(l)    
  if (10 == len(l['fecRes'])): fr = l['fecRes'][0:6] + l['fecRes'][-2:]
  else: fr = ''.ljust(8)
  if (10 == len(l['fecFir'])): ff = l['fecFir'][0:6] +l['fecFir'][-2:]
  else: ff = ''.ljust(8)
#  print(col)
  if (l['estatus'] in ('S')):
    if not bCaidas: return ''
    sColor = CO.ROJO
# Cada columna a agregar podria tener dos o seis campos; dos:
# indice de la lista del campo a agregar, longitud de ese campo.
# Si se agregan 6 valores: se compara el segundo (indice de la lista)
# con el valor en el quinto parametro. Si la comparacion es verdadera;
# el campo identificacado en el 1er valor se sumara; luego, se compara
# el cuarto con el quinto. Si la comparacion es verdadera; el campo
# identificacado en 3er valor se sumara. El sexto valor es la longitud.
  sCol = ''
  if (2 == len(col)):
    sCol = FG.formateaNumero(l[col[0]], 2).rjust(col[1])
  elif (6 == len(col)):
    if (l['estatus'] in ('P', 'C')):
      comi = 0.00    
      if (col[4] == l[col[1]]): comi += l[col[0]]
      if (col[4] == l[col[3]]): comi += l[col[2]]
      sCol = FG.formateaNumero(comi, 2).rjust(col[5])
    else: sCol = '0.00'.rjust(col[5])
  return sColor + l['codigo'].ljust(7) + fr.ljust(9) + ff.ljust(9) +\
        l['nombre'][0:20].ljust(21) + str(l['lados']).rjust(2) +\
        (l['moneda'] + FG.formateaNumero(l['precio'])).rjust(11) +\
        FG.formateaNumero(l['prVeRe']).rjust(14) +\
        sCol + CO.FIN + "\n"
# Funcion detalles
def titTotales(tipo='Asesor', tam=20):
  return CO.AZUL + tipo.ljust(tam) + "Lad".rjust(4) + \
          "Precio V Real".rjust(14) + "Comision".rjust(12) +\
          "Comis Captado".rjust(15) + "Comis Cerrado".rjust(15) +\
          CO.FIN + "\n"
# Funcion titTotales
def detTotales(cad, lados, pvr, cap, cer, lCap, lCer, bImpar, tam=20,
                color=False):
  if (0 == lados) and (0 == cap) and (0 == cer) and (0 == lCap) and\
      (0 == lCer):
    return bImpar, ''
  (sColor, bImpar) = (color, not bImpar) if (color) else\
                                        ES.colorLinea(bImpar, CO.VERDE)
  return bImpar, sColor + cad[0:tam-1].ljust(tam) +\
        FG.formateaNumero(lados).rjust(4) +\
        FG.formateaNumero(pvr, 2).rjust(14) +\
        FG.formateaNumero(cap+cer, 2).rjust(12) +\
        (FG.formateaNumero(cap, 2) + '(' +\
        FG.formateaNumero(lCap) + ')').rjust(15) +\
        (FG.formateaNumero(cer, 2) + '(' +\
        FG.formateaNumero(lCer) + ')').rjust(15) + CO.FIN + "\n"
# Funcion detTotales
def totTotales(tipoTot, tLados, tPvr, tCap, tCer, tLaCap, tLaCer,
                tam=20, subrayar=False, mTPrecioVentaRea=True):
  '''
    Muestra la linea de totales de los totales. Se subraya antes
    del penultimo subtotal, si existe, antes del total de la oficina.
    mTPrecioVentaReal indica si se debe mostrar el precio de venta real
    de la oficina. En el caso de ambos lados en la oficina.
  '''
  return CO.AMARI + (CO.SUBRAYADO if subrayar else '') +\
        tipoTot.ljust(tam) + FG.formateaNumero(tLados).rjust(4) +\
        FG.formateaNumero(tPvr, 2).rjust(14) +\
        FG.formateaNumero(tCap+tCer, 2).rjust(12) +\
        (FG.formateaNumero(tCap, 2) + '(' +\
        FG.formateaNumero(tLaCap) + ')').rjust(15) +\
        (FG.formateaNumero(tCer, 2) + '(' +\
        FG.formateaNumero(tLaCer) + ')').rjust(15) + CO.FIN + "\n"
# Funcion totTotales
def getPropiedad(id):
  global lPro

  for p in lPro:
    #print(p)    
    if (id == p['id']): return p
  else: return None
# Funcion getPropiedad
def mPropiedad(lCod, titOpc):
  global lPro, dMsj

  if (0 == len(lCod)): return
  elif (1 == len(lCod)):
    id = lCod[0][1]
  else:
    id = FG.selOpcionMenu(lCod + [['Volver', -2]], titOpc)
    if (0 > id): return id

  prop = getPropiedad(id)
  if None == prop: return None
  sMsj = ''
  moneda = prop['moneda']
  try:
    for k in dMsj:
      val = prop[k]
      if k in ('negoc', 'estatus', 'estaC21', 'tipo_id',\
              'caracteristica_id', 'ciudad_id', 'municipio_id',\
              'estado_id', 'cliente_id'):
        if 'negoc' == k: cad  = COM.descNegociacion(val)
        elif 'estatus' == k: cad  = COM.descEstatus(val)
        elif 'estaC21' == k: cad  = COM.descEstatusC21(val)
        elif 'tipo_id' == k: cad  = COM.descTipo(str(val))
        elif 'caracteristica_id' == k:
          cad  = COM.descCaracteristica(str(val))
        elif 'ciudad_id' == k: cad  = COM.descCiudad(str(val))
        elif 'municipio_id' == k: cad  = COM.descMunicipio(str(val))
        elif 'estado_id' == k: cad  = COM.descEstado(str(val))
        elif 'cliente_id' == k: cad  = Cli.Cliente.nombre(val)
        else: cad = ':Descripcion no fue encontrada ?????'
        desc = dMsj[k][0]
        cad  = '[' + str(val) + '] ' + cad
        sMsj += COM.prepLnCad(desc, cad)
      elif k in ('iva', 'pcFrq', 'pcReCaNa', 'pcRega', 'pcCap',\
                  'pcGer', 'pcCer', 'asCapId', 'asCerId'): continue
      elif ('comision' == k):
        sMsj += COM.prepLnCad(dMsj[k][0], FG.numeroPorc(val, 3) +\
                              CO.AZUL + ' IVA: ' + CO.FIN +\
                              FG.numeroPorc(prop['iva'], 2))
      elif k in ('frqSIva', 'frqCIva'):
        sMsj += COM.prepLnCad(dMsj[k][0],\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcFrq'], 3) + ']')
      elif (k == 'frqPaRe'):
        sMsj += COM.prepLnCad(dMsj[k][0], ' ' +\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcReCaNa'], 3) + ']')
      elif ('regalia' == k):
            sMsj += COM.prepLnCad(dMsj[k][0],\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcRega'], 3) + ']')
      elif ('capPrbr' == k):
            sMsj += COM.prepLnCad(dMsj[k][0],\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcCap'], 3) + ']')
      elif ('gerente' == k):
            sMsj += COM.prepLnCad(dMsj[k][0],\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcGer'], 3) + ']')
      elif ('cerPrbr' == k):
        sMsj += COM.prepLnCad(dMsj[k][0],\
                              FG.numeroMon(val, 2, moneda) + ' [' +\
                              FG.numeroPorc(prop['pcCer'], 3) + ']')
      else: sMsj += COM.prepLnMsj(dMsj, prop, k)
    # Fin for k in dMsj
  except KeyError:
    print('Propblemas con la llave:' + k + ', su valor es:' + val)
    pass
  tec = ES.imprime(sMsj.rstrip(' \t\n\r'))
  return tec
# Funcion mPropiedad
def todasPropiedades(bCaidas=True):
  '''Lee los datos de propiedades y los despliega
      fila['id']: numero incremental.
      fila['codigo']: Codigo casa nacional.
      fila['fecRes']: fecha de reserva.
      fila['fecFir']: fecha de firma.
      fila['negoc']: Negociacion: Venta o Alquiler.
      fila['nombre']: Nombre de la propiedad.
      fila['estatus']: Status.
      fila['moneda']: Moneda.
      fila['precio']: Precio.
  '''
  global lPro

  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = titulo("Neto ofic.", 11)
  for l in lPro:
    if (l['estatus'] in ('P', 'C')):
      nV += 1
      tLados += l['lados']
      tPrecios += l['precio']
      tPrVeReal += l['prVeRe']
      tNetos += l['ingNeOf']
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, bCaidas, 'ingNeOf', 11)
  # Fin for
  st += CO.AMARI + 'TOTALES:'.ljust(45) +\
        FG.formateaNumero(tLados).rjust(3) +\
        FG.formateaNumero(tPrecios).rjust(11) +\
        FG.formateaNumero(tPrVeReal).rjust(14) +\
        FG.formateaNumero(tNetos, 2).rjust(11) + CO.FIN + "\n"
  st += FG.formateaNumero(len(lPro)) + ' negociaciones [' + \
        FG.formateaNumero(nV) + ' validas].'

  return ES.imprime(st.rstrip(' \t\n\r'))
# funcion todasPropiedades
def lstXEstatus():
  global lPro

  est = COM.selEstatus()
  if ('v' == est): return -1

  nvaLst = []
  for l in lPro:
    if (est != l['estatus']): continue
    nvaLst.append(l)
  # for l in lPro

  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = CO.CYAN + COM.dEst[est] + CO.FIN + '\n'
  st += titulo("Neto ofic.", 11)
  for l in nvaLst:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, True, 'ingNeOf', 11)
    nV += 1
    tLados += l['lados']
    tPrecios += l['precio']
    tPrVeReal += l['prVeRe']
    tNetos += l['ingNeOf']
  # for l in nvaLst
  st += CO.AMARI + 'TOTALES:'.ljust(45) +\
        FG.formateaNumero(tLados).rjust(3) +\
        FG.formateaNumero(tPrecios).rjust(11) +\
        FG.formateaNumero(tPrVeReal).rjust(14) +\
        FG.formateaNumero(tNetos, 2).rjust(11) + CO.FIN + "\n"
  st += FG.formateaNumero(len(nvaLst)) + ' negociaciones'

  return ES.imprime(st.rstrip(' \t\n\r'))
# Funcion lstXEstatus
def lstXAsesor():
  global lPro

  id = FG.selOpcionMenu(ASE.lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  nvaLst = []
  for l in lPro:
    if not (isinstance(l['asCapId'], int)) or \
       not (isinstance(l['asCerId'], int)) or \
       ((id != l['asCapId']) and (id != l['asCerId'])):
      continue
    nvaLst.append(l)
  # for l in lPro

  tPrecios = tPrVeReal = tCap = tCer = 0.00
  nF = nV = tLados = 0
  bImpar = True
  st = CO.CYAN + ASE.lAse[id-1]['name'] + CO.FIN + '\n'
  st += titulo("Comision", 10)
  for l in nvaLst:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, True, 'capPrbr', 'asCapId',
                        'cerPrbr', 'asCerId', id, 10)
    if (l['estatus'] not in ('P', 'C')): continue
    nV += 1
    tLados += l['lados']
    tPrecios += l['precio']
    tPrVeReal += l['prVeRe']
    if (id == l['asCapId']):
      try: tCap += float(l['capPrbr'])    
      except: pass
    if (id == l['asCerId']):
      try: tCer += float(l['cerPrbr'])    
      except: pass
  # Fin for
  st += CO.AMARI + 'TOTALES:'.ljust(45) +\
        FG.formateaNumero(tLados).rjust(3) +\
        FG.formateaNumero(tPrecios).rjust(11) +\
        FG.formateaNumero(tPrVeReal).rjust(14) +\
        FG.formateaNumero(tCap+tCer, 2).rjust(10) + CO.FIN + "\n"
  st += CO.AMARI + FG.formateaNumero(len(nvaLst)) +\
        ' negociaciones [' + FG.formateaNumero(nV) + ' validas]. ' +\
        'Total captado: ' + FG.formateaNumero(tCap, 2) +\
        ' y cerrado: ' + FG.formateaNumero(tCer, 2) + CO.FIN

  return ES.imprime(st.rstrip(' \t\n\r'))
# Funcion lstXAsesor
def lstXMes():

  agno, mes = COM.selMes(lTMe)
  if ('v' == agno): return -1
  
  nvaLst = []
  for l in lPro:
    if ('00' == mes) and (("" == l['fecRes']) or ("" == l['fecFir'])):
      nvaLst.append(l)
      continue
    if (("" != l['fecFir']) and (10 == len(l['fecFir'])) and\
        (agno == l['fecFir'][-4:]) and (mes == l['fecFir'][3:5])) or\
       (("" != l['fecRes']) and (10 == len(l['fecRes'])) and\
        (agno == l['fecRes'][-4:]) and (mes == l['fecRes'][3:5])):
      nvaLst.append(l)
  # for l in lPro
  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = CO.CYAN + agno + ' ' + CO.meses[int(mes)] + CO.FIN + '\n'
  st += titulo("Neto ofic.", 11)
  for l in nvaLst:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, True, 'ingNeOf', 11)
    if (l['estatus'] in ('P', 'C')):
      nV += 1
      tLados += l['lados']
      tPrecios += l['precio']
      tPrVeReal += l['prVeRe']
      tNetos += l['ingNeOf']
  # for l in nvaLst
  st += CO.AMARI + 'TOTALES:'.ljust(45) +\
        FG.formateaNumero(tLados).rjust(3) +\
        FG.formateaNumero(tPrecios).rjust(11) +\
        FG.formateaNumero(tPrVeReal).rjust(14) +\
        FG.formateaNumero(tNetos, 2).rjust(11) + CO.FIN + "\n"
  st += CO.AMARI + FG.formateaNumero(len(nvaLst)) + ' negociaciones ['\
        + FG.formateaNumero(nV) + ' validas].' + CO.FIN
  return ES.imprime(st.rstrip(' \t\n\r'))
# Funcion lstXMes
def LstPropPor():
  global lMenuLstPro
  return COM.selOpcion(lMenuLstPro, 'Listar propiedades')
# Funcion LstPropPor
def xEstatus():
  global lPro

  st = COM.selEstatus()
  if ('v' == st): return -1

  lCod = []
  for l in lPro:
    if (st != l['estatus']): continue
    lst = (l['codigo']+'-'+l['nombre'], l['id']-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, COM.dEst[st])
# Funcion xEstatus
def xNegociacion():
  global lPro
  lNeg = [(COM.dNeg[key], key) for key in COM.dNeg]

  ng = FG.selOpcionMenu(lNeg + [['Volver', 'v']], 'Negociacion')
  if ('v' == ng): return ng

  lCod = []
  for l in lPro:
    if (ng != l['negoc']): continue
    lst = (l['codigo']+'-'+l['nombre'], l['id']-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, COM.dNeg[ng])
# Funcion xNegociacion
def xNombre():
  global lPro

  cod = ES.entradaNombre(droid, 'Nombre de la propiedad',
                      'Introduzca el nombre o parte de el', lPro[0]['nombre'])
  lCod = []
  for l in lPro:
    nombre = l['nombre']
    if (l['nombre']) and (0 <= nombre.lower().find(cod.lower())):
#   if (l['nombre']) and (cod.lower() in nombre.lower()):
      if ('S' == l['estatus']): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l['codigo']+'-'+l['nombre'], l['id']-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Nombre de la propiedad:'+cod)
# Funcion xNombre
def xAsesor():
  global lPro

  id = FG.selOpcionMenu(ASE.lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  lCod = []
  for l in lPro:
    if not (isinstance(l['asCapId'], int)) or \
       not (isinstance(l['asCerId'], int)):
      continue
    if (id != l['asCapId']) and (id != l['asCerId']): continue
    if ('S' == l['estatus']): caida = 'Caida: '
    else: caida = ''
    lst = (caida+l['codigo']+'-'+l['nombre'], l['id']-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, ASE.lAse[id-1]['name'])
# Funcion xAsesor
def xCodigo():
  global droid
  global lPro

  codigo = ES.entradaNumero(droid, 'Codigo de Casa Nacional',
                      'Introduzca el codigo o parte de el', lPro[0]['codigo'])
  cod = str(codigo).rstrip(' \t\n\r')
  lCod = []
  for l in lPro:
    if cod in l['codigo']:
      if ('S' == l['estatus']): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l['codigo']+'-'+l['nombre'], l['id']-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Codigo CN:'+cod)
# Funcion xCodigo
def xReporte():
  global lPro

  cod = ES.entradaNombre(droid, 'Reporte de Casa Nacional',
                'Introduzca el reporte o parte de el', lPro[0]['repCaNa'])
  lCod = []
  #print(cod, lPro[0]['repCaNa'])
  for l in lPro:
    if (l['repCaNa']) and (cod in l['repCaNa']):
      if ('S' == l['estatus']): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l['repCaNa']+'-'+l['nombre'], l['id']-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Reporte CN:'+cod)
# Funcion xReporte
def buscProp():
  global lMenuProEsp
  return COM.selOpcion(lMenuProEsp, 'Buscar una propiedad especifica')
# Funcion BuscProp
def totAsesor():
  ''' Agregar 1, correspondiente a el 'id' del asesor.
      0:filas, 1:tPrecio, 2:tLados, 3:tCompartidoConIva,
      4:tFranquiciaSinIva, 5:tFranquiciaConIva, 6:tFranquiciaPagarR,
      7:tRegalia, 8:tSanaf5PorCiento, 9:tOficinaBrutoReal,
      10:tBaseHonorariosSo, 11:tBaseParaHonorari, 12:tCaptadorPrbr,
      13:tGerente, 14:tCerradorPrbr, 15:tBonificaciones,
      16:tComisionBancaria, 17:tIngresoNetoOfici, 18:tPrecioVentaReal,
      19:tPuntos, 20:tCaptadorPrbrSel, 21:tCerradorPrbrSel,
      22:tLadosCap, 23:tLadosCer, 24:tPvrCaptadorPrbrSel,
      25:tPvrCerradorPrbrSel, 26:tPuntosCaptador, 27:tPuntosCerrador
  '''
  global lTAs

  st = titTotales('Asesor', 20)
  bImpar = True
  tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTAs:
    try:
      bImpar, cad = detTotales(ASE.nombreAsesor(l[0]), l[23]+l[24],
                          l[25]+l[26], l[21], l[22], l[23], l[24], bImpar, 20)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[0])):   # l[0] es el 'id' del asesor.
        tPrVeReal, tCap, tCer = tPrVeReal+l[25]+l[26], tCap+l[21], tCer+l[22]
        tLaCap, tLaCer = tLaCap+l[23], tLaCer+l[24]
    except:
      print('ERROR totales:', ASE.nombreAsesor(l[0]) + ' => ',
            'filas:', l[1], '; Precio:', l[2], '; lados:', l[3],
            '; PVR:', l[19], '; Puntos:', l[20], '; asesor Cap:', l[21],
            '; asesor Cer:', l[22], '; lados Cap:', l[23],
            '; lados Cer:', l[24], '; PVR Cap:', l[25],
            '; PVR Cer:', l[26], sep='')
  try:
    st += totTotales('Total Oficina', tLaCap + tLaCer, tPrVeReal,\
                          tCap, tCer, tLaCap, tLaCer, 20, False, False)
  except:
    print('ERROR linea totales:')
    print(tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesor
def totMes():
  ''' Agregar 1, correspondiente al 'agno-mes'.
      0:filas, 1:tPrecio, 2:tLados, 3:tCompartidoConIva,
      4:tFranquiciaSinIva, 5:tFranquiciaConIva, 6:tFranquiciaPagarR,
      7:tRegalia, 8:tSanaf5PorCiento, 9:tOficinaBrutoReal,
      10:tBaseHonorariosSo, 11:tBaseParaHonorari, 12:tCaptadorPrbr,
      13:tGerente, 14:tCerradorPrbr, 15:tBonificaciones,
      16:tComisionBancaria, 17:tIngresoNetoOfici, 18:tPrecioVentaReal,
      19:tPuntos, 20:tCaptadorPrbrSel, 21:tCerradorPrbrSel,
      22:tLadosCap, 23:tLadosCer, 24:tPvrCaptadorPrbrSel,
      25:tPvrCerradorPrbrSel, 26:tPuntosCaptador, 27:tPuntosCerrador
  '''
  global lTMe

  st = titTotales('Agno Mes', 17)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTMe:
    try:
      bImpar, cad = detTotales(l[0][0:4]+' '+CO.meses[int(l[0][5:])],
                    l[3], l[19], l[13], l[15], l[23], l[24], bImpar, 17)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tPrVeReal, tCap, tCer = tPrVeReal+l[19], tCap+l[13], tCer+l[15]
      tLaCap, tLaCer, tLados = tLaCap+l[23], tLaCer+l[24], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[13], l[15], l[23], l[24])
  try:
    st += totTotales('Total Oficina', tLados, tPrVeReal, tCap, tCer,
                      tLaCap, tLaCer, 17)
  except:
    print('ERROR linea totales:')
    print(tPrVeReal, tCap, tCer, tLados, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totMes
def totEst():
  ''' Agregar 1, correspondiente al 'estatus'.
      0:filas, 1:tPrecio, 2:tLados, 3:tCompartidoConIva,
      4:tFranquiciaSinIva, 5:tFranquiciaConIva, 6:tFranquiciaPagarR,
      7:tRegalia, 8:tSanaf5PorCiento, 9:tOficinaBrutoReal,
      10:tBaseHonorariosSo, 11:tBaseParaHonorari, 12:tCaptadorPrbr,
      13:tGerente, 14:tCerradorPrbr, 15:tBonificaciones,
      16:tComisionBancaria, 17:tIngresoNetoOfici, 18:tPrecioVentaReal,
      19:tPuntos, 20:tCaptadorPrbrSel, 21:tCerradorPrbrSel,
      22:tLadosCap, 23:tLadosCer, 24:tPvrCaptadorPrbrSel,
      25:tPvrCerradorPrbrSel, 26:tPuntosCaptador, 27:tPuntosCerrador
  '''
  global lTEs

  st = titTotales('Estatus', 20)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTEs:
    try:
      bImpar, cad = detTotales(COM.descEstatus(l[0]), l[3], l[19],
                                l[13], l[15], l[23], l[24], bImpar,
                                20, CO.ROJO if ('S'==l[0]) else False)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (l[0] in ('P', 'C')):
        tPrVeReal, tCap, tCer = tPrVeReal+l[19], tCap+l[13], tCer+l[15]
        tLaCap, tLaCer, tLados = tLaCap+l[23], tLaCer+l[24], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[19], l[13], l[15], l[23], l[24])
  try:
    st += totTotales('Total Oficina', tLados, tPrVeReal, tCap, tCer,\
                      tLaCap, tLaCer, 20)
  except:
    print('ERROR linea totales:')
    print(tPrVeReal, tCap, tCer, tLados, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totEst
def totAsesorMes():
  ''' 0:'id' del asesor, 1:'agno-mes'.
      2:filas, 3:tPrecio, 4:tLados, 5:tCompartidoConIva,
      6:tFranquiciaSinIva, 7:tFranquiciaConIva, 8:tFranquiciaPagarR,
      9:tRegalia, 10:tSanaf5PorCiento, 11:tOficinaBrutoReal,
      12:tBaseHonorariosSo, 13:tBaseParaHonorari, 14:tCaptadorPrbr,
      15:tGerente, 16:tCerradorPrbr, 17:tBonificaciones,
      18:tComisionBancaria, 19:tIngresoNetoOfici, 20:tPrecioVentaReal,
      21:tPuntos, 22:tCaptadorPrbrSel, 23:tCerradorPrbrSel,
      24:tLadosCap, 25:tLadosCer, 26:tPvrCaptadorPrbrSel,
      27:tPvrCerradorPrbrSel, 28:tPuntosCaptador, 29:tPuntosCerrador
  '''
  global lTAM

# lNAs contiene listas de dos elementos: nombre y id real de cada asesor.
# id va a obtener 0 o 2, 3, 4, 5, ... # id del ultimo asesor.
  id  = FG.selOpcionMenu([['Todos', 0]] + ASE.lNAs + [['Volver', -2]],
                                                            'Asesor')
  if (0 > id): return id
  todos = (0 == id)

  st = titTotales('Agno Mes', 16)
  bImpar = True
  tAsLados = tAsLaCap = tAsLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tAsPvr = tAsCap = tAsCer = tPvr = tCap = tCer = 0.00
  idAse = 0
  for l in lTAM:
    if not todos:
      if (id != l[0]): continue    
    try:
      if (idAse != l[0]):
        if (0 < idAse):
          st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsPvr,
                            tAsCap, tAsCer, tAsLaCap, tAsLaCer, 16)
        idAse = l[0]
        st += CO.CYAN + ASE.nombreAsesor(l[0]) + CO.FIN + '\n'
        tAsLados = tAsLaCap = tAsLaCer = 0
        tAsPvr = tAsCap = tAsCer = 0.00
      bImpar, cad = detTotales(l[1][0:4]+' '+CO.meses[int(l[1][5:])],
                              l[24] + l[25], l[26]+l[27], l[22],\
                              l[23], l[24], l[25], bImpar, 16)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tAsPvr, tAsCap, tAsCer = tAsPvr+l[26]+l[27], tAsCap+l[22],\
                                tAsCer+l[23]
      tAsLaCap, tAsLaCer, tAsLados = tAsLaCap+l[24], tAsLaCer+l[25],\
                                tAsLados+l[24]+l[25]
      if todos and (1 < int(l[0])):
        tPvr, tCap, tCer = tPvr+l[26]+l[27], tCap+l[22], tCer+l[23]
        tLaCap, tLaCer, tLados = tLaCap+l[24], tLaCer+l[25],\
                                  tLados+l[24]+l[25]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[22], l[23], l[24], l[25], l[26],\
            l[27])
  try:
    st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsPvr,
                      tAsCap, tAsCer, tAsLaCap, tAsLaCer, 16, todos)
    if todos:
      st += totTotales('Total Oficina', tLaCap + tLaCer, tPvr,
                      tCap, tCer, tLaCap, tLaCer, 16, False, False)
  except:
    print('ERROR linea totales:')
    print(tAsLaCap, tAsLaCer, tAsPvr, tAsCap, tAsCer, tLados, tPvr,
              tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesorMes
def totMesAsesor():
  ''' 0:'agno-mes', 1:'id' del asesor,
      2:filas, 3:tPrecio, 4:tLados, 5:tCompartidoConIva,
      6:tFranquiciaSinIva, 7:tFranquiciaConIva, 8:tFranquiciaPagarR,
      9:tRegalia, 10:tSanaf5PorCiento, 11:tOficinaBrutoReal,
      12:tBaseHonorariosSo, 13:tBaseParaHonorari, 14:tCaptadorPrbr,
      15:tGerente, 16:tCerradorPrbr, 17:tBonificaciones,
      18:tComisionBancaria, 19:tIngresoNetoOfici, 20:tPrecioVentaReal,
      21:tPuntos, 22:tCaptadorPrbrSel, 23:tCerradorPrbrSel,
      24:tLadosCap, 25:tLadosCer, 26:tPvrCaptadorPrbrSel,
      27:tPvrCerradorPrbrSel, 28:tPuntosCaptador, 29:tPuntosCerrador
  '''
  global lTMA

  agno, mes = COM.selMes(lTMe, True)
  if ('v' == agno): return -1
  todos = ('t' == agno)
  
  st = titTotales('Asesor', 21)
  bImpar = True
  tMeLados = tMeLaCap = tMeLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tMePvr = tMeCap = tMeCer = tPvr = tCap = tCer = 0.00
  idMes = ''
  for l in lTMA:
    if not todos:
      if (agno+'-'+mes.zfill(2)) != l[0]: continue
    try:
      if (idMes != l[0]):
        if ('' != idMes):
          st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                        tMePvr, tMeCap, tMeCer, tMeLaCap, tMeLaCer, 20)
        idMes = l[0]
        st += CO.CYAN + l[0] + CO.FIN + '\n'
        tMeLados = tMeLaCap = tMeLaCer = 0
        tMePvr = tMeCap = tMeCer = 0.00
      bImpar, cad = detTotales(ASE.nombreAsesor(l[1]), l[24] + l[25],
                        l[26]+l[27], l[22], l[23], l[24], l[25], bImpar, 20)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[1])):
        tMePvr, tMeCap, tMeCer = tMePvr+l[26]+l[27], tMeCap+l[22],\
                                  tMeCer+l[23]
        tMeLaCap, tMeLaCer, tMeLados = tMeLaCap+l[24], tMeLaCer+l[25],\
                                  tMeLados+l[24]+l[25]
        if todos:
          tPvr, tCap, tCer = tPvr+l[26]+l[27], tCap+l[22], tCer+l[23]
          tLaCap, tLaCer, tLados = tLaCap+l[24], tLaCer+l[25],\
                                  tLados+l[24]+l[25]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[22], l[23], l[24], l[25], l[26],\
            l[27])
  try:
    st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                  tMePvr, tMeCap, tMeCer, tMeLaCap, tMeLaCer, 20, todos)
    if todos:
      st += totTotales('Total Oficina', tLaCap + tLaCer, tPvr, tCap,
                        tCer, tLaCap, tLaCer, 20, False, False)
  except:
    print('ERROR linea totales:')
    print(tMeLaCap, tMeLaCer, tMePvr, tMeCap, tMeCer, tLados, tPvr,
          tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totMesAsesor
def totPor():
  global lMenuTot
  return COM.selOpcion(lMenuTot, 'Totalizar')
# Funcion totPor
def totales():
  ''' 0:filas, 1:tPrecio, 2:tLados, 3:tCompartidoConIva,
      4:tFranquiciaSinIva, 5:tFranquiciaConIva, 6:tFranquiciaPagarR,
      7:tRegalia, 8:tSanaf5PorCiento, 9:tOficinaBrutoReal,
      10:tBaseHonorariosSo, 11:tBaseParaHonorari, 12:tCaptadorPrbr,
      13:tGerente, 14:tCerradorPrbr, 15:tBonificaciones,
      16:tComisionBancaria, 17:tIngresoNetoOfici, 18:tPrecioVentaReal,
      19:tPuntos, 20:tCaptadorPrbrSel, 21:tCerradorPrbrSel,
      22:tLadosCap, 23:tLadosCer, 24:tPvrCaptadorPrbrSel,
      25:tPvrCerradorPrbrSel, 26:tPuntosCaptador, 27:tPuntosCerrador
  '''
  global lTot

  if not lTot: return

  sMsj = ("%d %snegociaciones validas%s\n") % (lTot[0], CO.AZUL, CO.FIN)
  sMsj += ("%sTOTALES:%s\n") % (CO.CYAN, CO.FIN)
  sMsj += COM.prepLnNum("Precio", lTot[1], 2)
  sMsj += COM.prepLnNum("Compartido con IVA", lTot[3], 2)
  sMsj += COM.prepLnNum("Lados", lTot[2])
  sMsj += COM.prepLnNum("Franquicia a pagar reportada", lTot[6], 2)
  sMsj += COM.prepLnNum("Asesor captador PrBr", lTot[12], 2)
  sMsj += COM.prepLnNum("Gerente", lTot[13], 2)
  sMsj += COM.prepLnNum("Asesor cerrador PrBr", lTot[14], 2)
  sMsj += COM.prepLnNum("Bonificaciones", lTot[15], 2)
  sMsj += COM.prepLnNum("Comisiones bancarias", lTot[16], 2)
  sMsj += COM.prepLnNum("Ingreso neto de la oficina", lTot[17], 2)
  sMsj += COM.prepLnNum("Precio de venta real", lTot[18], 2)
  sMsj += COM.prepLnNum("Puntos", lTot[19], 2)
  opc = ES.imprime(sMsj.rstrip(' \t\n\r'))

  return opc
# Funcion totales
def propiedades(bCaidas=True):
  global lMenu
  op = ''
  while ('' == op): op = COM.selOpcion(lMenu, 'Menu de propiedades')
# Funcion propiedades
def prepararListas(dir=''):
  global lTot, lTAs, lTMe, lTEs, lTAM, lTMA

  lTot, lTAs, lTMe, lTEs, lTAM, lTMA = [], [], [], [], [], []
  lst = ES.cargaListaJson(dir+'totales.txt')
  lst = lst if lst else []
  for l in lst:
    tipo = l.pop(0)         # Elimina el primer elemento (indice 0) de 'l' y devuelve su valor.
    if ('A' == tipo):       # 'tipo' contiene el valor devuelto por pop. Totales por asesor.
      lTAs.append(l)        # El primer elemento de esta lista es el 'id' del asesor.
    elif ('M' == tipo):     # 'tipo' contiene el valor devuelto por pop. Totales por mes.
      lTMe.append(l)        # El primer elemento (0) de esta lista es el 'aaaa-mm'.
    elif ('E' == tipo):     # 'tipo' contiene el valor devuelto por pop. Totales por mes.
      lTEs.append(l)        # El primer elemento (0) de esta lista es el 'aaaa-mm'.
    elif ('AM' == tipo):    # 'tipo' contiene el valor devuelto por pop. Totales por asesor y por mes.
      lTAM.append(l)        # El primer elemento (0) de esta lista es el 'id' del asesor y el 2do (1) 'aaaa-mm'.
    elif ('MA' == tipo):    # 'tipo' contiene el valor devuelto por pop. Totales por mes y por asesor.
      lTMA.append(l)        # El primer elemento (0) de esta lista es 'aaaa-mm' y el 2do es el 'id' del asesor.
    elif ('T' == l.pop(0)): # Elimina el 2do item de 'l' y devuelve su valor. Anteriormente se elimino el 1ro.
      lTot = l              # El primer elemento (0) pasa a ser el numero total de negociaciones.
# Funcion prepararListas

#Variables globales
if __name__ == '__main__':
  lng = 80
  COM.prepararDiccionarios('../data/')
  ASE.prepararListaDeAsesores('../data/')
  prepararListaDePropiedades('../data/', True)
  prepararListas('../data/')
  print('**** propiedades() ****')
  propiedades()
  print('**** totAsesor() ****')
  totAsesor()
  print('**** totMes() ****')
  totMes()
  print('**** totEst() ****')
  totEst()
  print('**** totAsesorMes() ****')
  totAsesorMes()
  print('**** totMesAsesor() ****')
  totMesAsesor()
  print('**** totales() ****')
  totales()
  print('**** Las llaves de propiedades ****')
  st = ln = ''
  i  = 0
  for k in lPro[0].keys():
    i += 1
    st += str(i) + ') ' + k + '\n'
    ln += k + ' '
  ES.imprime(st.rstrip(' \t\n\r'))
  ES.imprime(ln.rstrip(' \t\n\r'))
  lng = 81  # Cada linea tiene 81 llaves.
  print('**** Las propiedades con longitud diferente a %d: llaves ****' % lng)
  for l in lPro:
    if (40 < len(l)) and (lng != len(l)):
      print(l['id'], l['codigo'], l['prVeRe'], l['nroRec'], l['pagGer'],
            l['factGer'], l['pagAses'], l['factAse'], l['pagOtOf'],
            l['estaC21'], l['repCaNa'], l['repCaNa'], l['factAyS'],
            len(l), sep='|')
  else: print('* NO HAY *')
