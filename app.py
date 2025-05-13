import streamlit as st
import pandas as pd
import requests
import pickle

# Load the movie data and cosine similarity matrix
with open('movie_data.pkl', "rb") as file:
    movies, cosine_sim = pickle.load(file)

# Function to get recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies["title"] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get the scores of the 10 most similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices]

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = "f4f2a8053cd54d38429a968a3b49ecfe"  # Replace with your API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    else:
        return ""

# Streamlit App UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies["title"].values)

if st.button("Show Recommendations"):
    recommendations = get_recommendations(selected_movie)

    st.write("### Top 10 Recommended Movies:")
    
    for i in range(0, 10, 5):  # 2 columns per row
        cols = st.columns(5)
        for j in range(5):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]["title"]
                movie_id = recommendations.iloc[j]["movie_id"]
                poster_url = fetch_poster(movie_id)
                with cols[j]:
                    st.image(poster_url, width=130)
                    st.write(movie_title)
                    
                

