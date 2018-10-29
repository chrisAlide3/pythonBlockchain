##Importing Vehicle class and pass it to the Bus class for inheritance
from vehicle import Vehicle

class Bus(Vehicle):
    #Constructor
    def __init__(self, starting_top_speed=100):
        ##super()__init__ runs the constructor of the main class (Vehicle)
        super().__init__(starting_top_speed)
        self.passengers = []

    def add_passengers(self, passenger_list):
        self.passengers.extend(passenger_list)

    def get_passengers(self):
        return self.passengers

bus1 = Bus(200)
bus1.drive()
bus1.add_passengers(['Marc', 'Dany', 'Chris'])
print(bus1.get_passengers())
