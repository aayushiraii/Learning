def local():
    x=10
    print(x)
local()


x=100

def glo():
    print(x)
glo()

com="bitcot"
def comp():
    print(com)
comp()

#changing global 

x=99
def moGlo():
    mGlo = 78
    print(mGlo)
moGlo()
print(x)

x = 10
def change():
    global x
    x = 20

change()
print(x) 

def outer():
    x="outer"
    def inner():
        print(x)
    inner()
outer()
#nonlocal
def outer():
    x="outer"
    def inner():
        nonlocal x
        x=30
        print(x)
    inner()
outer()

def com():
    c="bitcot"
    def comp2():
        nonlocal c
        c="jp morgan"
        print(c)
    comp2()
com()