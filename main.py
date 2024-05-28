import logging
import shutil
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


@app.post('/upload')
def upload_file(uploaded_file: UploadFile = File(...)):
    path = f"static/upload/{uploaded_file.filename}"
    print({uploaded_file.filename})
    with open(path, 'w+b') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return {
        'file': uploaded_file.filename,
        'content': uploaded_file.content_type,
        'path': path,
    }    