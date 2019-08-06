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
          "Cheque", "Codigo", "Nombre", "Monto", "Estado", "Fecha", "Concepto"
               ]
'''
lMenu = [
          ['Calcular cuota', 'cuota'],                  # 0
          ['Calcular comision', 'comisiones'],          # 1
          ['Asesor', 'ASE.asesor'], 
          ['Todas las propiedades', 'PRO.propiedades'], 
          ['Propiedades X Asesor', 'PRO.xAsesor'],
          ['Codigo de casa nacional', 'PRO.xCodigo'], 
          ['Reporte en casa nacional', 'PRO.xReporte'], 
          ['Montos totales', 'PRO.totales'],            # 6
          ['Salir', 'salir']
		    ]

dMsj  = {
          "cedula":"Cedula de identidad",
          "name":"Nombre",
          "telefono":"Telefono",
          "email":"Correo electronico",
          "email_c21":"Correo electronico Century 21",
          "licencia_mls":"Licencia MLS",
          "fecha_ingreso":"Fecha de ingreso",
          "fecha_nacimiento":"Fecha de nacimiento",
          "sexo":"Sexo",
          "estado_civil":"Estado civil",
          "profesion":"Profesion",
          "direccion":"Direccion",
          "tCap":"Total captado",
          "tCer":"Total cerrado",
          "tCaptCer":"Total captado y cerrado",
          "0":"Numero incremental",
          "1":"Codigo casa nacional",
          "2":"fecha de reserva",
          "3":"fecha de firma",
          "4":"Negociacion:",
          "5":"Nombre de la propiedad",
          "6":"Status",
          "7":"Moneda",
          "8":"Precio",
          "9":"Comision",
          "10":"Monto de la reserva sin IVA",
          "11":"IVA",
          "12":"Monto de la reserva con IVA",
          "13":"Monto compartido con otra oficina con IVA",
          "14":"Monto compartido con otra oficina sin IVA",
          "15":"Lados",
          "16":"Franquicia de reserva sin IVA",
          "17":"Franquicia de reserva con IVA",
          "18":"Porcentaje Franquicia",
          "19":"Franquicia a pagar reportada",
          "20":"Porcentaje reportado a casa nacional",
          "21":"Porcentaje Regalia",
          "22":"Regalia",
          "23":"Sanaf - 5%",
          "24":"Bruto real de la oficina",
          "25":"Base para honorario de los socios",
          "26":"Base para honorario",
          "27":"Id del asesor captador",
          "28":"Nombre del asesor captador",
          "29":"Porcentaje Comision del captador",
          "30":"Comision del captador PrBr",
          "31":"Porcentaje Comision del gerente",
          "32":"Comision del gerente",
          "33":"Id del asesor cerrador",
          "34":"Nombre del asesor cerrador",
          "35":"Porcentaje Comision del cerrador PrBr",
          "36":"Comision del cerrador",
          "37":"Porcentaje Bonificacion",
          "38":"Bonificacion",
          "39":"Comision bancaria",
          "40":"Ingreso neto de la oficina",
          "41":"Numero de recibo",
          "42":"Forma de pago al gerente",
          "43":"Factura gerente",
          "44":"Forma de pago a los asesores",
          "45":"Factura asesores",
          "46":"Pago otra oficina",
          "47":"Pagado a Casa Nacional",
          "48":"Status C21",
          "49":"Reporte Casa Nacional",
          "50":"Factura A&S",
          "51":"Comentarios"
        }

def prepLnCad(desc, cad, ln=''):
  try:    
    if ('' != cad): return ("%s" + desc + ":%s %" + ln + "s\n")\
                        % (CO.AZUL, CO.FIN, cad)
    else: return ''
  except: return ''
# Funcion prepLnCad
def prepLnNum(desc, num, dec=0, ln=''):
  try:    
    if (0 != num): return ("%s" + desc + ":%s %" + ln + "s\n")\
                        % (CO.AZUL, CO.FIN, FG.formateaNumero(num, dec))
    else: return ''
  except: return ''
# Funcion prepLnNum
def prepLnFec(desc, fec, ln=''):
  try:    
    if ('' != fec): return ("%s" + desc + ":%s %" + ln + "s\n")\
                        % (CO.AZUL, CO.FIN, FG.formateaFecha(fec))
    else: return ''
  except: return ''
# Funcion prepLnFec
def prepLnTel(desc, tel, ln=''):
  try:    
    if ('' != tel): return ("%s" + desc + ":%s %" + ln + "s\n")\
                % (CO.AZUL, CO.FIN, FG.formateaNumeroTelefono(tel))
    else: return ''
  except: return ''
# Funcion prepLnTel
def prepLnMon(desc, num, dec=0, mon='$', ln=''):
  try:    
    if (0 != num): return ("%s" + desc + ":%s %" + ln + "s\n")\
                        % (CO.AZUL, CO.FIN, FG.numeroMon(num, dec, mon))
    else: return ''
  except: return ''
# Funcion prepLnMon
def prepLnPorc(desc, num, dec=0, ln=''):
  try:    
    if (0 != num): return ("%s" + desc + ":%s %" + ln + "s\n")\
                        % (CO.AZUL, CO.FIN, FG.numeroPorc(num, dec))
    else: return ''
  except: return ''
# Funcion prepLnPorc
def prepLnMsj(dic, campo, tipo=0, lng='', dec=0):
  '''
    Prepara la linea a imprimir:
    dic: Diccionario desde donde se tomara el valor a imprimir.    
    campo: llave en el diccionario del campo a imprimir. Tambien, para dMsj.
    tipo: tipo de campo. 0:cadena, 1:numero, 2:fecha, 3:telefono, 4:moneda, 5:porcentaje
    lng: longitud de caracteres, minimo, a mostrar del campo.
    dec: numero de decimales, si el campo a imprimir es numerico.
  '''
  if not dic[campo]: return ''    
  if (0 == tipo): sMsj = prepLnCad(dMsj[campo], dic[campo], lng)
  elif (1 == tipo): sMsj = prepLnNum(dMsj[campo], dic[campo], dec, lng)
  elif (2 == tipo): sMsj = prepLnFec(dMsj[campo], dic[campo][0:10], lng)
  elif (3 == tipo): sMsj = prepLnTel(dMsj[campo], dic[campo], lng)
  elif (4 == tipo): sMsj = prepLnMon(dMsj[campo], dic[campo], lng)
  elif (5 == tipo): sMsj = prepLnPorc(dMsj[campo], dic[campo], lng)
  else: sMsj = ''
  return sMsj
# Funcion prepLnMsj
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
def mNombre(co, lPro):

  sNombre = 'NO'
  for l in lPro:
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
def prepararDiccionarios(dir=''):
  global dNeg, dMon, dEst, dSC21

  dNeg = ES.cargaJson(dir+'negociacion.txt')
  if not dNeg: dNeg = {}
  dMon = ES.cargaJson(dir+'moneda.txt')
  if not dMon: dMon = {}
  dEst = ES.cargaJson(dir+'estatus.txt')
  if not dEst: dEst = {}
  dSC21 = ES.cargaJson(dir+'estatus_sistema_c21.txt')
  if not dSC21: dSC21 = {}
# Funcion prepararDiccionarios

#Variables globales
iCodCN = 1                # Indice del codigo a Casa Nacional.
iFeRes = 2                # Indice de la fecha de reserva.
iFeFir = 3                # Indice de la fecha firma.
iNegoc = 4                # Indice de la negociacion.
iNombr = 5                # Indice del nombre de la propiedad.
iStatu = 6                # Indice del estatus.
iMoned = 7                # Indice de la moneda.
iPreci = 8                # Indice del precio.
iComis = 9                # Indice de la comision de la negociacion.
iIVA   = 11               # Indice del IVA usado en la negociacion.
iLados = 15               # Indice de lados.
iPoFra = 18               # Indice del porcentaje de franquicia.
iPoRCN = 20               # Indice del porcentaje de Reporte a Casa Nacional.
iPoReg = 21               # Indice del porcentaje de Regalia.
iRegal = 22               # Indice de la regalia.
iIdCap = 27               # Indice del userId del asesor captador.
iNbCap = 28               # Indice del nombre del asesor captador. Inicialmente, cuando es de otra oficina.
iPoCap = 29               # Indice del porcentaje del asesor captador.
iCoCap = 30               # Indice de la comision del asesor captador.
iPoGer = 31               # Indice del porcentaje del asesor gerente.
iCoGer = 32               # Indice de la comision del gerente.
iIdCer = 33               # Indice del userId del asesor cerrador.
iNbCer = 34               # Indice del nombre del asesor cerrador. Inicialmente, cuando es de otra oficina.
iPoCer = 35               # Indice del porcentaje del asesor cerrador.
iCoCer = 36               # Indice de la comision del asesor cerrador.
iNetos = 40               # Indice del neto.
iStC21 = 48               # Indice del estatus del sistema Century 21.
iRepCN = 49               # Indice del reporte a Casa Nacional.