#!/usr/bin/python
import sys
import io

class color:
	PURPLE   = '\033[95m'
	HEADER   = '\033[95m'
	CYAN     = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE     = '\033[94m'
	OKBLUE   = '\033[94m'
	GREEN    = '\033[92m'
	OKGREEN  = '\033[92m'
	YELLOW   = '\033[93m'
	WARNING  = '\033[93m'
	RED      = '\033[91m'
	BOLD     = '\033[1m'
	UNDERLINE = '\033[4m'
	END      = '\033[0m'
	FAIL     = '\033[91m'
AMARI = color.YELLOW	# Primer titulo.
CYAN  = color.CYAN	# Identificacion del socio.
AZUL  = color.BLUE	# Identificacion de los datos.
PURPURA = color.PURPLE	# Linea final (total de prestamos).
VERDE = color.GREEN	# Linea final (totales).
ROJO  = color.RED	# Error
FIN   = color.END

f = io.open(sys.argv[1], mode='r', encoding='latin-1')
lista = [(linea.rstrip()[0:10], linea.rstrip()[11:83], linea.rstrip()[42:44], linea.rstrip()[45:65], linea.rstrip()[83:85], linea.rstrip()[86:106]) for linea in f]
dicc = {}
lConc = []
i = 0
for l in lista:
  if not dicc.has_key(l[0]):
    dicc[l[0]] = (l[0], l[1], l[2], l[3], l[4], l[5])
    lConc.insert(i, l[0])
    i += 1
#
lConc.sort()
iL = 0		# Numero de linea leida.
#print(lConc)
nC = 0		# Numero de linea corta.
nL = 0		# Numero de linea larga.
for v in lConc:
  if '' == v or '' == v.strip() or None == v or not v: continue
  iL += 1
  try:
    if dicc[v][2].isdigit() and dicc[v][3].isdigit():	# Linea corta
      if 0 == (iL%100): print("%8d %30.30s Nuc==>> %s Cta==>> %s" % (int(dicc[v][0]), dicc[v][1], dicc[v][2], dicc[v][3]))
      nC += 1
    elif dicc[v][4].isdigit() and dicc[v][5].isdigit():	# Linea larga
      if 0 == (iL%100): print("%8d %30.30s Nuc==>> %s Cta==>> %s" % (int(dicc[v][0]), dicc[v][1], dicc[v][4], dicc[v][5]))
      nL += 1
    else:
      print("%sERROR: (%d{%d/%d})%s;%d:%25.25s; Nucleo: {%s|%s}; Cuenta: {%s|%s}" % (ROJO, iL, nC, nL, FIN, len(dicc[v][0]), dicc[v][1], dicc[v][2], dicc[v][4], dicc[v][3], dicc[v][5]))
      break
  except:
    print(ROJO + 'PROBABLEMENTE HAY UN ERROR (' + str(iL) + '{' + str(nC) + '/' + str(nL) + '}' + ': ' + v + '|' + dicc[v][1] + '|' + dicc[v][2] + '|' + dicc[v][3] + '|' + dicc[v][4] + '|' + dicc[v][5] + '|' + ') CON EL ARCHIVO: ' + sys.argv[1] + FIN)
    break
#
if 0 < nC: print("%8d %30.30s Nuc==>> %s Cta==>> %s" % (int(dicc[v][0]), dicc[v][1], dicc[v][2], dicc[v][3]))
else: print("%8d %30.30s Nuc==>> %s Cta==>> %s" % (int(dicc[v][0]), dicc[v][1], dicc[v][4], dicc[v][5]))
print("%s%d lineas; %d lineas cortas y %d lineas largas%s" % (VERDE, iL, nC, nL, FIN))
f.close()
