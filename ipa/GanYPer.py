# libGanYPer: Modulo de ganancias y perdidas para IPASPUDO.
#-*- coding:ISO-8859-1 -*-
from lib import ES, Const as CO, General as FG

def ganYperXmes():
  'Lee los datos de ganancias y perdidas por mes y los despliega'
  global lGyPxM

#  st = AMARI + lFecha("Sinca", "GanyPerxMes") + ' (Descargado:' + FIN + lFecha('egyp.txt', '') + ')' + "\n"
  nF = 0
  bImpar = True

  sTitPrestamos = CO.AZUL + "MES" + "Ingresos".rjust(15) + "FACTOR".rjust(7) +\
            "Egresos".rjust(15) + "FACTOR".rjust(7) + "Resultado".rjust(15) +\
                                              "FACTOR".rjust(8) + CO.FIN + "\n"
  st = sTitPrestamos
  rTotIng = float(lGyPxM[len(lGyPxM)-1][1])
  rTotEgr = float(lGyPxM[len(lGyPxM)-1][2])
  for l in lGyPxM:
      nF += 1
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
# 0:Mes,1:Ingresos,2:Egresos,3:Resultado
      if 0.00 != rTotIng: fcti = float(l[1])/rTotIng
      else: fcti = 0.00
      if 0.00 != rTotEgr: fcte = float(l[2])/rTotEgr
      else: fcte = 0.00
      if 0.00 != float(l[1]): fct = float(l[2])/float(l[1])
      else: fct = 0.00
      if 13 > int(l[0]): sMes = str(l[0])
      else: sMes = 'TO'
      if 1 >= abs(fct): sColorFactor = ''
      else: sColorFactor = CO.FIN + CO.ROJO
      st += sColor + sMes.rjust(2) + ' ' +\
		FG.formateaNumero(l[1], 2).rstrip().rjust(15) +\
		FG.formateaNumero(fcti, 3).rstrip().rjust(7) +\
		FG.formateaNumero(l[2], 2).rstrip().rjust(15) +\
		FG.formateaNumero(fcte, 3).rstrip().rjust(7) +\
		FG.formateaNumero(l[3], 2).rstrip().rjust(15) +\
		sColorFactor +\
		FG.formateaNumero(fct, 3).rstrip().rjust(8) +\
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

  sTitPrestamos = CO.AZUL + "CTA " + "DESCRIPCION".ljust(35) + \
                    "Ingresos".rjust(15) + "Egresos".rjust(15) + CO.FIN + "\n"
  st = sTitPrestamos
  
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

lGyPxM = ES.cargaLista("egyp.txt")	# [0]Mes; [1]Ingreso; [2]Egreso; [3]Resultado;
lGyPAc = ES.cargaLista("egypacu.txt")	# [0]Cta; [1]Descripcion; [2]Ingreso; [3]Egreso
