class Printable:
    #Executes automatically by Python on print() statment of the object
    def __repr__(self):
        #We change the object to a Dictionary, then convert it to string
        return str(self.__dict__)
