# libAhorroYPrestamo: Modulo de ahorro y prestamo para IPASPUDO.
#-*-coding:utf8;-*-
from operator import itemgetter, attrgetter
from ipa import ExtensionYServiFun as ESF
from ipa import Nomina as NOM
from ipa import Comun as COM
from lib import ES, Const as CO, General as FG

try:
  from lib import DIR, LINEA, bMovil
except:
  DIR    = './'
  LINEA  = 70
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
    ES.alerta(droid, 'CHEQUE EN TRANSITO',
                    "No hay cheque en transito del banco %s!" % lNombreB[iCB])
    return None
  nlNvaCh = len(lNvaCh)
  if 1 == nlNvaCh:
    return lNvaCh[0]
#  lNvaCh.sort(lFuncionClas[iClas])
  lNvaCh.sort(key=itemgetter(iClas))
  try:
    lCheq = [COM.creaOp(l) for l in lNvaCh if 8 >= len(l)]	# Solo las lineas que contengan 8 o mas campos
  except UnicodeError:
    ES.alerta(droid, 'lCheques: ' + str(nlNvaCh),
                                "Hubo un error al tratar de crear opciones!")
    print >> fErr, l
    print >> fErr, len(lNvaCh)
    return None
  nCheques = len(lCheq)
  if (nCheques > CO.NMAXITEM):
    nInicial = int((nCheques/CO.NMAXITEM)+1)
    ES.alerta(droid, 'lCheques', 'Son ' + str(nCheques) +
                          ' cheques! Mostrare ' + str(nInicial) + ' listas!')
    for k in range(nInicial):				# Si el numero de cheques es grande mostrar varias listas de CO.NMAXITEM cada una.
      if (k+1)*CO.NMAXITEM >= nCheques:
        iUltimo = nCheques
        lNueva  = lCheq[k*CO.NMAXITEM:iUltimo]
      else:
        iUltimo = (k+1)*CO.NMAXITEM
        lNueva  = lCheq[k*CO.NMAXITEM:iUltimo] + ['Proxima lista']
      ind = ES.entradaConLista(droid, str(nCheques) + ' CHEQUES. De ' +
                    str((k*CO.NMAXITEM)+1) + ' a ' + str(iUltimo), '', lNueva)
      if None == ind or 0 > ind: return None
      if CO.NMAXITEM > ind:					# Si ind == CO.NMAXITEM, se selecciono la opcion 'Continuar'.
        indice = ind + (k*CO.NMAXITEM)
        break
  else:
    indice = ES.entradaConLista(droid, 'CHEQUES: ' + str(nCheques),
                                                  'Seleccione cheque', lCheq)
    if None == indice or 0 > indice: return None
  return lNvaCh[indice]
# Funcion lCheques
def mCheque(lChe):
  st = CO.AMARI + COM.lFecha("Sinca", "Cheques")  + ' (Descargado:' + CO.FIN +\
                                    COM.lFecha('cheques.txt', '') + ')' + "\n"
  if '99' == lChe[0]: sDesc = 'TRA'
  elif 6 > len(lChe[1]): sDesc = 'CHQ'
  else: sDesc = 'DEP'
  st += ("Banco:%+10.9s (%-.6s [%s]); Est:%+7.6s\nBeneficiario: "
          "%-12.11s%-30.30s\nConcepto: %-31.30s\nFecha:%+11.10s Monto: "
          "%-15.14s") % (COM.mBanco(lChe[0]), lChe[1], sDesc,
        COM.mEstado(lChe[7]), FG.formateaNumero(lChe[2]),
        COM.extraeNombre(lChe[3]), lChe[5], lChe[4], FG.formateaNumero(lChe[6],
        2))
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion mCheque
def cheque():
  '''Maneja la lista de cheques y muestra la informacion de uno o
    varios cheque(s).'''
  global lCh

  ch = ES.entradaNumero(droid, "CHEQUE", "Numero de cheque", "0", True, True)
  if None == ch or 0 > ch:
    ES.alerta(droid, 'CHEQUE', "Cheque no encontrado!")
    return None
  if 0 == ch:
    nCh = lCheques()
    if not nCh: return None
    else:
      mCheque(nCh)
      return None
  bEnc = False
  for l in lCh:
    if ch > int(l[1]): continue
    elif ch == int(l[1]):
      bEnc = True
      mCheque(l)
  # return	# Comentada para poder mostrar mas de un cheque con el mismo numero.
    else: break
  # Fin for
  if not bEnc: ES.alerta(droid, 'CHEQUE', "El cheque %5d no fue encontrado." 
                                                                        % ch)
  return None
# Funcion cheque
def depositos():
  '''Maneja la lista de cheques y muestra los depositos de
    una fecha especifica.'''
  global lCh

  sFecha = ES.entradaFechaLocal(droid)

  lDep = [l for l in lCh if '' != l[2] and 6 <= len(l[1]) and sFecha == l[4]]    # Nueva lista de cheques. Solo depositos (# cheque > 100000)
  if not lDep:
    ES.alerta(droid, 'DEPOSITOS X FECHA', "No hay depositos en esa fecha %s!"
                                                                    % sFecha)
    return -3
  nlDep = len(lDep)
  if 1 == nlDep:
    return mCheque(lDep[0])
#  print("Numero de item en arreglo: %5d\n" % nlDep)
#  lCheq = map(creaOp, lDep)  # En vez de list 'comprehensions', como en lCheques.
  lCheq = list(map(COM.creaOp, lDep))  # En vez de list 'comprehensions', como en lCheques.
  indice = ES.entradaConLista(droid, 'DEPOSITOS ENCONTRADOS: ' + str(nlDep),
                                                  'Seleccione deposito', lCheq)
  if None == indice or 0 > indice: return -3
  mCheque(lDep[indice])
# Funcion depositos
def chequeXCedula(ci, llCh=None):
  'Maneja la lista de cheques y muestra los cheques en transito de un socio.'
  global lCh
  if None==llCh: llCh = lCh

  if 0 >= ci: return -2

  lCheq = [l for l in llCh if '' != l[2] and ci == int(l[2])]    # Nueva lista de cheques.
  if not lCheq:
    ES.alerta(droid, 'CHEQUE x CEDULA', "No hay cheque en transito con cedula "
                                        "%s!" % FG.formateaNumero(ci))
    return -2
  nCheques = len(lCheq)
  if 1 == nCheques:
    return mCheque(lCheq[0])
#  lCheq = map(creaOp, lCheq)  # En vez de list 'comprehensions', como en lCheques.
  lCheqO = list(map(COM.creaOp, lCheq))  # En vez de list 'comprehensions', como en lCheques.
  indice = ES.entradaConLista(droid, 'CHEQUES ENCONTRADOS: ' + str(nCheques), 
                                                  'Seleccione cheque', lCheqO)
  if None == indice or 0 > indice: return -2
  mCheque(lCheq[indice])
# Funcion chequeXCedula
def heuteXCedula(ci):
  global lHeute

  chequeXCedula(ci, lHeute)
# Funcion heuteXCedula
def disponibilidad(ci):
  'Maneja la lista de conceptos de un socio y muestra la informacion.'
  global lSi

  dConc = CO.dConceptos
  sNombre = COM.mNombre(ci)
  if 0 >= ci: return -4

  st = CO.AMARI + COM.lFecha("Sinca", "Disponibilidad") + ' (Descargado:' + \
        CO.FIN + COM.lFecha('disponibilidad.txt', '') + ')' + "\n"	# 'Conta' se refiere al sistema de contabilidad.
  nF = 0		# Numero de registros de una misma persona (socio)
  for l in lSi:
    if 0 == nF and ('' == l[0] or ci > int(l[0])): continue
    elif l[0] in ('','0',str(ci)):
      nF += 1
      if l[1] in dConc:
        if '0' == l[1]: stl = CO.AZUL + dConc[l[1]].rstrip().rjust(20) + \
                                      CO.FIN + ': ' + l[2].rstrip().ljust(12)
        elif l[1] in ('D', 'E', 'F'):
          stl = CO.AZUL
          if 55 <= CO.nCarLin:
            stl += ('NETO NOMINA ' + dConc[l[1]]).rstrip().rjust(20)
          else: stl += dConc[l[1]].rstrip().rjust(9)
          stl += CO.FIN + ': '
          if (6 <= len(l)):
            stl += FG.formateaNumero(l[2]) + '-' + FG.formateaNumero(l[3]) + \
                    ' = ' + FG.formateaNumero(l[4], 2) + '(' + \
                                                FG.formateaNumero(l[5]) + '%)'
        else:
          stl = CO.AZUL + dConc[l[1]].rstrip().rjust(20) + CO.FIN + ': ' + \
                                FG.formateaNumero(l[2], 2).rstrip().ljust(12)
        if 1 == nF:
          stl = CO.CYAN + FG.formateaNumero(ci) + ':' + \
                                COM.nombreSocio(sNombre) + CO.FIN + "\n" + stl
#        if 'B' == l[1]: disp = l[2].rstrip().rjust(12)
      else: stl = l[2].rstrip() + ' DESCONOCIDO (' + l[1] + ')'
      if '0.00' != l[2].rstrip() or 'A' == l[1]:
        st += stl + '\n'
      if 'C' == l[1] and 55 > CO.nCarLin:
        st += CO.CYAN + 'N E T O S'.rjust(int((CO.nCarLin-9)/2)+9) + '\n' + \
                                                    CO.FIN	# 9 es la longitud de 'N E T O S'
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  else:
    st += CO.AZUL + ('Dividendo ' + CO.anoDividendo).rjust(20) + CO.FIN + \
              ': ' + FG.formateaNumero(COM.mDividendo(ci), 2).ljust(12) + '\n'
#    ES.alerta(droid, 'DISPONIBILIDAD', '%s: %12s' % (sNombre, FG.formateaNumero(disp, 2)))
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion disponibilidad
def prestamos(ci):
  '''Maneja la lista de conceptos de prestamos de un socio y
    muestra la informacion.'''
  global lPre

  if 0 >= ci: return -5

  st = CO.AMARI + COM.lFecha("Sinca", "Prestamos") + ' (Descargado:' + \
                        CO.FIN + COM.lFecha('prestamos.txt', '') + ')' + "\n"
  nF = 0
  bImpar = True

  nCarDesc = CO.nCarLin - 26 - 1		# Numero de caracteres (espacio total), donde se mostrara el campo. 26 es resto.
  maxLongCad = 30									# numero maximo de caracteres del campo especificado.
  if maxLongCad < nCarDesc: nCarDesc = maxLongCad	# > longitud maxima de la cadena a mostrar en el campo.
  nCarMostrar = 23 + nCarDesc						# Numero de caracteres, maximo, a mostrar por linea.
  sTitPrestamos = CO.AZUL + "CON " + CO.justIzqTituloCol('DESCRIPCION', \
                                          nCarDesc) + "    Saldo  Cuota FeSol"
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
      stl = sColor + l[1] + ' ' + \
              COM.mConcepto(l[1])[0:nCarDesc].ljust(nCarDesc, " ") + ' ' + \
      		    FG.formateaNumero(l[4]).rstrip().rjust(9) + \
              FG.formateaNumero(l[6]).rstrip().rjust(7) + ' ' + \
              l[7].rstrip().rjust(5)
      if bExtra:
        stl += ' ' + FG.formateaNumero(l[2]).rstrip().rjust(9) + ' ' + \
      					FG.formateaNumero(l[5]).rstrip().rjust(9) + ' ' + \
                l[8].rstrip().rjust(2) + ' ' + l[9].rstrip().rjust(7)
      stl += CO.FIN
      if 1 == nF:
        stl = CO.CYAN + FG.formateaNumero(ci) + ':' + \
                COM.nombreSocio(COM.mNombre(ci)) + CO.FIN + "\n" + \
                sTitPrestamos + stl
      # if '0.00' != l[2].rstrip():		# Comparar, cuando agregar la linea. Solicitado = 0.00. Mes ult. act .vs. fecha.
      st += stl + '\n'
    else: break
  # Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  opc = ES.imprime(st.rstrip(' \t\n\r'))
  return opc
# Funcion prestamos
def detallePrestamo(ced, sNombre, lPres, lDesc):
  '''Muestra el detalle de prestamo de un socio.'''

#  sTitulo = "Detalle de un Prestamo"
  sMensaje = ''
  sMensaje  = "%sSocio: %s %s%s\n" % (CO.CYAN, FG.formateaNumero(ced), 
                                      sNombre.lstrip().split('|')[0], CO.FIN)	# Cedula, Nombre, Codigo y descripcion del concepto.
  sMoPre = FG.formateaNumero(lPres[2], 2)	# Monto concedido
  sTotal = FG.formateaNumero(lPres[3], 2)	# Monto total (Concedido + intereses)
  sSaldo = FG.formateaNumero(lPres[4], 2)	# Saldo
  sSdoTo = FG.formateaNumero(lPres[5], 2)	# Saldo total (Saldo + intereses)
  sCuota = FG.formateaNumero(lPres[6], 2)	# Cuota
  sMensaje += "%sCodigo del Prestamo:%s %s\n" % (CO.AZUL, CO.FIN, lPres[1])
  sMensaje += "%sDescripcion:%s %s\n" % (CO.AZUL, CO.FIN, lDesc)
  sMensaje += "%sMonto concedido:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN, 
                                            len(sMoPre), len(sMoPre), sMoPre)
  if CO.bPantAmplia: sExtra = ' (Concedido + intereses)'
  else: sExtra = ''
  sMensaje += "%sMonto total%s:%s BsF. %*.*s\n" % (CO.AZUL, sExtra, CO.FIN,
                                            len(sTotal), len(sTotal), sTotal)
  sMensaje += "%sSaldo del Prestamo:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN,
                                            len(sSaldo), len(sSaldo), sSaldo)
  if CO.bPantAmplia: sExtra = ' (Saldo + intereses)'
  else: sExtra = ''
  sMensaje += "%sMonto total deuda%s:%s BsF. %*.*s\n" % (CO.AZUL, sExtra,
                                      CO.FIN, len(sSdoTo), len(sSdoTo), sSdoTo)
  sMensaje += "%sMonto de la cuota:%s BsF. %*.*s\n" % (CO.AZUL, CO.FIN,
                                              len(sCuota), len(sCuota), sCuota)
  sMensaje += "%sFecha de la solicitud:%s %s\n" % (CO.AZUL, CO.FIN, lPres[7])
  if 0 < len(lPres[8]): sMensaje += "%sMes ult Actualizacion:%s %s\n" %\
                                                  (CO.AZUL, CO.FIN, lPres[8])
  if 0 < len(lPres[9]): sMensaje += "%sNumero de cuotas:%s %s\n" % (CO.AZUL,
                                                            CO.FIN, lPres[9])
  opc = ES.imprime(sMensaje.rstrip(' \t\n\r'))
  return opc
# Funcion detallePrestamo
def prestamo(ci):
  '''Maneja la lista de los prestamos de un socio en Prestamos y
    muestra el detalle de cualquiera de los prestamos.'''
  global lPre

  sNombre = COM.mNombre(ci)
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
    indice = ES.entradaConLista(droid, 'Prestamos', '', lDescripcion)
    if None == indice or 0 > indice: return None
    # if indice < len(lCodigo): detallePrestamo(ci, sNombre, lPrestamo[indice], lDescripcion[indice].lstrip().split(':')[1])
    if indice < len(lCodigo): return detallePrestamo(ci, sNombre,
                             lPrestamo[indice], COM.mConcepto(lCodigo[indice]))
    else: return None
# Funcion prestamo
def ubicacion(ci):
  '''Maneja la lista con los telefonos y correo electronico de cada socio.'''
  global lUb

  if 0 >= ci: return -9

  st = CO.AMARI + COM.lFecha('Sinca', 'Ubicacion') + ' (Descargado:' + CO.FIN \
                                + COM.lFecha('ubicacion.txt', '') + ')' + "\n"
  nF = 0
  nJustDerecha = 21
  for l in lUb:
    if ci > int(l[0]): continue
    elif ci == int(l[0]):
      st += "%s%s:%-30.29s%s" % (CO.CYAN, FG.formateaNumero(ci),
                                    COM.nombreSocio(COM.mNombre(ci)), CO.FIN)
      if 1 < len(l) and '' != l[1]:
        st += "\n"
        st += CO.AZUL + "Telefono habitacion: ".rjust(nJustDerecha) + CO.FIN +\
                                                FG.formateaNumeroTelefono(l[1])
      if 2 < len(l) and '' != l[2]:
        st += "\n"
        st += CO.AZUL + "Telefono trabajo: ".rjust(nJustDerecha) + CO.FIN +\
                                                FG.formateaNumeroTelefono(l[2])
      if 3 < len(l) and '' != l[3]:
        st += "\n"
        st += CO.AZUL + "Celular: ".rjust(nJustDerecha) + CO.FIN +\
                                                FG.formateaNumeroTelefono(l[3])
      if 4 < len(l) and '' != l[4]:
        st += "\n"
        st += CO.AZUL + "Celular: ".rjust(nJustDerecha) + CO.FIN +\
                                                FG.formateaNumeroTelefono(l[4])
      if 5 < len(l) and '' != l[5]:
        if len(l[5].rstrip(' \t\n\r')) > (CO.nCarLin - nJustDerecha - 1):	# Cars a justificar derecha + 1 espacio despues ':'.
          nJustDerecha = CO.nCarLin - len(l[5].rstrip(' \t\n\r')) - 1
        st += "\n"
        st += CO.AZUL + "Correo:".rjust(nJustDerecha) + CO.FIN + " %s" %\
                                                      l[5].rstrip(' \t\n\r')
      nF += 1
# Fin elif
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  opc = ES.imprime(st)
  return opc
# Funcion ubicacion

# Definir variables globales
def prepararListasDeTrabajo():
  global lCh, lHeute, lSi, lPre, lUb

  lHeute = ES.cargaLista("heute.txt")		# [0]Banco; [1]Numero; [2]Cedula;
  											# [3]Nombre; [4]Fecha(d/m/a); [5]descripcion; [6]monto; [7]estado
  lCh = ES.cargaLista("cheques.txt")		# [0]Banco; [1]Numero; [2]Cedula;
  											# [3]Nombre; [4]Fecha(d/m/a); [5]descripcion; [6]monto; [7]estado
  lSi = ES.cargaLista("disponibilidad.txt")	# [0]Cedula;
  											# [1]Codigo identificador proximo campo; [2] Campo(Fecha, Monto, etc)
  lPre = ES.cargaLista("prestamos.txt")	# [0]Cedula; [1]Concepto;
  											# [2]Monto solicitado; [3]Monto total(Concedido + intereses); [4]Saldo;
  											# [5]Saldo total(Saldo + intereses); [6]Cuota; [7]Fecha inicial (mm/aa);
  											# [8]ult actualizacion (mm); [9]cuotas (pagadas/total)
  lUb = ES.cargaLista("ubicacion.txt")	# [0]Cedula;
  											# [1]Telefono habitacion; [2]Telefono trabajo; [3]Celular 1; [4]Celular 2;
  											# [5]Correo electronico
# Funcion prepararListasDeTrabajo
fErr   = ES.abrirErr("ipaspudo.err")