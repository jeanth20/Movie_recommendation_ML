import csv
import json
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def csv_to_json(csv_file, json_file):
    movie_data = []

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_id = row["id"]
            movie_title = row["title"]
            movie_url = fetch_poster(movie_id)

            movie = {
                "image_id": movie_id,
                "image_url": movie_url,
                "title": movie_title
            }
            movie_data.append(movie)

    with open(json_file, "w") as file:
        json.dump(movie_data, file, indent=4)

def save_feedback(user_id, image_id, feedback):
    # Load user's JSON file
    with open(f"{user_id}.json", "r") as file:
        data = json.load(file)

    # Save feedback to JSON
    data[image_id] = feedback

    # Write updated data to JSON file
    with open(f"{user_id}.json", "w") as file:
        json.dump(data, file)

# Convert CSV to JSON
# csv_file = "../movies_ids.csv"
# json_file = "movies.json"
# csv_to_json(csv_file, json_file)

# Main Application
st.header("My taste in movies")
user_id = st.text_input("User ID")

# Load image data
with open(json_file, "r") as file:
    image_data = json.load(file)

# Create or load user's JSON file
try:
    with open(f"{user_id}.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

# Initialize current_index session state variable
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

try:
    # Get the current image and its details
    current_image = image_data[st.session_state.current_index]
    image_id = current_image["image_id"]
    image_url = current_image["image_url"]

    # Display image
    st.image(image_url)

    # Display buttons
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        if st.button(f"Like##{image_id}"):
            save_feedback(user_id, image_id, "like")
            st.session_state.current_index += 1

    with col2:
        if st.button(f"Dislike##{image_id}"):
            save_feedback(user_id, image_id, "dislike")
            st.session_state.current_index += 1

    with col3:
        if st.button(f"Skip##{image_id}"):
            save_feedback(user_id, image_id, "skip")
            st.session_state.current_index += 1

except IndexError:
    st.write("All movies have been voted on!")

# Save final data to JSON file
with open(f"{user_id}.json", "w") as file:
    json.dump(data, file, indent=4)
