import os
import spotipy
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from scipy.spatial.distance import cdist
import random

# Initialize Spotify API
def initialize_spotify_api():
    credentials = SpotifyClientCredentials("client_id", "client_secret")
    return spotipy.Spotify(auth_manager=credentials)

# Fetch song details from Spotify
def retrieve_song_details(track_name, track_attribute, attribute_value):
    sp_instance = initialize_spotify_api()
    song_attributes = defaultdict()
    search_query = f'track: {track_name} {track_attribute}: {attribute_value}'
    query_result = sp_instance.search(q=search_query, limit=1)['tracks']['items']

    if not query_result:
        return None
    
    track_details = query_result[0]
    track_id = track_details['id']
    audio_attrs = sp_instance.audio_features(track_id)[0]
    
    song_attributes.update(audio_attrs)
    song_attributes['name'] = track_name
    song_attributes[track_attribute] = attribute_value
    
    return song_attributes

# Calculate mean vector based on input songs
def calc_mean_vector(songs, data_frame, attributes):
    vectors = []
    for song in songs:
        song_vector = data_frame[(data_frame['name'] == song['name']) 
                                  & (data_frame[attributes] == song[attributes])].iloc[0]
        if song_vector.empty:
            print(f'Warning: {song["name"]} is not available in the dataset')
            continue
        vectors.append(song_vector[attributes].values)
        
    matrix = np.array(vectors)
    return np.mean(matrix, axis=0)

# Offer song recommendations based on mean vector
def offer_song_recommendations(input_songs, data, attributes, recommended_count=10):
    center_vector = calc_mean_vector(input_songs, data, attributes)
    dists = cdist([center_vector], data[attributes], 'cosine')
    closest_indices = np.argsort(dists)[:, :recommended_count][0]
    
    suggestions = data.iloc[closest_indices]
    return suggestions[['name', 'artists', attributes]].to_dict(orient='records')

if __name__ == "__main__":
    # User inputs dataset path
    dataset_path = input("Enter the path to your dataset: ")
    data = pd.read_csv(dataset_path)

    # Show available attributes and ask user to select one
    available_attributes = list(data.columns)
    print("Available attributes in the dataset:", available_attributes)
    selected_attribute = input("Select an attribute for recommendations: ")
    
    # Show a random example for the selected attribute
    random_example = data.sample(1)
    print(f"Random example - Song: {random_example['name'].values[0]}, {selected_attribute}: {random_example[selected_attribute].values[0]}")
    
    # User inputs songs
    input_song_count = int(input("How many songs do you want to enter? "))
    input_songs = []
    for _ in range(input_song_count):
        song_name = input("Enter the song name: ")
        attribute_value = input(f"Enter the value for {selected_attribute}: ")
        input_songs.append({'name': song_name, selected_attribute: attribute_value})

    # Get and print song recommendations
    recommendations = offer_song_recommendations(input_songs, data, selected_attribute)
    print("Recommended songs:", recommendations)
