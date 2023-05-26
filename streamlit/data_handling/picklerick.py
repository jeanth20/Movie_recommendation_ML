import pickle
import requests
import random
import difflib
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
# pip install python-Levenshtein


def load_pickle(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
            return content
    except FileNotFoundError:
        print("Pickle file not found.")


def unpickle(file_path, return_value=False):
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
            if isinstance(content, pd.DataFrame):
                if return_value == True:
                    print(content.values)
                    return content.values
                print(content.columns)
                return content.columns
            else:
                print("Unpickled object is not a DataFrame.")
                return None

    except FileNotFoundError:
        print("Pickle file not found.")
        return None
# unpickle("movies_list.pkl", )

def unpickle_filter2(file_path, filter_data=False):
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
            if filter_data:
                return content[["id", "title"]].values.tolist()
            else:
                return content
    except FileNotFoundError:
        print("Pickle file not found.")

def unpickle_filter(file_path, filter_columns=None):
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
            if filter_columns:
                filtered_content = content[filter_columns]
                return filtered_content.values.tolist()
            else:
                return content
    except FileNotFoundError:
        print("Pickle file not found.")


# search movie by title
# only works with exact match
def unpickle_search_title(file_path, search_title):
    data = unpickle_filter(file_path, True)
    for item in data:
        title_id = item[0]
        title = item[1]
        if title == search_title:
            print(title_id, title)
            break
    else:
        # print("Title not found.")
        return("Title not found.")
unpickle_search_title("movies_ids.pkl", "The Godfather")

# search movie by id
# only works with exact match
def unpickle_search_id(file_path, search_id):
    data = unpickle(file_path, True)
    for item in data:
        title_id = item[0]
        title = item[1]
        if title_id == search_id:
            print(title_id, title)
            break
    else:
        # print("Title not found.")
        return("Title not found.")
# unpickle_search_id("movies_ids.pkl", 238)

def unpickle_search_all(file_path, search_title):
    data = unpickle("movies_ids.pkl", filter_columns=["id", "title", "tags"])
    # data = unpickle_filter(file_path, True)
    for item in data:
        id = item[0]
        title = item[1]
        tags = item[2]

        if title == search_title:
            print(id, title, tags)
            break
    else:
        # print("Title not found.")
        return("Title not found.")
unpickle_search_all("movies_list.pkl", "The Godfather")


# ?? not working
# def difflib_search(file_path, search_term):
#     data = load_pickle(file_path)
#     threshold = 0.7
#     results = []
#     for item in data:
#         similarity_ratio = difflib.SequenceMatcher(None, item, search_term).ratio()
#         if similarity_ratio > threshold:
#             results.append(item)
#     if results:
#         print("Search Results:")
#         for result in results:
#             print(result)
#     else:
#         print("No matching results found.")
# difflib_search("movies_ids.pkl", "the shawshank redemption")

# def fuzzy_search(file_path, search_term):
#     data = load_pickle(file_path)
#     threshold = 30
#     results = []
#     for item in data:
#         similarity_ratio = fuzz.ratio(item, search_term)
#         if similarity_ratio > threshold:
#             results.append(item)

#     if results:
#         print("Search Results:")
#         for result in results:
#             print(result)
#     else:
#         print("No matching results found.")
# fuzzy_search("movies_ids.pkl", "the shawshank redemption")





