from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

app = FastAPI()
some_file_path = "alprVideo.mp4"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"message": "Hello World"}




@app.get("/video")
def main():
    def iterfile():  # 
        with open(some_file_path, mode="rb") as file_like:  # 
            yield from file_like  # 

    return StreamingResponse(iterfile(), media_type="video/mp4")    


@app.get("/alpr", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})    
