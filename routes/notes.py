from fastapi import FastAPI, Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from models.note import Note
from schemas.note import noteEntity,notesEntities 
from config.db import conn
from fastapi.templating import Jinja2Templates 
from bson import ObjectId 

notes = APIRouter() 

templates = Jinja2Templates(directory="templates")  

@notes.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    print(docs)
    newDocs = []
    for doc in docs:
        print(doc)
        newDocs.append({
            "id": str(doc["_id"]),  # Convert ObjectId to string for proper usage in templates
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
        })


    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


 
@notes.post("/")

async def create_note(request: Request): 
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    print("Form Data After Processing:", formDict)
    
    note = conn.notes.notes.insert_one(formDict)
    return {"Success": True, "note_id": str(note.inserted_id)}

@notes.put("/{note_id}")
async def update_note(note_id: str, request: Request):
    form = await request.form()
    update_data = dict(form)
    update_data["important"] = True if update_data.get("important") == "on" else False

    # Convert `note_id` to ObjectId and update the document
    result = conn.notes.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {
            "title": update_data.get("title"),
            "desc": update_data.get("desc"),
            "important": update_data.get("important")
        }}
    )
    
    if result.modified_count == 1:
        return {"Success": True, "message": "Note updated successfully"}
    else:
        return {"Success": False, "message": "Note not found or no changes made"}
    
@notes.delete("/{note_id}")
async def delete_note(note_id: str):
    # Convert `note_id` to ObjectId and delete the document
    result = conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
    
    if result.deleted_count == 1:
        return {"Success": True, "message": "Note deleted successfully"}
    else:
        return {"Success": False, "message": "Note not found"}


