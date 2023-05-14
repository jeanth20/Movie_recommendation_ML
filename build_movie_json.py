import json
import pandas as pd
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


movies_df = pd.read_csv("DATA/movies.csv")

# Define the maximum number of entries to fetch
max_entries = 100

movie_data = []

# Iterate over the limited number of rows in the DataFrame
for _, row in movies_df.head(max_entries).iterrows():
    movie_title = row['title']
    poster_url = search_movie_poster(movie_title)
    
    if poster_url:
        print("Poster URL:", poster_url)
        # Use the poster URL for further processing
    else:
        print("No poster found for the movie:", movie_title)

    image_src = poster_url
    id = row['id']
    title = movie_title
    runtime = row['runtime']
    genre = 'Genre'
    vote_count = row['vote_count']
    ranking = row["popularity"]
    rating = str(row['vote_average'])

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

# Save the movie data to a JSON file with indentation and new lines
with open("movies.json", "a") as outfile:
    json.dump(movie_data, outfile, indent=2)
    outfile.write("\n")
    
