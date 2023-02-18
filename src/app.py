from fastapi import FastAPI, Path

""" recommended by fast api when using optional parameters """
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you would like to view", gt=0, lt=100)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item_name(*, item_id: Optional[int] = None, name: str, test:  Optional[int] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"Data": "Not Found"}


@app.get("/")
def home():
    return {"Data": "Test"}


@app.get("/about")
def about():
    return {"Data": "About"}


@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item already exists."}
    inventory[item_id] = item
    return inventory[item_id]
