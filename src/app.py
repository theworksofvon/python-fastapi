from fastapi import FastAPI, Path, Query, HTTPException, status

""" recommended by fast api when using optional parameters """
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name:  Optional[str] = None
    price:  Optional[float] = None
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you would like to view", gt=0, lt=100)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID does not exist.")
    return inventory[item_id]


@app.get("/get-by-name")
def get_item_name(*, item_id: Optional[int] = None, name: str, test:  Optional[int] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item name not found.")


@app.get("/")
def home():
    return {"Data": "Test"}


@app.get("/about")
def about():
    return {"Data": "About"}


@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Item ID already exist.")
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item ID does not exist.")
    inventory[item_id].update(item)
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete.")):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID does not exist.")

    del inventory[item_id]
