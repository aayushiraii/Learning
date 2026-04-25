from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 🔹 Pydantic Model
class Product(BaseModel):
    name: str
    price: float


# 🔹 POST Route using the model
@app.POST("/products")
def create_product(product: Product):
    return product

@app.GET("/products")
def read_product(product: Product):
    return product