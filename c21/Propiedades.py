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

import sys
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG
from c21 import Comun as COM
from c21 import Asesores as ASE

# Definir variables globales
def prepararListaDePropiedades(dir=''):
  global iIdCap, iNbCap, iIdCer, iNbCer
  global lPro

  # Descripcion de las filas de propiedades.txt
  # fila[0]: numero incremental.
  # fila[1]: Codigo casa nacional.
  # fila[2]: fecha de reserva.
  # fila[3]: fecha de firma.
  # fila[4]: Negociacion: Venta o Alquiler.
  # fila[5]: Nombre de la propiedad.
  # fila[6]: Status.
  # fila[7]: Moneda.
  # fila[8]: Precio.
  # fila[9]: Comision.
  # fila[10]: Monto de la reserva sin IVA.
  # fila[11]: IVA.
  # fila[12]: Monto de la reserva con IVA.
  # fila[13]: Monto de compartido con otra oficina con IVA.
  # fila[14]: Monto de compartido con otra oficina sin IVA.
  # fila[15]: Lados.
  # fila[16]: Franquicia de reserva sin IVA.
  # fila[17]: Franquicia de reserva con IVA.
  # fila[18]: % Franquicia.
  # fila[19]: Franquicia a pagar reportada.
  # fila[20]: % reportado a casa nacional.
  # fila[21]: % Regalia.
  # fila[22]: Regalia.
  # fila[23]: Sanaf - 5%.
  # fila[24]: Bruto real de la oficina.
  # fila[25]: Base para honorario de los socios.
  # fila[26]: Base para honorario.
  # fila[27]: Id del asesor captador.
  # fila[28]: Nombre del asesor captador otra oficina.
  # fila[29]: % Comision del captador.
  # fila[30]: Comision del captador PrBr.
  # fila[31]: % Comision del gerente.
  # fila[32]: Comision del gerente.
  # fila[33]: Id del asesor cerrador.
  # fila[34]: Nombre del asesor cerrador otra oficina.
  # fila[35]: % Comision del cerrador PrBr.
  # fila[36]: Comision del cerrador.
  # fila[37]: % Bonificacion.
  # fila[38]: Bonificacion.
  # fila[39]: Comision bancaria.
  # fila[40]: Ingreso neto de la oficina.
  # fila[41]: Numero de recibo.
  # 42 y 43:  Pago y factura gerente.
  # 44 y 45:  Pago y factura asesores.
  # fila[46]: Pago otra oficina.
  # fila[47]: Pagado a Casa Nacional.
  # fila[48]: Status C21.
  # fila[49]: Reporte Casa Nacional.
  # fila[50]: Factura A&S.
  # fila[51]: Comentarios.
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
  return CO.AZUL + "Codigo".ljust(7) + "Fechas".ljust(17) +\
            " Nombre".ljust(21) + "L".rjust(2) + "N".rjust(2) +\
            "Precio".rjust(13) + "S".rjust(2) +\
            tCol + CO.FIN + "\n"
# Funcion titulo
def detalles(l, sColor, bCaidas=True, *col):
  if (10 == len(l[iFeRes])): fr = l[iFeRes][0:6] + l[iFeRes][-2:]
  else: fr = ''.ljust(8)
  if (10 == len(l[iFeFir])): ff = l[iFeFir][0:6] +l[iFeFir][-2:]
  else: ff = ''.ljust(8)
  sPor = ''             # Porcion a agregar
#  print(col)
  if ('S' == l[iStatu]):
    if not bCaidas: return ''
    sColor = CO.ROJO
  if (2 <= len(col)):
# Cada columna a agregar podria tener dos o cuatro valores:
# indice de la lista del campo a agregar, longitud de ese campo.
# Si se agregan 4 valores: se compara el tercero (indice de la lista)
# con el valor en el cuarto parametro. Si la comparacion es # verdadera;
# el campo identificacado en el 1er valor se mostrara en CYAN.
    for n in range(0, len(col), 4):
      sCol = FG.formateaNumero(l[col[n]], 2).rjust(col[n+1])
      if ('S' != l[iStatu]):
        if ((n+3) <= len(col)):
          if (col[n+3] == l[col[n+2]]):
            sCol = CO.CYAN + sCol + CO.FIN
      sPor += sCol
    sPor += sColor
  return sColor + l[iCodCN].ljust(7) + fr.ljust(9) + ff.ljust(9) +\
        l[iNombr][0:20].ljust(21) + str(l[iLados]).ljust(2) +\
        l[iNegoc].ljust(2) + (l[iMoned] +\
        FG.formateaNumero(l[iPreci])).rjust(12) + l[iStatu].rjust(2) +\
        sPor + CO.FIN + "\n"
# Funcion detalles
def titTotales(tipo='Asesor', tam=21):
  return CO.AZUL + tipo.ljust(tam) + "Lad".rjust(4) + \
          "Comisiones".rjust(14) + "Comision Captado".rjust(19) +\
          "Comision Cerrado".rjust(19) + CO.FIN + "\n"
# Funcion titTotales
def detTotales(cad, lados, cap, cer, lCap, lCer, bImpar, tam=21,
                color=False):
  if (0 == lados) and (0 == cap) and (0 == cer) and (0 == lCap) and\
      (0 == lCer):
    return bImpar, ''
  (sColor, bImpar) = (color, not bImpar) if (color) else\
                                        ES.colorLinea(bImpar, CO.VERDE)
  return bImpar, sColor + cad.ljust(tam) +\
        FG.formateaNumero(lados).rjust(4) +\
        FG.formateaNumero(cap+cer, 2).rjust(14) +\
        (FG.formateaNumero(cap, 2) + '(' +\
        FG.formateaNumero(lCap) + ')').rjust(19) +\
        (FG.formateaNumero(cer, 2) + '(' +\
        FG.formateaNumero(lCer) + ')').rjust(19) + CO.FIN + "\n"
# Funcion detTotales
def totTotales(tipoTot, tLados, tCap, tCer, tLaCap, tLaCer, tam=21,
                subrayar=False):
  return CO.AMARI + (CO.SUBRAYADO if subrayar else '') +\
        tipoTot.ljust(tam) + FG.formateaNumero(tLados).rjust(4) +\
        FG.formateaNumero(tCap+tCer, 2).rjust(14) +\
        (FG.formateaNumero(tCap, 2) + '(' +\
        FG.formateaNumero(tLaCap) + ')').rjust(19) +\
        (FG.formateaNumero(tCer, 2) + '(' +\
        FG.formateaNumero(tLaCer) + ')').rjust(19) + CO.FIN + "\n"
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
  ES.imprime(sMsj.rstrip(' \t\n\r'))
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
  tPrecios = tNetos = 0.00
  bImpar = True
  st = titulo("Neto ofic.", 11)
  for l in lPro:
    if ('S' != l[iStatu]):
      nV += 1
      tLados += l[iLados]
      tPrecios += l[iPreci]
      tNetos += l[iNetos]
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += detalles(l, sColor, bCaidas, iNetos, 11)
# Fin for
  st += CO.AMARI + 'TOTALES:' + FG.formateaNumero(tLados).rjust(39) +\
        FG.formateaNumero(tPrecios).rjust(15) +\
        FG.formateaNumero(tNetos, 2).rjust(13) + CO.FIN + "\n"
  st += FG.formateaNumero(len(lPro)) + ' negociaciones [' + \
        FG.formateaNumero(nV) + ' validas].'

  ES.imprime(st.rstrip(' \t\n\r'))
# funcion propiedades
def xEstatus():
  global iCodCN, iNombr, iStatu
  global lPro
  lEst = [(COM.dEst[key], key) for key in COM.dEst]

  st = FG.selOpcionMenu(lEst + [['Volver', 'v']], 'Estatus')
  if ('v' == st): return st

  lCod = []
  for l in lPro:
    if (st != l[iStatu]): continue
    lst = (l[iCodCN]+'-'+l[iNombr], l[0]-1)
    lCod.append(lst)
  # for l in lPro

  mPropiedad(lCod, COM.dEst[st])
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

  mPropiedad(lCod, COM.dNeg[ng])
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

  mPropiedad(lCod, 'Nombre de la propiedad:'+cod)
# Funcion xNombre
def xAsesor():
  global iIdCap, iNbCap, iIdCer, iNbCer
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

  mPropiedad(lCod, ASE.lAse[id-1]['name'])
# Funcion xAsesor
def xCodigo():
  global droid
  global lPro

  codigo = ES.entradaNumero(droid, 'Codigo de Casa Nacional',
                      'Introduzca el codigo o parte de el', lPro[0][iCodCN])
  cod = str(codigo)
  lCod = []
  for l in lPro:
    if cod in l[iCodCN]:
      if ('S' == l[iStatu]): caida = 'Caida: '
      else: caida = ''
      lst = (caida+l[iCodCN]+'-'+l[iNombr], l[0]-1)
      lCod.append(lst)
  # for l in lPro

  mPropiedad(lCod, 'Codigo CN:'+cod)
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

  mPropiedad(lCod, 'Reporte CN:'+cod)
# Funcion xReporte
def totAsesor():
  global lTAs

  st = titTotales('Asesor', 21)
  bImpar = True
  tLaCap = tLaCer = 0
  tCap = tCer = 0.00
  for l in lTAs:
    try:
      bImpar, cad = detTotales(ASE.nombreAsesor(l[0], 1), l[21]+l[22],
                              l[19], l[20], l[21], l[22], bImpar, 21)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[0])):
        tCap, tCer = tCap+l[19], tCer+l[20]
        tLaCap, tLaCer = tLaCap+l[21], tLaCer+l[22]
    except:
      print('ERROR totales:')
      print(l[1], l[19], l[20], l[21], l[22])
  try:
    st += totTotales('Total Oficina', tLaCap + tLaCer, tCap, tCer,
                      tLaCap, tLaCer, 21)
  except:
    print('ERROR linea totales:')
    print(tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesor
def totMes():
  global lTMe

  st = titTotales('Agno Mes', 16)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tCap = tCer = 0.00
  for l in lTMe:
    try:
      bImpar, cad = detTotales(l[0][0:4]+' '+CO.meses[int(l[0][5:])],
                          l[3], l[13], l[15], l[21], l[22], bImpar, 16)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tCap, tCer = tCap+l[13], tCer+l[15]
      tLaCap, tLaCer, tLados = tLaCap+l[21], tLaCer+l[22], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[13], l[15], l[21], l[22])
  try:
    st += totTotales('Total Oficina', tLados, tCap, tCer, tLaCap,
                      tLaCer, 16)
  except:
    print('ERROR linea totales:')
    print(tCap, tCer, tLados, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totMes
def totEst():
  global lTEs

  st = titTotales('Estatus', 21)
  bImpar = True
  tLados = tLaCap = tLaCer = 0
  tCap = tCer = 0.00
  for l in lTEs:
    try:
      bImpar, cad = detTotales(COM.descEstatus(l[0]), l[3], l[13],
                                l[15], l[21], l[22], bImpar, 21,
                                CO.ROJO if ('S'==l[0]) else False)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if ('S' != l[0]):
        tCap, tCer = tCap+l[13], tCer+l[15]
        tLaCap, tLaCer, tLados = tLaCap+l[21], tLaCer+l[22], tLados+l[3]
    except:
      print('ERROR totales:')
      print(l[1], l[3], l[13], l[15], l[21], l[22])
  try:
    st += totTotales('Total Oficina', tLados, tCap, tCer, tLaCap,
                      tLaCer, 21)
  except:
    print('ERROR linea totales:')
    print(tCap, tCer, tLados, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totEst
def totAsesorMes():
  global lTAM

  st = titTotales('Agno Mes', 16)
  bImpar = True
  tAsLados = tAsLaCap = tAsLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tAsCap = tAsCer = tCap = tCer = 0.00
  idAse = 0
  for l in lTAM:
    try:
      if (idAse != l[0]):
        if (0 < idAse):
          st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsCap,
                            tAsCer, tAsLaCap, tAsLaCer, 16)
        idAse = l[0]
        st += CO.CYAN + ASE.nombreAsesor(l[0], 1) + CO.FIN + '\n'
        tAsLados = tAsLaCap = tAsLaCer = 0
        tAsCap = tAsCer = 0.00
      bImpar, cad = detTotales(l[1][0:4]+' '+CO.meses[int(l[1][5:])],
                  l[22] + l[23], l[20], l[21], l[22], l[23], bImpar, 16)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      tAsCap, tAsCer = tAsCap+l[20], tAsCer+l[21]
      tAsLaCap, tAsLaCer, tAsLados = tAsLaCap+l[22], tAsLaCer+l[23],\
                                tAsLados+l[22]+l[23]
      if (1 < int(l[0])):
        tCap, tCer = tCap+l[20], tCer+l[21]
        tLaCap, tLaCer, tLados = tLaCap+l[22], tLaCer+l[23],\
                                  tLados+l[22]+l[23]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[20], l[21], l[22], l[23])
  try:
    st += totTotales('Total Asesor', tAsLaCap + tAsLaCer, tAsCap,
                      tAsCer, tAsLaCap, tAsLaCer, 16, True)
    st += totTotales('Total Oficina', tLaCap + tLaCer, tCap, tCer,
                      tLaCap, tLaCer, 16)
  except:
    print('ERROR linea totales:')
    print(tAsLaCap, tAsLaCer, tAsCap, tAsCer, tLados, tCap, tCer, tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totAsesorMes
def totMesAsesor():
  global lTMA

  st = titTotales('Asesor', 21)
  bImpar = True
  tMeLados = tMeLaCap = tMeLaCer = 0
  tLados = tLaCap = tLaCer = 0
  tMeCap = tMeCer = tCap = tCer = 0.00
  idMes = ''
  for l in lTMA:
    try:
      if (idMes != l[0]):
        if ('' != idMes):
          st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                            tMeCap, tMeCer, tMeLaCap, tMeLaCer, 21)
        idMes = l[0]
        st += CO.CYAN + l[0] + CO.FIN + '\n'
        tMeLados = tMeLaCap = tMeLaCer = 0
        tMeCap = tMeCer = 0.00
      bImpar, cad = detTotales(ASE.nombreAsesor(l[1], 1), l[22] + l[23],
                        l[20], l[21], l[22], l[23], bImpar, 21)
      st += cad
    except TypeError:
      print('ERROR detalle:')
      print(l)
    try:
      if (1 < int(l[1])):
        tMeCap, tMeCer = tMeCap+l[20], tMeCer+l[21]
        tMeLaCap, tMeLaCer, tMeLados = tMeLaCap+l[22], tMeLaCer+l[23],\
                                  tMeLados+l[22]+l[23]
        tCap, tCer = tCap+l[20], tCer+l[21]
        tLaCap, tLaCer, tLados = tLaCap+l[22], tLaCer+l[23],\
                                  tLados+l[22]+l[23]
    except:
      print('ERROR totales:')
      print(l[0], l[1], l[2], l[3], l[20], l[21], l[22], l[23])
  try:
    st += totTotales('Total mes ' + idMes, tMeLaCap + tMeLaCer,
                      tMeCap, tMeCer, tMeLaCap, tMeLaCer, 21, True)
    st += totTotales('Total Oficina', tLaCap + tLaCer, tCap, tCer,
                      tLaCap, tLaCer, 21)
  except:
    print('ERROR linea totales:')
    print(tMeLaCap, tMeLaCer, tMeCap, tMeCer, tLados, tCap, tCer,
          tLaCap, tLaCer)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion totMesAsesor
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
  sMsj += COM.prepLnNum("Comisiones bancarias", lTot[17], 2)
  sMsj += COM.prepLnNum("Ingreso neto de la oficina", lTot[16], 2)
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
iStC21 = COM.iStC21
iRepCN = COM.iRepCN
if __name__ == '__main__':
  lng = 52
  COM.prepararDiccionarios('../data/')
  ASE.prepararListaDeAsesores('../data/')
  prepararListaDePropiedades('../data/')
  prepararListas('../data/')
  propiedades()
  #print(lTot)
  #print(lTAs)
  #print(COM.dNeg)
  #print(COM.dMon)
  #print(COM.dEst)
  #print(COM.dSC21)
  #print(lPro[0:1])
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
