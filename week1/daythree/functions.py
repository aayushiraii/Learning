#basic calling function
def name():
    print("Aayushi")
name()

def company():
    print("bitcot")
company()
company()
company()

#using parameters
def evenOdd(x):
    if x % 2 == 0:
        print("even")
    else:
        print("odd")
evenOdd(3)
evenOdd(8)

def greet():
    return("hello,whatsup")
print(greet())

#using parameters
def student_name(fname,lname):
    print(fname,lname)
student_name(fname="Aayushi",lname="rai")


def person(name,age,city,mob):
    print(name,age,city,mob)
person("Aayushi",22,"vellore",123445679890)

def add(a,b):
    print(a+b)
add(3,9)

def mul(x):
    return(x*x)
print(mul(4))

def count_letters(word):
    return len(word)

print(count_letters("Bitcot"))
