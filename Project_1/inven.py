import csv
import logging
from pydantic import BaseModel, ValidationError, Field

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR)

# Pydantic Model
class Item(BaseModel):
    item_id: int
    name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0)

# Read CSV
def read_csv(file):
    with open(file, newline='') as f:
        return list(csv.DictReader(f))

# Validate data
def validate(data):
    valid_items = []
    for row in data:
        try:
            item = Item(**row)
            valid_items.append(item)
        except ValidationError as e:
            logging.error(f"Error in row {row}: {e}")
    return valid_items

# Low stock report
def low_stock(items, threshold=10):
    return [item for item in items if item.quantity < threshold]

# Main
def main():
    data = read_csv("inventory.csv")
    items = validate(data)

    low_items = low_stock(items)

    print("\nLow Stock Items:")
    for item in low_items:
        print(f"{item.name} (Qty: {item.quantity})")

if __name__ == "__main__":
    main()