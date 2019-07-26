# libPropiedades: Modulo de Propiedades para Century 21 Puente Real
#-*- coding:ISO-8859-1 -*-
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
def prepararListasDeTrabajo():
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
  # fila[18]: Franquicia a pagar reportada.
  # fila[19]: % reportado a casa nacional.
  # fila[20]: Regalia.
  # fila[21]: Sanaf - 5%.
  # ...
  # fila[7x]: Comentarios.
  lPro = ES.cargaLista("propiedades.txt")
# Funcion prepararListasDeTrabajo