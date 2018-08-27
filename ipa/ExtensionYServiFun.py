# libExtensionYServiFun: Modulo de extension y ServiFun para IPASPUDO.
#-*-coding:utf8;-*-
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

def extension():
  'Maneja la lista de la carga de un socio en la extension y muestra la informacion.'
  global lCgE
  from ipa.AhorroYPrestamo import cig as ci

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
          st += CO.CYAN + "SUMA ASEGURADA: " + l[4] + "UT = BsF. " + FG.formateaNumero(nSumaAseg) +\
          		CO.FIN + "\n" + sTitExtension
        nF += 1
        rC += float(l[5])
        if 0 < float(l[5]):
          if l[3].lstrip().split(' ')[0][0:3] in ['TIT', 'CON', 'tit', 'con']:
            sPar = l[3].lstrip().split(' ')[0][0:nCarPare-2] + '-' + l[3][-2:]
          else: sPar = l[3].lstrip().split(' ')[0][0:nCarPare]
          if 6 < len(l) and l[6].isdigit(): sAno = l[6]
          else: sAno = '----'
          st += sFormato % (sColor, FG.formateaNumero(l[1]), nCarNomb, nCarNomb, l[2].lstrip().split('|')[0], nCarPare,\
          					nCarPare, sPar, FG.formateaNumero(float(l[5])/12, iDec), sAno, CO.FIN)
      except Exception as ex:
        print('ex: ', ex)
# Fin elif
    else: break
# Fin for
  if 0 >= nF or 0.00 >= rC:
    st = COM.noCedula(ci)
#    ES.alerta(droid, 'EXTENSION', '%s: INACTIVO' % (sNombre))
  else:
    frC = FG.formateaNumero(rC, 2)
    fmC = FG.formateaNumero(rC/12, 2)
    stl = "TOTAL Anual: %-*.*s (mensual: %-*.*s)" % (len(str(frC)), len(str(frC))+1, frC, \
									len(fmC), len(str(fmC))+1, fmC)
    st += CO.CYAN + stl + CO.FIN
  ES.imprime(st)
# Funcion extension
def servifun():
  'Maneja la lista de la carga de un socio en ServiFun y muestra la informacion.'
  global lCgS
  from ipa.AhorroYPrestamo import cig as ci

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
      st += sFormato % (sColor, FG.formateaNumero(l[1], 0), nCarNomb, nCarNomb, l[2].lstrip().split('|')[0], nCarPare,\
      					nCarPare, l[3], l[4], nEd, CO.FIN)
    else: break
# Fin for
  if 0 >= nF: st = COM.noCedula(ci)
  else:
    if 1 == nF:
      fC += CO.CI
      sfC = FG.formateaNumero(fC, 2)
      sC = "igual a Bs. %*s" % (len(sfC), sfC)
    else:
      fC += CO.CCC
      sfC = FG.formateaNumero(fC, 2)
      sC = "mayor o igual a Bs. %*s" % (len(sfC), sfC)
    stl = "La cuota mensual es " + sC
    st += CO.CYAN + stl + CO.FIN
  ES.imprime(st.rstrip(' \t\n\r'))
# Funcion servifun
def servicioEspecifico(sCodigo, sNombre):
  'Muestra las indemnizaciones de ServiFun usando la lista con los parentesco.'
  global lPa
  from ipa.AhorroYPrestamo import utg
  #  sTitulo = "Servifun"
  sMensaje = ''
  for l in lPa:
    if sCodigo != l[0]: continue			# Codigo del parentesco
    sMensaje  = "%sServicios p/(%s) %s: %s%s\n" % (CO.CYAN, l[0], l[1], sNombre.lstrip().split('|')[0], CO.FIN)	# Codigo, descripcion del parentesco
    if 14 <= len(l): rLp = int(l[13]) * float(utg)			# Lapida
    else: rLp = 0
    sLp = FG.formateaNumero(rLp, 2)		# Lapida formateado
    if 13 <= len(l): rCr = int(l[12]) * float(utg)			# Cremacion
    else: rCr = 0
    sCr = FG.formateaNumero(rCr, 2)		# Cremacion formateado
    if 12 <= len(l): rFo = int(l[11]) * float(utg)			# Fosa
    else: rFo = 0
    sFo = FG.formateaNumero(rFo, 2)		# Fosa formateado
    if 11 <= len(l): rTr = int(l[10]) * float(utg)			# Traslado
    else: rTr = 0
    sTr = FG.formateaNumero(rTr, 2)		# Traslado formateado
    if 10 <= len(l): rSv = int(l[9]) * float(utg)			# Servicio
    else: rSv = 0
    sSv = FG.formateaNumero(rSv, 2)		# Servicio formateado
    if 9 <= len(l): rAy = int(l[8]) * float(utg)			# Ayuda
    else: rAy = 0
    sAy = FG.formateaNumero(rAy, 2)		# Ayuda formateado
    sMensaje += "%sAyuda:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sAy), len(sAy), sAy, l[8])
    sMensaje += "%sServicio:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sSv), len(sSv), sSv, l[9])
    sMensaje += "%sTraslado:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sTr), len(sTr), sTr, l[10])
    if 0 < rFo: sMensaje += "%sFosa (solo 1):%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sFo), len(sFo), sFo, l[11])
    if 0 < rCr: sMensaje += "%sCremacion:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sCr), len(sCr), sCr, l[12])
    if 0 < rLp: sMensaje += "%sLapida:%s BsF. %*.*s (%-3s UT)\n" % (CO.AZUL, CO.FIN, len(sLp), len(sLp), sLp, l[13])
  # Fin for
  ES.imprime(sMensaje.rstrip(' \t\n\r'))
# Funcion servicioEspecifico
def servicio():
  'Maneja la lista de la carga de un socio en ServiFun y muestra la cobertura a cualquiera de la carga.'
  global lCgS, lPa
  from ipa.AhorroYPrestamo import cig as ci

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
# Funcion servicio

# Definir variables globales
def prepararListasDeTrabajo():
  global lCgE, lCgS, lPa

  lCgE = ES.cargaLista("extension.txt")	# [0]Cedula; [1]Cedula carga;
  											# [2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco; [4]#UT; [5]Costo poliza
  lCgS = ES.cargaLista("servifun.txt")	# [0]Cedula; [1]Cedula carga;
  											# [2]Nombre(Nombre|Disponibilidad|A/N); [3]Parentesco;
  											# [4]Fecha ingreso a servifun
  lPa = ES.cargaLista("parentesco.txt")	# [0]Codigo; [1]Descripcion;
  											# [2]Identificar de cambio(Sexo/edad); [3]Poliza 500UT;
  											# [4]Poliza 500UT si cumple requisito de cambio, ver campo 2; [5]Poliza 1250UT;
  											# [6]Poliza 1250UT si cumple requisito de cambio, ver campo 2;
  											# Servifun: [7]Cuota extra; [8]Ayuda; [9]Servicio; [10]Traslado; [11]Fosa;
  											# [12]Cremacion
# Funcion prepararVariablesDeTrabajo