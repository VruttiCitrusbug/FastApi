from fastapi import FastAPI
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

class FoodEnum(str, Enum):
    Fruits = 'Fruits'
    FastFood = 'FastFood'

@app.get("/food/{food_name}")
async def get_food(food_name: FoodEnum):
    if(food_name == FoodEnum.FastFood):
        return {
            "food_name": food_name,
            "food_type": "Healthy"
        }
    if(food_name == FoodEnum.Fruits):
        return {
            "food_name": food_name,
            "food_type": "UnHealthy"
        }

class Item(BaseModel):
    item_name: str
    description: str | None = None
    price: float

class ItemUpdate(BaseModel):
    item_name: str | None = None
    description: str | None = None
    price: float | None = None

fake_items_db = [{"item_name": "1", "price": 1.10, "description": "lol"}, {"item_name": "2", "price": 2}, {"item_name": "3", "price": 3.10},{"item_name": "4", "price": 3.10}, {"item_name": "5", "price": 5}, {"item_name": "6", "price": 2.10},{"item_name": "7", "price": 4.10}, {"item_name": "8", "price": 8.10}, {"item_name": "9", "price": 7.10},{"item_name": "10", "price": 9.10}, {"item_name": "11", "price": 1.10}, {"item_name": "12", "price": 0}]

# get single item or item list with pagination
@app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10, q: Optional[int] = None): recommended not to use Optional where it found for the python below 3.10
async def read_item(skip: int = 0, limit: int = 3, id: int | None = None) -> List[Item] | Item:
    if id is not None:
        return fake_items_db[id]
    return fake_items_db[skip : skip + limit]

#create an item POST
@app.post("/items/")
async def create_item(item: Item) -> Item:
    fake_items_db.insert(0,item)
    return item

# change entire resource PUT
@app.put("/item/{id}")
async def replace_item(item: Item, id: int) -> Item:
    fake_items_db.insert(id,item)
    return item

# PATCH for the partial changes for resource
@app.patch("/item/{id}")
async def update_item(item: ItemUpdate, id: int) -> Item:
    item_dict = item.model_dump()
    get_item = fake_items_db[id]
    for key in item_dict.keys():
        if item_dict[key] is not None:
            get_item[key] = item_dict[key]
    fake_items_db[id] = get_item
    return fake_items_db[id]