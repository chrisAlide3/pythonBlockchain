##Importing Vehicle class and pass it to the Car class for inheritance
from vehicle import Vehicle

class Car(Vehicle):
    ## No class attributes defined. They are all inherited from vehicles

    def brag(self):
        print('Look at my nice car!')

car1 = Car(200)

car1.drive()
car1.brag()
car1.add_warnings('Be careful')
car1.get_warnings()
