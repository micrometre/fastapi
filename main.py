from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from models import ItemPayload
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from typing import Any, Dict, AnyStr, List, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import redis
from models import ItemPayload

app = FastAPI()
redis_client = redis.StrictRedis(host="0.0.0.0", port=6379, db=0, decode_responses=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
some_file_path = "static/upload/alprVideo.mp4"

@app.post("/alprd")
async def get_alprd(request: Request):
    alpr_data = await request.json()  
    alpr_uuid = alpr_data["uuid"]
    alpr_plate_results = alpr_data["results"]
    alpr_plate = alpr_plate_results[0]["plate"]
    alpr_id = redis_client.incr("item_ids")
    redis_client.hset(
            f"item_id:{alpr_id}",
            mapping={
                "item_id": alpr_id,
                "item_uuid": alpr_uuid,
                "item_name": alpr_plate,
            },
        )
    redis_client.hset("item_name_to_id", alpr_plate, alpr_id)
    print((alpr_plate))




@app.get("/video")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="video/mp4")    
