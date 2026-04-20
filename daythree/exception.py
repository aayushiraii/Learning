try:
    x = int(input("Enter number: "))
    print(10 / x)
except:
    print("Something went wrong")

try:
    num = int(input("Enter number: "))
    print(num)
except:
    print("You did not enter a number")

try:
    x = int(input("Enter number: "))
    print(10 / x)
except:
    print("Error happened")

try:
    x = int(input("Enter number: "))
    print(10 / x)

except:
    print("Error")

finally:
    print("Program finished")

try:
    file = open("data.txt", "r")
    print(file.read())

except FileNotFoundError:
    print("File not found")

finally:
    print("Done")


try:
    n = 0
    res = 100 / n
    
except ZeroDivisionError:
    print("You can't divide by zero!")
    
except ValueError:
    print("Enter a valid number!")
    
else:
    print("Result is", res)
    
finally:
    print("Execution complete.")