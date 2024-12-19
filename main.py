from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import load_dotenv
import os 

# Load environment variables from the .env file
load_dotenv()

# Access variables
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = MongoClient(DATABASE_URL)

docs = conn.notes.notes.find({}) 

newDocs = []
for doc in docs: 
     newDocs.append({
        "id" : doc["_id"],
        "note" : doc["note"]
    })

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request): 
    return templates.TemplateResponse("index.html", {"request" : request, "newDocs"  : newDocs})