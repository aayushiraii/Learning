from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/hello")
def say_hello():
    return {"message": "Hi there"}

@app.get("/")
def home():
    return {"message": "Home"}

@app.get("/about")
def about():
    return {"message": "About page"}

@app.get("/user/{name}")
def get_user(name: str):
    return {"user": name}

@app.post("/products")
def create_product():
    return {"msg": "product created"}

# @app.get("/test")
# def get_test():
#     return {"method": "GET"}

# @app.post("/test")
# def post_test():
#     return {"method": "POST"}

# @app.put("/test")
# def put_test():
#     return {"method": "PUT"}

# @app.delete("/test")
# def delete_test():
#     return {"method": "DELETE"}