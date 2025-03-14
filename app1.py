import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def hybrid_recommendation(movie, user_id, num_recommendations=10):
    recommended_movie_posters=[]
    # Content-Based Recommendations
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    content_based_recommendations = [movies.iloc[i[0]].title for i in distances[1:9]]

    # Collaborative Filtering Recommendations
    user_idx = user_id - 1
    user_ratings = user_item_sparse[user_idx]
    recommended_movie_indices, _ = model.recommend(user_idx, user_ratings, N=num_recommendations,
                                                   filter_already_liked_items=True)
    collaborative_recommendations = movies[movies['movie_id'].isin(recommended_movie_indices)]['title'].tolist()

    # Combine both recommendations (remove duplicates)
    combined_recommendations = list(set(content_based_recommendations + collaborative_recommendations))
    for i in distances[1:8]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))

    return combined_recommendations[:num_recommendations],recommended_movie_posters


# Example usage


st.header('Movie Recommender System')
movie_dict = pickle.load(open('movie_dict1.pkl','rb'))
user_item_sparse = pickle.load(open('user_item_sparse.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
user_ids = pickle.load(open('user_ids.pkl','rb'))
movies=pd.DataFrame(movie_dict)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
user_id = st.selectbox(
    "Select User Id",
    user_ids
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = hybrid_recommendation(selected_movie,user_id)
    col1, col2, col3, col4, col5,col6,col7 = st.columns(7)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    with col6:
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
    with col7:
        st.text(recommended_movie_names[6])
        st.image(recommended_movie_posters[6])





