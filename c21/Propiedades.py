# libPropiedades: Modulo de Propiedades para Century 21 Puente Real
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

# Definir variables globales
def prepararListaDePropiedades(dir=''):
  global iIdCap, iNbCap, iIdCer, iNbCer
  global lPro

  lPro = ES.cargaListaJson(dir+'propiedades.txt')
  if not lPro: lPro = []
  lAse = ASE.lAse
  for i in range(0, len(lPro)):
    if not (isinstance(lPro[i][iIdCap], int)) or\
       not (isinstance(lPro[i][iIdCer], int)):
      continue
    if (1 < lPro[i][iIdCap]):                         # El asesor captador es de la oficina.
      lPro[i][iNbCap] = lAse[lPro[i][iIdCap]-1]['name']   # Colocar el nombre del asesor captador de la oficina.
    if (1 < lPro[i][iIdCer]):                         # El asesor cerrador es de la oficina.
      lPro[i][iNbCer] = lAse[lPro[i][iIdCer]-1]['name']   # Colocar el nombre del asesor cerrador de la oficina.
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
  if (10 == len(l[iFeRes])): fr = l[iFeRes][0:6] + l[iFeRes][-2:]
  else: fr = ''.ljust(8)
  if (10 == len(l[iFeFir])): ff = l[iFeFir][0:6] +l[iFeFir][-2:]
  else: ff = ''.ljust(8)
#  print(col)
  if ('S' == l[iStatu]):
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
    if ('S' != l[iStatu]):
      comi = 0.00    
      if (col[4] == l[col[1]]): comi += l[col[0]]
      if (col[4] == l[col[3]]): comi += l[col[2]]
      sCol = FG.formateaNumero(comi, 2).rjust(col[5])
    else: sCol = '0.00'.rjust(col[5])
  return sColor + l[iCodCN].ljust(7) + fr.ljust(9) + ff.ljust(9) +\
        l[iNombr][0:20].ljust(21) + str(l[iLados]).rjust(2) +\
        (l[iMoned] + FG.formateaNumero(l[iPreci])).rjust(11) +\
        FG.formateaNumero(l[iPrVRe]).rjust(14) +\
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
                tam=20, subrayar=False):
  return CO.AMARI + (CO.SUBRAYADO if subrayar else '') +\
        tipoTot.ljust(tam) + FG.formateaNumero(tLados).rjust(4) +\
        FG.formateaNumero(tPvr, 2).rjust(14) +\
        FG.formateaNumero(tCap+tCer, 2).rjust(12) +\
        (FG.formateaNumero(tCap, 2) + '(' +\
        FG.formateaNumero(tLaCap) + ')').rjust(15) +\
        (FG.formateaNumero(tCer, 2) + '(' +\
        FG.formateaNumero(tLaCer) + ')').rjust(15) + CO.FIN + "\n"
# Funcion totTotales
def mPropiedad(lCod, titOpc):
  global iIdCap, iNbCap, iIdCer, iNbCer
  global lPro
  dNeg = COM.dNeg
  dEst = COM.dEst
  dSC21 = COM.dSC21

  if (0 == len(lCod)): return
  elif (1 == len(lCod)):
    id = lCod[0][1]
  else:
    id = FG.selOpcionMenu(lCod + [['Volver', -2]], titOpc)
    if (0 > id): return id

  prop = lPro[id]
  sMsj = ''
  for n in range(0, len(prop)):
    try:    
      p = prop[n]
      if (iMoned == n): mon = p
      elif (iPreci == n):
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], FG.numeroMon(p, 0, mon))
      elif (iComis == n):
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], FG.numeroPorc(p, 3) +\
              CO.AZUL + ' IVA: ' + CO.FIN + FG.numeroPorc(prop[iIVA], 2))
      elif (n in (iFRsIv, iFRcIv)):
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], FG.numeroMon(p, 2, mon) +\
                                ' [' + FG.numeroPorc(prop[iPoFra], 3) + ']')
      elif (n == iFraPR):
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], FG.numeroMon(p, 2, mon) +\
                                ' [' + FG.numeroPorc(prop[iPoRCN], 3) + ']')
      elif (n in (iRegal, iCoCap, iCoGer, iCoCer)):
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], FG.numeroMon(p, 2, mon) +\
                                ' [' + FG.numeroPorc(prop[n-1], 3) + ']')
      elif (n in (iIVA, iPoFra, iPoRCN, iPoReg, iPoCap, iPoGer, iPoCer)):
        continue
      elif (n in (iIdCap, iIdCer)):         # id del asesor captador y cerrador.
        continue
      elif (isinstance(p, str)):
        if (iNegoc == n): p = dNeg.get(p, 'Codigo errado:'+p)
        elif (iStatu == n): p = dEst.get(p, 'Codigo errado:'+p)
        elif (iStC21 == n): p = dSC21.get(p, 'Codigo errado:'+p)
        sMsj += COM.prepLnCad(COM.dMsj[str(n)], p)
      elif (isinstance(p, int)):
        sMsj += COM.prepLnNum(COM.dMsj[str(n)], p)
      else: sMsj += COM.prepLnNum(COM.dMsj[str(n)], p, 2)
    except KeyError:
      print(n, p)
      pass
  tec = ES.imprime(sMsj.rstrip(' \t\n\r'))
  return tec
# Funcion mPropiedad
def propiedades(bCaidas=True):
  '''Lee los datos de propiedades y los despliega
      fila[0]: numero incremental.
      fila[1]: Codigo casa nacional.
      fila[2]: fecha de reserva.
      fila[3]: fecha de firma.
      fila[4]: Negociacion: Venta o Alquiler.
      fila[5]: Nombre de la propiedad.
      fila[6]: Status.
      fila[7]: Moneda.
      fila[8]: Precio.
  '''
  global lPro

  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = titulo("Neto ofic.", 11)
  for l in lPro:
    if ('S' != l[iStatu]):
      nV += 1
      tLados += l[iLados]
      tPrecios += l[iPreci]
      tPrVeReal += l[iPrVRe]
      tNetos += l[iNetos]
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, bCaidas, iNetos, 11)
# Fin for
  st += CO.AMARI + 'TOTALES:'.ljust(45) +\
        FG.formateaNumero(tLados).rjust(3) +\
        FG.formateaNumero(tPrecios).rjust(11) +\
        FG.formateaNumero(tPrVeReal).rjust(14) +\
        FG.formateaNumero(tNetos, 2).rjust(11) + CO.FIN + "\n"
  st += FG.formateaNumero(len(lPro)) + ' negociaciones [' + \
        FG.formateaNumero(nV) + ' validas].'

  return ES.imprime(st.rstrip(' \t\n\r'))
# funcion propiedades
def lstXEstatus():
  global iStatu, iNetos
  global lPro

  est = COM.selEstatus()
  if ('v' == est): return -1

  nvaLst = []
  for l in lPro:
    if (est != l[iStatu]): continue
    nvaLst.append(l)
  # for l in lPro

  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = CO.CYAN + COM.dEst[est] + CO.FIN + '\n'
  st += titulo("Neto ofic.", 11)
  for l in nvaLst:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, True, iNetos, 11)
    nV += 1
    tLados += l[iLados]
    tPrecios += l[iPreci]
    tPrVeReal += l[iPrVRe]
    tNetos += l[iNetos]
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
  global iIdCap, iIdCer, iCoCap, iCoCer
  global lPro

  id = FG.selOpcionMenu(ASE.lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  nvaLst = []
  for l in lPro:
    if not (isinstance(l[iIdCap], int)) or \
       not (isinstance(l[iIdCer], int)) or \
       ((id != l[iIdCap]) and (id != l[iIdCer])):
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
    st += detalles(l, sColor, True, iCoCap, iIdCap,
                        iCoCer, iIdCer, id, 10)
    if ('S' == l[iStatu]): continue
    nV += 1
    tLados += l[iLados]
    tPrecios += l[iPreci]
    tPrVeReal += l[iPrVRe]
    if (id == l[iIdCap]):
      try: tCap += float(l[iCoCap])    
      except: pass
    if (id == l[iIdCer]):
      try: tCer += float(l[iCoCer])    
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
    if ('00' == mes) and (("" == l[iFeRes]) or ("" == l[iFeFir])):
      nvaLst.append(l)
      continue
    if (("" != l[iFeFir]) and (10 == len(l[iFeFir])) and\
        (agno == l[iFeFir][-4:]) and (mes == l[iFeFir][3:5])) or\
       (("" != l[iFeRes]) and (10 == len(l[iFeRes])) and\
        (agno == l[iFeRes][-4:]) and (mes == l[iFeRes][3:5])):
      nvaLst.append(l)
  # for l in lPro
  nV = tLados = 0
  tPrecios = tPrVeReal = tNetos = 0.00
  bImpar = True
  st = CO.CYAN + agno + ' ' + CO.meses[int(mes)] + CO.FIN + '\n'
  st += titulo("Neto ofic.", 11)
  for l in nvaLst:
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, True, iNetos, 11)
    if ('S' != l[iStatu]):
      nV += 1
      tLados += l[iLados]
      tPrecios += l[iPreci]
      tPrVeReal += l[iPrVRe]
      tNetos += l[iNetos]
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
  return COM.selOpcion(COM.lMenuLstPro, 'Listar propiedades')
# Funcion LstPropPor
def xEstatus():
  global iCodCN, iNombr, iStatu
  global lPro

  st = COM.selEstatus()
  if ('v' == st): return -1

  lCod = []
  for l in lPro:
    if (st != l[iStatu]): continue
    lst = (l[iCodCN]+'-'+l[iNombr], l[0]-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, COM.dEst[st])
# Funcion xEstatus
def xNegociacion():
  global iCodCN, iNombr, iStatu
  global lPro
  lNeg = [(COM.dNeg[key], key) for key in COM.dNeg]

  ng = FG.selOpcionMenu(lNeg + [['Volver', 'v']], 'Negociacion')
  if ('v' == ng): return ng

  lCod = []
  for l in lPro:
    if (ng != l[iNegoc]): continue
    lst = (l[iCodCN]+'-'+l[iNombr], l[0]-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, COM.dNeg[ng])
# Funcion xNegociacion
def xNombre():
  global iNombr, iStatu, iCodCN
  global lPro

  cod = ES.entradaNombre(droid, 'Nombre de la propiedad',
                      'Introduzca el nombre o parte de el', lPro[0][iNombr])
  lCod = []
  for l in lPro:
    nombre = l[iNombr]
    if (l[iNombr]) and (0 <= nombre.lower().find(cod.lower())):
#   if (l[iNombr]) and (cod.lower() in nombre.lower()):
      if ('S' == l[iStatu]): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l[iCodCN]+'-'+l[iNombr], l[0]-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Nombre de la propiedad:'+cod)
# Funcion xNombre
def xAsesor():
  global iIdCap, iIdCer, iStatu, iCodCN, iNombr
  global lPro

  id = FG.selOpcionMenu(ASE.lNAs + [['Volver', -2]], 'Asesor')
  if (0 > id): return id

  lCod = []
  for l in lPro:
    if not (isinstance(l[iIdCap], int)) or \
       not (isinstance(l[iIdCer], int)):
      continue
    if (id != l[iIdCap]) and (id != l[iIdCer]): continue
    if ('S' == l[iStatu]): caida = 'Caida: '
    else: caida = ''
    lst = (caida+l[iCodCN]+'-'+l[iNombr], l[0]-1)
    lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, ASE.lAse[id-1]['name'])
# Funcion xAsesor
def xCodigo():
  global droid
  global lPro

  codigo = ES.entradaNumero(droid, 'Codigo de Casa Nacional',
                      'Introduzca el codigo o parte de el', lPro[0][iCodCN])
  cod = str(codigo).rstrip(' \t\n\r')
  lCod = []
  for l in lPro:
    if cod in l[iCodCN]:
      if ('S' == l[iStatu]): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l[iCodCN]+'-'+l[iNombr], l[0]-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Codigo CN:'+cod)
# Funcion xCodigo
def xReporte():
  global lPro

  cod = ES.entradaNombre(droid, 'Reporte de Casa Nacional',
                'Introduzca el reporte o parte de el', lPro[0][iRepCN])
  lCod = []
  #print(cod, lPro[0][iRepCN])
  for l in lPro:
    if (l[iRepCN]) and (cod in l[iRepCN]):
      if ('S' == l[iStatu]): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l[iRepCN]+'-'+l[iNombr], l[0]-1)
      lCod.append(lst)
  # for l in lPro

  return mPropiedad(lCod, 'Reporte CN:'+cod)
# Funcion xReporte
def buscProp():
  return COM.selOpcion(COM.lMenuProEsp, 'Buscar una propiedad especifica')
# Funcion BuscProp
def totAsesor():
  global lTAs

  st = titTotales('Asesor', 20)
  bImpar = True
  tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTAs:
    try:
      bImpar, cad = detTotales(ASE.nombreAsesor(l[0], 1), l[22]+l[23],
                          l[19], l[20], l[21], l[22], l[23], bImpar, 20)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[0])):
        tPrVeReal, tCap, tCer = tPrVeReal+l[19], tCap+l[20], tCer+l[21]
        tLaCap, tLaCer = tLaCap+l[22], tLaCer+l[23]
    except:
      print('ERROR totales:')
      print(l[1], l[20], l[21], l[22], l[23])
  try:
    st += totTotales('Total Oficina', tLaCap + tLaCer, tPrVeReal,\
                                      tCap, tCer, tLaCap, tLaCer, 20)
  except:
    print('ERROR linea totales:')
    print(tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesor
def totMes():
  global lTMe

  st = titTotales('Agno Mes', 17)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTMe:
    try:
      bImpar, cad = detTotales(l[0][0:4]+' '+CO.meses[int(l[0][5:])],
                    l[3], l[19], l[13], l[15], l[22], l[23], bImpar, 17)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tPrVeReal, tCap, tCer = tPrVeReal+l[19], tCap+l[13], tCer+l[15]
      tLaCap, tLaCer, tLados = tLaCap+l[22], tLaCer+l[23], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[13], l[15], l[22], l[23])
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
  global lTEs

  st = titTotales('Estatus', 20)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tPrVeReal = tCap = tCer = 0.00
  for l in lTEs:
    try:
      bImpar, cad = detTotales(COM.descEstatus(l[0]), l[3], l[19],
                                l[13], l[15], l[22], l[23], bImpar,
                                20, CO.ROJO if ('S'==l[0]) else False)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if ('S' != l[0]):
        tPrVeReal, tCap, tCer = tPrVeReal+l[19], tCap+l[13], tCer+l[15]
        tLaCap, tLaCer, tLados = tLaCap+l[22], tLaCer+l[23], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[19], l[13], l[15], l[22], l[23])
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
  global lTAM

  st = titTotales('Agno Mes', 16)
  bImpar = True
  tAsLados = tAsLaCap = tAsLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tAsPvr = tAsCap = tAsCer = tPvr = tCap = tCer = 0.00
  idAse = 0
  for l in lTAM:
    try:
      if (idAse != l[0]):
        if (0 < idAse):
          st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsPvr,
                            tAsCap, tAsCer, tAsLaCap, tAsLaCer, 16)
        idAse = l[0]
        st += CO.CYAN + ASE.nombreAsesor(l[0], 1) + CO.FIN + '\n'
        tAsLados = tAsLaCap = tAsLaCer = 0
        tAsPvr = tAsCap = tAsCer = 0.00
      bImpar, cad = detTotales(l[1][0:4]+' '+CO.meses[int(l[1][5:])],
          l[23] + l[24], l[20], l[21], l[22], l[23], l[24], bImpar, 16)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tAsPvr, tAsCap, tAsCer = tAsPvr+l[20], tAsCap+l[21], tAsCer+l[22]
      tAsLaCap, tAsLaCer, tAsLados = tAsLaCap+l[23], tAsLaCer+l[24],\
                                tAsLados+l[23]+l[24]
      if (1 < int(l[0])):
        tPvr, tCap, tCer = tPvr+l[20], tCap+l[21], tCer+l[22]
        tLaCap, tLaCer, tLados = tLaCap+l[23], tLaCer+l[24],\
                                  tLados+l[23]+l[24]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[20], l[21], l[22], l[23], l[24])
  try:
    st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsPvr,
                      tAsCap, tAsCer, tAsLaCap, tAsLaCer, 16, True)
    st += totTotales('Total Oficina', tLaCap + tLaCer, tPvr,
                      tCap, tCer, tLaCap, tLaCer, 16)
  except:
    print('ERROR linea totales:')
    print(tAsLaCap, tAsLaCer, tAsPvr, tAsCap, tAsCer, tLados, tPvr,
              tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesorMes
def totMesAsesor():
  global lTMA

  st = titTotales('Asesor', 21)
  bImpar = True
  tMeLados = tMeLaCap = tMeLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tMePvr = tMeCap = tMeCer = tPvr = tCap = tCer = 0.00
  idMes = ''
  for l in lTMA:
    try:
      if (idMes != l[0]):
        if ('' != idMes):
          st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                        tMePvr, tMeCap, tMeCer, tMeLaCap, tMeLaCer, 20)
        idMes = l[0]
        st += CO.CYAN + l[0] + CO.FIN + '\n'
        tMeLados = tMeLaCap = tMeLaCer = 0
        tMePvr = tMeCap = tMeCer = 0.00
      bImpar, cad = detTotales(ASE.nombreAsesor(l[1], 1), l[23] + l[24],
                        l[20], l[21], l[22], l[23], l[24], bImpar, 20)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[1])):
        tMePvr, tMeCap, tMeCer = tMePvr+l[20], tMeCap+l[21], tMeCer+l[22]
        tMeLaCap, tMeLaCer, tMeLados = tMeLaCap+l[23], tMeLaCer+l[24],\
                                  tMeLados+l[23]+l[24]
        tPvr, tCap, tCer = tPvr+l[20], tCap+l[21], tCer+l[22]
        tLaCap, tLaCer, tLados = tLaCap+l[23], tLaCer+l[24],\
                                  tLados+l[23]+l[24]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[20], l[21], l[22], l[23], l[24])
  try:
    st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                  tMePvr, tMeCap, tMeCer, tMeLaCap, tMeLaCer, 20, True)
    st += totTotales('Total Oficina', tLaCap + tLaCer, tPvr, tCap, tCer,
                      tLaCap, tLaCer, 20)
  except:
    print('ERROR linea totales:')
    print(tMeLaCap, tMeLaCer, tMePvr, tMeCap, tMeCer, tLados, tPvr,
          tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totMesAsesor
def totPor():
  return COM.selOpcion(COM.lMenuTot, 'Totalizar')
# Funcion totPor
def totales():
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
  opc = ES.imprime(sMsj.rstrip(' \t\n\r'))

  return opc
# Funcion totales
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
iPrVRe = COM.iPrVRe
iStC21 = COM.iStC21
iRepCN = COM.iRepCN
if __name__ == '__main__':
  lng = 52
  COM.prepararDiccionarios('../data/')
  ASE.prepararListaDeAsesores('../data/')
  prepararListaDePropiedades('../data/')
  prepararListas('../data/')
  propiedades()
  totAsesor()
  totMes()
  totEst()
  totAsesorMes()
  totMesAsesor()
  totales()
  print('**** Las propiedades con longitud diferente a %d: ****' % lng)
  for l in lPro:
    if (40 < len(l)) and (52 != len(l)):
      print(l[0], l[iCodCN], l[41], l[42], l[43], l[44], l[45], l[46], l[47],
            l[iStC21], l[iRepCN], l[50], l[51], sep='|')
