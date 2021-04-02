from enum import Enum
from typing import Optional

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_item_db = [{"item_name": "Foo"},
                {"item_name": "Bar"},
                {"item_name": "Baz"}]


@app.get("/items/{item_id}")
async def read_item(
        *,
        item_id: int = Path(..., title="The ID of the item to get", le=1000),
        q: str,
        size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    print(item)
    print(item.dict())
    print(item.json())
    print(item.validate)
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
