import sys
import re
import fnmatch
import math
#local libraries
from ProcessData import Process

# revisa si existe un espacio disponible
# si no existe regresa -1
# si existe regra sa dirrecion inicial
def checkForSpace(Memoria,Tamaño):
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
#function to move to swaping
def MoveToSwapping(ProcessQueue,Memoria,Swapping,TablaDeProcesos,ProcessInSwapping,Proceso,Tamaño,FalloDePagina):
    Dir = checkForSpace(Memoria,Tamaño)
    print('Los siguientes procesos pasaran a swapping: ')
    while Dir == -1:
        FalloDePagina =  FalloDePagina + 1
        PNum = ProcessQueue[0].ProcessNum
        FisicalDir = getRealMemory(TablaDeProcesos[PNum],ProcessQueue[0].Dir)
        print('direccion fisica del proceso(' + str(PNum) + '): ' + str(FisicalDir))
        DeleteFromMemory(Memoria,FisicalDir,ProcessQueue[0].Bytes) #borramos los datos de la memoria
        tablaDePagina[PNum] = -1 #significa que esta en swapping y no tiene Marco
        FisicalDir = checkForSpace(Swapping,ProcessQueue[0].Bytes) #nos cambia a swapping
        ProcessInSwapping.append(ProcessQueue[0]) #hay que guardar el proceso en otro 
        ModMemoria(Swapping,FisicalDir,ProcessQueue[0].Bytes,PNum)
        ProcessQueue.remove(ProcessQueue[0]) #lo removemos de la cola
        Dir = checkForSpace(Memoria,Tamaño)
    ModMemoria(Memoria,Dir,Tamaño,Proceso)
    return Dir,FalloDePagina #regresa la direccion del proceso inicial

#BORRAMOS DE MEMORIA
def DeleteFromMemory(Memoria,Dir,Tamaño):
    for x in range(Dir,Dir+Tamaño):
        Memoria[x] = -1
    return
def getRealMemory(Marco,Despl):
    return int(math.floor(Marco * 16) + Despl)
#modifica la memoria para agregar un proceso con un tamaño desde una direccion inicial
def ModMemoria(Memoria,Dir,Tamaño,process):
    for x in range(Dir,Tamaño+Dir):
        Memoria[x] = process
    return
def SearchWithPNum(ProcessQueue,Pnum):
    for i in range(len(ProcessQueue)):
        if ProcessQueue[i].ProcessNum == Pnum:
            return ProcessQueue[i]
    return None

# fucniones auxiliares
def checkFirstValList(X):
    return X[0]
def printComment(X):
    return X[2:]
        

#-------------------------------------------------Inicio------------------------------------------------------------------
# sys.argv[] has the arguments from a python command line 
pattern = re.compile(r'(.)*(.txt)')
#regex para buscar los commandos
parser = re.compile(r'P\s+\d+\s+\d+|A\s+\d+\s+\d+\s+\d|L\s+\d+|C .+|F[^A-Za-z]|E$')
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
        Memoria = [-1] * 2048 # memoria real
        Swapping = [-1] * 4096 # memoria reservada para swapping
        ProcessQueue = [] # fila de los procesos para saber cual entro primero siguendo FIFO
        tablaDePagina = {} # para guardar los marcos y saber si estan en memoria real o virtual
        FalloDePagina = 0
        ProcessInSwapping = [] # para guardar los objetos procesos en swapping
        #---------------------iniciamos simulador----------------------------
        for i in range(length): 
            state = checkFirstValList(lista[i])
            if state == 'C':
                print(printComment(lista[i]))
            elif state == 'F':
                print('-----------------F---------------')
                print('Fallos de pagina: ' + str(FalloDePagina))
            elif state == 'P': #----- falta revisar que no exista un proceso igual
                
                print('-----------------P---------------')
                corte = lista[i].split() # separa en substrings
                Pnum = int(corte[2]) #numero de proceso
                bytesP = int(corte[1]) #tamaño
                Dir = checkForSpace(Memoria,bytesP) #dirrecion fisica inicial
                
                if Dir != -1:
                    tablaDePagina[Pnum] = Dir / 16 #guarda el marco de pagina 
                    Despl = Dir - math.floor(Dir/16)*16 #sacar el despl
                    P = Process(Pnum,bytesP,Despl) # se guarda objeto Proceso
                    ProcessQueue.append(P) 
                    ModMemoria(Memoria,Dir,bytesP,Pnum)
                    
                else:
                    if bytesP > 2048:
                        print('Demasiado grande para caber en memoria')
                    else:
                        print('no hay espacio en memoria') #Ejecutar LRU
                        print('utilizando remplazo LRU')
                        Dir,FalloDePagina = MoveToSwapping(ProcessQueue,Memoria,Swapping,tablaDePagina,ProcessInSwapping,Pnum,bytesP,FalloDePagina)
                        tablaDePagina[Pnum] = Dir/16
                        Despl = Dir - math.floor(Dir/16)*16
                        ObjectP = Process(Pnum,bytesP,Despl)
                        ProcessQueue.append(ObjectP)
                        
            elif state == 'A':
                print('-----------------A---------------')
                print('A')
            elif state == 'L':
                print('-----------------L---------------')
                corte = lista[i].split()
                pnum = int(corte[1])
                p = SearchWithPNum(ProcessQueue,pnum)
                if p == None:
                    print('El proceso no existe en memoria')
                    continue
                Tam = p.Bytes #buscar tamaño del 
                DRF = getRealMemory(tablaDePagina[pnum],p.Dir) #direccion fisica
                DeleteFromMemory(Memoria,DRF,Tam) # se elimina de memoria real
                tablaDePagina.pop(pnum) #se elimina de la tabla de paginas
                ProcessQueue.remove(p)
                print('Se elimino el proceso('+str(pnum) + ')')
            else:
                print('E')
        
        
        