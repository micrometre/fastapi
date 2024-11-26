from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
import redis
from models import ItemPayload
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from typing import Any, Dict, AnyStr, List, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from models import ItemPayload, Item, Plate


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
some_file_path = "static/upload/alprVideo.mp4"
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0, decode_responses=True)

@app.post("/items/")
async def create_item1(item: Item):
    return item



@app.post("/plates/")
async def create_item(plate: Plate):
    return plate

@app.post("/alprd2")
async def get_alprd(request: Request):
    alpr_data = await request.json()  
    alpr_plate_results = alpr_data["results"]
    alpr_plate = alpr_plate_results[0]["plate"]
    alpr_id = redis_client.incr("alpr_ids")
    redis_client.hset(
            f"alpr_id:{alpr_id}",
            mapping={
                "alpr_plate": alpr_plate,
            },
        )
    redis_client.hset("alpr_plate_to_id", alpr_plate, alpr_id)
    redis_client.publish("bigboxcode", alpr_plate)
    print((alpr_data))






@app.get("/video")
def steam_video():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="video/mp4")    
