# libComisiones: Modulo para el manejo de las comisiones.
#-*- coding:ISO-8859-1 -*-
if __name__ == '__main__': import ES, Const as CO, General as FG
else: from lib import ES, Const as CO, General as FG

def calComisiones(rPr, rCom, rIva=16.0, rXFranq=10.0, rXReCaNa=5.0, xRegalia=80.0):
	'''Calcula las comisiones de una venta, segun el precio,
		porcentaje de comision e IVA y otros:
		rPr:     Precio del inmueble (G)
		rCom:    % de comision (H)
		rIva:    % del IVA (J)
		rXFranq: Porcentaje de franquicia
		rXReCaNa: Porcentaje reportado a casa nacional
		xRegalia: Porcentaje regalia
		'''
	resSIva  = rPr * (rCom/100.0)				# Reserva sin IVA
	resCIva  = (1.0 + rIva/100.0) * resSIva		# Reserva con IVA
	compSIva = resSIva/2.0						# Compartido con otra oficina sin IVA
	compCIva = resCIva/2.0						# Compartido con otra oficina con IVA

	frqTSIva = (rXFranq/100.0) * resSIva	# Franquicia de reserva sin IVA. Aplicar. 2 lados
	frqFSIva = (rXFranq/100.0) * resCIva	# Franquicia de reserva sin IVA. No aplicar. 2 lados
	frnqCIva = (rXFranq/100.0) * resCIva	# Franquicia de reserva con IVA. Un calculo. 2 lados.

	frqTPaRe = (rXFranq/100.0) * (rXReCaNa/100.0) * rPr	# Franquicia a pagar reportada. Aplicar. 2 lados
	frqFPaRe = (rXFranq/100.0) * compSIva	# Franquicia a pagar reportada. No aplicar. 2 lados

	regaliaT = (xRegalia/100.0) * frqTPaRe	# Regalia. Aplicar para franquicia a pagar reportada.
	regaliaF = (xRegalia/100.0) * frqFPaRe	# Regalia. No aplicar para franquicia a pagar reportada.

	sanfT5XC = (0.20 * frqTPaRe) - (0.001 * resSIva)		# Sanaf aplicar franquicia a pagar reportada. Ambos lados.
	sanfT5XL = (0.20 * frqTPaRe) - (0.001 * resSIva / 2.0)	# Sanaf aplicar franquicia a pagar reportada. 1 lado.
	sanfF5XC = (0.20 * frqFPaRe) - (0.001 * resSIva)		# Sanaf no aplicar franquicia a pagar reportada. Ambos lados.
	sanfF5XL = (0.20 * frqFPaRe) - (0.001 * resSIva / 2.0)	# Sanaf no aplicar franquicia a pagar reportada. 1 lado.

	ofBruTRT = compCIva - frqTPaRe
	ofBruTRF = compCIva - frqFPaRe
	ofBruFRT = compCIva - frqTSIva
	ofBruFRF = compCIva - frqFSIva

	baHonSoc = compCIva - frnqCIva

	baTPaHon = compSIva - frqTSIva
	baFPaHon = compSIva - frqFSIva
	baTPaHoI = (compSIva - frqTSIva) / (1 + rIva/100.0)
	baFPaHoI = (compSIva - frqFSIva) / (1 + rIva/100.0)

	return resSIva, resCIva, compSIva, compCIva, frqTSIva, frqFSIva, frnqCIva,\
			frqTPaRe, frqFPaRe, regaliaT, regaliaF,\
			sanfT5XC, sanfT5XL, sanfF5XC, sanfF5XL,\
			ofBruTRT, ofBruTRF, ofBruFRT, ofBruFRF, baHonSoc,\
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI
# funcion calComisiones
def comisiones(droid=None, bImp=True):
	rPr  = ES.entradaNumeroConLista(droid, 'Precio del inmueble',
									'Introduzca el monto', CO.lMonto, False)
	rCom = ES.entradaNumeroConLista(droid, 'Comision',
									'Introduzca el porc de comision', CO.lComis, False)
	rIva = ES.entradaNumeroConLista(droid, 'Impuesto al valor agregado',
									'Introduzca el IVA', CO.lIva, False, True)
	(resSIva, resCIva, compSIva, compCIva, frqTSIva, frqFSIva, frnqCIva,
			frqTPaRe, frqFPaRe, regaliaT, regaliaF,
			sanfT5XC, sanfT5XL, sanfF5XC, sanfF5XL,
			ofBruTRT, ofBruTRF, ofBruFRT, ofBruFRF, baHonSoc,
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI) =\
														calComisiones(rPr, rCom, rIva)

	if bImp:
		if CO.bPantAmplia:
			sFormCuota = ("%sPrecio:%s %s, %sComision:%s %s%%, %sIVA:%s %s%%\n")
		else: sFormCuota = "%sPr:%s%s,%s%%Com:%s%s%%,%sIVA:%s%s%%\n"
		sMsj = sFormCuota % (CO.AZUL, CO.FIN, FG.formateaNumero(rPr, 2), CO.AZUL,
								CO.FIN, FG.formateaNumero(rCom, 2), CO.AZUL,
								CO.FIN, FG.formateaNumero(rIva, 2))
		sMsj += ("%sReserva sin IVA:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(resSIva, 2))
		sMsj += ("%sReserva con IVA:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(resCIva, 2))
		sMsj += ("%sCompartido con otra oficina sin IVA:%s %s\n") % (CO.AZUL,
					CO.FIN, FG.formateaNumero(compSIva, 2))
		sMsj += ("%sCompartido con otra oficina con IVA:%s %s\n") % (CO.AZUL,
					CO.FIN, FG.formateaNumero(compCIva, 2))
		sMsj += ("%sFranquicia de reserva sin IVA usando reserva sin IVA:%s %s"
				 " [%s]\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(frqTSIva, 2), FG.formateaNumero(frqTSIva/2, 2))
		sMsj += ("%sFranquicia de reserva sin IVA usando reserva con IVA:%s %s "
				 "[%s]\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(frqFSIva, 2), FG.formateaNumero(frqFSIva/2, 2))
		sMsj += ("%sFranquicia de reserva con IVA:%s %s [%s]\n") % (CO.AZUL,
				 CO.FIN, FG.formateaNumero(frnqCIva, 2),
				 FG.formateaNumero(frnqCIva/2, 2))
		sMsj += ("%sFranquicia a pagar reportada usando %% reportado CN y precio:"
				 "%s %s [%s]\n") % (CO.AZUL, CO.FIN,
				 FG.formateaNumero(frqTPaRe, 2), FG.formateaNumero(frqTPaRe/2, 2))
		sMsj += ("%sFranquicia a pagar reportada usando compartido sin IVA:%s "
				 "%s\n") % (CO.AZUL, CO.FIN, FG.formateaNumero(frqFPaRe, 2))
		sMsj += ("%sSanaf menos 5 por ciento usando franq a pagar rep con %% rep"
				 " CN: %s %s [%s]\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(sanfT5XC, 2), FG.formateaNumero(sanfT5XL, 2))
		sMsj += ("%sSanaf menos 5 por ciento usando precio y lado:%s %s [%s]"
				 "\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(sanfF5XC, 2), FG.formateaNumero(sanfF5XL, 2))
		sMsj += ("%sOficina bruto real usando franquicia a pagar reportada:%s %s "
				 "%s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(ofBruTRT, 2), FG.formateaNumero(ofBruTRF, 2))
		sMsj += ("%sOficina bruto real usando franquicia de reserva sin IVA:%s %s"
				 " %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(ofBruFRT, 2), FG.formateaNumero(ofBruFRF, 2))
		sMsj += ("%sBase honorarios socios:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(baHonSoc, 2))
		sMsj += ("%sBase para honorarios usando franquicia sin IVA con reserva "
				 "sin IVA:%s %s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(baTPaHon, 2), FG.formateaNumero(baFPaHon, 2))
		sMsj += ("%sBase para honorarios usando franquicia sin IVA con reserva "
				 "con IVA:%s %s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(baTPaHoI, 2), FG.formateaNumero(baFPaHoI, 2))
		opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
		return opc
	return rPr, rCom, rIva, resSIva, resCIva, compSIva, compCIva, frqTSIva,\
			frqFSIva, frnqCIva, frqTPaRe, frqFPaRe, regaliaT, regaliaF,\
			sanfT5XC, sanfT5XL, sanfF5XC, sanfF5XL,\
			ofBruTRT, ofBruTRF, ofBruFRT, ofBruFRF, baHonSoc,\
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI
# funcion comisiones

if __name__ == '__main__':
	comisiones()