import csv
import logging
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, Field

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR)

app = FastAPI()


# -------------------
# MODEL
# -------------------
class Item(BaseModel):
    item_id: int
    name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0)


# -------------------
# OCP: FILE READER
# -------------------
class FileReader:
    def read(self, file):
        raise NotImplementedError


class CSVReader(FileReader):
    def read(self, file):
        try:
            with open(file, newline='') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print("File not found!")
            return []
        except Exception as e:
            print("Error reading file:", e)
            return []


# -------------------
# VALIDATION
# -------------------
def validate(data):
    valid_items = []

    for row in data:
        try:
            item = Item(**row)
            valid_items.append(item)

        except ValidationError as e:
            logging.error(f"Error in row {row}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in row {row}: {e}")

    return valid_items


# -------------------
# OCP: FILTERS
# -------------------
class Filter:
    def apply(self, item):
        raise NotImplementedError


class LowStockFilter(Filter):
    def __init__(self, threshold=10):
        self.threshold = threshold

    def apply(self, item):
        return item.quantity < self.threshold


def filter_items(items, filter_strategy):
    return [item for item in items if filter_strategy.apply(item)]


# -------------------
# HELPERS
# -------------------
FILE_NAME = "inventory.csv"


def load_items():
    reader = CSVReader()
    data = reader.read(FILE_NAME)
    return validate(data)


def save_item(item: Item):
    try:
        with open(FILE_NAME, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=item.model_dump().keys())

            # write header if file empty
            if f.tell() == 0:
                writer.writeheader()

            writer.writerow(item.model_dump())

    except Exception as e:
        print("Error saving item:", e)


# -------------------
# ROUTES
# -------------------

# GET all items
@app.get("/items")
def get_items():
    return load_items()


# GET low stock items
@app.get("/low-stock")
def get_low_stock():
    items = load_items()
    low_filter = LowStockFilter(10)
    return filter_items(items, low_filter)


# POST new item
@app.post("/items")
def add_item(item: Item):
    save_item(item)
    return {"message": "Item added successfully"}