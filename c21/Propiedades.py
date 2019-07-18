# libPropiedades: Modulo de Propiedades para Century 21 Puente Real
#-*- coding:ISO-8859-1 -*-
from lib import ES, Const as CO, General as FG

def propiedades():
  'Lee los datos de propiedades y los despliega'
  global lPro

  nF = 0
  bImpar = True

  sTitPropiedades = CO.AZUL + "Código".ljust(7) + "Fecha".just(17) + \
            "N".rjust(2) + " Nombre".ljust(22) + "S".rjust(2) + \
            "Precio".rjust(22) + CO.FIN + "\n"
  st = sTitPropiedades
  rTotPre = 0.00
  for l in lPro:
    nF += 1
    sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
    st += sColor + l[0].ljust(7) + l[1] + ' ' + l[2] + ' ' + l[3] +\
          ' ' + l[4][0:20] + ' ' + l[5] + ' ' + l[6] + l[7] +\
		      CO.FIN + "\n"
# Fin for
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion ganYperXmes
def ganYperAcum():
  'Lee los datos de ganancias y perdidas acumulado y los despliega'
  global lGyPAc

#  st = AMARI + lFecha("Sinca", "GanyPerAcum") + ' (Descargado:' + FIN + lFecha('egyp.txt', '') + ')' + "\n"
  nF = 0
#  bImpar = True

  sTitPropiedades = CO.AZUL + "CTA " + "DESCRIPCION".ljust(35) + \
                    "Ingresos".rjust(15) + "Egresos".rjust(15) + CO.FIN + "\n"
  st = sTitPropiedades
  
  rTotIng = 0.00; rTotEgr = 0.00
  for l in lGyPAc:
    nF += 1
#    sColor, bImpar = ES.colorLinea(bImpar, VERDE)
# 0:Cuenta,1:Descripcion,2:Ingresos,3:Egresos
    if '4--' == l[0]: rTotIng = float(l[2])
    if '5--' == l[0]: rTotEgr = float(l[3])
    if '-' == l[0][2:3]: sColor = CO.VERDE
    else: sColor = ''
    if 0.00 != float(l[2]): sIng = FG.formateaNumero(l[2], 2).rstrip()
    else: sIng = ''
    if 0.00 != float(l[3]): sEgr = FG.formateaNumero(l[3], 2).rstrip()
    else: sEgr = ''
    st += sColor + l[0].ljust(3) + ' ' + l[1][0:35].ljust(35) +\
			sIng.rjust(15) + sEgr.rjust(15) + CO.FIN + "\n"
# Fin for
  sTotIng = FG.formateaNumero(rTotIng, 2)
  sTotEgr = FG.formateaNumero(rTotEgr, 2)
  sDif    = FG.formateaNumero(rTotIng + rTotEgr, 2)
  st += "%sTOT Ingresos: %s%s%s, Egresos: %s%s%s; Dif: %s%s" % (CO.CYAN,
          CO.VERDE, sTotIng, CO.CYAN, CO.ROJO, sTotEgr, CO.CYAN, CO.FIN, sDif)
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion ganYperAcum

lPro = ES.cargaLista("egyp.txt")	# [0]Mes; [1]Ingreso; [2]Egreso; [3]Resultado;
lGyPAc = ES.cargaLista("egypacu.txt")	# [0]Cta; [1]Descripcion; [2]Ingreso; [3]Egreso
