import math

estrategia = False # LRU por default. Si se cambia a true significa que es FIFO
MEMORY_SIZE = 2048
PAGE_SIZE = 16
SWAP_SIZE = 4096

nextswap_fifo=[]
nextswap_lru=[]
proc_pags = {}
swapped_pags = {}
swapping = [0] * SWAP_SIZE
memory = [0] * MEMORY_SIZE
swaps = fallosdepag = time = 0

def findMemory():
    for i in range (0,MEMORY_SIZE,PAGE_SIZE):
        if(memory[i]==0):
             return i
    print('Memoria llena. No se ejecutará esta instrucción.')
    return -1

def findSwap():
    for i in range (0,SWAP_SIZE,PAGE_SIZE):
        if(swapping[i]==0):
            return i
    print('Memoria de swap llena. La instrucción no se ejecutará.')
    return -1


def pageToFrame(proceso, pag, n):
    if pag==0 and proceso==0:
        val=0
    else:
        val = [proceso,pag]
    for i in range(0, PAGE_SIZE):
        memory[n + i] = val
            

def pageToSwap(proceso, pag, n):
    if pag==0 and proceso==0:
        val=0
    else:
        val = [proceso,pag]
    for i in range(0, PAGE_SIZE):
        swapping[n + i] = val

def next():
    if(estrategia):
        # fifo
        next_frame = nextswap_fifo.pop()
        nextswap_fifo.insert(0, next_frame)
    else:
        # lru
        next_frame = nextswap_lru.pop()
        nextswap_lru.insert(0, next_frame)
    return next_frame



def E():
    print ('Fin de instrucciones')
    exit()
