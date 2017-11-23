class Temperature():
    def __init__(self, amount, Unit):
        self.Amount = amount #interger amount in C
        Unit = str(Unit).capitalize()
        Unit = Unit[0:1]
        #print ("Unit is: "+ Unit)
        self.Units= Unit #c or f

        ###THIS IS FOR OUTPUT####
        self.degsign ='DEG'

    def __str__(self):
        return  str(self.Amount) + " "+ self.degsign+" "+self.Units

    ### F functions
    def intF(self):
        #returns interger
        if(self.Units == 'C'):
            return int(float(self.Amount) *(9.0/5.0) + 32.5)
        else:
            return int(self.Amount)
    def strF(self):
        #returns string with units
        return str(self.intF())+" "+self.degsign+" F"


    ###C functions
    def intC(self):
        if (self.Units == 'F'):
            return int((float(self.Amount) -32.5)* (5.0/9.0))
        else:
            return int(self.Amount)
    def strC(self):
        return str(self.intC()) + " " + self.degsign + " C"

    ###GENERAL FUNCTIONS
def CtoF(amt):
    return int(float(amt) * (9.0 / 5.0) + 32.5)
def KPAtoPSI(amt):
    return float(amt)*0.145
def KmtoM(amt):
    return float(amt)*0.621


class Distance():
    def __init__(self):
        pass

###EXAMPLE AND TEST COMMENT OUT WHEN DONE####
#t= Temperature(36, 'c')

#print(t.strF())

#t2= Temperature(87, 'F')
#print(t2.strC())