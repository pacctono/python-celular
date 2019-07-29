# libPropiedades: Modulo de Propiedades para Century 21 Puente Real
#-*- coding:ISO-8859-1 -*-
from __future__ import print_function # Para poder usar 'print' de version 3.

import sys
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG

def propiedades():
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

  nF = 0
  bImpar = True

  sTitPropiedades = CO.AZUL + "Código".ljust(7) + "Fechas".ljust(17) + \
            "N".rjust(2) + " Nombre".ljust(22) + "S".rjust(2) + \
            "Precio".rjust(22) + CO.FIN + "\n"
  st = sTitPropiedades
  for l in lPro:
    if (nF >= int(l[0])): continue
    nF += 1
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += sColor + l[1].ljust(7) + l[2] + ' ' + l[3] + ' ' + l[4] +\
          ' ' + l[5][0:20] + ' ' + l[6] + ' ' + l[7] + l[8] +\
		      CO.FIN + "\n"
# Fin for
  st += nF + 'filas.'
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion ganYperXmes

# Definir variables globales
def prepararListaDePropiedades(nbArchivo="propiedades.txt"):
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
  lPro = ES.cargaLista(nbArchivo)
# Funcion prepararListaDePropiedades

if __name__ == '__main__':
  prepararListaDePropiedades("../data/propiedades.txt")
  for l in lPro:
    if (40 < len(l)): print(l[0], l[27], l[30], l[33], l[36], l[41], l[42], l[44], l[46], sep='|')