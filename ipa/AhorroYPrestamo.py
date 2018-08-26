# libIPASPUDO: Modulo para IPASPUDO.
#-*-coding:utf8;-*-
import types
from operator import itemgetter, attrgetter
import json
from ipa import Nomina as NOM
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

def lCheques():
  global lCh

  lClas = COM.lClasCheques
#  lFuncionClas = [compaNumCh, compaCedula, compaNombre, compaMonto, compaEstado, compaFecha, compaConcepto]
  lBanco   = [COM.mBanco(str(k)) for k in range(1, 24)]
  lNombreB = [lBanco[i] for i in range(len(lBanco)) if lBanco[i] != str(i+1)]
  lCodigoB = [str(i+1) for i in range(len(lBanco)) if lBanco[i] != str(i+1)]

  '''  campos = [("Banco", 'combo', (lNombreB, 0)),   # Mercantil por defecto
            ("Clasificacion",'combo', (lClas, 0))]   # Clasificar u ordenar por numero de cheque.
  iCB, iClas = forma(campos)  # Codigo del banco, Indice de clasificacion'''
  iCB   = ES.entradaConLista(droid, 'BANCOS', 'Seleccione banco', lNombreB)
  if None == iCB or 0 > iCB: return None
  iClas = ES.entradaConLista(droid, 'CLASIFICACION', 'Clasificar', lClas)
  if None == iClas or 0 > iClas: return None
  lNvaCh  = [l for l in lCh if ((lCodigoB[iCB] == l[0]) and (6 > len(l[1])))]	# Nueva lista de cheques, solo los del banco.
  																		# l[1]: numero de cheque, si 6 digito es deposito.
  if not lNvaCh:
    ES.alerta(droid, 'CHEQUE EN TRANSITO', "No hay cheque en transito del banco %s!" % lNombreB[iCB])
    return None
  nlNvaCh = len(lNvaCh)
  if 1 == nlNvaCh:
    return lNvaCh[0]
#  lNvaCh.sort(lFuncionClas[iClas])
  lNvaCh.sort(key=itemgetter(iClas))
  try:
    lCheq = [COM.creaOp(l) for l in lNvaCh if 8 >= len(l)]	# Solo las lineas que contengan 8 o mas campos
  except UnicodeError:
    ES.alerta(droid, 'lCheques: ' + str(nlNvaCh), "Hubo un error al tratar de crear opciones!")
    print >> fErr, l
    print >> fErr, len(lNvaCh)
    return None
  nCheques = len(lCheq)
  if (nCheques > CO.NMAXITEM):
    nInicial = int((nCheques/CO.NMAXITEM)+1)
    ES.alerta(droid, 'lCheques', 'Son ' + str(nCheques) + ' cheques! Mostrare ' + str(nInicial) + ' listas!')
    for k in range(nInicial):				# Si el numero de cheques es grande mostrar varias listas de CO.NMAXITEM cada una.
      if (k+1)*CO.NMAXITEM >= nCheques:
        iUltimo = nCheques
        lNueva  = lCheq[k*CO.NMAXITEM:iUltimo]
      else:
        iUltimo = (k+1)*CO.NMAXITEM
        lNueva  = lCheq[k*CO.NMAXITEM:iUltimo] + ['Proxima lista']
      ind = ES.entradaConLista(droid, str(nCheques) + ' CHEQUES. De ' + str((k*CO.NMAXITEM)+1) + ' a ' + str(iUltimo), '', lNueva)
      if None == ind or 0 > ind: return None
      if CO.NMAXITEM > ind:					# Si ind == CO.NMAXITEM, se selecciono la opcion 'Continuar'.
        indice = ind + (k*CO.NMAXITEM)
        break
  else:
    indice = ES.entradaConLista(droid, 'CHEQUES: ' + str(nCheques), 'Seleccione cheque', lCheq)
    if None == indice or 0 > indice: return None
  return lNvaCh[indice]
# funcion lCheques
def mCheque(lChe):
  st = CO.AMARI + COM.lFecha("Sinca", "Cheques")  + ' (Descargado:' + CO.FIN + COM.lFecha('cheques.txt', '') + ')' + "\n"
  if '99' == lChe[0]: sDesc = 'TRA'
  elif 6 > len(lChe[1]): sDesc = 'CHQ'
  else: sDesc = 'DEP'
  st += "Banco:%+10.9s (%-.6s [%s]); Est:%+7.6s\nBeneficiario: %-12.11s%-30.30s\nConcepto: %-31.30s\nFecha:%+11.10s Monto: %-15.14s" % \
  			 (COM.mBanco(lChe[0]), lChe[1], sDesc, COM.mEstado(lChe[7]), ES.fgFormateaNumero(lChe[2]), COM.extraeNombre(lChe[3]),\
  			 lChe[5], lChe[4], ES.fgFormateaNumero(lChe[6], 2))
  ES.imprime(st.rstrip(' \t\n\r'))
  return True
# funcion mCheque

def cheque():
  'Maneja la lista de cheques y muestra la informacion de uno o varios cheque(s).'
  global lCh
  ch = ES.entradaNumero(droid, "CHEQUE", "Numero de cheque", "0", True, True)
  if None == ch or 0 > ch:
    ES.alerta(droid, 'CHEQUE', "Cheque no encontrado!")
    return
  if 0 == ch:
    nCh = lCheques()
    if not nCh: return
    else:
      mCheque(nCh)
      return
  bEnc = False
  for l in lCh:
    if ch > int(l[1]): continue
    elif ch == int(l[1]):
      bEnc = True
      mCheque(l)
#      return	# Comentada para poder mostrar mas de un cheque con el mismo numero.
    else: break
# Fin for
  if not bEnc: ES.alerta(droid, 'CHEQUE', "El cheque %5d no fue encontrado." % ch)
# funcion cheque
def depositos():
  'Maneja la lista de cheques y muestra los depositos de una fecha especifica.'
  global lCh
  sFecha = ES.entradaFechaLocal(droid)

  lDep = [l for l in lCh if '' != l[2] and 6 <= len(l[1]) and sFecha == l[4]]    # Nueva lista de cheques. Solo depositos (# cheque > 100000)
  if not lDep:
    ES.alerta(droid, 'DEPOSITOS X FECHA', "No hay depositos en esa fecha %s!" % sFecha)
    return -3
  nlDep = len(lDep)
  if 1 == nlDep:
    return mCheque(lDep[0])
#  print("Numero de item en arreglo: %5d\n" % nlDep)
#  lCheq = map(creaOp, lDep)  # En vez de list 'comprehensions', como en lCheques.
  lCheq = list(map(COM.creaOp, lDep))  # En vez de list 'comprehensions', como en lCheques.
  indice = ES.entradaConLista(droid, 'DEPOSITOS ENCONTRADOS: ' + str(nlDep), 'Seleccione deposito', lCheq)
  if None == indice or 0 > indice: return -3
  mCheque(lDep[indice])
# funcion depositos
def chequeXCedula(llCh=None):
  'Maneja la lista de cheques y muestra los cheques en transito de un socio.'
  global lCh, cig
  if None==llCh: llCh = lCh

  ci = cig
  if 0 >= ci: return -2

  lCheq = [l for l in llCh if '' != l[2] and ci == int(l[2])]    # Nueva lista de cheques.
  if not lCheq:
    ES.alerta(droid, 'CHEQUE x CEDULA', "No hay cheque en transito con cedula %s!" % ES.fgFormateaNumero(ci))
    return -2
  nCheques = len(lCheq)
  if 1 == nCheques:
    return mCheque(lCheq[0])
#  lCheq = map(creaOp, lCheq)  # En vez de list 'comprehensions', como en lCheques.
  lCheqO = list(map(COM.creaOp, lCheq))  # En vez de list 'comprehensions', como en lCheques.
  indice = ES.entradaConLista(droid, 'CHEQUES ENCONTRADOS: ' + str(nCheques), 'Seleccione cheque', lCheqO)
  if None == indice or 0 > indice: return -2
  mCheque(lCheq[indice])
# funcion chequeXCedula
def heuteXCedula():
  global lHeute

  chequeXCedula(lHeute)
# funcion heuteXCedula
def disponibilidad():
  'Maneja la lista de conceptos de un socio y muestra la informacion.'
  global lSi, cig

  dConc = CO.dConceptos
  ci = cig; sNombre = COM.mNombre(ci)
  if 0 >= ci: return -4

  st = CO.AMARI + COM.lFecha("Sinca", "Disponibilidad") + ' (Descargado:' + CO.FIN + COM.lFecha('disponibilidad.txt', '') + ')' + "\n"	# 'Conta' se refiere al sistema de contabilidad.
  nF = 0		# Numero de registros de una misma persona (socio)
  for l in lSi:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      nF += 1
      if l[1] in dConc:
        if '0' == l[1]: stl = CO.AZUL + dConc[l[1]].rstrip().rjust(20) + CO.FIN + ': ' + l[2].rstrip().ljust(12)
        elif l[1] in ('D', 'E', 'F'):
          stl = CO.AZUL
          if 55 <= CO.nCarLin: stl += ('NETO NOMINA ' + dConc[l[1]]).rstrip().rjust(20)
          else: stl += dConc[l[1]].rstrip().rjust(9)
          stl += CO.FIN + ': '
          if (6 <= len(l)): stl += ES.fgFormateaNumero(l[2]) + '-' + ES.fgFormateaNumero(l[3]) + ' = ' +\
          											ES.fgFormateaNumero(l[4], 2) + '(' + ES.fgFormateaNumero(l[5]) + '%)'
        else: stl = CO.AZUL + dConc[l[1]].rstrip().rjust(20) + CO.FIN + ': ' + ES.fgFormateaNumero(l[2], 2).rstrip().ljust(12)
        if 1 == nF: stl = CO.CYAN + ES.fgFormateaNumero(ci) + ':' + COM.nombreSocio(sNombre) + CO.FIN + "\n" + stl
#        if 'B' == l[1]: disp = l[2].rstrip().rjust(12)
      else: stl = l[2].rstrip() + ' DESCONOCIDO (' + l[1] + ')'
      if '0.00' != l[2].rstrip() or 'A' == l[1]:
        st += stl + '\n'
      if 'C' == l[1] and 55 > CO.nCarLin: st += CO.CYAN + 'N E T O S'.rjust(int((CO.nCarLin-9)/2)+9) + '\n' + CO.FIN	# 9 es la longitud de 'N E T O S'
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  else:
    st += CO.AZUL + ('Dividendo ' + CO.anoDividendo).rjust(20) + CO.FIN + ': '  + ES.fgFormateaNumero(COM.mDividendo(ci), 2).ljust(12) + '\n'
#    ES.alerta(droid, 'DISPONIBILIDAD', '%s: %12s' % (sNombre, ES.fgFormateaNumero(disp, 2)))
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion disponibilidad
def prestamos():
  'Maneja la lista de conceptos de prestamos de un socio y muestra la informacion.'
  global lPre, cig

  ci = cig
  if 0 >= ci: return -5

  st = CO.AMARI + COM.lFecha("Sinca", "Prestamos") + ' (Descargado:' + CO.FIN + COM.lFecha('prestamos.txt', '') + ')' + "\n"
  nF = 0
  bImpar = True

  nCarDesc = CO.nCarLin - 26 - 1		# Numero de caracteres (espacio total), donde se mostrara el campo. 26 es resto.
  maxLongCad = 30									# numero maximo de caracteres del campo especificado.
  if maxLongCad < nCarDesc: nCarDesc = maxLongCad	# > longitud maxima de la cadena a mostrar en el campo.
  nCarMostrar = 23 + nCarDesc						# Numero de caracteres, maximo, a mostrar por linea.
  sTitPrestamos = CO.AZUL + "CON " + CO.justIzqTituloCol('DESCRIPCION', nCarDesc) + "    Saldo  Cuota FeSol"
  if 31 <= (CO.nCarLin - nCarMostrar):				# 31 es la longitud de '     Saldo Saldo+Int Me  #CtCan'.
    sTitPrestamos += ' Monto Sol Saldo+Int Me  #CtCan'
    nCarMostrar   += 31
    bExtra         = True
  else: bExtra     = False
  sTitPrestamos += CO.FIN + "\n"
  for l in lPre:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      nF += 1
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
# 0:Cedula,1:Concepto,2:monto solicitado,3:Monto total(Concedido + intereses);4:Saldo;5:Saldo total(Saldo + intereses);6:Cuota,7:Fecha inicial (mm/aa),8:ult actualizacion (mm),9:cuotas (pagadas/total)
      stl = sColor + l[1] + ' ' + COM.mConcepto(l[1])[0:nCarDesc].ljust(nCarDesc, " ") + ' ' +\
      		ES.fgFormateaNumero(l[4]).rstrip().rjust(9) + ES.fgFormateaNumero(l[6]).rstrip().rjust(7) + ' ' + l[7].rstrip().rjust(5)
      if bExtra: stl += ' ' + ES.fgFormateaNumero(l[2]).rstrip().rjust(9) + ' ' +\
      					ES.fgFormateaNumero(l[5]).rstrip().rjust(9) + ' ' + l[8].rstrip().rjust(2) + ' ' +\
      					l[9].rstrip().rjust(7)
      stl += CO.FIN
      if 1 == nF: stl = CO.CYAN + ES.fgFormateaNumero(ci) + ':' + COM.nombreSocio(COM.mNombre(ci)) + CO.FIN + "\n" +\
      					sTitPrestamos + stl
#      if '0.00' != l[2].rstrip():		# Comparar, cuando agregar la linea. Solicitado = 0.00. Mes ult. act .vs. fecha.
      st += stl + '\n'
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion prestamos
def detallePrestamo(ced, sNombre, lPres, lDesc):
  '''Muestra el detalle de prestamo de un socio.'''

#  sTitulo = "Detalle de un Prestamo"
  sMensaje = ''
  sMensaje  = "%sSocio: %s %s%s\n" % (CO.CYAN, ES.fgFormateaNumero(ced), sNombre.lstrip().split('|')[0], CO.FIN)	# Cedula, Nombre, Codigo y descripcion del concepto.
  sMoPre = ES.fgFormateaNumero(lPres[2], 2)	# Monto concedido
  sTotal = ES.fgFormateaNumero(lPres[3], 2)	# Monto total (Concedido + intereses)
  sSaldo = ES.fgFormateaNumero(lPres[4], 2)	# Saldo
  sSdoTo = ES.fgFormateaNumero(lPres[5], 2)	# Saldo total (Saldo + intereses)
  sCuota = ES.fgFormateaNumero(lPres[6], 2)	# Cuota
  sMensaje += "%sCodigo del Prestamo:%s %s\n" % (CO.AZUL, CO.FIN, lPres[1])
  sMensaje += "%sDescripcion:%s %s\n" % (CO.AZUL, CO.FIN, lDesc)
  sMensaje += "%sMonto concedido:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN, len(sMoPre), len(sMoPre), sMoPre)
  if CO.bPantAmplia: sExtra = ' (Concedido + intereses)'
  else: sExtra = ''
  sMensaje += "%sMonto total%s:%s BsF. %*.*s\n" % (CO.AZUL, sExtra, CO.FIN, len(sTotal), len(sTotal), sTotal)
  sMensaje += "%sSaldo del Prestamo:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN, len(sSaldo), len(sSaldo), sSaldo)
  if CO.bPantAmplia: sExtra = ' (Saldo + intereses)'
  else: sExtra = ''
  sMensaje += "%sMonto total deuda%s:%s BsF. %*.*s\n" % (CO.AZUL, sExtra, CO.FIN, len(sSdoTo), len(sSdoTo), sSdoTo)
  sMensaje += "%sMonto de la cuota:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN, len(sCuota), len(sCuota), sCuota)
  sMensaje += "%sFecha de la solicitud:%s %s\n" % (CO.AZUL, CO.FIN, lPres[7])
  if 0 < len(lPres[8]): sMensaje += "%sMes ult Actualizacion:%s %s\n" % (CO.AZUL, CO.FIN, lPres[8])
  if 0 < len(lPres[9]): sMensaje += "%sNumero de cuotas:%s %s\n" % (CO.AZUL, CO.FIN, lPres[9])
  ES.imprime(sMensaje.rstrip(' \t\n\r'))
# funcion detallePrestamo
def prestamo():
  'Maneja la lista de los prestamos de un socio en Prestamos y muestra el detalle de cualquiera de los prestamos.'
  global lPre, cig

  ci = cig; sNombre = COM.mNombre(ci)
  if 0 >= ci: return -21

  nF = 0
  lCodigo = []
  lPrestamo = []
  lDescripcion = []
  for l in lPre:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      lCodigo.append(l[1])						# Codigo del prestamo
      lDescripcion.append(l[1] + ':' + COM.mConcepto(l[1]))		# Descripcion del prestamo
      lPrestamo.append(l)						# Lista del prestamo
      nF += 1
    else: break
# Fin for
  if 0 >= nF: return None
  else:
    indice      = ES.entradaConLista(droid, 'Prestamos', '', lDescripcion)
    if None == indice or 0 > indice: return None
#    if indice < len(lCodigo): detallePrestamo(ci, sNombre, lPrestamo[indice], lDescripcion[indice].lstrip().split(':')[1])
    if indice < len(lCodigo): detallePrestamo(ci, sNombre, lPrestamo[indice], COM.mConcepto(lCodigo[indice]))
    else: return None
# funcion prestamo
def extension():
  'Maneja la lista de la carga de un socio en la extension y muestra la informacion.'
  global lCgE, utg, cig

  ci = cig
  if 0 >= ci: return -6

  st = CO.AMARI + COM.lFecha("Extension", "Extension") + ' (Descargado:' + CO.FIN + COM.lFecha('extension.txt', '') + ')' + "\n"
  nF = 0											# Numero de filas
  rC = 0.00											# Cuota

  nCarMostrar, nCarNomb, maxCarLs = CO.carPorCampo(lCgE, 2, 28)	# Max numero cars de una linea, max # caracteres del campo.
  if CO.bPantAmplia:											# Verifica si la pantalla es amplia.
    nCarMostrar -= 12									# 12 = numero de caracteres aprox de disponibilidad y A/N.
    nCarNomb    -= 12
    maxCarLs    -= 12
    sParTi = 'PARENTESCO'
    sCuota = '    Cuota'
    nCarMostrar, nCarPare, maxCarLs = CO.carPorCampo(lCgE, 3, nCarMostrar)
  else:
    sParTi   = 'PAREN'
    nCarPare = 3
    sCuota = ' Cta.'
  sTitExtension = CO.AZUL + "    CEDULA " + CO.justIzqTituloCol('NOMBRE', nCarNomb) + CO.justIzqTituloCol(sParTi, nCarPare)\
  						+ sCuota + '  AIng' + CO.FIN + "\n"
  if CO.bPantAmplia:
    sFormato  = '%s%10.10s %-*.*s %-*.*s%8.8s %s%s\n'
    nCarPare += 3
    iDec      = 2
  else:
    sFormato = '%s%10.10s %-*.*s %-*.*s%5.5s %s%s\n'
    nCarPare += 2
    iDec      = 0
  bImpar = True
#[0]Cedula; [1]Cedula carga;[2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco; [4]#UT; [5]Costo poliza
  for l in lCgE:
    if (0 == nF) and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
      try:
        if 0 == nF:
          if '1250' == l[4]: nSumaAseg = 500000
          elif '500' == l[4]: nSumaAseg = 250000
          else: nSumaAseg = 0
          st += CO.CYAN + "SUMA ASEGURADA: " + l[4] + "UT = BsF. " + ES.fgFormateaNumero(nSumaAseg) +\
          		CO.FIN + "\n" + sTitExtension
        nF += 1
        rC += float(l[5])
        if 0 < float(l[5]):
          if l[3].lstrip().split(' ')[0][0:3] in ['TIT', 'CON', 'tit', 'con']:
            sPar = l[3].lstrip().split(' ')[0][0:nCarPare-2] + '-' + l[3][-2:]
          else: sPar = l[3].lstrip().split(' ')[0][0:nCarPare]
          if 6 < len(l) and l[6].isdigit(): sAno = l[6]
          else: sAno = '----'
          st += sFormato % (sColor, ES.fgFormateaNumero(l[1]), nCarNomb, nCarNomb, l[2].lstrip().split('|')[0], nCarPare,\
          					nCarPare, sPar, ES.fgFormateaNumero(float(l[5])/12, iDec), sAno, CO.FIN)
      except Exception as ex:
        print('ex: ', ex)
# Fin elif
    else: break
# Fin for
  if 0 >= nF or 0.00 >= rC:
    st = COM.noCedula(ci)
#    ES.alerta(droid, 'EXTENSION', '%s: INACTIVO' % (sNombre))
  else:
    frC = ES.fgFormateaNumero(rC, 2)
    fmC = ES.fgFormateaNumero(rC/12, 2)
    stl = "TOTAL Anual: %-*.*s (mensual: %-*.*s)" % (len(str(frC)), len(str(frC))+1, frC, \
									len(fmC), len(str(fmC))+1, fmC)
    st += CO.CYAN + stl + CO.FIN
  ES.imprime(st)
# funcion extension
def servifun():
  'Maneja la lista de la carga de un socio en ServiFun y muestra la informacion.'
  global lCgS, utg, cig

  ci = cig
  if 0 >= ci: return -7

  nF = 0
  fC = 0
  st = CO.AMARI + COM.lFecha("Sinca", "ServiFun") + ' (Descargado:' + CO.FIN + COM.lFecha('servifun.txt', '') + ')' + "\n"
  bImpar = True

  nCarMostrar, nCarNomb, maxCarLs = CO.carPorCampo(lCgS, 2, 23)	# Max numero cars de una linea, max # caracteres del campo.
  if CO.bPantAmplia:											# Verifica si la pantalla es amplia.
    nCarMostrar -= 12									# 12 = numero de caracteres aprox de disponibilidad y A/N.
    nCarNomb    -= 12
    maxCarLs    -= 12
    sParTi = 'PARENTE'
    sEsp   = ''
    nCarMostrar, nCarPare, maxCarLs = CO.carPorCampo(lCgS, 3, nCarMostrar)
  else:
    sParTi   = 'PAR'
    nCarPare = 3
    sEsp     = ''
  st += CO.AZUL + "    CEDULA " + CO.justIzqTituloCol('NOMBRE DE LA CARGA', nCarNomb) + CO.justIzqTituloCol(sParTi, nCarPare) +\
  				sEsp + "FInsc" + " Ed" + CO.FIN + "\n"

  sFormato = '%s%10.10s %-*.*s %-*.*s %-5.5s%3d%s\n'
# [0]Cedula; [1]Cedula carga;[2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco;[4]Fecha ingreso a servifun
  for l in lCgS:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      nF += 1
      if '-' == l[3][1:2] and l[3][0:1] in ('A', 'N', 'S', 'T'): fC += CO.CO
      if 5 < len(l) and l[5].isdigit():
        nEd = int(l[5])
        if (l[3][0:1] in ('6', '7')) and (25 < nEd): fC += CO.CHM25
        if (80 < nEd): fC += CO.CM80
        elif (75 < nEd): fC += CO.CM75
        elif (70 < nEd): fC += CO.CM70
      else: nEd = -1
      sColor, bImpar = ES.colorLinea(bImpar, CO.VERDE)
      st += sFormato % (sColor, ES.fgFormateaNumero(l[1], 0), nCarNomb, nCarNomb, l[2].lstrip().split('|')[0], nCarPare,\
      					nCarPare, l[3], l[4], nEd, CO.FIN)
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  else:
    if 1 == nF:
      fC += CO.CI
      sfC = ES.fgFormateaNumero(fC, 2)
      sC = "igual a Bs. %*s" % (len(sfC), sfC)
    else:
      fC += CO.CCC
      sfC = ES.fgFormateaNumero(fC, 2)
      sC = "mayor o igual a Bs. %*s" % (len(sfC), sfC)
    stl = "La cuota mensual es " + sC
    st += CO.CYAN + stl + CO.FIN
  ES.imprime(st.rstrip(' \t\n\r'))
# funcion servifun
def servicioEspecifico(sCodigo, sNombre):
  'Muestra las indemnizaciones de ServiFun usando la lista con los parentesco.'
  global lPa, utg
#  sTitulo = "Servifun"
  sMensaje = ''
  for l in lPa:
    if sCodigo != l[0]: continue			# Codigo del parentesco
    sMensaje  = "%sServicios p/(%s) %s: %s%s\n" % (CO.CYAN, l[0], l[1], sNombre.lstrip().split('|')[0], CO.FIN)	# Codigo, descripcion del parentesco
    if 14 <= len(l): rLp = int(l[13]) * float(utg)			# Lapida
    else: rLp = 0
    sLp = ES.fgFormateaNumero(rLp, 2)		# Lapida formateado
    if 13 <= len(l): rCr = int(l[12]) * float(utg)			# Cremacion
    else: rCr = 0
    sCr = ES.fgFormateaNumero(rCr, 2)		# Cremacion formateado
    if 12 <= len(l): rFo = int(l[11]) * float(utg)			# Fosa
    else: rFo = 0
    sFo = ES.fgFormateaNumero(rFo, 2)		# Fosa formateado
    if 11 <= len(l): rTr = int(l[10]) * float(utg)			# Traslado
    else: rTr = 0
    sTr = ES.fgFormateaNumero(rTr, 2)		# Traslado formateado
    if 10 <= len(l): rSv = int(l[9]) * float(utg)			# Servicio
    else: rSv = 0
    sSv = ES.fgFormateaNumero(rSv, 2)		# Servicio formateado
    if 9 <= len(l): rAy = int(l[8]) * float(utg)			# Ayuda
    else: rAy = 0
    sAy = ES.fgFormateaNumero(rAy, 2)		# Ayuda formateado
    sMensaje += "%sAyuda:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sAy), len(sAy), sAy, l[8])
    sMensaje += "%sServicio:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sSv), len(sSv), sSv, l[9])
    sMensaje += "%sTraslado:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sTr), len(sTr), sTr, l[10])
    if 0 < rFo: sMensaje += "%sFosa (solo 1):%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sFo), len(sFo), sFo, l[11])
    if 0 < rCr: sMensaje += "%sCremacion:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sCr), len(sCr), sCr, l[12])
    if 0 < rLp: sMensaje += "%sLapida:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sLp), len(sLp), sLp, l[13])
  # Fin for
  ES.imprime(sMensaje.rstrip(' \t\n\r'))
# funcion servicioEspecifico
def servicio():
  'Maneja la lista de la carga de un socio en ServiFun y muestra la cobertura a cualquiera de la carga.'
  global lCgS, lPa, cig

  ci = cig
  if 0 >= ci: return -7

  nF = 0
  lCodigo = []
  lParentesco = []
  lNombre = []
  for l in lCgS:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      lPar = l[3].rstrip().split('-')			# Parentesco: codigo-descripcion
      if 1 < len(lPar): lCod = lPar[0]
      else: lCod = '0'
      lCodigo.append(lCod)						# Titular
      lNombre.append(l[2])
      for lp in lPa:
        if lCod != lp[0]: continue				# Codigo del parentesco
        lParentesco.append(lp[1])
      nF += 1
    else: break
# Fin for
  if 0 >= nF: return None
  else:
    indice      = ES.entradaConLista(droid, 'Parentesco', '', lParentesco)
    if None == indice or 0 > indice: return None
    if indice < len(lCodigo): servicioEspecifico(lCodigo[indice], lNombre[indice])
    else: return None
# funcion servicio
def ubicacion():
  'Maneja la lista con los telefonos y correo electronico de cada socio.'
  global lUb, cig

  ci = cig
  if 0 >= ci: return -9

  st = CO.AMARI + COM.lFecha('Sinca', 'Ubicacion') + ' (Descargado:' + CO.FIN + COM.lFecha('ubicacion.txt', '') + ')' + "\n"
  nF = 0
  nJustDerecha = 21
  for l in lUb:
    if ci > int(l[0]): continue
    elif ci == int(l[0]):
      st += "%s%s:%-30.29s%s" % (CO.CYAN, ES.fgFormateaNumero(ci), COM.nombreSocio(COM.mNombre(ci)), CO.FIN)
      if 1 < len(l) and '' != l[1]:
        st += "\n"
        st += CO.AZUL + "Telefono habitacion:".rjust(nJustDerecha) + CO.FIN + " 0%3s-%3s-%4s" % (l[1][0:3], l[1][3:6], l[1][6:])
      if 2 < len(l) and '' != l[2]:
        st += "\n"
        st += CO.AZUL + "Telefono trabajo:".rjust(nJustDerecha) + CO.FIN + " 0%3s-%3s-%4s" % (l[2][0:3], l[2][3:6], l[2][6:])
      if 3 < len(l) and '' != l[3]:
        st += "\n"
        st += CO.AZUL + "Celular:".rjust(nJustDerecha) + CO.FIN + " 0%3s-%3s-%4s" % (l[3][0:3], l[3][3:6], l[3][6:])
      if 4 < len(l) and '' != l[4]:
        st += "\n"
        st += CO.AZUL + "Celular:".rjust(nJustDerecha) + CO.FIN + " 0%3s-%3s-%4s" % (l[4][0:3], l[4][3:6], l[4][6:])
      if 5 < len(l) and '' != l[5]:
        if len(l[5].rstrip(' \t\n\r')) > (CO.nCarLin - nJustDerecha - 1):	# Cars a justificar derecha + 1 espacio despues ':'.
          nJustDerecha = CO.nCarLin - len(l[5].rstrip(' \t\n\r')) - 1
        st += "\n"
        st += CO.AZUL + "Correo:".rjust(nJustDerecha) + CO.FIN + " %s" % l[5].rstrip(' \t\n\r')
      nF += 1
# Fin elif
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  ES.imprime(st)
# funcion ubicacion
def buscarNombre():
  global cig

  nombre = ES.entradaNombre(droid, 'Nombre del socio')
  if None == nombre:
    return -10, None
  nombres = []
  cedulas = []
  try:
    for k,v in COM.dPer.items():
      if 0 <= v.lower().find(nombre.lower()):
        nombres.append(v)
        cedulas.append(k)
  except UnicodeError: pass
  if not nombres:
    ES.alerta(droid, nombre, "No hubo coincidencias!")
    return -10, None
  indice = ES.entradaConLista(droid, 'SOCIOS ENCONTRADOS', 'Seleccione socio(a)', nombres)
  if None == indice or 0 > indice: return -10, None
  cig = int(cedulas[indice])
  return cig, nombres[indice]
# funcion buscarNombre
def selOpcionMenu(lOpciones, sTitulo='Que desea hacer'):	# Devuelve una de las opciones de lOpciones.
  ''' Menu desplegado al inicio. '''
  nOpciones = len(lOpciones)

  lSeleccion = [lOpciones[i][0] for i in range(nOpciones)]	# Opciones a desplegar.
  lFuncion   = [lOpciones[i][1] for i in range(nOpciones)]	# Funciones a ejecutar por cada opcion desplegada.
  indice = ES.entradaConLista(droid, sTitulo, 'Que desea hacer', lSeleccion)
  if None == indice or 0 > indice: return -11
  return lFuncion[indice]
# funcion selOpcionMenu(lOpciones)
def selFuncionInicial(nOpciones=6):		# nOpciones: Primeras opciones de lMenu a desplegar.
  ''' Menu desplegado al inicio. nOpciones = 6: <Cuota>, <Cedula>, <Nombre> ..... y <Salir>. '''

  return selOpcionMenu(COM.lMenu[0:nOpciones] + COM.lMenu[(len(COM.lMenu)-1):], 'Inicio')
# funcion selFuncionInicial(nOpciones)
def selFuncion(nOpcion=6):
  ''' Menu desplegado al suministrar una cedula o al encontrar la cedula de una
      parte de un nombre suministrado.
      Eliminados: ['Calcular cuota', 'cuota'], ['Cedula del socio', 'cedula'],
      ['Buscar cedula del socio', 'nombre'], ['Cheques', 'cheque'],
      ['Deposito por fecha', 'depositos'] '''

  lNuevoMenu = COM.lMenu[nOpcion:(len(COM.lMenu)-1)]+[['Volver', '-11']]	# lMenu sin las 4 primeras opciones + la opcion 'Volver'.
  sTitulo    = str(cig) + ':' + COM.nombreSocio(COM.mNombre(cig))	# Titulo a desplegar con las opciones.
  try:
    func = eval(selOpcionMenu(lNuevoMenu, sTitulo))	# Evaluar contenido de res['name']; el cual, debe ser una funcion conocida.
  except:
    return False
  if isinstance(func, types.FunctionType): func()	# Si la cadena evaluada es una funcion, ejecutela.
  else: return False
  return True
# funcion selFuncion
def prepararListasDeTrabajo(sNombre='todos'):
  global lHeute, lCh, lSi, lPre, lCgE, lCgS, lUb, lPa

  if ('todos'==sNombre) or ('heute'==sNombre):      lHeute = ES.cargaLista("heute.txt")		# [0]Banco; [1]Numero; [2]Cedula;
  											# [3]Nombre; [4]Fecha(d/m/a); [5]descripcion; [6]monto; [7]estado
  if ('todos'==sNombre) or ('cheques'==sNombre):    lCh = ES.cargaLista("cheques.txt")		# [0]Banco; [1]Numero; [2]Cedula;
  											# [3]Nombre; [4]Fecha(d/m/a); [5]descripcion; [6]monto; [7]estado
  if ('todos'==sNombre) or ('disponibilidad'==sNombre):    lSi = ES.cargaLista("disponibilidad.txt")	# [0]Cedula;
  											# [1]Codigo identificador proximo campo; [2] Campo(Fecha, Monto, etc)
  if ('todos'==sNombre) or ('prestamos'==sNombre):  lPre = ES.cargaLista("prestamos.txt")	# [0]Cedula; [1]Concepto;
  											# [2]Monto solicitado; [3]Monto total(Concedido + intereses); [4]Saldo;
  											# [5]Saldo total(Saldo + intereses); [6]Cuota; [7]Fecha inicial (mm/aa);
  											# [8]ult actualizacion (mm); [9]cuotas (pagadas/total)
  if ('todos'==sNombre) or ('extension'==sNombre):  lCgE = ES.cargaLista("extension.txt")	# [0]Cedula; [1]Cedula carga;
  											# [2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco; [4]#UT; [5]Costo poliza
  if ('todos'==sNombre) or ('servifun'==sNombre):   lCgS = ES.cargaLista("servifun.txt")	# [0]Cedula; [1]Cedula carga;
  											# [2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco;
  											# [4]Fecha ingreso a servifun
  if ('todos'==sNombre) or ('ubicacion'==sNombre):  lUb = ES.cargaLista("ubicacion.txt")	# [0]Cedula;
  											# [1]Telefono habitacion; [2]Telefono trabajo; [3]Celular 1; [4]Celular 2;
  											# [5]Correo electronico
  if ('todos'==sNombre) or ('parentesco'==sNombre): lPa = ES.cargaLista("parentesco.txt")	# [0]Codigo; [1]Descripcion;
  											# [2]Identificar de cambio(Sexo/edad); [3]Poliza 500UT;
  											# [4]Poliza 500UT si cumple requisito de cambio, ver campo 2; [5]Poliza 1250UT;
  											# [6]Poliza 1250UT si cumple requisito de cambio, ver campo 2;
  											# Servifun: [7]Cuota extra; [8]Ayuda; [9]Servicio; [10]Traslado; [11]Fosa;
  											# [12]Cremacion
# funcion prepararVariablesDeTrabajo
def leeValXDefecto():
  global cig

  fIpa = ES.abrir("ipaspudo.txt")
  if not fIpa:
    sUXD   = 'ipas'				# Usuario por defecto
    sCXD   = 'ipas'				# Contraseña por defecto
  else:
    try:
      sIpa = fIpa.read()
      lIpa = json.loads(sIpa)
      sUXD = lIpa[0]		# Usuario por defecto
      sCXD = lIpa[1]		# Contraseña por defecto
      cig  = lIpa[2]		# Cedula por defecto. Esta linea es solo para mejorar la vista.
    except: pass
    finally: fIpa.close()
  return sUXD, sCXD
# funcion leeValXDefecto
def escValXDefecto(sUXD, sCXD):
  global cig

  lIpa = [sUXD, sCXD, cig]
  fIpa = ES.abrir("ipaspudo.txt", 'w')
  if fIpa:
    try: fIpa.write(json.dumps(lIpa))
    except: pass
    finally: fIpa.close()
  else: print("No se grabaron los valores por defecto!")
# funcion escValXDefecto

# Definir variables globales
cig    = -1
utg    = CO.UT
fErr   = ES.abrirErr("ipaspudo.err")