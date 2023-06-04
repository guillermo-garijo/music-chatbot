import json
import webbrowser

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#---------------------------------------
#--------SPOTIFY API CONNECTION---------
#---------------------------------------
# Configurar las credenciales de la API de Spotify
client_id = '2ebf53b1776c4fbeb5f834b4d71d202e'
client_secret = 'f96c6c9e97fc4eeda66c49eab9bbe84e'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="http://localhost:8000/callback",
        client_id=client_id,
        client_secret=client_secret,
        cache_path="token.txt"
    )
)
def get_popular_songs():
    # Buscar las canciones más populares
    results = sp.search(q='year:2023', type='track', limit=10)

    # Procesar los resultados
    canciones_populares = []
    for track in results['tracks']['items']:
        artistas = [artista['name'] for artista in track['artists']]

        song_name = track['name']
        song_artist = artistas
        song_link = track['external_urls']['spotify']
        song_uri = track['uri']
        canciones_populares.append({'name': song_name, 'artist': song_artist, 'link': song_link, 'uri': song_uri})

    return canciones_populares

def get_songs_info_from_artists(artist_list, num_songs_per_artist):
    combined_songs_info = []

    for artist in artist_list:
        # Buscar el ID del artista
        results = sp.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            artist_id = items[0]['id']

            # Obtener las canciones principales del artista
            top_tracks = sp.artist_top_tracks(artist_id)

            # Extraer la información de cada canción
            songs_info = []
            for track in top_tracks['tracks'][:num_songs_per_artist]:
                song_name = track['name']
                song_artist = artist
                song_link = track['external_urls']['spotify']
                song_uri = track['uri']
                songs_info.append({'name': song_name,'artist': song_artist, 'link': song_link, 'uri': song_uri})

            combined_songs_info.extend(songs_info)

    return combined_songs_info

def get_songs_info_artists_and_numbers(art_and_num):
    combined_songs_info = []

    for artist in art_and_num.keys():
        # Buscar el ID del artista
        results = sp.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            artist_id = items[0]['id']

            # Obtener las canciones principales del artista
            top_tracks = sp.artist_top_tracks(artist_id)

            # Extraer la información de cada canción
            songs_info = []
            for track in top_tracks['tracks'][:int(art_and_num[artist])]:
                song_name = track['name']
                song_artist = artist
                song_link = track['external_urls']['spotify']
                song_uri = track['uri']
                songs_info.append({'name': song_name,'artist': song_artist, 'link': song_link, 'uri': song_uri})

            combined_songs_info.extend(songs_info)

    return combined_songs_info

def get_spanish_latin_artists():
    # Realizar una búsqueda de artistas españoles
    spanish_query = 'artistas españoles'
    spanish_results = sp.search(q=spanish_query, type='artist', limit=50)
    spanish_artists = [artist['name'] for artist in spanish_results['artists']['items']]

    # Realizar una búsqueda de artistas latinos
    latin_query = 'artistas latinos'
    latin_results = sp.search(q=latin_query, type='artist', limit=50)
    latin_artists = [artist['name'] for artist in latin_results['artists']['items']]

    # Combinar las listas de artistas españoles y latinos
    artists = spanish_artists + latin_artists

    # Imprimir la lista de artistas
    for artist in artists:
        print(artist)

def create_playlist_with_uris(playlist_name, track_uris):
    # Obtener el ID del usuario actual
    user_id = sp.current_user()['id']

    # Crear la playlist
    playlist = sp.user_playlist_create(user_id, playlist_name)

    # Obtener el ID de la playlist creada
    playlist_id = playlist['id']

    # Agregar las canciones a la playlist
    sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)

    # Obtener el enlace de la playlist
    playlist_link = playlist['external_urls']['spotify']

    return playlist_link

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
