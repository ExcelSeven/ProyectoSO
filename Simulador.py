import sys
import re
import fnmatch

#local libraries
from ProcessData import Process

# revisa si existe un espacio disponible
# si no existe regresa -1
# si existe regra sa dirrecion inicial
def chechForSpace(Memoria,Tamaño):
    Contador = 0
    Dir = -1
    state = True # valor para saber si es la primera direccion
    i = 0
    length = len(Memoria)
    for i in range(length):
        if Memoria[i] == -1:
            if Contador != Tamaño:
                Contador = Contador + 1
            if state :
                Dir = i
                state = False
        else:
            if Contador < Tamaño:
                Contador = 0
                state = True
#revisamos si no se paso del tamaño o si hay espacio suficiente
    if not(state) and Contador != Tamaño:
        return -1
    else:
        return Dir

#modifica la memoria para agregar un proceso con un tamaño desde una direccion inicial
def ModMemoria(Memoria,Dir,Tamaño,process):
    i = Dir
    for i in range(Tamaño):
        Memoria[i] = process
    return

    
# fucniones auxiliares
def checkFirstValList(X):
    return X[0]
def printComment(X):
    return X[2:]
        

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
        length = len(lista)
        Memoria = [-1] * 2048
        Swapping = [-1] * 4096
        ProcessList = []
        dict = {}
        #iniciamos simulador
        for i in range(length):
            state = checkFirstValList(lista[i])
            if state == 'C':
                print(printComment(lista[i]))
            elif state == 'F':
                print('F')
            elif state == 'P':
                corte = lista[i].split()
                Pnum = int(corte[2]) #numero de proceso
                bytesP = int(corte[1]) #tamaño
                Dir = chechForSpace(Memoria,bytesP) #dirrecion fisica inicial
                if Dir != -1:
                    P = Process(Pnum,bytesP,Dir)
                    ProcessList.append(P) # direccion de memoria libre
                    ModMemoria(Memoria,Dir,bytesP,Pnum)
                    print(Dir)
                else:
                    if bytesP > 2048:
                        print('Demasiado grande para caber en memoria')
                    else:
                        print('no hay espacio en memoria')
                    
            elif state == 'A':
                print('A')
            elif state == 'L':
                print('L')
            else:
                print('E')
        
