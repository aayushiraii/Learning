def add(a,b):
    return(a+b)
print(add(10,7))

def name(fname,lname):
    return(fname,lname)
print(name(lname="aayushi",fname="rai"))

def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("dog", "zed")

def guest(name,age):
   print(name,age)
print("Hello,what's your name and age?")
guest(name="Aayushi",age=23)

def greet(name="Guest"):
   print("hello",name)
greet()
greet("Aayushi")

#kwargs
def person(name,**data):
   print(name)
   print(data)

person(name="Aayushi",age=22,city="vellore",mob=123456780)

def person(name,**data):
   print(name)
   for i,j in data.items():
      print(i,j)
person(name="Aayushi",age=22,city="vellore",mob=123456780)

#args
def show_numbers(*args):
    print(args)

show_numbers(1, 2, 3)

def show_numbers(*args):
    for num in args:
        print(num)

show_numbers(10, 20, 30)

def add(*args):
    return sum(args)

print(add(1, 2))
print(add(1, 2, 3, 4))

def demo(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

demo(1, 2, 3, name="Aayushi", age=23)

def greet(*names):
  for i in names:
     print("hello",i)

greet("Aayushi","Thama","Jaya","Bharthi")

def name(fname,lname):
    return(fname,lname)
print(name(lname="aayushi",fname="rai"))


def name(fname,lname):
    return(fname,lname)
print(name(lname=23,fname="rai"))