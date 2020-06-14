import sys
import re
import fnmatch

# sys.argv[] has the arguments from a python command line 
pattern = re.compile(r'(.)*(.txt)')
parser = re.compile(r'P \d+ \d+|A \d+ \d+ \d|L \d+|C \w+|F[^A-Za-z]|E$')
if (len(sys.argv) != 2):
    print("argumentos incorrectos")
else:
    #revisa si el archivo no es txt
    if(pattern.search(sys.argv[1]) == None):
        print('el texto no es un .txt')
    else:
        file_Object = open(sys.argv[1],'r')
        data = file_Object.read()
        lista = parser.findall(data)
        print(lista)