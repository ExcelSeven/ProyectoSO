import threading

semaforo = threading.Semaphore(1)
contador=0
contadorsins=0

def funcion (n):
    semaforo.acquire()
    global contador
    contador+=1
    semaforo.release()

def funcionsinS (n):
    global contadorsins
    contadorsins+=1

for x in range(1, 10001):
    t = threading.Thread(target=funcion, args=(x,))
    t2 = threading.Thread(target=funcionsinS, args=(x,))
    t.start()
    t2.start()

print ("total contador con semaforos: ", contador)
print ("total contador sin semaforos: ", contadorsins)