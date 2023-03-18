import csv
import os
import pandas as pd

# Define the relative path to the file
relative_path = os.path.join('../data', 'data.csv')

# Construct the absolute path to the file
absolute_path = os.path.abspath(relative_path)

#retorna toda la info del parametro pasado en un array
def getByParameter(parameter):
    result=[]
    with open(absolute_path, 'r', encoding='utf-8') as f:
        reader = pd.read_csv(f)
        for p in parameter:
            result.append(reader.loc[: , p])
        f.close()
    return result

#Devuelve una lista de generos no repetidos que tiene el Dataset
def getAllGenres():
    genres= pd.DataFrame(getByParameter(['the genre of the track']))
    unique_genres = []
    for i in range(len(genres.values[0])):
        if genres[i].values[0] not in unique_genres:
            unique_genres.append(genres[i].values[0])
    return unique_genres

#Devuelve una lista de artistas no repetidos que tiene el Dataset
def getAllArtists():
    artists = pd.DataFrame(getByParameter(['artist']))
    unique_artists = []
    for i in range(len(artists.values[0])):
        if artists[i].values[0] not in unique_artists:
            unique_artists.append(artists[i].values[0])
    return unique_artists
