import os
import json
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
# from streamlit_card import card
import pickle
import requests
import random
import pandas as pd
import csv
import createPickle

st.set_page_config(
   page_title="MOOvie",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu, header, footer, .css-18ni7ap.e8zbici2 {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)




global movies
global similarity
global movies_list

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def random_movies_car():
    st.header("Random Recommendations")
    imageCarouselComponent = components.declare_component(
        "image-carousel-component", path="frontend/public")
    movies_ids = pd.read_csv('movies_ids.csv')
    randMovies = []
    i = 0
    while i != 5:
        movie_index = random.randint(0, len(movies_ids)-1)
        movie_id = movies_ids.loc[movie_index, 'id']
        movie_title = movies_ids.loc[movie_index, 'title']
        poster_url = fetch_poster(movie_id)
        randMovies.append((movie_id, movie_title, poster_url))
        i += 1
    imageUrls = []
    for movie_id, movie_title, movie_poster in randMovies:
        imageUrls.append(fetch_poster(movie_id))
    imageUrls = list(set(imageUrls))
    imageCarouselComponent(imageUrls=imageUrls, height=200)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:11]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster


def movie_profile(movie):
    print(movie)
    if movie in movies['title'].values:
        index = movies[movies['title'] == movie].index[0]
        movie_id = movies.iloc[index].id
        movie_title = movies.iloc[index].title
        movie_tags = movies.iloc[index].tags

        movie_details = {
            'id': movie_id,
            'title': movie_title,
            'tags': movie_tags,
        }
        return movie_details
    else:
        return None


def movie_profile_csv(movie):
    with open('dataset.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['title'] == movie:
                movie_id = row['id']
                movie_title = row['title']
                movie_genre = row['genre']
                movie_original_language = row['original_language']
                movie_overview = row['overview']
                movie_popularity = row['popularity']
                movie_release_date = row['release_date']
                movie_vote_average = row['vote_average']
                movie_vote_count = row['vote_count']

                movie_details = {
                    'id': movie_id,
                    'title': movie_title,
                    'genre': movie_genre,
                    'original_language': movie_original_language,
                    'overview': movie_overview,
                    'popularity': movie_popularity,
                    'release_date': movie_release_date,
                    'vote_average': movie_vote_average,
                    'vote_count': movie_vote_count,
                }
                return movie_details
    return None


def user_preference_json(json_file):
    movie_data = []

    with open("movies_ids.csv", "r") as file:
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


def save_feedback(user_id, movie_id, title, poster, feedback):
    json_file = f"{user_id}.json"

    if not os.path.exists(json_file):
        with open(json_file, "w") as file:
            file.write("[]")

    with open(json_file, "r") as file:
        file_content = file.read()

    if len(file_content.strip()) == 0:
        data = []
    else:
        data = json.loads(file_content)

    entry = {
        "title": title,
        "id": movie_id,
        "poster": poster,
        "vote": feedback
    }

    data.append(entry)

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


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


def csv_to_json_format(csv_file, json_file):
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
        json.dump(movie_data, file, indent=4, ensure_ascii=False)


with st.sidebar:
    user_id = st.text_input("User ID", "Jean")
    # selected = option_menu(
    #     menu_title=None,
    #     options=["Home", "Similar", "My Picks", "Bio"],
    #     icons=["house", "book", "film", "receipt-cutoff"],
    #     menu_icon="cast",
    #     default_index=0,
    # )
    
selected = option_menu(
    menu_title=None,
    options=["Home", "Similar", "My Picks", "Bio"],
    icons=["house", "book", "film", "receipt-cutoff"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    # st.title(f"You are on the {selected}page")
    random_movies_car()

if selected == "Similar":
    # st.title(f"You are on the {selected} page")

    st.header("Recommend Similar")
    selectvalue = st.selectbox("Select movie from dropdown", movies_list)

    if st.button("Show Recommend"):
        movie_name, movie_poster = recommend(selectvalue)
        col1, col2, col3, col4, col5 = st.columns(5)
        col6, col7, col8, col9, col10 = st.columns(5)

        with col1:
            st.text(movie_name[0])
            st.image(movie_poster[0])
        with col2:
            st.text(movie_name[1])
            st.image(movie_poster[1])
        with col3:
            st.text(movie_name[2])
            st.image(movie_poster[2])
        with col4:
            st.text(movie_name[3])
            st.image(movie_poster[3])
        with col5:
            st.text(movie_name[4])
            st.image(movie_poster[4])
        with col6:
            st.text(movie_name[5])
            st.image(movie_poster[5])
        with col7:
            st.text(movie_name[6])
            st.image(movie_poster[6])
        with col8:
            st.text(movie_name[7])
            st.image(movie_poster[7])
        with col9:
            st.text(movie_name[8])
            st.image(movie_poster[8])
        with col10:
            st.text(movie_name[9])
            st.image(movie_poster[9])

if selected == "My Picks":
    st.header("My top picks")
    
    json_file = 'data_handling/moo.json'

    with open(json_file, "r") as file:
        image_data = json.load(file)

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    try:
        current_image = image_data[st.session_state.current_index]
        movie_id = current_image["id"]
        image_url = current_image["image_url"]
        title = current_image["title"]
        poster = image_url
        
        # Display image
        imgl, imgr = st.columns(2)

        with imgl:
            st.image(image_url, width=250)

        with imgr:
            st.subheader(title)
            if st.button(f"Like {movie_id}"):
                save_feedback(user_id, movie_id, title, poster, "like")
                st.session_state.current_index += 1

            if st.button(f"Skip {movie_id}"):
                save_feedback(user_id, movie_id, title, poster, "skip")
                st.session_state.current_index += 1

            if st.button(f"Dislike {movie_id}"):
                save_feedback(user_id, movie_id, title, poster, "dislike")
                st.session_state.current_index += 1

    except IndexError:
        st.write("All movies have been voted on!")
        
        liked, novote, disliked = st.columns(3)
        
        with open(json_file, "r") as file:
            vote_data = json.load(file)
        
        # with liked:
        #     for data in vote_data:
        #         if 'vote' in data and data['vote'] == 'like':
        #             st.write(data["title"])
        #             st.image(data["poster"])
            # for liked_movie in vote_data:
            #     if "like" in vote_data["vote"]:
            #     # Your code logic here
            #         st.image(vote_data["poster"])

            #     # if vote_data["vote"] in vote_data == "like":
            #     #     st.image(vote_data["poster"])








if selected == "Bio":
    # st.title(f"You are on the {selected} info page")
    st.header("Movie Bio")
    selectvalue = st.selectbox("Select movie from dropdown", movies_list)
    details = movie_profile_csv(selectvalue)
    if details is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(fetch_poster(details['id']))
        with col2:
            st.title(details['title'])
            st.caption(details['release_date'])
            st.write(details['overview'])
            # st.write(details['popularity'], "\t\t", details['vote_average'], "\t\t", details['vote_count'])
            st.caption(details['genre'])
    else:
        st.text("Movie details not found.")



    # hasClicked = card(
    # key="card1",
    # title="Hello World!",
    # text="This is a card",
    # url="https://github.com/gamcoh/st-card",
    # image="http://placekitten.com/200/300"
    # )

    # hasClicked2 = card(
    # key="card2",
    # title="Hello World!",
    # text="This is a card",
    # url="https://github.com/gamcoh/st-card",
    # image="http://placekitten.com/200/300"
    # )

    # html_string = '''
    # <h1></h1>

    # <script language="javascript">

    #     document.querySelector("h1").style.color = "red";
    #     alert("Streamlit runs JavaScript");

    # </script>
    # '''

    # components.html(html_string)  # JavaScript works

    # st.markdown(html_string, unsafe_allow_html=True)

    # With this you can add a html page
    # Read the contents of your HTML file
    # with open('static/index.html', 'r') as file:
    #     html_code = file.read()

    # with open('static/style.css', 'r') as file:
    #     css_code = file.read()

    # with open('static/script.js', 'r') as file:
    #     js_code = file.read()

    # Embed the HTML code in Streamlit using st.markdown or st.components.v1.html
    # st.markdown(html_code, unsafe_allow_html=True)
    # st.markdown(css_code, unsafe_allow_html=True)
    # st.markdown(js_code, unsafe_allow_html=True)

    # import streamlit.components.v1 as components

    # components.html(html_code)
    # # components.html(css_code)
    # components.html(js_code)

    # print(df[df['Name']=='Donna'].index.values)
