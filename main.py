# from fastapi import FastAPI, HTTPException
# import requests


# app = FastAPI(title="My Apis",
#              description="Developer : Mirshad")

# #domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


# @app.get("/")
# def home():
#     return {"Languages":['Hindi', 'English', 'Punjabi', 'Tamil', 'Telugu', 'Marathi', 'Gujarati', 'Bengali', 'Kannada', 'Bhojpuri', 'Malayalam', 'Urdu', 'Haryanvi', 'Rajasthani', 'Odia', 'Assamese']}


# @app.get('/api/music/music_home/{language}/')
# async def music_home(language: str):
#         response = requests.get('https://saavn.me/modules?language={language}').json()
#         return response


# @app.post('/api/music/search_all/')
# async def search_all(data : str):
#       response = requests.get('https://saavn.me/search/all?query={data}').json()
#       return response


# @app.post('/api/music/search_song/')
# async def searchsong(query:str):
#       response = requests.get('https://saavn.me/search/songs?query={query}&page=1&limit=8').json()
#       return response

# @app.post('/api/music/search_album/')
# async def searchalbums(query:str):
#       response = requests.get('https://saavn.me/search/albums?query={query}').json()
#       return response


# @app.post('/api/music/search_playlist/')
# async def search_playlist(query:str):
#       response = requests.get('https://saavn.me/search/playlists?query={query}').json()
#       return response

# @app.post('/api/music/search_artist/')
# async def search_artists(query:str):
#       response = requests.get('https://saavn.me/search/artists?query={query}').json()
#       return response

# # Details






from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database connection configuration
db_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "testcrud",
}

# Model for the item
class Item(BaseModel):
    name: str
    description: str

class Itemget(BaseModel):
    id:str
    name: str
    description: str

# Connect to the database
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Create table if it doesn't exist
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT
    )
""")
db_connection.commit()

# CRUD operations
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    query = "INSERT INTO items (name, description) VALUES (%s, %s)"
    values = (item.name, item.description)
    db_cursor.execute(query, values)
    db_connection.commit()
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    query = "SELECT id, name, description FROM items WHERE id = %s"
    db_cursor.execute(query, (item_id,))
    item = db_cursor.fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "description": item[2]}

@app.get("/items/", response_model=list[Itemget])
async def read_items():
    query = "SELECT id, name, description FROM items"
    db_cursor.execute(query)
    items = [{"id": str(item[0]), "name": item[1], "description": item[2]} for item in db_cursor.fetchall()]
    return items

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    query = "UPDATE items SET name = %s, description = %s WHERE id = %s"
    values = (item.name, item.description, item_id)
    db_cursor.execute(query, values,)
    db_connection.commit()
    return {"id": item_id, **item.dict()}

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    query = "DELETE FROM items WHERE id = %s"
    db_cursor.execute(query, (item_id,))
    db_connection.commit()
    return {"message": "Item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

