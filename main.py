from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import init_db, get_db
import sqlite3
import uvicorn


app = FastAPI()


# on startup, initialise database
@app.on_event("startup")
def startup():
    init_db()


# mounts the StaticFiles application for handling '/static/' queries
app.mount("/static/", StaticFiles(directory="static"), name="static")


# show home page
@app.get("/")
def homepage():
    return FileResponse("static/index.html")


# return categories data to Javascript
@app.get("/api/categories")
def get_categories(db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute("SELECT * FROM categories")
        list_of_rows = [dict(item) for item in cursor.fetchall()]
        return list_of_rows
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# return items data to Javascript
@app.get("/api/items")
def get_items(db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute("SELECT * FROM items")
        list_of_rows = [dict(item) for item in cursor.fetchall()]
        return list_of_rows
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# return specific item data to Javascript
@app.get("/api/items/{id}")
def get_item(id, db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute("SELECT * FROM items WHERE id=?", (id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Item Not Found")
        return dict(row)
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Internal Server Error")
