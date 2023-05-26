import pickle
import requests
import random
import difflib
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import picklerick as rick
# pip install python-Levenshtein



# data var to make loading simpler for all functions
data = pickle.load(open("movies_ids.pkl", 'rb'))

movies_ids_directory = rick.load_pickle("movies_ids.pkl")
movies_list = rick.load_pickle("movies_list.pkl")
similarity = rick.load_pickle("similarity.pkl")


rick.print_pickle("movies_ids.pkl")
rick.print_pickle("movies_list.pkl")
rick.print_pickle("similarity.pkl")






def difflib_search():
    # Search for similar matches
    search_term = 'The Shawshank Redemption'
    results = []

    # Iterate over the data to find matches
    for item in data:
        # similarity_ratio = fuzz.ratio(item.lower(), search_term.lower())
        similarity_ratio = difflib.SequenceMatcher(None, item, search_term).ratio()
        if similarity_ratio > 0.7:
            results.append(item)

    # Print the search results
    if results:
        print("Search Results:")
        for result in results:
            print(result)
    else:
        print("No matching results found.")
# difflib_search()

def fuzzy_search():
    # Search for similar matches using fuzzywuzzy
    search_term = 'example'
    results = []

    # Iterate over the data to find matches
    for item in data:
        similarity_ratio = fuzz.ratio(item, search_term)
        if similarity_ratio > 30:  # Adjust the threshold as needed
            results.append(item)

    # Print the search results
    if results:
        print("Search Results:")
        for result in results:
            print(result)
    else:
        print("No matching results found.")
# fuzzy_search()


def search_file(movie_id):
    try:
        movies_ids = data
        found = False
        
        for movie in movies_ids:
            if movie[0] == movie_id:
                print("id:", movie[0], "\t\ttitle:", movie[1])
                found = True
                break

        if not found:
            print("Movie ID not found.")
    except FileNotFoundError:
        print("Pickle file not found.")
    print("Completed searching.")

search_file("372754")

 
# # Search within the loaded data
# search_term = 'a'
# results = []

# # Iterate over the data to find matches
# for item in data:
#     if search_term in item:
#         results.append(item)

# # Print the search results
# if results:
#     print("Search Results:")
#     for result in results:
#         print(result)
# else:
#     print("No matching results found.")















# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# movies = pickle.load(open("movies_list.pkl", 'rb'))
# similarity = pickle.load(open("similarity.pkl", 'rb'))
# movies_list = movies['title'].values


# imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# movies_ids = pd.read_csv('movies_ids.csv')

# randMovies = []
# i = 0

# while i != 5:
#     movie_index = random.randint(0, len(movies_ids)-1)
#     movie_id = movies_ids.loc[movie_index, 'id']
#     movie_title = movies_ids.loc[movie_index, 'title']
#     poster_url = fetch_poster(movie_id)
#     randMovies.append((movie_id, movie_title, poster_url))
#     i += 1

# imageUrls = []

# for movie_id, movie_title, movie_poster in randMovies:
#     imageUrls.append(fetch_poster(movie_id))

# imageUrls = list(set(imageUrls))  # Remove duplicates (if any)


# import pandas as pd
# import random

# movies_ids = pd.read_csv('movies_ids.csv')

# randMovies = []
# i = 0

# while i != 5:
#     movie_index = random.randint(0, len(movies_ids)-1)
#     movie_id = movies_ids.loc[movie_index, 'id']
#     movie_title = movies_ids.loc[movie_index, 'title']
#     randMovies.append((movie_id, movie_title))
#     i += 1

# for movie_id, movie_title in randMovies:
#     print("Movie ID:", movie_id)
#     print("Movie Title:", movie_title)
#     print()






# # Adding data to pickle file .pkl
# def write_file():
  
#     f = open("travel.txt", "wb")
#     op = 'y'
  
#     while op == 'y':
  
#         Travelcode = int(input("enter the travel id"))
#         Place = input("Enter the Place")
#         Travellers = int(input("Enter the number of travellers"))
#         buses = int(input("Enter the number of buses"))
  
#         pickle.dump([Travelcode, Place, Travellers, buses], f)
#         op = input("Dp you want to continue> (y or n)")
  
#     f.close()
  
  
# print("entering the details of passengers in the pickle file")
# write_file()

# # Search the pkl file

# def search_file():
#     f = open("travel.txt", 'rb')
#     t_code = int(input("Enter the travel code to traveller : "))
      
#     while True:
#         try:
            
#             L = pickle.load(f)
              
#             if L[0] == t_code:
#                 print("Place", L[1], "\t\t Travellers :",
#                       L[2], "\t\t Buses :", L[3])
                  
#                 break
                  
#         except EOFError:
            
#             print("Completed reading details")
#     f.close()
  
  
# print("entering the details of passengers in the pickle file")
# write_file()
  
# print("Search the file using the passenger Code")
# search_file()