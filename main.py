from fastapi import FastAPI, HTTPException
import requests


app = FastAPI(title="My Apis",
             description="Developer : Mirshad")

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"Languages":['Hindi', 'English', 'Punjabi', 'Tamil', 'Telugu', 'Marathi', 'Gujarati', 'Bengali', 'Kannada', 'Bhojpuri', 'Malayalam', 'Urdu', 'Haryanvi', 'Rajasthani', 'Odia', 'Assamese']}


@app.get('/api/music/music_home/{language}/')
async def music_home(language: str):
        response = requests.get('https://saavn.me/modules?language={language}').json()
        return response


@app.post('/api/music/search_all/')
async def search_all(data : str):
      response = requests.get('https://saavn.me/search/all?query={data}').json()
      return response


@app.post('/api/music/search_song/')
async def searchsong(query:str):
      response = requests.get('https://saavn.me/search/songs?query={query}&page=1&limit=8').json()
      return response

@app.post('/api/music/search_album/')
async def searchalbums(query:str):
      response = requests.get('https://saavn.me/search/albums?query={query}').json()
      return response


@app.post('/api/music/search_playlist/')
async def search_playlist(query:str):
      response = requests.get('https://saavn.me/search/playlists?query={query}').json()
      return response

@app.post('/api/music/search_artist/')
async def search_artists(query:str):
      response = requests.get('https://saavn.me/search/artists?query={query}').json()
      return response

# Details
