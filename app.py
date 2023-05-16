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

    with open("DATA/json_files/movies.json") as file:
        data = json.load(file)

    # Create a DataFrame from the JSON data
    movies_df = pd.DataFrame(data)
    
    # Define the maximum number of entries to fetch
    max_entries = 200

    movie_data = []
    
    # Iterate over the limited number of rows in the DataFrame
    for _, row in movies_df.head(max_entries).iterrows():

        tmdb_id = row["tmdb_id"]
        imdb_id = row["imdb_id"]
        title = row["title"]
        original_title = row["original_title"]
        tagline = row["tagline"]
        overview = row["overview"]
        # "genre": [
        #     "Action",
        #     "Adventure",
        #     "Fantasy",
        #     "Science Fiction"
        # ],
        # "director": [],
        # "actors": [],
        release_year = str(row["release_year"])
        runtime = str(row["runtime"])
        language = row["language"]
        country = row["country"]
        poster_url = row["poster_url"]
        trailer_url = row["trailer_url"]
        revenue = str(row["revenue"])
        rating = str(row["rating"])
        popularity = str(row["popularity"])
        vote_average = str(row["vote_average"])
        vote_count = str(row["vote_count"])

        movie = {
            "tmdb_id": tmdb_id,
            "imdb_id": imdb_id,
            "title": title,
            "original_title": original_title,
            "tagline": tagline,
            "overview": overview,
            "release_year": release_year,
            "runtime": runtime,
            "language": language,
            "country": country,
            "poster_url": poster_url,
            "trailer_url": trailer_url,
            "revenue": revenue,
            "rating": rating,
            "popularity": popularity,
            "vote_average": vote_average,
            "vote_count": vote_count
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











