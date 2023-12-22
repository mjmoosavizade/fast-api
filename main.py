from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import aioredis
import json
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


class Item(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None


redis = None
REDIS_URL = os.getenv("REDIS_URL")


async def startup_event():
    global redis
    redis = await aioredis.from_url(os.getenv("REDIS_URL"))


async def shutdown_event():
    redis.close()
    await redis.wait_closed()


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


@app.post("/items/")
async def create_item(item: Item):
    item.id = await redis.incr("itemID")
    await redis.set(f"item:{item.id}", json.dumps(item.dict()))
    return item


@app.get("/items/")
async def read_items():
    keys = await redis.keys("item:*")
    items = []
    for key in keys:
        item = await redis.get(key)
        items.append(json.loads(item))
    return items


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = await redis.get(f"item:{item_id}")
    if item is not None:
        return json.loads(item)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    item.id = item_id
    await redis.set(f"item:{item_id}", json.dumps(item.dict()))
    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    deleted = await redis.delete(f"item:{item_id}")
    if deleted == 1:
        return {"message": "Item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
