# AAVE Song assistant - Recommender Engine

## Description

This Python-based project uses the Spotipy library to interface with Spotify's API and recommend songs based on user preferences. Users can select specific song attributes such as danceability, valence, etc., for tailored recommendations. The recommendation engine employs various metrics to find songs that closely match the user's taste.

## Features

- **Fetch Song Details**: Retrieve detailed attributes of songs from Spotify.
- **User-Selectable Attributes**: Allows the user to choose from available song attributes for recommendations.
- **Dynamic Attribute Handling**: The program adapts to various datasets with different attributes.
- **Personalized Recommendations**: Offers a tailored list of songs you might enjoy.

## Usage

### Running the Program

1. Run the program using `python3 main.py`.
2. You'll be prompted to enter the path to your dataset.
3. The program will display available attributes in the dataset. Choose an attribute for recommendations.
4. A random song example with the chosen attribute will be displayed for context.
5. You'll be prompted to enter how many songs you'd like to get recommendations for.
6. For each song, enter the name and the value for the chosen attribute.

Example:

```bash
python3 main.py
Enter the path to your dataset: dataset.csv
Available attributes in the dataset: ['name', 'artists', 'danceability', ...]
Select an attribute for recommendations: danceability
Random example - Song: XYZ, danceability: 0.8
How many songs do you want to enter? 2
Enter the song name: Song1
Enter the value for danceability: 0.7
```
