# libComun: Rutinas comunes para ipaspudo.
#-*- coding:ISO-8859-1 -*-
import types
import json
from lib import ES, Const as CO, General as FG
from c21 import propiedades as PRO

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
          "Cheque", "Codigo", "Nombre", "Monto", "Estado", "Fecha", "Concepto"
               ]
'''
lMenu = [
          ['Calcular cuota', 'cuota'],                  # 0
          ['Calcular comision', 'comisiones'],          # 1
          ['Asesor', 'asesor'], 
          ['Codigo de casa nacional', 'codigo'], 
          ['Reporte en casa nacional', 'reporte'], 
          ['Montos totales', 'MT.chequeXCodigo'],       # 5
          ['Salir', 'salir']
		    ]

def lFecha(k="Sinca", sig=""):
  global dFecha
  sFecha = sig + " " + dFecha.get(k, "No hay fecha.")
  if "ServiFun" == sig: return sFecha[0:-3]
  else: return sFecha
# Funcion lFecha
def noCodigo(co):
  return "El codigo %s no fue encontrado\n" % FG.formateaNumero(co)
# Funcion noCodigo
def codigoI(coAnt):
  
  while True:
    co = ES.entradaNumero(droid, "CODIGO DE CASA NACIONAL",
                "Codigo de la propiedad", str(coAnt), True, True, True)
    if 0 == co: return -1
    if co < 100000:
      print('Debe introducir un número entero de 6 o más dígitos')
    else: break
  return co
# Funcion codigoI
def extraeNombre(fila):
  ''' Extrae el nombre de una propiedad.
      '''
  return fila[5].strip(' "\t\n\r')
# Funcion extraeNombre
def nombreProp(fila):
  ''' Retorna el nombre de una propiedad.
      fila[0]: numero incremental.
      fila[1]: Codigo casa nacional.
      fila[2]: fecha de reserva.
      fila[3]: fecha de firma.
      fila[4]: Negociacion: Venta o Alquiler.
      fila[5]: Nombre de la propiedad.
  '''
  return fila[5].strip(' "\t\n\r')
# Funcion nombreProp
def mNombre(co):

  sNombre = 'NO'
  for l in PRO.lPro:
    if (co != l[1]): continue
    sNombre = l[5]
    break
  if ("NO" == sNombre):
    sNombre = "NO ENCONTRE EL NOMBRE"
    ES.alerta(droid, 'PROP ERROR', FG.formateaNumero(co) + ', ' + sNombre)
  return sNombre
# Funcion mNombre
def valProp(coAnt = -1):

  co = codigoI(coAnt)
  try:
    if 0 >= co: return -1, 'Zero o negativo'
  except:
    return -1, 'El codigo debe ser un número entero de 66 digitos.'
  
  return co, mNombre(co)    # Devuelve una tupla
# Funcion valSocio
def mSocio(Nombre, co, bCadena=True):
  global dPer

  if (bCadena): l = Nombre.rstrip().split('|')	# Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
  else: l = Nombre[1:]

  if (bCadena): sFecha = lFecha()
  else: sFecha = Nombre[len(Nombre)-1]
  st = CO.AMARI + sFecha + ' (Descargado:' + CO.FIN +\
        lFecha('persona.txt', '') + ')' + "\n" + CO.AZUL +\
        "Codigo:".rjust(21) + CO.FIN 
  if (bCadena): st += " %s" % (FG.formateaNumero(co))
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
def aSocio(lPer, co):    # Esta funcion no se utiliza.
  global dPer

  try:
    sNombre = dPer.get(str(co), "NO")
  except UnicodeError:
    print('ERROR: ' + str(co) + '|' + json.dumps(lPer))
    return False
  if ("NO" == sNombre):
    fPer = ES.abrir('persona.txt', 'a')
  # Nombre, nucleo, fecha de nacimiento, Disponibilidad y Extension
    if fPer:
      try:
        if (6 <= len(lPer)):
          fPer.write(str(co) + ';' + lPer[1] + '|' + lPer[2][0:1] + '|' +\
                        lPer[3] + '|' + lPer[4] + '|' + lPer[5][0:1] + "\n")
      except:
        pass
      fPer.close()
  return True
# Funcion aSocio
def mDividendo(co):
  global dDiv
  try:
    sDiv = dDiv.get(str(co), "0")
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
  codigos = []
  try:
    for k,v in dPer.items():
      if 0 <= v.lower().find(nombre.lower()):
        nombres.append(v)
        codigos.append(k)
  except UnicodeError: pass
  if not nombres:
    ES.alerta(droid, nombre, "No hubo coincidencias!")
    return -10, None
  indice = ES.entradaConLista(droid, 'SOCIOS ENCONTRADOS',
                                              'Seleccione socio(a)', nombres)
  if None == indice or 0 > indice: return -10, None
  return int(codigos[indice]), nombres[indice]
# Funcion buscarNombre

# Definir variables globales
def prepararListasDeTrabajo():
  global lAse

  fC21 = ES.abrir("asesores.txt")
  if not fC21:
    lAse = []           # Lista de asesores.
  else:
    try:
      sAse = fC21.read()
      lAse = json.loads(sAse)
    except: pass
    finally: fC21.close()
# Funcion prepararListasDeTrabajo

# Definir variables globales
def prepararDiccionariosDeTrabajo():
  global dPro, dPer

  dBanco = ES.cargaDicc("bancos.txt")		# [0]Codigo; [1]Descripcion
  dConcepto = ES.cargaDicc("conceptos.txt")	# [0]Codigo; [1]Descripcion
  dFecha = ES.cargaDicc("control.txt")	# [0]Identificacion del proceso; [1]Fecha
  dPer = ES.cargaDicc("persona.txt")		# [0]Codigo;
  # [1]Nombre(Nombre|Nucleo|Fecha de nacimiento o P:personal|disponibilidad o No|A/N:extension)
  dDiv = ES.cargaDicc("dividendos.txt")		# [0]Codigo; [1]Monto
# Funcion prepararDiccionariosDeTrabajo
