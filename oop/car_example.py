#Define class with class keyword. Name is capitalised(eg SportCar)
#A class is a blueprint for the object creation
class Car:
    # class attributes.
    attr_top_speed = 100
    attr_warnings = []
    ##Using constructor:
    def __init__(self, starting_top_speed=100): #double underscore init double underscore
        self.top_speed = starting_top_speed
        self.__warnings = []

    ##We can define private attributes that should only be changed through
    #Method within the class not from outside. Just start the field name with '__'
    #This insures that we cannot update the attribute outside of the class
    def add_warnings(self, warning_text):
        self.__warnings.append(warning_text)

    # class methods(function)
    # to use attributes from within the class pass 'self'
    def drive_attr(self):
        print("(attr)I'm driving but certainly not over {} kmh".format(self.attr_top_speed))
    def drive(self):
        print("(constr)I'm driving but certainly not over {} kmh".format(self.top_speed))

#Instantiate new object with class. 
#new_var = Classname()
#new_var.attribute or new_var.method()

car1 = Car()
## To work with the whole object attributes use __dict__. 
#  It returns a dictionary (only for contructors)
print(car1.__dict__)
print("Car1 attribute: {}".format(car1.drive_attr()))
print("Car1 construct: {}".format(car1.drive()))

#!!Class attributes are reference attribute. By changing the value of 
#an attribute on an instanciated object will change it for all
## Here car1.warnings.append will also append on Car, car2, car3 
## To avoid this we need a Constructor!
##With construcor each object attribute has it's own attribute
car1.attr_warnings.append("New warning attribute!")
# car1.__warnings.append("New warning car1")

car2 = Car(200)
car2.add_warnings("car2 class warning")
print("Car2 attribute: {}".format(car2.drive_attr()))
print("Car2 construct: {}".format(car2.drive()))
print("Car2 attr.warnings: {}".format(car2.attr_warnings))
# print("Car2 const.warnings: {}".format(car2.__warnings))

car3 = Car(300)
print("Car3 attribute: {}".format(car3.drive_attr()))
print("Car3 construct: {}".format(car3.drive()))
print("Car3 attr.warnings: {}".format(car3.attr_warnings))
# print("Car3 const.warnings: {}".format(car3.__warnings))



    