from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from models import ItemPayload
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from typing import Any, Dict, AnyStr, List, Union


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
grocery_list: dict[int, ItemPayload] = {}
some_file_path = "static/upload/alprVideo.mp4"

@app.post("/alprd")
async def root(request: Request):
    request_body = await request.body()
    print(request_body)




@app.get("/video")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="video/mp4")    
