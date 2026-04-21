#factory is a function that creates objects for you
#actory decides WHICH object to create and gives it to you
# dog = Dog()
# #instead use
# dog = factory("dog")
#instead of using the code everywhere use the factory() function 

#singleton
#only one object is allowed 
#even if you try to create it as many times as you want it will only give the same object
#factory
class Dog:
    def speak(self):
        return "Bark"

class Cat:
    def speak(self):
        return "Meow"


def animal_factory(animal_type):
    if animal_type == "dog":
        return Dog()
    elif animal_type == "cat":
        return Cat()

animal = animal_factory("dog")

print(animal.speak())

class Circle:
    def draw(self):
        return "Drawing Circle"

class Square:
    def draw(self):
        return "Drawing Square"


def shape_factory(shape_type):
    shapes = {
        "circle": Circle,
        "square": Square
    }
    return shapes[shape_type]()
shape = shape_factory("circle")
print(shape.draw())

#singleton
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating Logger...")
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, msg):
        print(f"LOG: {msg}")
        log1 = Logger()
log1 = Logger()
log2 = Logger()

log1.log("Hello")
print(log1 is log2)   

# Factory creates objects smartly
# Singleton limits to one object
# Together controlled + clean system

