f = open("/home/bitcot/Desktop/learnings/Learning/daythree/sample.txt") #syntax

f = open("sample.txt")
print(f.read())

with open("/home/bitcot/Desktop/learnings/Learning/daythree/sample.txt","w") as f:
    print(f.write("sample"))
#   print(f.read())


f = open("sample.txt")
print(f.readline())
f.close()


with open("sample.txt") as f:
  print(f.readline())


with open("sample.txt") as f:
  for x in f:
    print(x)

print(f.write("sample"))
file = open("sample.txt", "w")  # "w" means write
file.write("Hello, this is my first file!")
file.close()

file = open("sample.txt", "r")  # "r" means read
content = file.read()
print(content)
file.close()

import csv

with open("sample.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    writer.writerow(["name", "age", "city"])
    writer.writerow(["John", 25, "Chennai"])
    writer.writerow(["Sara", 22, "Delhi"])

f=open("sample.txt","w")
print(f.write())
f.close()

