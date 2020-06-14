def parser ():
    entrada = input ('Introduce nombre de archivo: ')
    path = entrada.rstrip('\r')
    if not path.isfile(path):
        print ('No se ha encontrado el archivo. El programa terminará')
        exit()
    instrucciones = []
    with open (path.rstrip('\r')) as archivo:
        # division del archivo en renglones y se almacena en variable lineas
        lineas = archivo.read.splitlines()
        i=0
        for linea in lineas:
            i=i+1
            palabras = ' '.join(linea.split()).split(' ')
            if palabras[0]=='P':
                if len(palabras)>3:
                    instruccion = [palabras[0]]
                    instruccion.append(int(palabras[1]))
                    instruccion.append(int(palabras[2]))
                    instrucciones.append(instruccion)
                else:
                    print ('No se ejecutará la instruccion P. Se requieren 3 argumentos')
            elif palabras[0]=='A':
                if len(palabras)>3:
                    instruccion = [palabras[0]]
                    instruccion.append(int(palabras[1]))
                    instruccion.append(int(palabras[2]))
                    instruccion.append(int(palabras[3]))
                else:
                    print ('No se ejecutará la instruccion A. Se requieren 3 argumentos')
            elif palabras[0]=='L':
                if (len(palabras)>1):
                    instruccion=[palabras[0]]
                    instruccion.append(int(palabras[1]))
                    instrucciones.append(instruccion)
                else:
                    print ('No se ejecutará la instruccion L. Se requieren 2 argumentos')
            elif palabras[0]=='C':
                instruccion= [palabras[0]]
                # se unen los comentarios que se mostraran
                instruccion.append(' '.join(palabras[1::]))
                instrucciones.append(instruccion)
            elif palabras[0]=='F' or palabras[0]=='E':
                instruccion = [palabras[0]]
                instrucciones.append(instruccion)
            else:
                print ('No se ejecutara ninguna instruccion (instruccion no valida en linea ', i, ')') 
        return instrucciones