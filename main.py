import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import redis
import asyncio
from sse_starlette.sse import EventSourceResponse
import time
import asyncio
import uvicorn
from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI, Request
from typing import Annotated

from fastapi import  File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from models import ItemPayload
logger = logging.getLogger()

some_file_path = "static/upload/alprVideo.mp4"

app = FastAPI(debug=True) # type: ignore
redis_client = redis.StrictRedis(host="0.0.0.0", port=6379, db=0, decode_responses=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stream")
def read_root():
    return {"Hello": "World"}


@app.post("/alprd1/alprd1")
async def get_alprd(request: Request):
    req_header = request.headers
    client_host = request.client.host
    alpr_data = await request.json()  
    alpr_uuid = alpr_data["uuid"]
    alpr_img = alpr_data["uuid"]
    alpr_plate_results = alpr_data["results"]
    alpr_plate = alpr_plate_results[0]["plate"]
    alpr_img_url = 'http://'+ client_host + ':5000' + '/images/' + alpr_uuid + '.jpg'
    alpr_id = redis_client.incr("alpr_ids")
    redis_client.hset(
        f"alpr_plate:{alpr_plate}",
        mapping={
            "alpr_plate_id": alpr_plate,
            "alpr_plate": alpr_plate,
            "alpr_plate_img": alpr_img,
            "alpr_plate_url": alpr_img_url,
        },
    ) 
    redis_client.hset("alpr_plate_to_id", alpr_plate, alpr_plate)
    redis_client.hset("alpr_plate_to_img_url", alpr_plate, alpr_img_url)
    redis_client.hset("alpr_plate_to_img", alpr_plate, alpr_img)
    redis_client.publish("bigboxcode", alpr_plate)
    print((alpr_img_url))
    return {"client_host": client_host}


# Route to list a specific item by ID but using Redis
@app.get("/alprs/{alpr_id}")
def list_item(item_id: int) -> dict[str, dict[str, str]]:
    if not redis_client.hexists(f"alpr_id:{item_id}", "alpr_id"):
        raise HTTPException(status_code=404, detail="Item not found.")
    else:
        return {"alpr": redis_client.hgetall(f"alpr_id:{item_id}")}

@app.get("/video")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="video/mp4")    



@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}



@app.get("/upload")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>

</body>
    """
    return HTMLResponse(content=content)    


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})    