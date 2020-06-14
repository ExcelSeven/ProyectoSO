import sys
from parser import parser

if (sys.argv[1] not in ['fifo', 'lru'] or len(sys.argv) < 2):
    print ('Para la ejecucion se necesita un argumento, ademas de que este sea valido (fifo o lru)). Cerrando programa')
    exit()
print ('Estrategia a usar: ', sys.argv[1])
instruccionesParser = parser()
# estrategia es una variable booleana que almacena estrategia. false es lru y true es fifo
if sys.argv[1]=='fifo':
    instrucciones.estrategia = True
for instruccion in instruccionesParser:
    if instruccion[0] == 'P':
        instrucciones.P(instruccion[1], instruccion[2])
    elif instruccion[0] == 'A':
        instrucciones.A(instruccion[1], instruccion[2], instruccion[3])
    elif instruccion[0] == 'L':
        instrucciones.L(instruccion[1])
    elif instruccion[0] == 'F':
        instrucciones.F()
    elif instruccion[0] == 'E':
        instrucciones.E()
    elif instruccion[0] != 'C':
        print("Instrucción no valida. Fin del programa")
        exit()