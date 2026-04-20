def add(a:int,b:int): #-> int 
    return(a+b)
"""returns sum of two values"""
print(add(3,7))

def greet(name:str): #->string(str)
    return("hello",name)
"""This code returns a string type datatype and print with the given statement"""
"""returns hello message"""
print(greet("Aayushi"))

def num(n:int): #-> int
    return n*n
"""returns the square of the number"""
print(num(6))

def is_even(n: int) -> bool:
    """Check if number is even"""
    return n % 2 == 0

print(is_even(6))

def length(text: str) -> int:
    """Return length of text"""
    return len(text)

print(length("heuheuehuheuheuheuhuehuehuehuehuehuheuhheuheu"))

def multiply(a:int, b:int):
    """Return product of two numbers"""
    return a * b
print(multiply(2,10))

def is_positive(n:int): #bool
    """Check if number is positive"""
    return n > 0
print(is_positive(0))

def to_upper(text):
    """Convert text to uppercase"""
    return text.upper()
print(to_upper("i want sushi,ugh im so hungry"))

def divide(a, b):
    """
    Divide two numbers.

    Returns result of a / b.
    """
    return a / b
print(divide(3,8))

