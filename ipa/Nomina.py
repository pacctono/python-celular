# libNomina: Modulo para el manejo de la nomina de la UDO para IPASPUDO.
#-*-coding:utf8;-*-
from ipa import Comun as COM
from lib import ES, Const as CO

try:
  from lib import DIR, LINEA, bMovil
except:
  DIR = './'
  bMovil = False

if bMovil:
  try:
    import androidhelper as android
  except:
    import android
  droid = android.Android()
else: droid = None

def resNominaN(lN=None):
  '''Maneja el resumen de todos los conceptos de IPASPUDO de la nomina
    recibida como parametro.'''
  global lNomN
  if None == lN: lN = lNomN
  
  st = CO.AMARI + COM.lFecha("Nomina", "Nomina") + ' (Descargado:' + CO.FIN + \
                                      COM.lFecha('nomina.txt', '') + ')' + "\n"
  ftValFi = 0.00
  ftValVa = 0.00
  ftTotal = 0.00
  bImpar  = True

  sTitNomina  = CO.AZUL + "CON".ljust(4) + 'DESCRIPCION'.ljust(25) +\
                      "VALOR FIJO".rjust(16) + "VALOR VARIABLE".rjust(16) + \
                      "T O T A L".rjust(16) + CO.FIN + "\n"
  st += sTitNomina
  for l in lN:
      if 8 > len(l) or 0.00 == float(l[7]): continue
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
      # 0:Concepto, 1:Descripcion, 2:Cta credito, 3:Cta Debito, 4:Cta Interese, 5:Valor fijo, 6: Valor variable, 7:Total
      stl = "%s%.3s %-25.25s %15.15s %15.15s %15.15s%s" % (sColor, l[0], l[1],
                      ES.fgFormateaNumero(l[5], 2).rstrip().rjust(15),
                      ES.fgFormateaNumero(l[6], 2).rstrip().rjust(15),
                      ES.fgFormateaNumero(l[7], 2).rstrip().rjust(15), CO.FIN)
      ftValFi += float(l[5])
      ftValVa += float(l[6])
      ftTotal += float(l[7])
      st += stl + '\n'
  # Fin for
  stValFi = ES.fgFormateaNumero(ftValFi, 2)
  stValVa = ES.fgFormateaNumero(ftValVa, 2)
  stTotal = ES.fgFormateaNumero(ftTotal, 2)
  stl = CO.AZUL + "T O T A L E S".rjust(29) + stValFi.rjust(16) + \
                                stValVa.rjust(16) + stTotal.rjust(16) + CO.FIN
  st += stl
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion resNominaN
def resNominaH():
	global lNomH
	resNominaN(lNomH)
# funcion resNominaH
def resNominaC():
	global lNomC
	resNominaN(lNomC)
# funcion resNominaN
def resNominaCcE():
	global lNomCcE
	resNominaN(lNomCcE)
# funcion resNominaN
def nomina(bLN=True):
  '''Maneja la lista de conceptos de nomina de un socio y
    muestra la informacion.'''
  global lNom, lNomCNE
  from ipa.AhorroYPrestamo import cig as ci
 
  if bLN: lN = lNom
  else: lN   = lNomCNE
  if 0 >= ci: return -8

  st = CO.AMARI + COM.lFecha("Nomina", "Nomina") + ' (Descargado:' + CO.FIN + \
                                      COM.lFecha('nomina.txt', '') + ')' + "\n"
  nF = 0
  ftAsig = 0.00
  ftDed  = 0.00
  bImpar = True

  nCarDesc = CO.nCarLin - 23 - 1	# Numero de caracteres (espacio total), donde se mostrara el campo. 23 es resto.
  maxLongCad = 28									# numero maximo de caracteres del campo especificado.
  if maxLongCad < nCarDesc: nCarDesc = maxLongCad	# > longitud maxima de la cadena a mostrar en el campo.
  nCarMostrar = 23 + nCarDesc			# Numero de caracteres, maximo, a mostrar por linea.
  sTitNomina  = CO.AZUL + "CON " + CO.justIzqTituloCol('DESCRIPCION',
                                        nCarDesc) + "  ValorFijo ValorVariab"
  if 25 <= (CO.nCarLin - nCarMostrar):				# 25 es la maxima longitud del 'saldo[cuota]'.
    sTitNomina  += '          Saldo:[Cuota]'
    nCarMostrar += 25
    nCarSaldo    = 15
    bSaldo       = True
  else:
    nCarSaldo = 0
    bSaldo    = False
  sTitNomina += CO.FIN + "\n"
  for l in lN:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      nF += 1
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
      # 0:Cedula, 1:Concepto, 2:Valor fijo, 3: Valor variable, 4:Saldo, 5:Cuota
      stl = "%s%.3s %*.*s %.11s %.11s%s" % (sColor, l[1], nCarDesc, nCarDesc,
                                      COM.mConcepto(l[1]).ljust(nCarDesc, " "),
                              ES.fgFormateaNumero(l[2], 2).rstrip().rjust(11),
                              ES.fgFormateaNumero(l[3], 2).rstrip().rjust(11),
                              CO.FIN)
      if bSaldo:
        if (0.00 < float(l[4])):
          stl += "%s%.*s[%s]%s" % (sColor, nCarSaldo,
                      ES.fgFormateaNumero(l[4], 2).rstrip().rjust(nCarSaldo),
                      ES.fgFormateaNumero(l[5], 2).rstrip(), CO.FIN)
      try:
        if (500 > int(l[1])): ftAsig += float(l[2]) + float(l[3])
        else: ftDed += float(l[2]) + float(l[3])
      except Exception as ex:
        print('Tipo: ' + type(ex), ', ex: ', ex)
      if 1 == nF:
        stl = CO.CYAN + ES.fgFormateaNumero(ci) + ':' + \
            COM.nombreSocio(COM.mNombre(ci)) + CO.FIN + "\n" + sTitNomina + stl
      st += stl + '\n'
    else: break
  # Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  elif (0.00 != ftAsig) or (0.00 != ftDed):
    fNeto = ftAsig - ftDed
    stAsig = ES.fgFormateaNumero(ftAsig, 2)
    stDed  = ES.fgFormateaNumero(ftDed, 2)
    sNeto  = ES.fgFormateaNumero(fNeto, 2)
    if bSaldo:
      sFormato = ("%sAsignaciones:%s%-*.*s; %sDeducciones:%s%-*.*s; "
                  "%sNeto:%s %-*.*s")
    else: sFormato = "%sAs:%s%-*.*s;%sDs:%s%-*.*s;%sNeto:%s %-*.*s"
    stl = sFormato % (CO.AZUL, CO.FIN, len(stAsig), len(stAsig)+1, stAsig, 
              				CO.AZUL, CO.FIN, len(stDed), len(stDed)+1, stDed,
                      CO.AZUL, CO.FIN, len(sNeto), len(sNeto)+1, sNeto)
    st += stl
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion nomina
def detalleConcepto(ced, sNombre, lCon, lDesc):
  'Muestra el detalle de Concepto de un socio.'
  #  sTitulo = "Detalle de un Concepto"
  sMensaje = ''
  # 0:Cedula, 1:Concepto, 2:Valor fijo, 3: Valor variable, 4:Saldo, 5:Cuota
  sMensaje  = "%sSocio: %s %s%s\n" % (CO.CYAN, ES.fgFormateaNumero(ced), 
                                      sNombre.lstrip().split('|')[0], CO.FIN)	# Cedula, Nombre, Codigo y descripcion del concepto.
  sVaFij = ES.fgFormateaNumero(lCon[2], 2)	# Valor fijo
  sVaVar = ES.fgFormateaNumero(lCon[3], 2)	# Valor variable
  sSaldo = ES.fgFormateaNumero(lCon[4], 2)	# Saldo
  sCuota = ES.fgFormateaNumero(lCon[5], 2)	# Cuota
  sMensaje += "%sCodigo del Concepto:%s %s\n" % (CO.AZUL, CO.FIN, lCon[1])
  sMensaje += "%sDescripcion:%s %s\n" % (CO.AZUL, CO.FIN, lDesc)
  sMensaje += "%sValor fijo:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN, len(sVaFij),
                                                          len(sVaFij), sVaFij)
  sMensaje += "%sValor variable:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN,
                                              len(sVaVar), len(sVaVar), sVaVar)
  sMensaje += "%sSaldo del Concepto:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN,
                                              len(sSaldo), len(sSaldo), sSaldo)
  sMensaje += "%sMonto de la cuota:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN,
                                              len(sCuota), len(sCuota), sCuota)
  # Fin for
  ES.imprime(sMensaje.rstrip(' \t\n\r'))
# funcion detalleConcepto
def concepto(bLN=True):
  '''Maneja la lista de los conceptos de un socio en Nomina y
    muestra el detalle de cualquiera de los conceptos.'''
  global lNom, lNomCNE
  from ipa.AhorroYPrestamo import cig as ci

  if bLN: lN = lNom
  else: lN   = lNomCNE
  sNombre = COM.mNombre(ci)
  if 0 >= ci: return -21

  nF = 0
  lCodigo = []
  lConcepto = []
  lDescripcion = []
  for l in lN:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      lCodigo.append(l[1])						# Codigo del concepto
      lDescripcion.append(l[1] + ':' + COM.mConcepto(l[1]))		# Descripcion del concepto
      lConcepto.append(l)						# Lista del concepto
      nF += 1
    else: break
  # Fin for
  if 0 >= nF: return None
  else:
    indice      = ES.entradaConLista(droid, 'Conceptos', '', lDescripcion)
    if None == indice or 0 > indice: return None
    # if indice < len(lCodigo): detalleConcepto(ci, sNombre, lConcepto[indice], lDescripcion[indice].lstrip().split(':')[1])
    if indice < len(lCodigo):
      detalleConcepto(ci, sNombre, lConcepto[indice],
                                                COM.mConcepto(lCodigo[indice]))
    else: return None
# funcion concepto
def nominacne():
  '''Maneja la lista de conceptos de nomina de un socio y
    muestra la informacion.'''
  nomina(False)
# funcion nominacne
def conceptocne():
  concepto(False)
# funcion conceptocne
lNom = ES.cargaLista("nomina.txt")		# [0]Cedula; [1]Concepto;
  											# [2]Valor fijo; [3]Valor variable; [4]Saldo; [5]Cuota
lNomCNE = ES.cargaLista("nominacne.txt")	# [0]Cedula; [1]Concepto;
  											# [2]Valor fijo; [3]Valor variable; [4]Saldo; [5]Cuota
lNomN = ES.cargaLista("concNominaN.txt")	# [0]Concepto; [1]Descripcion;
  											# [2]Cta Debito; [3]cta credito; [4]cta interes;
  											# [5]Valor fijo; [6]Valor variable; [7]Total
lNomH = ES.cargaLista("concNominaH.txt")	# [0]Concepto; [1]Descripcion;
  											# [2]Cta Debito; [3]cta credito; [4]cta interes;
  											# [5]Valor fijo; [6]Valor variable; [7]Total
lNomC = ES.cargaLista("concNominaC.txt")	# [0]Concepto; [1]Descripcion;
  											# [2]Cta Debito; [3]cta credito; [4]cta interes;
  											# [5]Valor fijo; [6]Valor variable; [7]Total
lNomCcE = ES.cargaLista("concNominaCcE.txt")	# [0]Concepto; [1]Descripcion;
  											# [2]Cta Debito; [3]cta credito; [4]cta interes;
  											# [5]Valor fijo; [6]Valor variable; [7]Total