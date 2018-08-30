#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys

from lib import Const as CO

sCodCta = '01340055500553285809'
def banesco(f, sFecha, sRif, sEmpresa, sBanco):
  global sCodCta

  # 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
  try:
    sFechaValor = sFecha
    ln = f.readline()
    ln1 = (ln[0:3], ln[3:18], ln[18:])	# El ultimo campo tiene 16 caracteres (maximo).
    if 'HDR' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna de "
                        "la primera fila no tiene un 'HDR', pero contiene: '" +
                        ln1[0] + "'.")
    elif sBanco != ln1[1].rstrip():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La palabra '" + sBanco +
                        "' deberia estar en la columna 4 de la primera fila, "
                        "pero contiene: '" + ln1[1] + "'.")
    elif 34 < len(ln):
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La longitud de la "
                        "primera fila no deberia ser mayor de 34, pero es: '" +
                        str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:37], ln[37:38], ln[40:48], ln[75:83], ln[83:89])
    if '01' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna de "
                        "la segunda fila no tiene un '01', pero contiene: '" +
                        ln1[0] + "'.")
    elif '9' != ln1[2]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 38 de la "
                        "segunda fila no tiene un '9', pero contiene: '" +
                        ln1[2] + "'.")
    elif not ln1[3].isdigit():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 41 de la "
                        "segunda fila deberia contener 8 digitos, pero "
                        "contiene: '" + ln1[3] + "'.")
    else: sNumLote = ln1[3]
    if sFechaValor != ln1[4]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 76 de la "
                        "segunda fila deberia contener la fecha valor: '" +
                        sFechaValor + "', pero contiene: '" + ln1[4] + "'.")
    elif not ln1[5].isdigit():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 84 de la "
                        "segunda fila deberia contener 6 digitos (hora), pero "
                        "contiene: '" + ln1[5] + "'.")
    else: sHora = ln1[5]
    if 91 < len(ln):
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La longitud de la "
                        "segunda fila no deberia ser mayor de 91, pero es: '" +
                        str(len(ln)) + "'.")
    ln = f.readline()
    ln1 = (ln[0:2], ln[2:10], ln[32:42], ln[49:57], float(ln[84:99])/100,
            ln[103:123], ln[137:144], ln[148:156])
    if '02' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna "
                        "de la tercera fila no tiene un '02', pero "
                        "contiene: '" + ln1[0] + "'.")
    elif sFechaValor != ln1[1] or sFechaValor != ln1[7]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 3 o 149 "
                        "de la tercera fila deberia contener la fecha valor: "
                        "'" + sFechaValor + "', pero contiene: '" + ln1[1] +
                        "' y '" + ln1[7] + "'.")
    elif sRif != ln1[2]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Rif en columna 2 de "
                        "tercera fila errada, deberia ser '" + sRif + "'")
    elif sEmpresa != ln1[3]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 50 de la "
                        "tercera fila deberia contener '" + sEmpresa + 
                        "', pero contiene: '" + ln1[3] + "'.")
    elif sCodCta != ln1[5]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Codigo cuenta errada, "
                        "en col 104 de la tercera fila, deberia ser : '" + 
                        sCodCta + "', pero tiene '" + ln1[5] + "'.")
    elif sBanco != ln1[6].rstrip():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La palabra '" + sBanco +
                        "' deberia estar en la columna 138 de la tercera "
                        "fila, pero contiene: '" + ln1[6] + "'.")
    if 157 < len(ln):
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La longitud de la "
                        "tercera fila no deberia ser mayor de 157, pero es: "
                        "'" + str(len(ln)) + "'.")
    fMtoTot = ln1[4]
  # Linea de detalle y ultima
    sLnDet = '03'
    lista = []
    for ln in f:
      if sLnDet == ln[0:2]:
  # Cualquiera de las tres (3) lineas funcionan.
  #   lista.append((ln[0:2], float(ln[32:47])/100, ln[50:70], ln[94:95], ln[95:104], ln[111:171], ln[171:]))	# El ultimo campo tiene 215 car's.
        lista[len(lista):] = [(ln[0:2], float(ln[32:47])/100, ln[50:70],
                              ln[94:95], ln[95:104], ln[111:171], ln[171:])]	# El ultimo campo tiene 215 car's.
      elif '06' == ln[0:2]: ln1 = (ln[0:2], ln[16:17], ln[29:32],
                                    float(ln[32:47])/100)
      else: raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera "
                              "columna de la fila  de detalle tiene un "
                              "identificador errado, contiene: '" +
                              ln[0] + "'.")
    if '06' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna de "
                        "la tercera fila no tiene un '02', pero contiene: '" +
                        ln1[0] + "'.")
    elif '1' != ln1[1]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 17 de la "
                        "ultima fila no tiene un '1', pero contiene: '" +
                        ln1[1] + "'.")
    elif not ln1[2].isdigit():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 30 de la "
                        "ultima fila deberia contener digitos, pero contiene: "
                        "'" + ln1[2] + "'.")
    else:
      nroReg = int(ln1[2])
    if fMtoTot != ln1[3]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La columna 33 de la "
                        "ultima fila deberia contener el mismo valor del monto "
                        "total de la tercera fila: " + str(fMtoTot) +
                        ", pero contiene: '" + ln1[2] + "'.")
    elif 48 < len(ln):
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La longitud de la "
                        "ultima fila no deberia ser mayor de 48, pero es: "
                        "'" + str(len(ln)) + "'.")
    return lista, 0, sNumLote, sFechaValor, sHora, nroReg, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion banesco