import sys
from parser import parser
import funciones #funciones seria un archivo a parte con las funciones

if (sys.argv[1] not in ['fifo', 'lru'] or len(sys.argv) < 2):
    print ('Para la ejecucion se necesita un argumento, ademas de que este sea valido (fifo o lru)). Cerrando programa')
    exit()
print ('Estrategia a usar: ', sys.argv[1])
instruccionesParser = parser()
# estrategia es una variable booleana que almacena estrategia. false es lru y true es fifo
if sys.argv[1]=='fifo':
    #funciones seria un archivo a parte con las funciones
    funciones.estrategia = True
for instruccion in instruccionesParser:
   #print("\n", ' '.join(str(s) for s in instruccion), sep="")
    if instruccion[0] == 'P':
        funciones.P(instruccion[1], instruccion[2])
    elif instruccion[0] == 'A':
        funciones.A(instruccion[1], instruccion[2], instruccion[3])
    elif instruccion[0] == 'L':
        funciones.L(instruccion[1])
    elif instruccion[0] == 'F':
        funciones.F()
    elif instruccion[0] == 'E':
        funciones.E()
    elif instruccion[0] != 'C':
        print("Instrucción no valida. Fin del programa")
        exit()

