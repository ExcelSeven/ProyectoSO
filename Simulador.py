import sys
import re
import fnmatch

# sys.argv[] has the arguments from a python command line 
pattern = re.compile(r'(.)*(.txt)')
if (len(sys.argv) != 2):
    print("argumentos incorrectos")
else:
    #revisa si el archivo no es txt
    if(pattern.search(sys.argv[1]) == None):
        print('el texto no es un .txt')

