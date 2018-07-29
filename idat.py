#!/usr/bin/python
import sys
f = open(sys.argv[1], 'r')
lista = [(linea.rstrip()[9:12], float(linea.rstrip()[12:20])/100, float(linea.rstrip()[20:])/100) for linea in f]
dicc = {}
dicc['998'] = (0, 0.00, 0.00, 0.00)
dicc['999'] = (0, 0.00, 0.00, 0.00)
for l in lista:
  if not dicc.has_key(l[0]): dicc[l[0]] = (0, 0.00, 0.00, 0.00)
  dicc[l[0]] = (dicc[l[0]][0]+1, dicc[l[0]][1]+l[1], dicc[l[0]][2]+l[2], dicc[l[0]][3]+l[1]+l[2])
  dicc['999'] = (dicc['999'][0]+1, dicc['999'][1]+l[1], dicc['999'][2]+l[2], dicc['999'][3]+l[1]+l[2])
  if l[0] not in ('511','561', '562', '563', '570'):
    dicc['998'] = (dicc['998'][0]+1, dicc['998'][1]+l[1], dicc['998'][2]+l[2], dicc['998'][3]+l[1]+l[2])
#
lconc = []
i = 0
for ld in dicc.items():
  lconc.insert(i, ld[0])
  i += 1
lconc.sort()
for v in lconc:
  print "%4s %5d %11.2f %11.2f %11.2f" % (v, dicc[v][0], dicc[v][1], dicc[v][2], dicc[v][3])
#
f.close()
