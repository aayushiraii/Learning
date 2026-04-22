#encapsulation--protects data inside a class 
#keeping data and methods together in a class
#protected and private
#protected is defined as single underscore
#private is defined as double underscore

class Person:
  def __init__(self, name, age):
    self.name = name
    self._age = age #protected 

p1 = Person("Aayushi", 22)
print(p1.name)
print(p1._age) # Can access, but shouldn't

class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age

  def get_age(self):
    return self.__age

p1 = Person("Tobias", 25)
print(p1.get_age())

"""To access private property we can use getter method"""

class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age

  def get_age(self):
    return self.__age

  def set_age(self, age):
    if age > 0:
      self.__age = age
    else:
      print("Age must be positive")

p1 = Person("Aayushi", 22)
print(p1.get_age())

p1.set_age(23)
print(p1.get_age())

"""To change private property we can use setter"""

class Person:
  def __init__(self, name, salary):
    self.name = name
    self._salary = salary # Protected 

p1 = Person("Aayushi", 50000)
print(p1.name)
print(p1._salary) # Can access, but shouldn't


class Calculator:
  def __init__(self):
    self.result = 0

  def __validate(self, num):
    if not isinstance(num, (int, float)):
      return False
    return True

  def add(self, num):
    if self.__validate(num):
      self.result += num
    else:
      print("Invalid number")

calc = Calculator()
calc.add(10)
calc.add(5)
print(calc.result)

#Inheritance
# Inheritance allows us to define a class that inherits all the methods and properties from another class.
# Parent class is the class being inherited from, also called base class.
# Child class is the class that inherits from another class, also called derived class.

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object and then execute the printname method

x = Person("Aayushi", "Rai")
x.printname()

class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):  # inherits from Animal
    def bark(self):
        print("Dog barks")
        d = Dog()

d = Dog()
d.speak()  # inherited method
d.bark()   # child method

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)  # call parent constructor
        self.grade = grade

s = Student("Aayushi", "A")
print(s.name, s.grade)