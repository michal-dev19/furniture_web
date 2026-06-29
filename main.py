from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import init_db, get_db
import sqlite3
import uvicorn


app = FastAPI()


# create class for FastAPI to handle request data
class EnquiryForm(BaseModel):
    name: str
    email: str
    phone: str
    message: str


# create


# on startup, initialise database
@app.on_event("startup")
def startup():
    init_db()


# mounts the StaticFiles application for handling '/static/' queries
app.mount("/static/", StaticFiles(directory="static"), name="static")


# function for raising an Internal Server Error (500)
def ise():
    raise HTTPException(status_code=500, detail="Internal Server Error")


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
        ise()


# return items data to Javascript
@app.get("/api/items")
def get_items(db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute("SELECT * FROM items")
        list_of_rows = [dict(item) for item in cursor.fetchall()]
        return list_of_rows
    except sqlite3.Error:
        ise()


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
        ise()


# insert request data from user enquiry form
@app.post("/api/enquiries/{item_id}")
def insert_enquiry(item_id: int, enquiry: EnquiryForm, db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute(
            """INSERT INTO enquiries 
            (item_id, customer_name, customer_email, customer_phone, customer_message)
            VALUES 
            (?, ?, ?, ?, ?)""",
            (item_id, enquiry.name, enquiry.email, enquiry.phone, enquiry.message),
        )
        if cursor.rowcount == 0:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=400, detail="Bad Request")
        conn.commit()
        return {"request": "success"}
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        ise()


# (admin) returns all data in enquiry table
@app.get("/api/enquiries")
def get_enquiries(db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute("SELECT * FROM enquiries")
        list_of_rows = [dict(item) for item in cursor.fetchall()]
        return list_of_rows
    except sqlite3.Error:
        ise()


# (admin) patch data in enquiry table
@app.patch("/api/enquiries/{enquiry_id}")
def patch_enquiries(enquiry_id: int, status: str, db=Depends(get_db)):
    conn, cursor = db
    try:
        cursor.execute(
            """UPDATE enquiries SET
            status=?
            WHERE
            id=?""",
            (status, enquiry_id),
        )
        if cursor.rowcount == 0:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=400, detail="Bad Request")
        conn.commit()
        return {"request": "success"}
    except sqlite3.Error:
        ise()
