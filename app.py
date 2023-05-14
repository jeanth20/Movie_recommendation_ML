from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import uvicorn
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates 

# Creating FastAPI instance
app = FastAPI(title="Movie API", openapi_url="/openapi.json")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating class to define the request body
# and the type hints of each attribute
class request_body(BaseModel):
    sepal_length : float
    sepal_width : float
    petal_length : float
    petal_width : float
 

@app.get("/")
async def login(request: Request)->HTMLResponse:
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context=context)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import json
from typing import Optional
import imdb
import requests

def search_movie_poster(movie_title):
    # Create an instance of the IMDb class
    ia = imdb.IMDb()

    # Search for the movie by title
    movies = ia.search_movie(movie_title)

    if movies:
        # Retrieve the first movie from the search results
        movie = movies[0]

        # Get the IMDb ID of the movie
        movie_id = movie.movieID

        # Fetch additional details for the movie
        ia.update(movie)

        # Retrieve the IMDb poster URL for the movie
        poster_url = movie.get('full-size cover url')

        if poster_url:
            return poster_url
        else:
            return None
    else:
        return None




@app.get("/get_movie_data")
async def get_movies()->JSONResponse:
    # credits_df = pd.read_csv("DATA/credits.csv")
    # movies_df = pd.read_csv("DATA/movies.csv")

    with open("DATA/movies.json") as file:
        data = json.load(file)

    # Create a DataFrame from the JSON data
    movies_df = pd.DataFrame(data)
    
    # Define the maximum number of entries to fetch
    max_entries = 200

    movie_data = []
    
    # Iterate over the limited number of rows in the DataFrame
    for _, row in movies_df.head(max_entries).iterrows():
        # mtitle = row['title']
        # poster_url = search_movie_poster(mtitle)
        
        # if poster_url:
        #     print("Poster URL:", poster_url)
        #     # Use the poster URL for further processing
        # else:
        #     print("No poster found for the movie:", mtitle)

        image_src = row['imageSrc']
        id = row['id']
        title = row['title']
        runtime = row['runtime']
        genre = 'Genre'
        vote_count = row['vote_count']
        ranking = row["ranking"]
        rating = str(row['rating'])

        movie = {
            'imageSrc': image_src,
            'id': id,
            'title': title,
            'runtime': runtime,
            'genre': genre,
            'vote_count': vote_count,
            'ranking': ranking,
            'rating': rating
        }
        
        movie_data.append(movie)

    return JSONResponse(content=movie_data)


from pydantic import BaseModel

class SwipeAction(BaseModel):
    id: int
    username: str
    swipeDirection: str

# use this for a users swipe to rank a movie by id 
@app.post("/counter/")
def handle_swipe_action(swipe_action: SwipeAction):
    swipe_action_dict = swipe_action.dict()
    with open("DATA/ratings_test.json", "a") as outfile:
        json.dump(swipe_action_dict, outfile, indent=2)
        outfile.write(",\n")

    # print("Received swipe action:", swipe_action)
    return {"message": "Swipe action received"}
    # if item_id not in counters:
    #     counters[item_id] = {}
    
    # # Check if the username exists for the item ID
    # if username not in counters[item_id]:
    #     counters[item_id][username] = 0
    
    # # Increment or decrement the counter based on the 'increment' parameter
    # if increment:
    #     counters[item_id][username] += 1
    # else:
    #     counters[item_id][username] -= 1
    
    # return {"item_id": item_id, "username": username, "counter": counters[item_id][username]}











