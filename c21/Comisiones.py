# libComisiones: Modulo para el manejo de las comisiones.
#-*- coding:ISO-8859-1 -*-
import sys
if __name__ == '__main__': sys.path.append('../')
from lib import ES, Const as CO, General as FG

def calComisiones(rPr, rCom, rIva=16.0, lados=2, xPReCaNa=5.0,
					asCapSoc=False, asCerSoc=False, xPorcBon=0.00,
					xPorcCap=20.0, xPorcCer=20.0, comBanca=0.00,
					xPorcGer=10.0, xPcFranq=10.0, xPorcReg=80.0,
					xPorcSan=20.0):
	'''Calcula las comisiones de una venta, segun el precio,
		porcentaje de comision e IVA y otros:
		rPr:     Precio del inmueble (G)
		rCom:    % de comision (H)
		rIva:    % del IVA (J)
		lados:	 Numero de la dos de la oficina (1 o 2)
		asCapSoc: Es el asesor captador un socio
		asCerSoc: Es el asesor cerrador un socio
		xPorcBon: Porcentaje de comision para bonificacion
		xPorcCap: Porcentaje de comision para captador
		xPorcCer: Porcentaje de comision para cerrador
		comBanca: Comision bancaria descontada
		xPorcGer: Porcentaje de comision del gerente
		xPcFranq: Porcentaje de franquicia
		xPReCaNa: Porcentaje reportado a casa nacional (R)
		xPorcReg: Porcentaje regalia
		xPorcSan: Porcentaje Sanaf
		'''
	IVA = 16.0
	resSIva  = rPr * (rCom/100.0)				# (I) Reserva sin IVA
	resCIva  = (1.0 + rIva/100.0) * resSIva		# (K) Reserva con IVA
	if (2 == lados): div = 1
	else: div = 2
	compSIva = resSIva/div						# (M) Compartido con otra oficina sin IVA
	compCIva = resCIva/div						# (L) Compartido con otra oficina con IVA

	frnqSIva = (xPcFranq/100.0) * compSIva	# (O) Franquicia de reserva sin IVA. Aplicar. 2 lados
	frnqCIva = (xPcFranq/100.0) * compCIva	# (P) Franquicia de reserva con IVA. Un calculo. 2 lados.

	frnqPaRe = (xPcFranq/100.0) * (xPReCaNa/100.0) * rPr / div	# (Q) Franquicia a pagar reportada. Aplicar. 2 lados

	regalia  = (xPorcReg/100.0) * frnqPaRe	# (S) Regalia. Aplicar para franquicia a pagar reportada.

	sanfm5XC = ((xPorcSan/100.0) * frnqPaRe) -\
				((0.5/100.0) * (xPorcSan/100.0) * compSIva)		# (T) Sanaf aplicar franquicia a pagar reportada. Ambos lados.

	ofBruRea = compCIva - frnqPaRe			# (U)=(L)-(Q) Oficina bruto real = compartido con otra oficina - franquicia a pagar reportada.

	basHoSoc = compCIva - frnqCIva			# (V)=(L)-(P) Base de honorarios socios = compartido con otra oficina - franqquicia de reserva sin IVA.
# Calculo del monto Base para honorarios:
	if (0.00 < rIva): basPaHon = compSIva - frnqSIva	# (W)=(M)-(O) compartido con otrs oficina sin IVA - franquicia de reserva sin IVA.
	else: basPaHon = (compSIva - frnqSIva) / (1 + IVA/100.0)	# (W)=(M)-(O) cuando iva = 0. Se divide entre 1.16.
# Calculo del monto de la comision del asesor captador(X).
	xFactCap = xPorcCap/100.0
	if (asCapSoc): captador = xFactCap * basHoSoc	# Si captador es socio; porc captador x base para honorarios socios.
	else:
		captador = (xFactCap * basPaHon) - ((1.0/100.0) * xFactCap *\
						basPaHon) + ((IVA/100.0) * xFactCap * basPaHon)
# Calculo del monto de la comision del gerente (Y):
	xFactGer = xPorcGer/100.0
	gerente  = xFactGer * basHoSoc			# (Y) = % * (V)
# Calculo del monto de la comision del asesor cerrador(Z):
	xFactCer = xPorcCer/100.0
	if (asCerSoc): cerrador = xFactCer * basHoSoc	# Si cerrador es socio; porc cerrador x base para honorarios socios.
	else:
		cerrador = (xFactCer * basPaHon) - ((1.0/100.0) * xFactCer *\
						basPaHon) + ((IVA/100.0) * xFactCer * basPaHon)
	bonifica = (xPorcBon/100.0) * basPaHon			# (AA) = % * (W)
	netoOfic = compCIva - frnqPaRe - captador - gerente -\
				cerrador - bonifica - comBanca

	return resSIva, resCIva, compSIva, compCIva, frnqSIva, frnqCIva,\
			frnqPaRe, regalia, sanfm5XC, ofBruRea, basHoSoc,\
			basPaHon, captador, gerente, cerrador, bonifica, netoOfic
# funcion calComisiones
def comisiones(droid=None, bImp=True):
	rPr = rCom = rIva = lados = xPReCaNa = asCapSoc = asCerSoc = None
	xPorcBon = xPorcCap = xPorcCer = comBanca = None
	while (None == rPr):
		rPr  = ES.entradaNumeroConLista(droid, 'Precio del inmueble',
							'Introduzca el monto', CO.lMonto, False)
	while (None == rCom):
		rCom = ES.entradaNumeroConLista(droid, 'Comision',
					'Introduzca el porc de comision', CO.lComis, False)
	while (None == rIva):
		rIva = ES.entradaNumeroConLista(droid, 'Impuesto al valor '
				'agregado', 'Introduzca el IVA', CO.lIva, False, True)
	while (None == lados):
		lados = ES.entradaNumero(droid, 'Numero de lados',
							'Cuantos lados, 1 o 2?', '2')
		if (None != lados):
			if (1 > lados) or (2 < lados): lados = None
	while (None == xPReCaNa):
		xPReCaNa = ES.entradaNumeroConLista(droid,
				'Porcentaje reportada a Casa Nacional', '% Reportado a '
				'Casa Nacional?', ['5.0', '4.9', '4.8', '4.7', '4.6',
				'4.5', '4.4', '4.3', '4.2', '4.1', 'Otro'], False, True)
	while (None == asCapSoc):
		resp = ES.siNo(droid, 'El asesor captador es socio',
								'El Captador es socio PrBr?', CO.lNoSi)
		if ('S' == resp): asCapSoc = True
		else: asCapSoc = False
	while (None == asCerSoc):
		resp = ES.siNo(droid, 'El asesor cerrador es socio',
								'El Cerrador es socio PrBr?', CO.lNoSi)
		if ('S' == resp): asCerSoc = True
		else: asCerSoc = False
	while (None == xPorcBon):
		xPorcBon = ES.entradaNumeroConLista(droid,
				'Porcentaje de bonificacion', '% de bonificacion?',
				['0.00', '2.5', '5.0', '10.0', 'Otro'], False, True)
	xPorcCap = ES.entradaNumero(droid, 'Comision captador',
				'% de la comision del captador?', '20.00', False, True)
	if (None == xPorcCap): xPorcCap = 20.00
	xPorcCer = ES.entradaNumero(droid, 'Comision cerrador',
				'% de la comision del cerrador?', '20.00', False, True)
	if (None == xPorcCer): xPorcCer = 20.00
	comBanca = ES.entradaNumero(droid, 'Comision bancaria',
				'Monto de la comision bancaria?', '0.00', False, True)
	if (None == comBanca): comBanca = 0.00
	xPorcGer = 10.0
	xPcFranq = 10.0
	xPorcReg = 80.0
	xPorcSan = 20.0
	(resSIva, resCIva, compSIva, compCIva, frnqSIva, frnqCIva,\
		frnqPaRe, regalia, sanfm5XC, ofBruRea, basHoSoc, basPaHon,\
		captador, gerente, cerrador, bonifica, netoOfic) =\
	calComisiones(rPr, rCom, rIva, lados, xPReCaNa, asCapSoc, asCerSoc,
					xPorcBon, xPorcCap, xPorcCer, comBanca, xPorcGer,
					xPcFranq, xPorcReg, xPorcSan)

	if bImp:
		if CO.bPantAmplia:
			sFormCuota = ("%sPrecio:%s %s, %sComision:%s %s%%, %sIVA:%s"
							" %s%%, %d %slado(s)%s\n")
		else: sFormCuota = "%sPr:%s%s,%s%%Com:%s%s%%,%sIVA:%s%s%%\n"
		sMsj = sFormCuota % (CO.AZUL, CO.FIN, FG.formateaNumero(rPr, 2),
						CO.AZUL, CO.FIN, FG.formateaNumero(rCom, 2),
						CO.AZUL, CO.FIN, FG.formateaNumero(rIva, 2),
						lados, CO.AZUL, CO.FIN)
		sMsj += ("%sReserva sin IVA:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(resSIva, 2))
		sMsj += ("%sReserva con IVA:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(resCIva, 2))
		sMsj += ("%sCompartido con otra oficina con IVA:%s %s\n") %\
				(CO.AZUL, CO.FIN, FG.formateaNumero(compCIva, 2))
		sMsj += ("%sCompartido con otra oficina sin IVA:%s %s\n") %\
				(CO.AZUL, CO.FIN, FG.formateaNumero(compSIva, 2))
		sMsj += ("%sFranquicia de reserva sin IVA:%s %s (%s%%)\n") %\
				(CO.AZUL, CO.FIN, FG.formateaNumero(frnqSIva, 2),
				FG.formateaNumero(xPcFranq, 2))
		sMsj += ("%sFranquicia de reserva con IVA:%s %s (%s%%)\n") %\
				(CO.AZUL, CO.FIN, FG.formateaNumero(frnqCIva, 2),
				FG.formateaNumero(xPcFranq, 2))
		sMsj += ("%sFranquicia a pagar reportada:%s %s (%s%%)\n") %\
				(CO.AZUL, CO.FIN, FG.formateaNumero(frnqPaRe, 2),
				FG.formateaNumero(xPReCaNa, 2))
		sMsj += ("%sRegalia:%s %s (%s%%)\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(regalia, 2),
				FG.formateaNumero(xPorcReg, 2))
		sMsj += ("%sSanaf menos 5 por ciento:%s %s (%s%%)\n") % (CO.AZUL,
				CO.FIN, FG.formateaNumero(sanfm5XC, 2),
				FG.formateaNumero(xPorcSan, 2))
		sMsj += ("%sOficina bruto real:%s %s\n") % (CO.AZUL, CO.FIN,
				 FG.formateaNumero(ofBruRea, 2))
		sMsj += ("%sBase honorarios socios:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(basHoSoc, 2))
		sMsj += ("%sBase para honorarios:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(basPaHon, 2))
		sMsj += ("%sComision del captador:%s %s (%s%%)\n") % (CO.AZUL,
				CO.FIN, FG.formateaNumero(captador, 2),
				FG.formateaNumero(xPorcCap, 2))
		sMsj += ("%sComision del gerente:%s %s (%s%%)\n") % (CO.AZUL,
				CO.FIN, FG.formateaNumero(gerente, 2),
				FG.formateaNumero(xPorcGer, 2))
		sMsj += ("%sComision del cerrador:%s %s (%s%%)\n") % (CO.AZUL,
				CO.FIN, FG.formateaNumero(cerrador, 2),
				FG.formateaNumero(xPorcCer, 2))
		if (0.00 != xPorcBon):
			sMsj += ("%sBonificacion:%s %s (%s%%)\n") % (CO.AZUL,
					CO.FIN, FG.formateaNumero(bonifica, 2),
					FG.formateaNumero(xPorcBon, 2))
		if (0.00 != comBanca):
			sMsj += ("%sComision bancaria:%s %s\n") % (CO.AZUL, CO.FIN,
					FG.formateaNumero(comBanca, 2))
		sMsj += ("%sIngreso neto de la oficina:%s %s\n") % (CO.AZUL,
				CO.FIN, FG.formateaNumero(netoOfic, 2))
		opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
		return opc
	return rPr, rCom, rIva, lados, resSIva, resCIva, compSIva,\
		compCIva, frnqSIva, frnqCIva, frnqPaRe, regalia, sanfm5XC,\
		ofBruRea, basHoSoc, basPaHon, captador, gerente, cerrador,\
		bonifica, comBanca, netoOfic
# funcion comisiones

if __name__ == '__main__':
	comisiones()