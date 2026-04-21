class Student:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.name)
s = Student("Aayushi")
s.speak()

class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("Bark")

d = Dog("Rocky")
d.bark()

class Student:
    def __init__(self, name):
        self.name = name

s1 = Student("Aayushi")
s2 = Student("Adi")

print(s1.name)
print(s2.name)

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

s = Student("Aayushi", 90)

print(s.name)
print(s.marks)

class Car:
    def __init__(self, brand):
        self.brand = brand

c1 = Car("BMW")
c2 = Car("Audi")

print(c1.brand)
print(c2.brand)

class Phone:
    def __init__(self, brand):
        self.brand = brand

    def change_brand(self, new_brand):
        self.brand = new_brand

p = Phone("Apple")
print(p.brand)

p.change_brand("Samsung")
print(p.brand)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, u, p):
        if self.username == u and self.password == p:
            print("Login success")
        else:
            print("Wrong details")

u1 = User("admin", "1234")
u1.login("admin", "1234")