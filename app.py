import streamlit as st
import pickle
import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Load data
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = pickle.load(open('movies.pkl','rb'))

def fetch_poster(movie_id):
    """Fetch poster with error handling."""
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    data = response.json()
    
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Placeholder if poster is missing
        return "https://via.placeholder.com/500x750?text=No+Poster"

def actual(movie):
    movie_index = movies_list[movies_list['title']==movie].movie_id.values[0]
    movie_name = movie
    movie_poster = fetch_poster(movie_index)
    return movie_name, movie_poster

def recommend(movie):
    movie_index = movies_list[movies_list['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_indices:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Streamlit UI
movie_titles = movies_list['title'].values
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movie_titles,
)

if st.button("Recommend"):
    # names1, posters1 = actual(selected_movie_name)
    # st.text(names1)
    # st.image(posters1)
    st.header('Recommended Movies')

    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(names[idx])
        col.image(posters[idx])
