import sys
import re
import fnmatch

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
        #iniciamos simulador
        for i in range(length):
            state = checkFirstValList(lista[i])
            if state == 'C':
                print(printComment(lista[i]))
            elif state == 'F':
                print('F')
            elif state == 'P':
                print('P')
            elif state == 'A':
                print('A')
            elif state == 'L':
                print('L')
            else:
                print('E')
        
