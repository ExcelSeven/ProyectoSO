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

def MoveToSwapping(ProcessQueue,Memoria,Swapping,TablaDeProcesos,ProcessInSwapping,Proceso,Tamaño,FalloDePagina,contSwapping):
    Dir = checkForSpace(Memoria,Tamaño)
    
    while Dir == -1:
        contSwapping = contSwapping + 1
        PNum = ProcessQueue[0].ProcessNum

        FalloDePagina[Proceso] = FalloDePagina[Proceso] + 1

        FisicalDir = getRealMemory(TablaDeProcesos[PNum],ProcessQueue[0].Dir)

        print('direccion fisica del proceso(' + str(PNum) + '): ' + str(FisicalDir) + ' Despues de pasar a swapping')

        DeleteFromMemory(Memoria,FisicalDir,ProcessQueue[0].Bytes) #borramos los datos de la memoria

        tablaDePagina[PNum] = -1 #significa que esta en swapping y no tiene Marco

        FisicalDir = checkForSpace(Swapping,ProcessQueue[0].Bytes) #nos cambia a swapping

        ModMemoria(Swapping,FisicalDir,ProcessQueue[0].Bytes,PNum)

        ProcessInSwapping.append(ProcessQueue[0]) #hay que guardar el proceso en otro


        ProcessQueue.remove(ProcessQueue[0]) #lo removemos de la cola

        Dir = checkForSpace(Memoria,Tamaño)
    Dir = checkForSpace(Memoria,Tamaño)
    ModMemoria(Memoria,Dir,Tamaño,Proceso)
    return Dir,contSwapping #regresa la direccion del proceso inicial



#BORRAMOS DE MEMORIA
def DeleteFromMemory(Memoria,Dir,Tamaño):
    for x in range(Dir,Dir+Tamaño):
        Memoria[x] = -1
    return
def getRealMemory(Marco,Despl):
    return int(Marco * 16 + Despl)
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
        lista = parser.findall(data)
        #hace print de los comandos
        print(lista)
        length = len(lista)
        Memoria = [-1] * 2048 # memoria real
        Swapping = [-1] * 4096 # memoria reservada para swapping
        ProcessQueue = [] # fila de los procesos para saber cual entro primero siguendo FIFO
        tablaDePagina = {} # para guardar los marcos y saber si estan en memoria real o virtual
        FalloDePagina = {} # para guardar los fallos de pagina
        turnAround = {} # para guardar los turnaround
        turnAroundProm = 0 #promedio
        contSwapping = 0
        ProcessInSwapping = [] # para guardar los objetos procesos en swapping
        #---------------------iniciamos simulador----------------------------
        for i in range(length): 
            state = checkFirstValList(lista[i])
            if state == 'C':
                print('C')
                print(printComment(lista[i]))
            elif state == 'F':
                print('-----------------F---------------')
                print('F')
                for Key,Fallos in FalloDePagina.items():
                    print('Fallos de pagina al inroducir el proceso (' + str(Key) + '): ' + str(Fallos)) #desplieja todos los fallos por proceso
                    FalloDePagina[Key] = 0
                for i in turnAround.values():
                    turnAroundProm = turnAroundProm + i
                if len(turnAround) != 0:
                    turnAroundProm = turnAroundProm / len(turnAround)
                for Key,Fallos in turnAround.items():
                    print('TurnAround del proceso (' + str(Key) + '): ' + str(Fallos)) #desplieja todos los fallos por proceso
                    turnAround[Key] = 0
                print('TurnAround Promedio: ', turnAroundProm)
                print("Numero de Swappings: ", contSwapping)

                contSwapping = 0
                turnAroundProm = 0
                
                      
                
            elif state == 'P': #----- falta revisar que no exista un proceso igual
                
                print('-----------------P---------------')
                corte = lista[i].split() # separa en substrings
                print(corte[0] + ' ' + corte[1] + ' ' + corte[2])
                Pnum = int(corte[2]) #numero de proceso
                bytesP = int(corte[1]) #tamaño
                Dir = checkForSpace(Memoria,bytesP) #dirrecion fisica inicial
                
                if Dir != -1:
                    tablaDePagina[Pnum] = Dir / 16 #guarda el marco de pagina 
                    Despl = Dir - (Dir/16)*16 #sacar el despl
                    P = Process(Pnum,bytesP,Despl) # se guarda objeto Proceso
                    ProcessQueue.append(P) 
                    ModMemoria(Memoria,Dir,bytesP,Pnum)
                    FalloDePagina[Pnum]  = 0
                    print('Proceso (' + str(Pnum) + ') Introducido en Memoria Exitosamente')
                    if Dir != 0:
                         turnAround[Pnum] = (Dir/16)
                else:
                    if bytesP > 2048:
                        print('Demasiado grande para caber en memoria')
                    else:
                        print('no hay espacio en memoria') #Ejecutar LRU
                        print('utilizando remplazo LRU')
                        FalloDePagina[Pnum] = 0
                        
                        Dir,contSwapping = MoveToSwapping(ProcessQueue,Memoria,Swapping,tablaDePagina,ProcessInSwapping,Pnum,bytesP,FalloDePagina,contSwapping)
                        tablaDePagina[Pnum] = Dir/16
                        Despl = Dir - math.floor(Dir/16)*16
                        ObjectP = Process(Pnum,bytesP,Despl)
                        ProcessQueue.append(ObjectP)
                        print('Proceso (' + str(Pnum) + ') Introducido en Memoria Exitosamente')
                        if Dir != 0:
                         turnAround[Pnum] = (Dir/16)
                
                        
            elif state == 'A':
                print('-----------------A---------------')
                corte = lista[i].split()
                Pnum = int(corte[2])
                Vdir = int(corte[1])
                print('A ' + corte[1] + ' ' + corte[2])
                p = SearchWithPNum(ProcessQueue,Pnum)
                if p == None:
                    #hay que mover de swapping a memory
                        z = SearchWithPNum(ProcessInSwapping,Pnum)
                        if z == None:
                            print('no existe el proceso')
                        else:
                            DeleteFromMemory(Swapping,int(z.Dir),z.Bytes)
                            Dir,contSwapping = MoveToSwapping(ProcessQueue,Memoria,Swapping,tablaDePagina,ProcessInSwapping,Pnum,z.Bytes,FalloDePagina,contSwapping)
                            ProcessQueue.append(z)
                            ProcessInSwapping.remove(z)
                            tablaDePagina[Pnum] = Dir/16
                            Despl = Dir - math.floor(Dir/16)*16
                            z.Dir = Despl

                            
                
                Fdir = getRealMemory(tablaDePagina[Pnum],SearchWithPNum(ProcessQueue,Pnum).Dir)
                print('A - La direccion asignada es (' + str(Fdir) + ')')
            elif state == 'L':
                
                print('-----------------L---------------')
                
                corte = lista[i].split()
                print('L ' + corte[1])
                pnum = int(corte[1])
                p = SearchWithPNum(ProcessQueue,pnum)
                Z = SearchWithPNum(ProcessInSwapping,pnum)
                if p != None:
                    Tam = p.Bytes #buscar tamaño del 
                    DRF = getRealMemory(tablaDePagina[pnum],p.Dir) #direccion fisica
                    DeleteFromMemory(Memoria,DRF,Tam) # se elimina de memoria real
                    tablaDePagina.pop(pnum) #se elimina de la tabla de paginas
                    ProcessQueue.remove(p)
                    print('Se elimino el proceso('+str(pnum) + ')')
                
                elif Z != None:
                    Tam = Z.Bytes #buscar tamaño del 
                    DRF = Z.Dir #direccion fisica
                    DeleteFromMemory(Swapping,DRF,Tam) # se elimina de memoria real
                    tablaDePagina.pop(pnum) #se elimina de la tabla de paginas
                    ProcessInSwapping.remove(Z)
                    print('Se elimino el proceso('+str(pnum) + ')')
                else:
                    print('no existe el proceso')

                
            else:
                print('E')
        
        
        