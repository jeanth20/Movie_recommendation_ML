import json
import pandas as pd
import imdb
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# pip install imdb-lib

# Constants for API endpoints
# IMDB_API_ENDPOINT = "https://api.imdb.com"
TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
OMDB_API_ENDPOINT = "http://www.omdbapi.com"

# API keys (replace with your own)
# IMDB_API_KEY = "YOUR_IMDB_API_KEY"
TMDB_API_KEY = "e6ef0fe5f8d01ee77a06cdb3985c2a23"
OMDB_API_KEY = "http://www.omdbapi.com/?i=tt3896198&apikey=b047d87a"
GOOGLE_API_KEY = "AIzaSyBRAT_uUYmiqGc4AvKQT0u3L39tHLnizFY"




# Give us a more control not to overload api or machine
# Function to check if a movie is already recorded
def is_movie_recorded(title, movie_records):
    for record in movie_records:
        if record["title"] == title:
            return True
    return False


# Function to limit the number of records processed
def limit_records(records, limit):
    return records[:limit]


# Function to search imdb for a movie's poster
def search_movie_poster(movie_title):
    ia = imdb.IMDb()
    movies = ia.search_movie(movie_title)
    if movies:
        movie = movies[0]
        movie_id = movie.movieID
        ia.update(movie)
        poster_url = movie.get('full-size cover url')
        if poster_url:
            return poster_url
        else:
            return None
    else:
        return None


# Function to search YouTube for a movie's trailer
def search_movie_trailer(movie_title):
    youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
    query = f'{movie_title} trailer'
    
    try:
        search_response = youtube.search().list(
            q=query,
            part='id',
            maxResults=1,
            type='video'
        ).execute()
        
        if 'items' in search_response:
            video_id = search_response['items'][0]['id']['videoId']
            trailer_url = f'https://www.youtube.com/watch?v={video_id}'
            return trailer_url
    except HttpError as e:
        print('An error occurred while searching for the trailer:', e)
    
    return None


# Function to get movie details from TMDb
def get_tmdb_movie_details(title):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title
    }
    response = requests.get(f"{TMDB_API_ENDPOINT}/search/movie", params=params)
    data = response.json()

    if "results" in data:
        movie = data["results"][0]
        
        # Retrieve the movie details
        movie_id = movie.get("id")
        movie_details_response = requests.get(f"{TMDB_API_ENDPOINT}/movie/{movie_id}", params=params)
        movie_details = movie_details_response.json()
        
        genres_data = movie_details.get("genres", [])
        genres = [genre["name"] for genre in genres_data]
        
        directors_data = movie_details.get("credits", {}).get("crew", [])
        directors = [person["name"] for person in directors_data if person.get("job") == "Director"]

        actors_data = movie_details.get("credits", {}).get("cast", [])
        actors = [actor["name"] for actor in actors_data[:5]]

        return {            
            "tmdb_id": movie.get("id", "Null"),
            "imdb_id": movie_details.get("imdb_id", "Null"),
            "title": movie.get("title", "Null"),
            "original_title": movie.get("original_title", "Null"),
            "tagline": movie_details.get("tagline", "Null"), 
            "overview": movie.get("overview", "Null"),
            "genre": genres,
            "director": directors,
            "actors": actors,
            "release_year": movie.get("release_date", "Null")[:4],
            "runtime": movie.get("runtime", "Null"),
            "language": movie.get("original_language", "Null"),
            "country": movie_details.get("production_countries", [{}])[0].get("name", "Null"),
            "poster_url": f"https://image.tmdb.org/t/p/original{movie.get('poster_path', '')}",
            "trailer_url": search_movie_trailer(title),
            "revenue": movie.get("revenue", "Null"),            
            "rating": movie.get("vote_average", "Null"),
            "popularity": movie.get("popularity", "Null"),
            "vote_average": movie.get("vote_average", "Null"),
            "vote_count": movie.get("vote_count", "Null"),
        }
    else:
        return None

# Test example
# tmdb = get_tmdb_movie_details("Avatar")
# formatted_movie_details = json.dumps(tmdb, indent=4)
# print(formatted_movie_details)

# json_file_path = "json_files/movies_list.json"

# with open(json_file_path, "r") as file:
#     data_str = file.read()
#     data = json.loads(data_str)
    
#     for item in data:
#         print(item)
#         tmdb = get_tmdb_movie_details(item)
#         formatted_movie_details = json.dumps(tmdb, indent=4)
#         print(formatted_movie_details)

#         # Specify the path to the output JSON file
#         output_file_path = "json_files/Jean_test_data.json"

#         # Write the movie_details to the JSON file
#         with open(output_file_path, "a") as file:
#             json.dump(formatted_movie_details, file, indent=4)
#             # file.write(",\n")
        

json_file_path = "json_files/movies_list.json"
output_file_path = "json_files/Jean_test_data.json"

with open(json_file_path, "r") as file:
    data_str = file.read()
    data = json.loads(data_str)

# Create an empty list to store the formatted movie details
formatted_movies = []

for item in data:
    print(item)
    tmdb = get_tmdb_movie_details(item)
    formatted_movie_details = json.dumps(tmdb, indent=4)
    formatted_movies.append(formatted_movie_details)

# Write the formatted movie details as a JSON array to the output file
with open(output_file_path, "w") as file:
    file.write("[\n")
    file.write(",\n".join(formatted_movies))
    file.write("\n]")
