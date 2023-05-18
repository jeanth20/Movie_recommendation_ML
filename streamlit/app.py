import streamlit as st
import pickle
import requests

st.markdown("""
<style>
    #MainMenu, .header, .css-18ni7ap.e8zbici2 {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

from streamlit_option_menu import option_menu

# with st.sidebar:
selected = option_menu(
    menu_title=None,
    options=["Home", "Similar"],
    icons=["house", "book"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    st.title(f"You are on the {selected}")
    
    # Read the contents of your HTML file
    with open('static/index.html', 'r') as file:
        html_code = file.read()
        
    with open('static/style.css', 'r') as file:
        css_code = file.read()

    with open('static/script.js', 'r') as file:
        js_code = file.read()
        
    # Embed the HTML code in Streamlit using st.markdown or st.components.v1.html
    # st.markdown(html_code, unsafe_allow_html=True)
    # st.markdown(css_code, unsafe_allow_html=True)
    # st.markdown(js_code, unsafe_allow_html=True)
    
    # import streamlit.components.v1 as components

    # components.html(html_code)
    # # components.html(css_code)
    # components.html(js_code)
    
    import streamlit as st
    import streamlit.components.v1 as components

    html_string = '''
    <h1>HTML string in RED</h1>

    <script language="javascript">
    document.querySelector("h1").style.color = "red";
    console.log("Streamlit runs JavaScript");
    alert("Streamlit runs JavaScript");
    </script>
    '''

    components.html(html_string)  # JavaScript works

    st.markdown(html_string, unsafe_allow_html=True)    
    
    
    
    

if selected == "Similar":
    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
        data=requests.get(url)
        data=data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
        return full_path

    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list=movies['title'].values

    st.header("Movie Recommender System")

    import streamlit.components.v1 as components

    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


    # import random
    # random_number1 = random.randint(10, 1000)
    # random_number2 = random.randint(1000, 10000)
    # random_number3 = random.randint(10000, 20000)
    # random_number4 = random.randint(20000, 30000)
    # random_number5 = random.randint(40000, 50000)
    
    # print(random_number1)
    # print(random_number2)
    # print(random_number3)
    # print(random_number4)
    # print(random_number5)
        
    # imageUrls = [
    #     fetch_poster(int(random_number1)),
    #     fetch_poster(int(random_number2)),
    #     fetch_poster(int(random_number3)),
    #     fetch_poster(int(random_number4)),
    #     fetch_poster(int(random_number5)),
    # ]

    # num_of_random_numbers = 5
    # random_numbers = []
    # imageUrls = []

    # for _ in range(num_of_random_numbers):
    #     random_number = random.randint(10, 572154)
    #     random_numbers.append(random_number)
    #     print(random_number)

    #     # Accessing each value individually
    #     image_url = "fetch_poster(int({random_number}))"  # Using string formatting
    #     # image_url = "fetch_poster(" + str(random_number) + ")"  # Using concatenation
    #     imageUrls.append(image_url)

        

    imageUrls = [
        # fetch_poster(1632),
        fetch_poster(299536),
        fetch_poster(17455),
        fetch_poster(2830),
        fetch_poster(429422),
        # fetch_poster(9722),
        fetch_poster(13972),
        # fetch_poster(240),
        # fetch_poster(155),
        # fetch_poster(598),
        # fetch_poster(914),
        # fetch_poster(255709),
        # fetch_poster(572154)
    
        ]


    imageCarouselComponent(imageUrls=imageUrls, height=200)
    selectvalue=st.selectbox("Select movie from dropdown", movies_list)

    def recommend(movie):
        index=movies[movies['title']==movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
        recommend_movie=[]
        recommend_poster=[]
        for i in distance[1:11]:
            movies_id=movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movies_id))
        return recommend_movie, recommend_poster



    if st.button("Show Recommend"):
        movie_name, movie_poster = recommend(selectvalue)
        col1,col2,col3,col4,col5=st.columns(5)
        col6,col7,col8,col9,col10=st.columns(5)
        
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
