#L-liskov substitution principle 
#child class should replace parent class without breaking the parent class 

class Bird:
    pass


class FlyingBird(Bird):
    def fly(self):
        print("Flying")


class Sparrow(FlyingBird):
    pass


class Penguin(Bird):
    def swim(self):
        print("Swimming")


#I- interface segregation princple 
#the methods that are of not use, doesnt need to be in the function 
#make smalllll,specific interface

class Workable:
    def work(self):
        pass


class Eatable:
    def eat(self):
        pass


class Human(Workable, Eatable):
    pass


class Robot(Workable):
    pass

#D- dependency inversion princple 
# meaning it has nothing to do with the logic it depends on abstraction 
# use common interface 
# avoid hardcoding specific implementations


class TV:
    def on(self):
        pass


class SamsungTV(TV):
    def on(self):
        print("Samsung TV ON")


class LGTV(TV):
    def on(self):
        print("LG TV ON")


class Remote:
    def __init__(self, tv: TV):
        self.tv = tv

    def power_on(self):
        self.tv.on()