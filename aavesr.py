import os
import spotipy
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist

def initialize_spotify_api():
    credentials = SpotifyClientCredentials("bb2c5bfa0b484f2e8b51aec60e9e70c3","76bbc095bec74377a164bedd2d8fbfbc")
    return spotipy.Spotify(auth_manager=credentials)

def retrieve_song_details(track_name, track_year):
    sp_instance = initialize_spotify_api()
    song_attributes = defaultdict()
    search_query = f'track: {track_name} year: {track_year}'
    query_result = sp_instance.search(q=search_query, limit=1)['tracks']['items']
    
    if not query_result:
        return None
    
    track_details = query_result[0]
    track_id = track_details['id']
    audio_attrs = sp_instance.audio_features(track_id)[0]
    
    song_attributes.update({
        'name': [track_name],
        'year': [track_year],
        'explicit': [int(track_details['explicit'])],
        'duration_ms': [track_details['duration_ms']],
        'popularity': [track_details['popularity']]
    })

    song_attributes.update(audio_attrs)
    
    return pd.DataFrame(song_attributes)

def extract_song_vector(target_song, song_data_frame):
    try:
        return song_data_frame[(song_data_frame['name'] == target_song['name']) 
                                & (song_data_frame['year'] == target_song['year'])].iloc[0]
    except IndexError:
        return retrieve_song_details(target_song['name'], target_song['year'])

def calc_mean_vector(songs, data_frame):
    vectors = []
    for song in songs:
        song_vector = extract_song_vector(song, data_frame)
        if song_vector is None:
            print(f'Warning: {song["name"]} is not available in Spotify or database')
            continue
        vectors.append(song_vector[number_attributes].values)
        
    matrix = np.array(vectors)
    return np.mean(matrix, axis=0)

def normalize_dict_entries(dict_entries):
    flat_dict = defaultdict(list)
    
    for entry in dict_entries:
        for k, v in entry.items():
            flat_dict[k].append(v)
            
    return flat_dict

number_attributes = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 
                     'energy', 'explicit', 'instrumentalness', 'key', 'liveness', 
                     'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

def offer_song_recommendations(input_songs, song_data, recommended_count=10):
    song_attributes = normalize_dict_entries(input_songs)
    center_vector = calc_mean_vector(input_songs, song_data)
    
    pipeline_scaler = song_cluster_pipeline.steps[0][1]
    scaled_database = pipeline_scaler.transform(song_data[number_attributes])
    scaled_center_vector = pipeline_scaler.transform(center_vector.reshape(1, -1))
    
    dists = cdist(scaled_center_vector, scaled_database, 'cosine')
    closest_indices = np.argsort(dists)[:, :recommended_count][0]
    
    suggestions = song_data.iloc[closest_indices]
    filtered_suggestions = suggestions[~suggestions['name'].isin(song_attributes['name'])]
    
    return filtered_suggestions[['name', 'year', 'artists']].to_dict(orient='records')

# Usage
data = pd.read_csv("dataset.csv")
offer_song_recommendations([
    {'name': 'Come As You Are', 'year': 1991},
    {'name': 'Smells Like Teen Spirit', 'year': 1991},
    {'name': 'Lithium', 'year': 1992},
    {'name': 'All Apologies', 'year': 1993},
    {'name': 'Stay Away', 'year': 1993}], data)
