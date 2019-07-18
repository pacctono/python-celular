# libComun: Rutinas comunes para ipaspudo.
#-*- coding:ISO-8859-1 -*-
import types
import json
from lib import ES, Const as CO, General as FG

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

'''lClasCheques = [
          "Cheque", "Cedula", "Nombre", "Monto", "Estado", "Fecha", "Concepto"
               ]
'''
lMenu = [
          ['Calcular comision', 'comision'],              # 0
          ['Asesor', 'asesor'], 
          ['Codigo de casa nacional', 'codigo'], 
          ['Reporte en casa nacional', 'reporte'], 
          ['Montos totales', 'MT.chequeXCedula'],         # 4
          ['Salir', 'salir']
		    ]

def lFecha(k="Sinca", sig=""):
  global dFecha
  sFecha = sig + " " + dFecha.get(k, "No hay fecha.")
  if "ServiFun" == sig: return sFecha[0:-3]
  else: return sFecha
# Funcion lFecha
def noCedula(ci):
  return "La cedula %s no fue encontrada\n" % FG.formateaNumero(ci)
# Funcion noCedula
def cedulaI(ciAnt):
  
  while True:
    ci = ES.entradaNumero(droid, "CEDULA DE IDENTIDAD",
                "Cedula de identidad del socio", str(ciAnt), True, True, True)
    if 0 == ci: return -1
    if ci < 100000:
      print('Debe introducir un número entero de 6 o más dígitos')
    else: break
  return ci
# Funcion cedulaI
def extraeNombre(sNombre):
  ''' Extrae el nombre de una cadena denominada nombre; pero, contiene:
  		Nombre, nucleo (primera letra), fecha de nacimiento (sin separador,
      8 digitos), Disponibilidad (o No) y Extension ('A' o 'N'). Separados
      por '|' en 'persona.txt'. Nombre en extension.txt y servifun.txt,
      beneficiario y concepto en cheques.txt, solo contiene: Nombre,
      Disponibilidad (o No) y Extension ('A' o 'N'). Separados pr '|'. '''
  try:
    sub = sNombre.rstrip(' \t\n\r')[0:sNombre.index('|', 0)] 
  except ValueError:
    sub = sNombre
  return sub.rstrip(' \t\n\r')
# Funcion nombreSocio
def nombreSocio(sNombre):
  ''' Extrae el nombre de una cadena denominada nombre; pero, contiene:
  		Nombre, nucleo (primera letra), fecha de nacimiento (sin separador,
      8 digitos), Disponibilidad (o No) y Extension ('A' o 'N'). Separados
      por '|' en 'persona.txt'. Nombre en extension.txt y servifun.txt,
      beneficiario y concepto en cheques.txt, solo contiene: Nombre,
      Disponibilidad (o No) y Extension ('A' o 'N'). Separados pr '|'. '''
  l = sNombre.rstrip(' \t\n\r').split('|')
  return l[0].rstrip(' \t\n\r')
# Funcion nombreSocio
def mNombre(ci):

  try:
    sNombre = dPer.get(str(ci), "NO")
  except UnicodeError:
    sNombre = "UnicodeError: " + ci
  if ("NO" == sNombre):
    sNombre = "NO ENCONTRE EL NOMBRE"
    ES.alerta(droid, 'SOCIO ERROR', FG.formateaNumero(ci) + ', ' + sNombre)
  return sNombre
# Funcion mNombre
def valSocio(ciAnt = -1):

  ci = cedulaI(ciAnt)
  try:
    if 0 >= ci: return -1, 'Zero o negativo'
  except:
    return -1, 'La cedula debe ser un número entero'
  
  return ci, mNombre(ci)    # Devuelve una tupla
# Funcion valSocio
def mSocio(Nombre, ci, bCadena=True):
  global dPer

  if (bCadena): l = Nombre.rstrip().split('|')	# Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
  else: l = Nombre[1:]

  if (bCadena): sFecha = lFecha()
  else: sFecha = Nombre[len(Nombre)-1]
  st = CO.AMARI + sFecha + ' (Descargado:' + CO.FIN +\
        lFecha('persona.txt', '') + ')' + "\n" + CO.AZUL +\
        "Cedula:".rjust(21) + CO.FIN 
  if (bCadena): st += " %s" % (FG.formateaNumero(ci))
  else: st += " %s" % Nombre[0]
  nJustDerecha = 21
  if 0 < len(l) and '' != l[0]:
    if len(l[0].rstrip(' \t\n\r')) > (CO.nCarLin - nJustDerecha - 1):	# Cars a justificar derecha + 1 espacio despues ':'.
      nJustDerecha = CO.nCarLin - len(l[0].rstrip(' \t\n\r')) - 1
    st += "\n"
    st += CO.AZUL + "Nombre:".rjust(nJustDerecha) + CO.FIN + " %s" %\
                                                      (l[0].rstrip(' \t\n\r'))
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
    st += CO.AZUL + "Disponibilidad:".rjust(nJustDerecha) + CO.FIN + " %s" %\
                                                                        (l[3])
  if 4 < len(l) and '' != l[4]:
    st += "\n" + CO.AZUL + "Extension:".rjust(nJustDerecha) + CO.FIN
    if (bCadena): st += " %s" % (CO.dExtension.get(l[4], 'ERRADA'))
    else: st+= " %s" % (l[4])
  if not bCadena:
    st += "\n" + CO.AZUL + "Fe ingreso IPASPUDO:".rjust(nJustDerecha) +\
                                                      CO.FIN + " %s" % (l[5])
    st += "\n" + CO.AZUL + "Servicio funerario:".rjust(nJustDerecha) +\
                                                      CO.FIN + " %s" % (l[6])
  opc = ES.imprime(st)
  return opc
# Funcion mSocio
def aSocio(lPer, ci):    # Esta funcion no se utiliza.
  global dPer

  try:
    sNombre = dPer.get(str(ci), "NO")
  except UnicodeError:
    print('ERROR: ' + str(ci) + '|' + json.dumps(lPer))
    return False
  if ("NO" == sNombre):
    fPer = ES.abrir('persona.txt', 'a')
  # Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
    if fPer:
      try:
        if (6 <= len(lPer)):
          fPer.write(str(ci) + ';' + lPer[1] + '|' + lPer[2][0:1] + '|' +\
                        lPer[3] + '|' + lPer[4] + '|' + lPer[5][0:1] + "\n")
      except:
        pass
      fPer.close()
  return True
# Funcion aSocio
def mDividendo(ci):
  global dDiv
  try:
    sDiv = dDiv.get(str(ci), "0")
    if sDiv.isdigit(): rDividendo = float(int(sDiv)/100)
    else: rDividendo = -1.00
  except UnicodeError:
    rDividendo = -2.00
  return rDividendo
# Funcion mDividendo
def mBanco(cbn):
  global dBanco
  return dBanco.get(cbn, cbn)
# Funcion mBanco
def mConcepto(ccp):
  global dConcepto
  return dConcepto.get(ccp, "NO DESCRIPCION")
# Funcion mConcepto
def mEstado(sI= '0'):
  lEstado = CO.lEstado   # Estado del cheque
  i = int(sI)
  if (0 > i) or (3 < i): return sI
  else: return lEstado[i]
# Funcion mEstado
def creaOp(l):
  return ("%-.6s %-.1s %-.25s %-.8s %-.10s" % (l[1], mEstado(l[7])[0:1],
                      extraeNombre(l[3])[0:25], l[4][0:6]+l[4][8:10], l[6]))
# Funcion creaOp
def buscarNombre():
  global dPer

  nombre = ES.entradaNombre(droid, 'Nombre del socio')
  if None == nombre:
    return -10, None
  nombres = []
  cedulas = []
  try:
    for k,v in dPer.items():
      if 0 <= v.lower().find(nombre.lower()):
        nombres.append(v)
        cedulas.append(k)
  except UnicodeError: pass
  if not nombres:
    ES.alerta(droid, nombre, "No hubo coincidencias!")
    return -10, None
  indice = ES.entradaConLista(droid, 'SOCIOS ENCONTRADOS',
                                              'Seleccione socio(a)', nombres)
  if None == indice or 0 > indice: return -10, None
  return int(cedulas[indice]), nombres[indice]
# Funcion buscarNombre

# Definir variables globales
def prepararDiccionariosDeTrabajo():
  global dPro, dPer

  dBanco = ES.cargaDicc("bancos.txt")		# [0]Codigo; [1]Descripcion
  dConcepto = ES.cargaDicc("conceptos.txt")	# [0]Codigo; [1]Descripcion
  dFecha = ES.cargaDicc("control.txt")	# [0]Identificacion del proceso; [1]Fecha
  dPer = ES.cargaDicc("persona.txt")		# [0]Cedula;
  # [1]Nombre(Nombre|Nucleo|Fecha de nacimiento o P:personal|disponibilidad o No|A/N:extension)
  dDiv = ES.cargaDicc("dividendos.txt")		# [0]Cedula; [1]Monto
# Funcion prepararDiccionariosDeTrabajo
