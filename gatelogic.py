############### INPUT #############
###################################
class INPUT:
    def __init__(self, port):
        self.port = port
        self.INPUT = input("INPUT ("+ port + ") :  ")
###################################

############### NOT ###############
###################################
class NOT:
    def __init__(self, INPUT = 1):
        self.INPUT = INPUT
                
    def OUTPUT(self):
        if (self.INPUT == False):
            return 1
        if (self.INPUT == True):
            return 0
###################################

############### AND ###############
###################################
class AND:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = self.INPUT1 & self.INPUT2
        return (self.pinOUT)
###################################

############### NAND ##############
###################################
class NAND:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = NOT(self.INPUT1 & self.INPUT2).OUTPUT()
        return (self.pinOUT)
###################################

############### OR ################
###################################
class OR:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = self.INPUT1 | self.INPUT2
        return (self.pinOUT)
###################################

############### NOR ###############
###################################
class NOR:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = NOT(self.INPUT1 | self.INPUT2).OUTPUT()
        return (self.pinOUT)
###################################

############### XOR ###############
###################################
class XOR:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = self.INPUT1 ^ self.INPUT2
        return (self.pinOUT)
###################################

############### XNOR ##############
###################################
class XNOR:
    def __init__(self, INPUT1 = 0, INPUT2 = 0):
        self.INPUT1 = INPUT1
        self.INPUT2 = INPUT2
                
    def OUTPUT(self):
        self.pinOUT = NOT(self.INPUT1 ^ self.INPUT2).OUTPUT()
        return (self.pinOUT)
###################################
