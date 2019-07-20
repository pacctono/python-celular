# libComisiones: Modulo para el manejo de las comisiones.
#-*- coding:ISO-8859-1 -*-
if __name__ == '__main__': import ES, Const as CO, General as FG
else: from lib import ES, Const as CO, General as FG

def calComisiones(rPr, rCom, rIva=16.0, rXFranq=10.0, rXReCaNa=5.0, xRegalia=80.0,
				xPorcCap=20.0, xPorcGer=10.0):
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
	compSIva = resSIva							# Compartido con otra oficina sin IVA
	compCIva = resCIva							# Compartido con otra oficina con IVA

	frqTSIva = (rXFranq/100.0) * resSIva	# Franquicia de reserva sin IVA. Aplicar. 2 lados
	frqFSIva = (rXFranq/100.0) * resCIva	# Franquicia de reserva sin IVA. No aplicar. 2 lados
	frnqCIva = (rXFranq/100.0) * resCIva	# Franquicia de reserva con IVA. Un calculo. 2 lados.

	frqTPaRe = (rXFranq/100.0) * (rXReCaNa/100.0) * rPr	# Franquicia a pagar reportada. Aplicar. 2 lados
	frqFPaRe = (rXFranq/100.0) * compSIva	# Franquicia a pagar reportada. No aplicar. 2 lados

	regaliaT = (xRegalia/100.0) * frqTPaRe	# Regalia. Aplicar para franquicia a pagar reportada.
	regaliaF = (xRegalia/100.0) * frqFPaRe	# Regalia. No aplicar para franquicia a pagar reportada.

	sanfT5XC = (0.20 * frqTPaRe) - (0.001 * resSIva)		# Sanaf aplicar franquicia a pagar reportada. Ambos lados.
	sanfT5XL = (0.20 * frqTPaRe/2.0) - (0.001 * resSIva / 2.0)	# Sanaf aplicar franquicia a pagar reportada. 1 lado.
	sanfF5XC = (0.20 * frqFPaRe) - (0.001 * resSIva)		# Sanaf no aplicar franquicia a pagar reportada. Ambos lados.
	sanfF5XL = (0.20 * frqFPaRe/2.0) - (0.001 * resSIva / 2.0)	# Sanaf no aplicar franquicia a pagar reportada. 1 lado.

	ofBruTRT = compCIva - frqTPaRe			# Usando franquicia a pagar reportada con %% reportado a Casa Nacional y precio.
	ofBruTRF = compCIva - frqFPaRe			# Usando franquicia a pagar reportada con monto compartido sin IVA.
	ofBruFRT = compCIva - frqTSIva			# Usando franquicia de reserva sin IVA con monto de reserva sin IVA.
	ofBruFRF = compCIva - frqFSIva			# Usando franquicia de reserva sin IVA con monto de reserva con IVA.

	baHonSoc = compCIva - frnqCIva			# Base de honorarios socios.
# Calculo del monto Base para honorarios:
	baTPaHon = compSIva - frqTSIva			# Usando franquicia de reserva sin IVA con monto de reserva sin IVA.
	baFPaHon = compSIva - frqFSIva			# Usando franquicia de reserva sin IVA con monto de reserva con IVA.
	baTPaHoI = (compSIva - frqTSIva) / (1 + CO.IVA/100.0)	# Usando franquicia de reserva sin IVA con monto de reserva con IVA, cuando iva de la negociacion es 0.00.
	baFPaHoI = (compSIva - frqFSIva) / (1 + CO.IVA/100.0)	# Usando franquicia de reserva sin IVA con monto de reserva con IVA, cuando iva de la negociacion es 0.00.
# Calculo del monto de la comision del asesor captador/cerrador:
	xFactCap = xPorcCap/100.0
	capPBTTT = xFactCap * ofBruTRT
	capPBTFT = xFactCap * ofBruTRF
	capPBFTT = xFactCap * ofBruFRT
	capPBFFT = xFactCap * ofBruFRF
	capPBTTF = (xFactCap * baTPaHon) - (0.002 * baTPaHon) + ((rIva/100.0) * xFactCap * baTPaHon)
	capPBTFF = (xFactCap * baFPaHon) - (0.002 * baTPaHon) + ((rIva/100.0) * xFactCap * baTPaHon)
	capPBFTF = (xFactCap * baTPaHoI) - (0.002 * baTPaHon) + ((rIva/100.0) * xFactCap * baTPaHon)
	capPBFFF = (xFactCap * baFPaHoI) - (0.002 * baTPaHon) + ((rIva/100.0) * xFactCap * baTPaHon)
# Calculo del monto de la comision del gerente:
	xFactGer = xPorcGer/100.0
	gerenTTT = xFactGer * ofBruTRT
	gerenTFT = xFactGer * ofBruTRF
	gerenFTT = xFactGer * ofBruFRT
	gerenFFT = xFactGer * ofBruFRF
	gerenTTF = xFactGer * baTPaHon
	gerenTFF = xFactGer * baFPaHon
	gerenFTF = xFactGer * baTPaHoI
	gerenFFF = xFactGer * baFPaHoI

	return resSIva, resCIva, compSIva, compCIva, frqTSIva, frqFSIva, frnqCIva,\
			frqTPaRe, frqFPaRe, regaliaT, regaliaF,\
			sanfT5XC, sanfT5XL, sanfF5XC, sanfF5XL,\
			ofBruTRT, ofBruTRF, ofBruFRT, ofBruFRF, baHonSoc,\
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI,\
			capPBTTT, capPBTFT, capPBFTT, capPBFFT, capPBTTF, capPBTFF, capPBFTF, capPBFFF,\
			gerenTTT, gerenTFT, gerenFTT, gerenFFT, gerenTTF, gerenTFF, gerenFTF, gerenFFF
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
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI,
			capPBTTT, capPBTFT, capPBFTT, capPBFFT, capPBTTF, capPBTFF, capPBFTF, capPBFFF,
			gerenTTT, gerenTFT, gerenFTT, gerenFFT, gerenTTF, gerenTFF, gerenFTF, gerenFFF) =\
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
		sMsj += ("%sCompartido con otra oficina sin IVA:%s %s [%s]\n") % (CO.AZUL,
					CO.FIN, FG.formateaNumero(compSIva, 2),
					FG.formateaNumero(compSIva/2.0, 2))
		sMsj += ("%sCompartido con otra oficina con IVA:%s %s [%s]\n") % (CO.AZUL,
					CO.FIN, FG.formateaNumero(compCIva, 2),
					FG.formateaNumero(compCIva/2.0, 2))
		sMsj += ("%sFranquicia de reserva sin IVA:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando monto de reserva sin IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(frqTSIva, 2), FG.formateaNumero(frqTSIva/2, 2))
		sMsj += ("\t%sUsando monto de reserva con IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(frqFSIva, 2), FG.formateaNumero(frqFSIva/2, 2))
		sMsj += ("%sFranquicia de reserva con IVA:%s %s [%s]\n") % (CO.AZUL,
				 CO.FIN, FG.formateaNumero(frnqCIva, 2),
				 FG.formateaNumero(frnqCIva/2, 2))
		sMsj += ("%sFranquicia a pagar reportada:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando %% reportado a Casa Nacional y precio:"
				 "%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				 FG.formateaNumero(frqTPaRe, 2), FG.formateaNumero(frqTPaRe/2, 2))
		sMsj += ("\t%sUsando monto compartido sin IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				 FG.formateaNumero(frqFPaRe, 2), FG.formateaNumero(frqFPaRe/2.0, 2))
		sMsj += ("%sRegalia:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia a pagar reportada calculada con precio:%s "
				 "%s [%s]\n") % (CO.CYAN, CO.FIN,
				 FG.formateaNumero(regaliaT, 2), FG.formateaNumero(regaliaT/2.0, 2))
		sMsj += ("\t%sUsando franquicia a pagar reportada calculada con monto compartido"
				 " sin IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				 FG.formateaNumero(regaliaT, 2), FG.formateaNumero(regaliaT/2.0, 2))
		sMsj += ("%sSanaf menos 5 por ciento:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia a pagar reportada con %% repeportado"
				 " a Casa Nacional: %s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(sanfT5XC, 2), FG.formateaNumero(sanfT5XL, 2))
		sMsj += ("\t%sUsando precio y lado:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(sanfF5XC, 2), FG.formateaNumero(sanfF5XL, 2))
		sMsj += ("%sOficina bruto real:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia a pagar reportada con %% reportado a Casa "
				 "Nacional y precio:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(ofBruTRT, 2), FG.formateaNumero(ofBruTRT/2.0, 2))
		sMsj += ("\t%sUsando franquicia a pagar reportada con monto compartido sin IVA"
				 ":%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(ofBruTRF, 2), FG.formateaNumero(ofBruTRF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(ofBruFRT, 2), FG.formateaNumero(ofBruFRT/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(ofBruFRF, 2), FG.formateaNumero(ofBruFRF/2.0, 2))
		sMsj += ("%sBase honorarios socios:%s %s\n") % (CO.AZUL, CO.FIN,
				FG.formateaNumero(baHonSoc, 2))
		sMsj += ("%sBase para honorarios:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(baTPaHon, 2), FG.formateaNumero(baTPaHon/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(baFPaHon, 2), FG.formateaNumero(baFPaHon/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(baTPaHoI, 2), FG.formateaNumero(baTPaHoI/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(baFPaHoI, 2), FG.formateaNumero(baFPaHoI/2.0, 2))
		sMsj += ("%s1) Comision del captador/cerrador como un %% del monto bruto real de "
				 "la oficina:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia a pagar reportada con %% reportado a Casa "
				 "Nacional y precio:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBTTT, 2), FG.formateaNumero(capPBTTT/2.0, 2))
		sMsj += ("\t%sUsando franquicia a pagar reportada con monto compartido sin IVA"
				 ":%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBTFT, 2), FG.formateaNumero(capPBTFT/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBFTT, 2), FG.formateaNumero(capPBFTT/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBFFT, 2), FG.formateaNumero(capPBFFT/2.0, 2))
		sMsj += ("%s2) Comision del captador/cerrador como una expresion del monto base "
				 "para honorarios:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBTTF, 2), FG.formateaNumero(capPBTTF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBTFF, 2), FG.formateaNumero(capPBTFF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBFTF, 2), FG.formateaNumero(capPBFTF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(capPBFFF, 2), FG.formateaNumero(capPBFFF/2.0, 2))
		sMsj += ("%s1) Comision del gerente como un %% del monto bruto real de "
				 "la oficina:%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia a pagar reportada con %% reportado a Casa "
				 "Nacional y precio:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenTTT, 2), FG.formateaNumero(gerenTTT/2.0, 2))
		sMsj += ("\t%sUsando franquicia a pagar reportada con monto compartido sin IVA"
				 ":%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenTFT, 2), FG.formateaNumero(gerenTFT/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenFTT, 2), FG.formateaNumero(gerenFTT/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenFFT, 2), FG.formateaNumero(gerenFFT/2.0, 2))
		sMsj += ("%s2) Comision del gerente como un %% del monto base para honorarios"
				 ":%s\n") % (CO.AZUL, CO.FIN)
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva sin "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenTTF, 2), FG.formateaNumero(gerenTTF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA:%s %s [%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenTFF, 2), FG.formateaNumero(gerenTFF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenFTF, 2), FG.formateaNumero(gerenFTF/2.0, 2))
		sMsj += ("\t%sUsando franquicia de reserva sin IVA con monto de reserva con "
				 "IVA, cuando iva de la negociacion es 0.00:%s %s "
				 "[%s]\n") % (CO.CYAN, CO.FIN,
				FG.formateaNumero(gerenFFF, 2), FG.formateaNumero(gerenFFF/2.0, 2))
		opc = ES.imprime(sMsj.rstrip(' \t\n\r'))
		return opc
	return rPr, rCom, rIva, resSIva, resCIva, compSIva, compCIva, frqTSIva,\
			frqFSIva, frnqCIva, frqTPaRe, frqFPaRe, regaliaT, regaliaF,\
			sanfT5XC, sanfT5XL, sanfF5XC, sanfF5XL,\
			ofBruTRT, ofBruTRF, ofBruFRT, ofBruFRF, baHonSoc,\
			baTPaHon, baFPaHon, baTPaHoI, baFPaHoI,\
			capPBTTT, capPBTFT, capPBFTT, capPBFFT, capPBTTF, capPBTFF, capPBFTF, capPBFFF,\
			gerenTTT, gerenTFT, gerenFTT, gerenFFT, gerenTTF, gerenTFF, gerenFTF, gerenFFF
# funcion comisiones

if __name__ == '__main__':
	comisiones()