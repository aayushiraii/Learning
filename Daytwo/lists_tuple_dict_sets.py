#list
marks=[90,98,97,95,92]
print(marks[0])
marks.append(5)
print(marks)
#dict
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

