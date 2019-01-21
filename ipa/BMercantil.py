#!/usr/bin/python3
#-*- coding:ISO-8859-1 -*-
#qpy:3
#qpy:console
from __future__ import print_function # Para poder usar 'print' de version 3.
import sys

from lib import Const as CO

sCodCta = '01050068121068204451'
def mercantil(bMerc, f, sFecha, sRif):
  global sCodCta

  # 60,8:#Regs; 68,17:mtoTot; 93,20:CtaDebito. Detalle: 3,15:CI; 81,17:Monto; 61,20:CtaCliente
  try:
    if bMerc:
      sNumLote = sFecha
      sFechaValor = sFecha[1:9]
      sHora = sFecha[9:]
    else:
      sFechaValor = sFecha
      sHora = ''
    ln = f.readline()
    ln1 = (ln[0:1], ln[1:13], ln[13:28], ln[28:33], ln[33:43], ln[43:44], 
            ln[44:59], ln[59:67], float(ln[67:84])/100, ln[84:92], ln[92:112],
            ln[112:119], ln[139:])	# El ultimo campo tiene 261 caracteres (todos zeros).
    if '1' != ln1[0]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " La primera columna "
                      "de la primera fila no tiene un '1', pero contiene: '" +
                      ln1[0] + "'.")
    elif 'BAMRVECA' != ln1[1].strip():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " identifcacion del "
                        "banco en 2da columna de 1ra fila errada, deberia ser "
                        "'BAMRVECA', pero contiene: '" + ln1[1] + "'.")
    if bMerc:
      if sNumLote != ln1[2]:
        raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Numero de lote "
                          "errado, en col 14 de 1ra fila, deberia ser : '" + 
                          sNumLote + "', pero tiene '" + ln1[2] + "'")
      sTPro = 'NOMIN'
      sTPag = '0000000414'
    else:		# Proveedores
      sNumLote = ln1[2]
      sTPro = 'PROVE'
      sTPag = '0000000062'
    if sTPro != ln1[3]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Tipo de producto en "
                        "columna 29 de 1ra fila errado, deberia ser '" +
                        sTPro + "'")
    elif sTPag != ln1[4]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Tipo de pago en "
                        "columna 34 de 1ra fila errada, deberia ser '" +
                        sTPag + "' (Prestamo caja de ahorros o Pago "
                        "proveedores)")
    elif sRif[0:1] != ln1[5] or sRif[1:] != ln1[6].lstrip('0'):
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Rif en columna 44 de "
                        "1ra fila errada, deberia ser '" + sRif + "'.")
    elif not ln1[7].isdigit():
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Numero de registros "
                        "en columna 60 de 1ra fila errada, deberia ser "
                        "numerico, pero es: '" + ln1[7] + "'")
    elif sFechaValor != ln1[9]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Fecha valor errada, "
                        "en col 85 de 1ra fila, deberia ser : '" +
                        sFechaValor + "', pero tiene '" + ln1[9] + "'")
    elif sCodCta != ln1[10]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " Codigo cuenta errada, "
                        "en col 93 de 1ra fila, deberia ser : '" + sCodCta +
                        "', pero tiene '" + ln1[10] + "'.")
    elif '0000000' != ln1[11]:
      raise ValueError(CO.ROJO + "Error:" + CO.FIN + " En columna 113 de 1ra "
                        "fila errada, deberia ser '0000000', pero tiene '" +
                        ln1[11] + "'")
    nroReg = int(ln1[7])
    fMtoTot = ln1[8]
    lista = [(ln[0:1], ln[1:2], ln[2:17], ln[17:18], ln[18:30], ln[30:60],
              ln[60:80], float(ln[80:97])/100, ln[97:113], ln[113:123],
              ln[123:126], ln[126:186], ln[186:201], ln[201:251], ln[285:365],
              ln[365:]) for ln in f]	# El ultimo campo tiene 35 car's.
    return lista, sTPag, sNumLote, sFechaValor, sHora, nroReg, fMtoTot
  except ValueError as er:
    print(er)
    sys.exit()
# FIN funcion mercantil
