import nltk
import random
import User
import ReadData
import Utils
import pandas as pd
import sys
from time import sleep

from fuzzywuzzy import fuzz, process
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


greetings = ['Hello!', 'Whatz up?', 'Nice to meet you!', 'You look handsome!']
youWelcome = ['You Welcome!', 'My pleasure! Do you need something? You can ask about artists, genres, top songs...','Happy to be of service. What do you want? :)', 'It was nothing. Ask me what you need :)']
answerHowAreYou = ["I'm fine thanks! Do you need something?","I'm listening to music right now, but i'm here to help you, How can I help?"]
genres = ['Hardcore', 'Techno', 'Rock']
artists = ['Nerve Agent', 'Arctic Monkeys', 'Sefa']
songs = ['Hoy estoy feliz - Nerve Agent', 'Cigarette Smoker Fiona - Arctic Monkeys', 'Going Under - Sefa']

lastKey = ['hello']
inputKeys = ["hello",
             "hi",
             "hey",

             ##Podriamos recomendar una cancion ejemplo: If you are fine/bad maybe you like this song! XXXXXXXXXXXX
             "i'm fine",
             "i'm good",
             "i'm happy",
             "i feel good today",

             "i'm not fine"
             "i'm bad",
             "i'm sad",
             "i feel sad today",

             "how are you",
             "How's it going?",
             "What's up?",

             'thanks',
             'thank you',

             "what are your favourite",
             "which you like most",
             "can you tell your",
             "your best",

             "show top songs",
             "show top music",
             "tell me top songs",
             "tell me top music",
             "can you tell me top songs",
             "can you tell me top music",
             "top songs",

             "can you repeat",
             "repeat please",
             "repeat",
             "again",
             "give another one",

             "show information",
             "life about"]

def printUI():
    print('\033[95m',"Hello I'm music-chatbot! Ask me anything you want about music.", '\033[0m')
    print('\033[95m',"To end the conversation type: 'exit'", '\033[0m')

def start():
    user = User.User()
    last_key = 'Hello'
    run = True
    while (run):
        print('\nUser > ', end='')
        user_input = input()
        if (user_input == 'exit'):
            run = False

        ##Typing Effect##
        print('\033[95mMelody > ', end='')
        for char in generateResponse(user_input, user, lastKey):
            sleep(0.05)
            sys.stdout.write(char)
            sys.stdout.flush()
        print("\033[0m", end= '')
        print()


def main():
    #print(ReadData.getByParameter(['artist', 'title']))
    printUI()
    start()




"""
################################################################
processInput: Generate a response given an input
################################################################
"""
def generateResponse(s, user, lastKey):
    # hacer las reglas y generar la respuesta
    global genre, artist, year
    questionKey = processInput(s)
    ## USER IS SAYING HELLO ##
    if (questionKey == 'hello' or questionKey == 'hi' or questionKey == 'hey'):
        return greetings[random.randint(0, len(greetings) - 1)]
    ## USER IS SAYING HELLO ##
    if (questionKey == 'how are you' or questionKey == "How's it going?" or questionKey == "What's up?"):
        return answerHowAreYou[random.randint(0, len(answerHowAreYou) - 1)]
    ## USER IS SAYING THANKS ##
    if (questionKey == 'thanks' or questionKey == 'thank you'):
        return youWelcome[random.randint(0, len(youWelcome) - 1)]
    ## USER IS HAPPY ##
    if (questionKey =="i'm fine" or questionKey =="i'm good" or questionKey == "i'm happy" or questionKey == 'i feel good today'):
        lastKey = lastKey
        return getRandomHappySong()
    ## USER IS SAD ##
    if(questionKey =="i'm bad" or questionKey == "i'm sad" or questionKey == "i feel sad today" or questionKey == "i'm not fine"):
        lastKey = lastKey
        return getRandomSadSong()

    ## USER ASKING FOR BOT FAVOURITE GENRES/ARTISTS/SONGS
    if (questionKey == "what are your favourite" or questionKey == "which you like most" or questionKey == "your best" or questionKey == "can you tell your"):
        ##CHECK IF ASKING FOR GENRE
        askGenres = fuzz.partial_ratio(s, 'genre') > 75  ##check if 'genre' in input
        askArtists = fuzz.partial_ratio(s, 'artist') > 75  ##check if 'genre' in input
        askSongs = fuzz.partial_ratio(s, 'song') > 75  ##check if 'genre' in input

        if askGenres:
            number = getNumber(s) #Get number of genres asking
            if (number <= len(genres) and number != 0): #If number < number of genres, show them
                r = 'My ' + str(number) + ' favourite genres are:\033[0m'
                for i in range(number):
                    r += '\n              ' + str(i+1) + '.\033[94m' + genres[i] + '\033[0m'
            elif (number == 0): #If no number show all
                r = 'My favourite genres are \033[0m'
                for i in range(len(genres)):
                    r += '\n              ' + str(i+1) + '.\033[94m' + genres[i] + '\033[0m'
            else: #If Number > number of genres, show all
                r = "I only have " + str(len(genres)) + " favourite genres:"
                for i in range(len(genres)):
                    r += '\n              ' + str(i+1) + '.\033[94m' + genres[i] + '\033[0m'
            return r

        if askArtists:
            number = getNumber(s) #Get number of artists asking
            if (number <= len(artists) and number != 0): #If number < number of artists, show them
                r = 'My ' + str(number) + ' favourite artists are:\033[0m'
                for i in range(number):
                    r += '\n              ' + str(i+1) + '.\033[96m' + artists[i] + '\033[0m'
            elif (number == 0): #If no number show all
                r = 'My favourite artists are:'
                for i in range(len(artists)):
                    r += '\n              ' + str(i+1) + '.\033[96m' + artists[i] + '\033[0m'
            else: #If Number > number of artists, show all
                r = "I only have " + str(len(artists)) + " favourite artists:\033[0m"
                for i in range(len(artists)):
                    r += '\n              ' + str(i+1) + '.\033[96m' + artists[i] + '\033[0m'
            return r  # Delete last comma

        if askSongs:
            number = getNumber(s) #Get number of songs asking
            if (number <= len(songs) and number != 0): #If number < number of genres, show them
                r = 'My ' + str(number) + ' favourite songs are:\033[0m'
                for i in range(number):
                    r += '\n              ' + str(i+1) + '.\033[92m' + songs[i] + '\033[0m'
            elif (number == 0): #If no number show all
                r = 'My favourite songs are'
                for i in range(len(songs)):
                    r += '\n              ' + str(i+1) + '.\033[92m' + songs[i] + '\033[0m'
            else: #If Number > number of songs, show all
                r = "I only have " + str(len(songs)) + " favourite songs:"
                for i in range(len(songs)):
                    r += '\n              ' + str(i+1) + '.\033[92m' + songs[i] + '\033[0m'
            return r

    ## USER ASKING FOR TOP FAVOURITE GENRES/ARTISTS/SONGS

    if (questionKey == "show top songs" or questionKey == "show top music" or questionKey == "tell me top songs" or questionKey == "tell me top music" or questionKey == "can you tell me top songs" or questionKey == "can you tell me top music" or questionKey == 'top songs'):

        askedGenre= getGenre(s) ##Check if asking for genre
        askedArtist = getArtist(s) ##Check if asking for artist
        askedNumber = getNumber(s)  # Get number asking

        if askedGenre:
            return getXtopSongsGenre(askedNumber,askedGenre)

        if askedArtist:
            return getXtopSongsArtist(askedNumber,askedArtist)

        if askedGenre and askedArtist:
            return "At the moment I am not able to tell you the songs of an artist by genre"
        else:
            return getXTopSongs(askedNumber)

    if (questionKey == "life about" or questionKey == "show information"):
        askedArtist = getArtist(s)
        if askedArtist:
            r = "Sure, here you have some information about " + askedArtist + "\n\n \033[94m"
            r += ReadData.buscar_definicion_wp(askedArtist)
            r += "\033[0m\033[95m\n\n           Ask for more information if you need it :)\033[0m"

            if (len(r) > 180):
                return r
            else:
                return "Sorry, I' dont have enough information about " + askedArtist
        else:
            return "Sorry, I can't find the artist"
    if (questionKey == "can you repeat" or questionKey == "repeat please" or questionKey =="repeat" or questionKey =="again" or questionKey =="give another one"):
        if(lastKey =="i'm fine" or lastKey =="i'm good" or lastKey == "i'm happy" or lastKey == 'i feel good today'):
            return getRandomHappySong()

        if (lastKey == "i'm bad" or lastKey == "i'm sad" or lastKey == "i feel sad today" or lastKey == "i'm not fine"):
            return getRandomHappySong()
    return "No entendi la pregunta"


"""
################################################################
processInput: Receives an input and return the most similar question key from inputKeys
################################################################
"""
def processInput(input):
    questionKey = process.extractOne(input.lower(), inputKeys)
    ##print("Debug:",questionKey)
    if questionKey[1] >= 50:  # Consideramos que a partir de ratio 60, ha acertado
        return questionKey[0]  # Devolvemos clave, es decir, la pregunta predeterminada identificada
    else:
        return None


"""
################################################################
getXtopSongsGenre: Receive the wanted number of songs and a genre 
                   and returns top X songs with that genre
################################################################
"""
def getXtopSongsGenre(askedNumber,askedGenre):
    if(askedNumber == 0):
        r = ('Here are top 3' + ' ' + askedGenre.capitalize() + ' songs: ')
        number = 3
    else:
        r = ('Here are top ' + str(askedNumber) + ' ' + askedGenre.capitalize() + ' songs: ')
        number = askedNumber

    arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'the genre of the track','Popularity']))  # {[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
    index = 0
    selected_songs_indexs = []
    while len(selected_songs_indexs) < number:
        if arrayData[index][2] == askedGenre:  ##Comprobamos si coincide el genero
            selected_songs_indexs.append(index)  ##añadimos a la lista
            r += '\n              ' + str(len(selected_songs_indexs)) + '.\033[94m' + arrayData[index][1] + ' - ' + \
                 arrayData[index][0] + '\033[0m'
        index += 1
    return r

"""
################################################################
getXtopSongsArtist: Receive a number of songs wanted and an artist
                     and returns top X songs of that artist
################################################################
"""
def getXtopSongsArtist(askedNumber,askedArtist):
    if(askedNumber == 0):
        r = ('Here are top 3 songs of ' + askedArtist.capitalize() + ":" )
        number = 3
    else:
        r = ('Here are top ' + str(askedNumber) + 'songs of ' + askedArtist.capitalize() + ":")
        number = askedNumber

    arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'the genre of the track','Popularity']))  # {[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
    index = 0
    selected_songs_indexs = []
    while len(selected_songs_indexs) < number:
        if arrayData[index][0] == askedArtist:  ##Comprobamos si coincide el artista
            selected_songs_indexs.append(index)  ##añadimos a la lista
            r += '\n              ' + str(len(selected_songs_indexs)) + '.\033[94m' + arrayData[index][1] + ' - ' + \
                 arrayData[index][0] + '\033[0m'
        index += 1
    return r

def getRandomHappySong():
    r = ("Maybe this song goes according to your mood: ")
    arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'Valence','Popularity']))  # {[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
    index = random.randint(0,round(len(arrayData.values[0])/2))
    found = False
    while not found:
        if arrayData[index][2] > 80:  ##comprobamos el valor de Valence (CUANTO MAS ALTO MAS HAPPY)
            r += '\n               1.\033[94m' + arrayData[index][1] + ' - ' + arrayData[index][0] + '\033[0m'
            found = True
        index += 1
    return r

def getRandomSadSong():
    r = ("Sometimes is good to be sad, try to listen this song for your mood: ")
    arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'Valence','Popularity']))  # {[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
    index = random.randint(0,round(len(arrayData.values[0])/2))
    found = False
    while not found:
        if arrayData[index][2] < 22:  ##comprobamos el valor de Valence (CUANTO MAS ALTO MAS HAPPY)
            r += '\n               1.\033[94m' + arrayData[index][1] + ' - ' + arrayData[index][0] + '\033[0m'
            found = True
        index += 1
    return r


"""
################################################################
getXtopSongsGenre: Receive the wanted number of songs and a genre 
                   and returns top X songs with that genre
################################################################
"""
def getXTopSongs(askedNumber):
    if(askedNumber == 0):
        r = ('Here are top 3 songs: ')
        number = 3
    else:
        r = ('Here are top ' + str(askedNumber) + ' songs: ')
        number = askedNumber

    arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'the genre of the track','Popularity']))  # {[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
    index = 0
    selected_songs_indexs = []
    while len(selected_songs_indexs) < number:
        selected_songs_indexs.append(index)  ##añadimos a la lista
        r += '\n              ' + str(len(selected_songs_indexs)) + '.\033[94m' + arrayData[index][1] + ' - ' + arrayData[index][0] + '\033[0m'
        index += 1
    return r
"""
################################################################
getGenre: Receive an input and returns the genre that is there.
################################################################
"""
def getGenre(input):
    all_genres = ReadData.getAllGenres()
    for genre in all_genres:
        similarityRatio = fuzz.token_set_ratio(input, genre)
        #print(genre,"-",similarityRatio)
        if similarityRatio >= 75:
            #print("EL GENERO PEDIDO ES: ",genre)
            return genre
    return False




""""
################################################################
getArtist: Receive an input and returns the artist that is there.
#################################################################
"""
def getArtist(input):
    all_artists = ReadData.getAllArtists()
    ##print("LONGITUD: " ,len(all_artists))
    ##print("Artistas: " ,all_artists)

    for artist in all_artists:
        similarityRatio = fuzz.token_set_ratio(input, artist)
        #print(artist,"-",similarityRatio)
        if similarityRatio >= 50:
            #print("EL ARTISTA PEDIDO ES: ",genre)
            return artist
    return False

"""
getNumber: Receive an input and returns the number that is there.
"""
def getNumber(value):
    for word in value.split(' '):
        if word.isdigit():
            return int(word)
    return int(0)


if __name__ == "__main__":
    main()

"""
def processInput(input):
    # añadir otros procesados si fuese necesario
    porter = nltk.PorterStemmer()
    tokens = nltk.word_tokenize(input)
    stop_words = nltk.corpus.stopwords.words('english')
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(porter.stem(word))
    print(filtered)
    return filtered */
    
def buscar_clave(pregunta):
    puntajes = process.extract(pregunta, respuestas.keys()) #Genera una lista de tuplas con la clave y un Puntaje de cuanto se parece a lo que escribe el usuario
    ##print(puntajes)
    mejor_puntaje = max(puntajes, key=lambda x: x[1]) #Se queda con la clave del maximo puntaje
    if mejor_puntaje[1] >= 5: #Consideramos que a partir de ratio 60, ha acertado
        return mejor_puntaje[0] #Devolvemos clave, es decir, la pregunta predeterminada identificada
    else:
        return None

def buscar_artista(pregunta):
    puntajes = process.extract(pregunta, artistas.keys()) #Genera una lista de tuplas con la clave y un Puntaje de cuanto se parece al artista
    ##print(puntajes)
    mejor_puntaje = max(puntajes, key=lambda x: x[1]) #Se queda con la clave del maximo puntaje
    if mejor_puntaje[1] >= 60: #Consideramos que a partir de ratio 60, ha acertado
        return mejor_puntaje[0] #Devolvemos clave, es decir, el artista
    else:
        return None

def buscar_respuesta(pregunta, artistas):
    clave = buscar_clave(pregunta) ##Busca que clave predeterminada de pregunta se identifica mas con la pregunta del usuario
    if clave: #Si hemos encontrado clave
        artista = buscar_artista(pregunta) #Busca si en la frase menciona alguna artisata
        if artista: #Si hay artista
            return random.choice(respuestas[clave]).format(artista, artistas[artista]) #Respondemos dando el artista y su cancion
        else:
            return random.choice(respuestas[clave]) #Respondemos sin artista ni cancion
    else:
        return "Lo siento, no entiendo lo que estás diciendo."

    """