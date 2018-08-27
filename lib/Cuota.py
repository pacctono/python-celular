# libCuota: Modulo para el manejo de cuota.
#-*-coding:utf8;-*-
from lib import ES, Const as CO, General as FG

def calCuota(rM, iN, rI=12):	# Monto (rM), numero de meses (iN) e interes anual (rI).
	'Calcula la cuota de un prestamo, segun el monto, numero de cuotas y porcentaje.'
	rm = rI/(12.0 * 100.0)	# Interes mensual.
	c = round(rM * (pow((1 + rm), iN) * rm)/(pow((1 + rm),  iN) - 1), 2)
	return c
# funcion calCuota
def calAmortizacion(rM, iN, rI, c):	# Monto (rM), numero de meses (iN), interes anual (rI) y cuota (c).
	'Calcula saldo, intereses pagados de un prestamo, segun el monto, numero de cuotas y porcentaje.'
	rm      = rI/(12.0 * 100.0)	# Interes mensual.
	rSaldo  = rM
	rInt    = round(100*(rm * rSaldo))/100
	rAmor   = c - rInt
	return rInt, rAmor
# funcion calAmortizacion
def cuota(droid=None, bImp=True):
	rM = ES.entradaNumeroConLista(droid, 'Monto del prestamo', 'Introduzca el monto', CO.lMonto, False)
	iN = ES.entradaNumeroConLista(droid, 'Meses', 'Introduzca el numero de meses', CO.lNuMes)
	rI = ES.entradaNumeroConLista(droid, 'Interes anual', 'Introduzca el interes', CO.lInter, False)
	c  = calCuota(rM, iN, rI)

	ES.alerta(droid, 'CUOTA DEL PRESTAMO', '%9.2f' % c)
	if bImp:
		if CO.bPantAmplia: sFormCuota = "%sMonto:%s %s, %sNumero de meses:%s %s, %sInteres:%s %s, %sCuota:%s %s"
		else: sFormCuota = "%sMo:%s%s,%s#Mes:%s%s,%sI:%s%s,%sCta:%s%s"
		sMsj = sFormCuota % (CO.AZUL, CO.FIN, FG.formateaNumero(rM), CO.AZUL, CO.FIN, FG.formateaNumero(iN), CO.AZUL, CO.FIN,\
										FG.formateaNumero(rI, 2), CO.AZUL, CO.FIN, FG.formateaNumero(c, 2))
		ES.imprime(sMsj.rstrip(' \t\n\r'))
	return rM, iN, rI, c
# funcion cuota
