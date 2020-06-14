import sys
import funciones #funciones seria un archivo a parte con las funciones
import re
import fnmatch

# sys.argv[] has the arguments from a python command line 
pattern = re.compile(r'(.)*(.txt)')
#regex para buscar los commandos
parser = re.compile(r'P \d+ \d+|A \d+ \d+ \d|L \d+|C \w+|F[^A-Za-z]|E$')
if (len(sys.argv) != 2):
    print("argumentos incorrectos")
else:
    #revisa si el archivo no es txt
    if(pattern.search(sys.argv[1]) == None):
        print('el texto no es un .txt')
    else:
        #abre el archivo txt
        file_Object = open(sys.argv[1],'r')
        # lo guarda en un objeto file
         #leemos el objeto file como string
        data = file_Object.read()
       # el regex nos regresa una lista con  los comandos por ejectuar ignorando lo
       #demas, tambien estan en orden, al revisar el f el regex te lo regresa f/n 
       # no se porque xd
        lista = parser.findall(data)
        #hace print de los comandos
        print(lista)

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

