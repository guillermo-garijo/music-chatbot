import csv
import os

#import BeautifulSoup4
import pandas as pd
import requests
import spotipy
import json
import webbrowser
#from bs4 import BeautifulSoup
from time import sleep
import re
import textwrap

from fuzzywuzzy import fuzz

linksWikipedia = [   'Train: https://en.wikipedia.org/wiki/Train',
    'Eminem: https://en.wikipedia.org/wiki/Eminem',
    'Kesha: https://en.wikipedia.org/wiki/Kesha',
    'Lady Gaga: https://en.wikipedia.org/wiki/Lady_Gaga',
    'Bruno Mars: https://en.wikipedia.org/wiki/Bruno_Mars',
    'Justin Bieber: https://en.wikipedia.org/wiki/Justin_Bieber',
    'Taio Cruz: https://en.wikipedia.org/wiki/Taio_Cruz',
    'OneRepublic: https://en.wikipedia.org/wiki/OneRepublic',
    'Alicia Keys: https://en.wikipedia.org/wiki/Alicia_Keys',
    'Rihanna: https://en.wikipedia.org/wiki/Rihanna',
    'Flo Rida: https://en.wikipedia.org/wiki/Flo_Rida',
    'Mike Posner: https://en.wikipedia.org/wiki/Mike_Posner',
    'Far East Movement: https://en.wikipedia.org/wiki/Far_East_Movement',
    'Usher: https://en.wikipedia.org/wiki/Usher',
    'Sean Kingston: https://en.wikipedia.org/wiki/Sean_Kingston',
    'The Black Eyed Peas: https://en.wikipedia.org/wiki/The_Black_Eyed_Peas',
    'Adam Lambert: https://en.wikipedia.org/wiki/Adam_Lambert',
    'Maroon 5: https://en.wikipedia.org/wiki/Maroon_5',
    'Neon Trees: https://en.wikipedia.org/wiki/Neon_Trees',
    'Selena Gomez & The Scene: https://en.wikipedia.org/wiki/Selena_Gomez_%26_The_Scene',
    'Enrique Iglesias: https://en.wikipedia.org/wiki/Enrique_Iglesias',
    'Katy Perry: https://en.wikipedia.org/wiki/Katy_Perry',
    'Britney Spears: https://en.wikipedia.org/wiki/Britney_Spears',
    '3OH!3: https://en.wikipedia.org/wiki/3OH!3',
    'David Guetta: https://en.wikipedia.org/wiki/David_Guetta',
    'Christina Aguilera: https://en.wikipedia.org/wiki/Christina_Aguilera',
    'Florence + The Machine: https://en.wikipedia.org/wiki/Florence_%2B_The_Machine',
    'Shakira: https://en.wikipedia.org/wiki/Shakira',
    'Tinie Tempah: https://en.wikipedia.org/wiki/Tinie_Tempah',
    'T.I.: https://en.wikipedia.org/wiki/T.I.',
    'Martin Solveig: https://en.wikipedia.org/wiki/Martin_Solveig',
    'Christina Perri: https://en.wikipedia.org/wiki/Christina_Perri',
    'Adele: https://en.wikipedia.org/wiki/Adele',
    'Pitbull: https://en.wikipedia.org/wiki/Pitbull',
    'Beyonce: https://en.wikipedia.org/wiki/Beyonce',
    'Hot Chelle Rae: https://en.wikipedia.org/wiki/Hot_Chelle_Rae',
    'Avril Lavigne: https://en.wikipedia.org/wiki/Avril_Lavigne',
    'Kanye West: https://en.wikipedia.org/wiki/Kanye_West',
    'LMFAO: https://en.wikipedia.org/wiki/LMFAO',
    'Jessie J: https://en.wikipedia.org/wiki/Jessie_J',
    'Jennifer Lopez: https://en.wikipedia.org/wiki/Jennifer_Lopez',
    'Chris Brown: https://en.wikipedia.org/wiki/Chris_Brown',
    'Sleeping At Last: https://en.wikipedia.org/wiki/Sleeping_at_Last',
]

# Define the relative path to the file
from numpy.core.defchararray import capitalize

relative_path = os.path.join('../data', 'data.csv')

# Construct the absolute path to the file
absolute_path = os.path.abspath(relative_path)

def displaySong(song):
    clientID = 'your_client_id'
    clientSecret = 'your_client_secret'
    redirectURI = 'http://google.com/'

    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI)

    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']


    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    json.dumps(user, sort_keys=True, indent=4)
    searchResults = spotifyObject.search(song, 1, 0, "track")
    tracks_dict = searchResults['tracks']
    tracks_items = tracks_dict['items']
    song = tracks_items[0]['external_urls']['spotify']
    webbrowser.open(song)



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

def buscar_definicion_wp(artist):
    #Get link of Artist in wikipedia
    url = getLink(artist)
    ##Get response of url
    response = requests.get(url)
    #Beautify url
    soup = BeautifulSoup4(response.content, 'html.parser')
    ##String Manipulation for getting the important information.
    texto_principal_element = soup.find('div', {'id': 'mw-content-text'})
    texto_principal = texto_principal_element.find(class_='mw-parser-output')
    texto_principal = texto_principal.get_text().split("\n\n") ##Hay mucha info basura hasta que hay doble salto de linea
    texto_principal_sorted = sorted(texto_principal[:5], key=lambda x: len(x))
    texto_principal_sorted_limpio = texto_principal_sorted[-1].split("\n")
    texto_final = sorted(texto_principal_sorted_limpio, key=len, reverse=True) #Ordenamos candidatos de mas texto a menos
    returned_string = texto_final[0] #Asumimos que este parrafo es bueno
    if(len(texto_final[1])>120): #El siguiente, si puede aportar informacion, la añadimos, osea que sea una parrafo largo
        returned_string += returned_string + texto_final[1]
    #Manipulamos el string final para limpiar las referencias y jutificarlo
    returned_string_without_references = re.sub(r'\[\w+\]', ' ', returned_string)
    texto_justificado = textwrap.wrap(returned_string_without_references, width=85)
    returned_string_final = ''
    for linea in texto_justificado:
        returned_string_final += '              ' + linea + '\n'
    return returned_string_final[:450] + "..."

def getLink(artist):
    for link in linksWikipedia:
        similarityRatio = fuzz.token_set_ratio(artist, link)
        if similarityRatio >= 75:
            #print(link, "-", similarityRatio)
            #print("URL: ",link.split(': ')[1])
            return link.split(': ')[1]
    return False