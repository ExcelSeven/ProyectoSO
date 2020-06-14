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



def swap(new_process, new_page, next_frame):
    if findSwap()== -1:
        return False
    
    global time
    prev_proc, prev_pag = memory[next_frame]
    print("La pagina ", prev_pag, " del proceso ", prev_proc, " ha sido swappeada al marco ", math.floor(findSwap()/PAGE_SIZE), " de swapping.")
    pageToSwap(prev_proc, prev_pag, findSwap())

    if prev_proc not in swapped_pags:
        swapped_pags[prev_proc] = {}

    swapped_pags[prev_proc][prev_pag] = findSwap()
    del proc_pags[prev_proc][prev_pag]

    
    pageToFrame(new_process, new_page, next_frame)
    proc_pags[new_process][new_page] = next_frame
    
    time+= 2
    return True

