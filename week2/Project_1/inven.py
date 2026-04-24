import csv
import logging
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, Field

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR)

app = FastAPI()



# MODEL

class Item(BaseModel):
    item_id: int
    name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0)



# OCP: FILE READER

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



# VALIDATION

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



# OCP: FILTERS

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



# HELPERS

FILE_NAME = "inventory.csv"


def load_items():
    reader = CSVReader()
    data = reader.read(FILE_NAME)
    return validate(data)


def save_item(item: Item):
    try:
        with open(FILE_NAME, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=item.model_dump().keys())

            if f.tell() == 0:
                writer.writeheader()

            writer.writerow(item.model_dump())

    except Exception as e:
        print("Error saving item:", e)


# ROUTES 


@app.get("/items")
def get_items():
    try:
        return load_items()
    except Exception as e:
        logging.error(f"Error fetching items: {e}")
        return {"error": "Something went wrong while fetching items"}


@app.get("/low-stock")
def get_low_stock():
    try:
        items = load_items()
        low_filter = LowStockFilter(10)
        return filter_items(items, low_filter)
    except Exception as e:
        logging.error(f"Error fetching low stock items: {e}")
        return {"error": "Something went wrong while filtering items"}


@app.post("/items")
def add_item(item: Item):
    try:
        save_item(item)
        return {"message": "Item added successfully"}
    except Exception as e:
        logging.error(f"Error adding item {item}: {e}")
        return {"error": "Failed to add item"}