import requests
import re
import time

from fuzzywuzzy import fuzz, process
from bot.Constants import common_keywords, common_numbers



def get_event_information(artists):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "GxuS8MSyTlbBK5XHdtzzbTHuIEVskIlC"  # Replace with your Ticketmaster API key

    event_info = []

    for artist in artists:
        params = {
            "keyword": artist,
            "apikey": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the response
            print(data)
            events = data["_embedded"]["events"]
            for event in events:
                event_info.append({
                    "artist": artist,
                    "event_name": event["name"],
                    "venue": event["_embedded"]["venues"][0]["name"],
                    "date": event["dates"]["start"]["localDate"]
                })

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving information for {artist}: {e}")

    return event_info


def get_event_information_cities(cities):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "GxuS8MSyTlbBK5XHdtzzbTHuIEVskIlC"  # Replace with your Ticketmaster API key

    event_info = []

    for city in cities:
        params = {
            "keyword": city,
            "apikey": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the response
            #print(data)
            events = data["_embedded"]["events"]
            for event in events:
                event_info.append({
                    "event_name": event["name"],
                    "venue": event["_embedded"]["venues"][0]["name"],
                    "date": event["dates"]["start"]["localDate"],
                    "location": event["_embedded"]["venues"][0]["city"]['name']
                })

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving information for {city}: {e}")

    return event_info



def filter_artist_from_sentence(sentence, keywords, numbers):
    common_k = keywords + numbers
    filtered_sentence = ' '.join(word for word in sentence.lower().split() if word not in common_k)
    return filtered_sentence.strip()

def filter_artist_and_numbers_from_sentence(sentence, keywords):
    filtered_sentence = ' '.join(word for word in sentence.lower().split() if word not in keywords)
    return filtered_sentence.strip()

def find_artists_in_sentence(sentence, artist_list):
    sentence_filtered = filter_artist_from_sentence(sentence, common_keywords, common_numbers)
    sentence_filtered_coma = sentence_filtered.split(',')
    artists_found = []

    better_performance = False
    if len(sentence_filtered_coma) > 1:
        better_performance = True

    inicio = time.time()
    tiempo_limite = 20 #segundos

    for artist in artist_list:
        artist_lower = artist.lower()
        if better_performance:
            artist_found, ratio = process.extractOne(artist, sentence_filtered_coma)
            if ratio > 90:
                print(ratio)
                print(artist)
                if artist not in artists_found: artists_found.append(artist)
                if len(artists_found) == len(sentence_filtered_coma): return artists_found
        else:
            ratio = fuzz.token_set_ratio(sentence_filtered.lower(), artist_lower)
            if ratio > 80:
                print(ratio)
                print(artist)
                if artist not in artists_found: artists_found.append(artist)

        if time.time() - inicio > tiempo_limite:
            print("Tiempo límite excedido. Deteniendo el bucle.")
            break
    return artists_found

def ordenar_lista(lista, frase):
    sentence_filtered = filter_artist_and_numbers_from_sentence(frase, common_keywords)
    frase_sin_comas = sentence_filtered.replace(",", "")
    palabras_frase = frase_sin_comas.split(' ')
    orden = []

    for palabra in palabras_frase:
        if palabra.isdigit():
            orden.append(int(palabra))
        elif palabra in sentence_filtered:
            orden.append(palabra)
        elif ' '.join([palabra, palabras_frase[palabras_frase.index(palabra) + 1]]) in sentence_filtered:
            orden.append(' '.join([palabra, palabras_frase[palabras_frase.index(palabra) + 1]]))

    lista_ordenada = []
    for elemento in orden:
        if str(elemento) in [element.lower() for element in lista]:
            lista_ordenada.append(elemento)

    return lista_ordenada

def get_artists_and_numbers_from_response(artistas, numeros, frase):
    resultado = {}
    # Si la longitud de las listas coincide, devolver la estructura directamente
    if len(artistas) == len(numeros):
        for i in range(len(artistas)):
            artista = artistas[i]
            numero = numeros[i]
            resultado[artista] = numero
        return resultado

    else:
        lista_ordenada = ordenar_lista(numeros+artistas,frase)

        if len(lista_ordenada) > 0:
            primer_elemento = str(lista_ordenada[0])
            print(primer_elemento)
            if primer_elemento.isdigit():
                last_number = primer_elemento
                for element in lista_ordenada:
                    if str(element).isdigit():
                        last_number = element
                    else:
                        resultado[element] = last_number
            else:
                lista_ordenada_rev = lista_ordenada[::-1]
                primer_elemento = str(lista_ordenada_rev[0])
                last_number = primer_elemento
                for element in lista_ordenada_rev:
                    if str(element).isdigit():
                        last_number = element
                    else:
                        resultado[element] = last_number
                resultado = {clave: valor for clave, valor in reversed(resultado.items())}

        return resultado


def find_numbers_in_sentence(user_input):
    numbers = re.findall(r'\d+', user_input)
    return numbers

