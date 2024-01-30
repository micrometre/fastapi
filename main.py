from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from models import ItemPayload
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from typing import Any, Dict, AnyStr, List, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
some_file_path = "static/upload/alprVideo.mp4"

@app.post("/alprd")
async def get_alprd(request: Request):
    request_body = await request.body()
    result = await request.json()  
    print((result["uuid"]))




@app.get("/video")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="video/mp4")    
