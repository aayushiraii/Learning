# print("hi")
# print("thamarai")
# name = input("Hi,What is your name")
# print(name)

#sum 
a=10
b=9
sum=a+b
print(sum)

#list
marks=[90,98,97,95,92]
print(marks[0])
marks.append(5)
print(marks)

n=8
for i in range (1,n+1):
    for j in range (1,i+1):
        print(j,end=" ")
    print()

country={"India" : "Delhi",
         "Korea" : "seoul",
         "japan" : "Tokyo"}
print(country)
print(country.keys())
print(country.values())
print(country.get("India"))

if country.get("Japan"):
    print("Yes")
else:
    print("NOT FOUND")

#sets
Sets={1,5,3,3,3,5,6}
#print(Sets)
Sets.pop()

num=[3,8,7,8]
for i in num:
    print(num)

count=0
while count<5:
    print(count)
    count+=1

for i in range(10):
    if i==2:
        break
    print(i)

for i in range(9):
    if i==8:
        continue
    print(i)

names=["Aayushi","Adi","Thama"]
search="Adi"
for name in names:
    if name==search:
        print("FOUND")
    # else:
    #     print("NOT FOUND")

num=[2,4,6,8,9]
even=0
odd=0
for nums in num:
    if nums%2==0:
        even+=1
    else:
        odd+=1
print("even",  even)
print("odd" , odd)

num=[3,4,5,6,7,8]
for nums in num:
    if nums % 2==0:
        print(nums)
    # else:
    #     print(odd)
for i in range(10):
    if i%2==0:
        print(i)

Words = ["Apples", "Laptop", "Bitcot"]
V = "aeiou"

for word in Words:
    for char in word.lower():
        if char in V:
            print(word)
            break
