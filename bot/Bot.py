import random

from fuzzywuzzy import process

import bot.Contexts
from bot import Contexts
from bot.SpotifyApi import get_songs_info_artists_and_numbers, get_popular_songs, create_playlist_with_uris
from bot.Utils import find_artists_in_sentence, find_numbers_in_sentence, get_artists_and_numbers_from_response

###COMMON####
playlist = []
contextLog = []
questionLog = []
inputArtistsAndNumbers = {}
querysongs = []
#############

def getFunctionCode(s):
    global contextLog
    contexts = Contexts.contexts
    best_intents = []
    for contextKey in contexts.keys():
        bestIntent = process.extractOne(s.lower(), contexts[contextKey]['intents'])
        score = bestIntent[1]
        if score >= 65:  # Consideramos que a partir de ratio 60, ha acertado
            best_intent = (contextKey, score)
            best_intents.append(best_intent)
    if len(best_intents) > 0:
        best_context = max(best_intents, key=lambda x: x[1])[0]
        contextLog.insert(0,best_context)
        return contexts[best_context]['functionCode']
    else:
        return "None:)"


def get_AskingSongs_function_code(artists_found, numbers_found, user_input):
    if len(artists_found) == 0 and len(numbers_found) == 0:
        return 1  # Return ton 10 popular songs

    elif len(artists_found) == 0 and len(artists_found) == 1:
        return 2  # Return ton X popular songs

    else:
        global inputArtistsAndNumbers
        inputArtistsAndNumbers = get_artists_and_numbers_from_response(artists_found, numbers_found, user_input)
        return 3  # Return X,Y,Z number of songs o A,B,C Artists


def generateResponse(user_input, artists_db):
    global questionLog

    questionLog.insert(0,user_input)

    function_code = getFunctionCode(user_input)
    # User Saying hello
    if function_code == 1:
        return "Hello!"

    # User Asking how I am
    elif function_code == 2:
        return "Fine thanks. How Can I help you?"

    # User Asking for songs
    elif function_code == 3:  ##ASKING SONGS
        global querysongs
        artists_found = find_artists_in_sentence(user_input, artists_db)
        numbers_found = find_numbers_in_sentence(user_input)
        askingSongs_function_code = get_AskingSongs_function_code(artists_found, numbers_found, user_input)

        if (askingSongs_function_code == 1):  # Get songs
            # Return top 10 popular songs of this year
            response = "Aqui tienes las canciones mas populares de 2023:\n"
            songs = get_popular_songs()

            querysongs = songs

            i = 1
            for song in songs:
                response += str(i) + '. ' + song['name'] + ' - ' + song['artist'][0] + '\n'
                i += 1
            print()
            return response

        if (askingSongs_function_code == 2):
            print()
            # Return ton X popular songs

        if (askingSongs_function_code == 3):
            response = "Aqui tienes:\n"
            songs = get_songs_info_artists_and_numbers(inputArtistsAndNumbers)
            querysongs = songs

            i = 1
            for artist in inputArtistsAndNumbers.keys():
                response += "\n" + artist.capitalize() + ":\n"
                for song in songs:
                    if song['artist'].lower() == artist.lower():
                        response += str(i) + '. ' + song['name'] + ' - ' + song['artist'].capitalize() + '\n'
                        i += 1
                print()
            return response

    # User Asking to add something
    elif (function_code == 4):
        numbers_found = find_numbers_in_sentence(user_input)

        if len(numbers_found) == 1:
            response = "Ok, I added track "
        else:
            response = "Ok, I added tracks "

        if len(querysongs) != 0:
            for i, number in enumerate(numbers_found):
                response += number
                if i < len(numbers_found) - 2:
                    response += ", "
                elif i == len(numbers_found) - 2:
                    response += " and "
                else:
                    response += ""

                playlist.append(querysongs[int(number)-1]['name'])
            response += " to your playlist! :)"
            return response

        return "What do you want to add? If it's a song I mentioned before, tell me to add that number"

    # User Asking to delete something, ask if sure
    elif (function_code == 5):
        numbers_found = find_numbers_in_sentence(user_input)
        response = "Are you sure you want to delete "
        if len(numbers_found) == 1:
            response += 'track '
        else:
            response += "tracks "
        ##Empty playlist
        if len(playlist) == 0:
            return "Your playlist is empty! You should add something before."

        ##Delete numbers
        if len(numbers_found) != 0:
            for i, number in enumerate(numbers_found):
                response += number
                if i < len(numbers_found) - 2:
                    response += ", "
                elif i == len(numbers_found) - 2:
                    response += " and "
                else:
                    response += ""

            response += " from your playlist?"
            contextLog.insert(0,"deleteNumbers")
            return response

        return "What do you want to delete? If it's a song in your playlist, tell me to delete that number"


    # User Asking create PLAYLIST
    elif function_code == 6:
        uris = []

        for song_name in playlist:
            for song in querysongs:
                if song['name'] == song_name:
                    uris.append(song['uri'])
                    break

        response = "Time to enjoy! : "
        playlist_link = create_playlist_with_uris("New Paylist", uris)
        response += playlist_link
        return response

    #User affirmation
    elif function_code == 7:
        try:
            if contextLog[1] == "deleteNumbers":
                user_delete_query = questionLog[1]
                numbers_found = find_numbers_in_sentence(user_delete_query)
                response = "Done, I deleted "

                if len(numbers_found) == 1:
                    response += 'track '
                else:
                    response += "tracks "


                #Delete numbers and add response.
                out_of_index_numbers = []
                for i, number in enumerate(numbers_found):

                    index = int(number)-1  # Índice del elemento a borrar
                    if index >= 0 and index < len(playlist): ## comprobar si indice es correcto
                        response += number
                        if i < len(numbers_found) - 2:
                            response += ", "
                        elif i == len(numbers_found) - 2:
                            response += " and "
                        else:
                            response += ""

                        removed_song = playlist.pop(index)
                    else:
                        out_of_index_numbers.append(int(number))

                response += " from your playlist."

                ##If numbers not in list add couldn't find that numbers to response
                if len(out_of_index_numbers) > 0:
                    response += " Couldn't find "
                    if len(out_of_index_numbers) == 1:
                        response += 'track '
                    else:
                        response += "tracks "
                    for i, number in enumerate(out_of_index_numbers):

                        response += str(number)
                        if i < len(out_of_index_numbers) - 2:
                            response += ", "
                        elif i == len(out_of_index_numbers) - 2:
                            response += " and "
                        else:
                            response += ""

                    response += " ."

                contextLog.pop(1)
                return response
            else:
                return "What dou yo mean? Specify please :) "
        except:
            return "What dou yo mean? Specify please :) "

    #User Negation
    elif function_code == 8:
        try:
            if contextLog[1] == "deleteNumbers":
                contextLog.pop(1)
                return "Okey, i wouldn't delete that numbers. "
            else:
                return "What dou yo mean? Specify please :) "
        except:
            return "What dou yo mean? Specify please :) "

    #Randomize list
    elif function_code == 9:
        random.shuffle(playlist)
        return "I've just randomized your playlist! :)"

    return (function_code)
