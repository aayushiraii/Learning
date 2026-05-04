# fastapi project

this is a small project i made while learning fastapi and database stuff

i didnt try to make it perfect, just wanted to understand how things work



## what is this

it is a basic api where:

 user can be created
 each user has categories
 each category has items
 item has name, quantity and price

so structure is like:

user -> category -> items



## tech used

 fastapi
 sqlalchemy
 postgres


## how to run

install things:


pip install fastapi uvicorn sqlalchemy psycopg2-binary


then run:


uvicorn main:app --reload


open this:

http://127.0.0.1:8000/docs



## files 

 main.py → routes
 models.py → database tables
 schemas.py → input/output
 crud.py → db logic
 database.py → connection



## what i understood from this

 difference between models and schemas
 how foreign keys work
 how data is connected
 how to write basic crud



there are probably many things to improve like:

 auth
 better structure
 validation

but for now it works 



