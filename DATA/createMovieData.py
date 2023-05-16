import requests
import json
import imdb
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# pip install tmdb-python
# pip install IMDb

# Constants for API endpoints
# IMDB_API_ENDPOINT = "https://api.imdb.com"
TMDB_API_ENDPOINT = "https://api.themoviedb.org/3"
OMDB_API_ENDPOINT = "http://www.omdbapi.com"

# API keys (replace with your own)
# IMDB_API_KEY = "YOUR_IMDB_API_KEY"
TMDB_API_KEY = "e6ef0fe5f8d01ee77a06cdb3985c2a23"
OMDB_API_KEY = "http://www.omdbapi.com/?i=tt3896198&apikey=b047d87a"


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
def search_movie_trailer(title, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    query = f'{title} trailer'
    
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


# Function to check if a movie is already recorded
def is_movie_recorded(title, movie_records):
    for record in movie_records:
        if record["title"] == title:
            return True
    return False


# Function to limit the number of records processed
def limit_records(records, limit):
    return records[:limit]


# Function to get movie details from IMDb
def get_imdb_movie_details(title):
    # params = {
    #     "apiKey": IMDB_API_KEY,
    #     "q": title
    # }
    # response = requests.get(f"{IMDB_API_ENDPOINT}/movie", params=params)
    # data = response.json()
    # if "results" in data:
    #     movie = data["results"][0]
    #     return {
    #         "title": movie.get("title", "NaN"),
    #         "release_year": movie.get("release_year", "NaN"),
    #         "genre": movie.get("genres", []),
    #         "director": movie.get("directors", ["NaN"]),
    #         "actors": movie.get("actors", ["NaN"]),
    #         "plot": movie.get("plot", "NaN"),
    #         "rating": movie.get("rating", "NaN"),
    #         "duration_minutes": movie.get("duration", "NaN"),
    #         "language": movie.get("language", "NaN"),
    #         "country": movie.get("country", "NaN"),
    #         "poster_url": movie.get("poster_url", "NaN"),
    #         "trailer_url": movie.get("trailer_url", "NaN")
    #     }
    # else:
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
        return {
            "title": movie.get("title", "NaN"),
            "release_year": movie.get("release_date", "NaN")[:4],
            "genre": [genre["name"] for genre in movie.get("genres", [])],
            "director": "NaN",
            "actors": "NaN",
            "plot": movie.get("overview", "NaN"),
            "rating": movie.get("vote_average", "NaN"),
            "duration_minutes": movie.get("runtime", "NaN"),
            "language": movie.get("original_language", "NaN"),
            "country": "NaN",
            "poster_url": f"https://image.tmdb.org/t/p/original{movie.get('poster_path', '')}",
            "trailer_url": "NaN"
        }
    else:
        return None


# Function to get movie details from OMDb
def get_omdb_movie_details(title):
    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }
    
    movie_title = title
    poster_url = search_movie_poster(movie_title)
    
    response = requests.get(OMDB_API_ENDPOINT, params=params)
    data = response.json()
    if "Response" in data and data["Response"] == "True":
        return {
            "title": data.get("Title", "NaN"),
            "release_year": data.get("Year", "NaN"),
            "genre": data.get("Genre", "").split(", "),
            "director": data.get("Director", "NaN"),
            "actors": data.get("Actors", "NaN").split(", "),
            "plot": data.get("Plot", "NaN"),
            "rating": data.get("imdbRating", "NaN"),
            "duration_minutes": data.get("Runtime", "NaN").split(" ")[0],
            "language": data.get("Language", "NaN"),
            "country": data.get("Country", "NaN"),
            "poster_url": poster_url,
            "trailer_url": "NaN"
        }
    else:
        return None


# Main function to scrape movie databases and create JSON objects
def scrape_movies(movie_titles, movie_records, limit=None):
    scraped_movies = []

    for title in movie_titles:
        if limit is not None and len(scraped_movies) >= limit:
            break

        if is_movie_recorded(title, movie_records):
            continue

        movie_details = {
            "title": title,
            "release_year": None,
            "genre": [],
            "director": None,
            "actors": [],
            "plot": None,
            "rating": None,
            "duration_minutes": None,
            "language": None,
            "country": None,
            "poster_url": None,
            "trailer_url": None
        }

        # Scrape movie details from different sources in the preferred order
        imdb_details = get_imdb_movie_details(title)
        if imdb_details is not None:
            movie_details["release_year"] = imdb_details["release_year"]
            movie_details["genre"] = imdb_details["genre"]
            movie_details["director"] = imdb_details["director"]
            movie_details["actors"] = imdb_details["actors"]

        tmdb_details = get_tmdb_movie_details(title)
        if tmdb_details is not None:
            movie_details["release_year"] = tmdb_details["release_year"]
            movie_details["genre"] = tmdb_details["genre"]
            movie_details["director"] = tmdb_details["director"]
            movie_details["actors"] = tmdb_details["actors"]

        omdb_details = get_omdb_movie_details(title)
        if omdb_details is not None:
            movie_details["release_year"] = omdb_details["release_year"]
            movie_details["genre"] = omdb_details["genre"]
            movie_details["director"] = omdb_details["director"]
            movie_details["actors"] = omdb_details["actors"]
            movie_details["plot"] = omdb_details["plot"]
            movie_details["rating"] = omdb_details["rating"]
            movie_details["duration_minutes"] = omdb_details["duration_minutes"]
            movie_details["language"] = omdb_details["language"]
            movie_details["country"] = omdb_details["country"]
            movie_details["poster_url"] = omdb_details["poster_url"]
            movie_details["trailer_url"] = omdb_details["trailer_url"]

        scraped_movies.append(movie_details)

    return scraped_movies

# Example usage
movie_titles = ["Avatar", "Pirates of the Caribbean: At World's End", "Spectre", "The Dark Knight Rises", "John Carter", "Spider-Man 3", "Tangled", "Avengers: Age of Ultron", "Harry Potter and the Half-Blood Prince", "Batman v Superman: Dawn of Justice", "Superman Returns"]
movie_records = []  # Existing movie records

scraped_movies = scrape_movies(movie_titles, movie_records, limit=1)

# Save scraped movies to a JSON file
with open("scraped_movies.json", "a") as outfile:
    json.dump(scraped_movies, outfile, indent=2)
    outfile.write(",\n")





    


