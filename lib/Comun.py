# libComun: Rutinas comunes para ipaspudo.
#-*-coding:utf8;-*-
import json
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

lClasCheques = [
          "Cheque", "Cedula", "Nombre", "Monto", "Estado", "Fecha", "Concepto"
               ]

lMenu = [['Calcular cuota', 'cuota'],					            # 0
		 ['Cedula del socio', 'cedula'], 
		 ['Buscar cedula del socio', 'nombre'], 
		 ['Cheques', 'cheque'], 
         ['Deposito por fecha', 'depositos'], 
         ['Ganancias y Perds X Mes', 'GyP.ganYperXmes'],  # 5
         ['Ganancias y Perds Acumu', 'GyP.ganYperAcum'],	# 6
         ['Resumen de Nomina normal', 'NOM.resNominaN'],	# 7
         ['Res Nomina homologacion', 'NOM.resNominaH'],		# 8
         ['Res Nomina completa', 'NOM.resNominaC'],			  # 9
         ['Res Nom comp con extras', 'NOM.resNominaCcE'],	# 10
		 ['Cheque por cedula', 'chequeXCedula'], 
         ['Ultimos deposito', 'heuteXCedula'], 
         ['Disponibilidad', 'disponibilidad'], 
 		 ['Prestamos', 'prestamos'],
 		 ['Detalle prestamo', 'prestamo'],
		 ['Extension', 'extension'], 
		 ['Servifun', 'servifun'], 
		 ['Servicio funerario', 'servicio'], 
		 ['Nomina', 'NOM.nomina'],
		 ['Detalle nomina', 'NOM.concepto'],
		 ['Nomina con extras', 'NOM.nominacne'],
		 ['Detalle nomina con extras', 'NOM.conceptocne'],
		 ['Ubicacion', 'ubicacion'], 
		 ['Salir', 'salir']
		]

def lFecha(k="Sinca", sig=""):
  global dFecha
  sFecha = sig + " " + dFecha.get(k, "No hay fecha.")
  if "ServiFun" == sig: return sFecha[0:-3]
  else: return sFecha
# funcion lFecha
def noCedula(ci):
  return "La cedula %s no fue encontrada\n" % ES.fgFormateaNumero(ci)
# funcion noCedula
def cedulaI(ciAnt):
  
  while True:
    ci = ES.entradaNumero(droid, "CEDULA DE IDENTIDAD",
                  "Cedula de identidad del socio", str(ciAnt), True, True, True)
    if 0 == ci: return -1
    if ci < 100000:
      print('Debe introducir un número entero de 6 o más dígitos')
    else: break
  return ci
# funcion cedulaI
def extraeNombre(sNombre):
  ''' Extrae el nombre de una cadena denominada nombre; pero, contiene:
  		Nombre, nucleo (primera letra), fecha de nacimiento (sin separador, 8 digitos), Disponibilidad (o No) y
  		Extension ('A' o 'N'). Separados pr '|' en 'persona.txt'. 
  		Nombre en extension.txt y servifun.txt, beneficiario y concepto en cheques.txt, solo contiene:
  		Nombre, Disponibilidad (o No) y Extension ('A' o 'N'). Separados pr '|'. '''
  try:
    sub = sNombre.rstrip(' \t\n\r')[0:sNombre.index('|', 0)] 
  except ValueError:
    sub = sNombre
  return sub.rstrip(' \t\n\r')
# funcion nombreSocio
def nombreSocio(sNombre):
  ''' Extrae el nombre de una cadena denominada nombre; pero, contiene:
  		Nombre, nucleo (primera letra), fecha de nacimiento (sin separador, 8 digitos), Disponibilidad (o No) y
  		Extension ('A' o 'N'). Separados pr '|' en 'persona.txt'. 
  		Nombre en extension.txt y servifun.txt, beneficiario y concepto en cheques.txt, solo contiene:
  		Nombre, Disponibilidad (o No) y Extension ('A' o 'N'). Separados pr '|'. '''
  l = sNombre.rstrip(' \t\n\r').split('|')
  return l[0].rstrip(' \t\n\r')
# funcion nombreSocio
def mNombre(ci):

  try:
    sNombre = dPer.get(str(ci), "NO")
  except UnicodeError:
    sNombre = "UnicodeError: " + ci
  if ("NO" == sNombre):
    sNombre = "NO ENCONTRE EL NOMBRE"
    ES.alerta(droid, 'SOCIO ERROR', ES.fgFormateaNumero(ci) + ', ' + sNombre)
  return sNombre
# funcion mNombre
def valSocio(ciAnt = -1):

  ci = cedulaI(ciAnt)
  try:
    if 0 >= ci: return -1, 'Zero o negativo'
  except:
    return -1, 'La cedula debe ser un número entero'
  
  return ci, mNombre(ci)    # Devuelve una tupla
# funcion valSocio
def mSocio(Nombre, ci, bCadena=True):
  global dPer

  if (bCadena): l = Nombre.rstrip().split('|')	# Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
  else: l = Nombre[1:]

  if (bCadena): sFecha = lFecha()
  else: sFecha = Nombre[len(Nombre)-1]
  st = CO.AMARI + sFecha + ' (Descargado:' + CO.FIN + lFecha('persona.txt', '') + ')' + "\n" + CO.AZUL + "Cedula:".rjust(21) + CO.FIN 
  if (bCadena): st += " %s" % (ES.fgFormateaNumero(ci))
  else: st += " %s" % Nombre[0]
  nJustDerecha = 21
  if 0 < len(l) and '' != l[0]:
    if len(l[0].rstrip(' \t\n\r')) > (CO.nCarLin - nJustDerecha - 1):	# Cars a justificar derecha + 1 espacio despues ':'.
      nJustDerecha = CO.nCarLin - len(l[0].rstrip(' \t\n\r')) - 1
    st += "\n"
    st += CO.AZUL + "Nombre:".rjust(nJustDerecha) + CO.FIN + " %s" % (l[0].rstrip(' \t\n\r'))
  nJustDerecha = 21
  if 1 < len(l) and '' != l[1]:
    st += "\n" + CO.AZUL + "Nucleo:".rjust(nJustDerecha) + CO.FIN
    if (bCadena): st += " %s" % (CO.dNucleo.get(l[1], 'ESTA ERRADO EN LA BD'))
    else: st += " %s" % (l[1])
  if 2 < len(l) and '' != l[2]:
    st += "\n" + CO.AZUL + "Fecha de nacimiento:".rjust(nJustDerecha) + CO.FIN
    if (bCadena): st += " %2s/%2s/%4s" % (l[2][0:2], l[2][2:4], l[2][4:])
    else: st+= " %s" % (l[2])
  if 3 < len(l) and '' != l[3]:
    st += "\n"
    st += CO.AZUL + "Disponibilidad:".rjust(nJustDerecha) + CO.FIN + " %s" % (l[3])
  if 4 < len(l) and '' != l[4]:
    st += "\n" + CO.AZUL + "Extension:".rjust(nJustDerecha) + CO.FIN
    if (bCadena): st += " %s" % (CO.dExtension.get(l[4], 'ERRADA'))
    else: st+= " %s" % (l[4])
  if not bCadena:
    st += "\n" + CO.AZUL + "Fe ingreso IPASPUDO:".rjust(nJustDerecha) + CO.FIN + " %s" % (l[5])
    st += "\n" + CO.AZUL + "Servicio funerario:".rjust(nJustDerecha) + CO.FIN + " %s" % (l[6])
  ES.imprime(st)
# funcion mSocio
def aSocio(lPer, cig):    # Esta funcion no se utiliza.
  global dPer

  try:
    sNombre = dPer.get(str(cig), "NO")
  except UnicodeError:
    print('ERROR: ' + str(cig) + '|' + json.dumps(lPer))
    return False
  if ("NO" == sNombre):
    fPer = ES.abrir('persona.txt', 'a')
  # Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
    if fPer:
      try:
        if (6 <= len(lPer)):
          fPer.write(str(cig) + ';' + lPer[1] + '|' + lPer[2][0:1] + '|' + lPer[3] + '|' + lPer[4] + '|' + lPer[5][0:1] + "\n")
      except:
        pass
      fPer.close()
  return True
# funcion aSocio
def mDividendo(ci):
  global dDiv
  try:
    sDiv = dDiv.get(str(ci), "0")
    if sDiv.isdigit(): rDividendo = float(int(sDiv)/100)
    else: rDividendo = -1.00
  except UnicodeError:
    rDividendo = -2.00
  return rDividendo
# funcion mDividendo
def mBanco(cbn):
  global dBanco
  return dBanco.get(cbn, cbn)
# funcion mBanco
def mConcepto(ccp):
  global dConcepto
  return dConcepto.get(ccp, "NO DESCRIPCION")
# funcion mConcepto
def mEstado(sI= '0'):
  lEstado = CO.lEstado   # Estado del cheque
  i = int(sI)
  if (0 > i) or (3 < i): return sI
  else: return lEstado[i]
# funcion mEstado
def creaOp(l):
  return ("%-.6s %-.1s %-.25s %-.8s %-.10s" % (l[1], mEstado(l[7])[0:1], extraeNombre(l[3])[0:25], l[4][0:6]+l[4][8:10], l[6]))
# funcion creaOp

dBanco = ES.cargaDicc("bancos.txt")		# [0]Codigo; [1]Descripcion
dConcepto = ES.cargaDicc("conceptos.txt")	# [0]Codigo; [1]Descripcion
dFecha = ES.cargaDicc("control.txt")	# [0]Identificacion del proceso; [1]Fecha
dPer = ES.cargaDicc("persona.txt")		# [0]Cedula;
  # [1]Nombre(Nombre|Nucleo|Fecha de nacimiento o P:personal|disponibilidad o No|A/N:extension)
dDiv = ES.cargaDicc("dividendos.txt")		# [0]Cedula; [1]Monto