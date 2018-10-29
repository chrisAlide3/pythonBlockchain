class Vehicle:
    #Create attribute constructor
    def __init__(self, starting_top_speed=100):
        self.top_speed = starting_top_speed
        #Define as private with leading double underscore
        self.__warnings = []

    def drive(self):
        print('I am not driving faster than {} km/h'.format(self.top_speed))
    
    def add_warnings(self, new_warning='New warning'):
        self.__warnings.append(new_warning)

    def get_warnings(self):
        print(self.__warnings)
