class Process:
    def __init__(self,ProcessNum,Bytes,Dir):
        self.ProcessNum = ProcessNum
        self.Bytes = Bytes
        self.Dir = Dir  #desplazamiento
        self.InRealMem = True