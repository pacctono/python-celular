#!/usr/bin/python3
#-*- coding:ISO-8859-1 -*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys

from lib import Const as CO

sCodCta = '01020672330000020336'
def vzla(f, sFecha, sRif, sEmpresa, sBanco):
  global sCodCta

  try:
    sDia = sFecha[6:]
    sMes = sFecha[4:6]
    sAno = sFecha[2:4]
    ln = f.readline()
    ln1 = (ln[0:1], ln[1:9], ln[9:41], ln[41:61], ln[61:63], ln[63:65],
            ln[66:68], ln[69:71], float(ln[71:84])/100, ln[84:])	# El ultimo campo tiene 6 caracteres.
    if 'H' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna de "
                        "la primera fila no tiene una 'H', pero contiene: '" +
                        ln1[0] + "'.")
    elif sEmpresa != ln1[1].strip():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La 2da columna de 1ra "
                        "fila deberia contener '" + sEmpresa +
                        "'; pero contiene: '" + ln1[1] + "'.")
    elif sCodCta != ln1[3]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Codigo cuenta errada, "
                        "en col 42 de 1ra fila, deberia ser : '" + sCodCta +
                        "', pero tiene '" + ln1[3] + "'.")
    elif sDia != ln1[5]:
      print(CO.ROJO + "Error:" + CO.FIN + " dia errado, en col 64 de 1ra "
              "fila, deberia ser : '" + sDia + "', pero tiene '" + ln1[5] +
              "'.")
    elif sMes != ln1[6]:
      print(CO.ROJO + "Error:" + CO.FIN + " Mes errado, en col 67 de 1ra "
              "fila, deberia ser : '" + sMes + "', pero tiene '" + ln1[6] + 
              "'.")
    elif sAno != ln1[7]:
      print(CO.ROJO + "Error:" + CO.FIN + " a#o errado, en col 70 de 1ra "
            "fila, deberia ser : '" + sAno + "', pero tiene '" + ln1[7] + "'.")
    sFechaValor = ln[63:71]
    fMtoTot = ln1[8]
    lista = [(ln[0:1], ln[1:21], float(ln[21:32])/100, ln[32:36], ln[36:76],
              ln[76:86], ln[86:]) for ln in f]	# El ultimo campo tiene 8 car's.
    return lista, 0, '', sFechaValor, '', 0, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion vzla
