import nltk
import random
import User
import ReadData
import pandas as pd

from fuzzywuzzy import fuzz, process
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

respuestas = {
    "Hola": ["¡Hola! ¿Cómo estás?", "¡Hola! ¿En qué puedo ayudarte?"],
    "Saludos": ["¡Hola! ¿Cómo estás?", "¡Hola! ¿En qué puedo ayudarte?"],
    "¿Bien y tu?": ["¡Yo tambien estoy bien, gracias!", "¡Aqui estamos!"],
    "Mal": ["Todo se pasa, no te preocupes"],
    "Fatal": ["Todo se pasa, no te preocupes"],
    "¿Cuantos artistas conoces?": ["Conozco los siguientes artistas:\n   -Beyonce \n   -Ed Sheeran \n   -Taylor Swift \n   -Michael Jackson \n   -Madonna\n ¿De quien quieres saber una cancion?"],
    "¿Que artistas conoces?": ["Conozco los siguientes artistas:\n   -Beyonce \n   -Ed Sheeran \n   -Taylor Swift \n   -Michael Jackson \n   -Madonna"],
    "¿Qué música me recomiendas de *?": ["Si te gusta la música de {0}, quizás te gustará también {1}", "Te recomiendo escuchar {1} de {0}."],
    "¿me puedes decir una cancion de *?": ["Si te gusta la música de {0}, quizás te gustará también {1}", "Te recomiendo escuchar {1} de {0}."],
    "¿y una de *?": ["Si te gusta la música de {0}, quizás te gustará también {1}", "Te recomiendo escuchar {1} de {0}."],
    "¿Cancion mas Popular *?": ["Si te gusta la música de {0}, quizás te gustará también {1}", "Te recomiendo escuchar {1} de {0}."],
    "¿Cancion mas Escuchada *?": ["Si te gusta la música de {0}, quizás te gustará también {1}", "Te recomiendo escuchar {1} de {0}."],
    "Adiós": ["¡Adiós!", "¡Hasta luego!", "¡Nos vemos pronto!"]
}

artistas = {
    "Beyonce": "Crazy in Love",
    "Ed Sheeran": "Shape of You",
    "Taylor Swift": "Shake It Off",
    "Michael Jackson": "Thriller",
    "Madonna": "Like a Prayer"
}

# gustos/saludos del bot
greetings = ['Hello!', 'Whatz up?', 'Nice to meet you!', 'You look handsome!']
genres = ['Hardcore', 'Techno', 'Rock']
artists = ['Nerve Agent', 'Arctic Monkeys', 'Sefa']
songs = ['Hoy estoy feliz - Nerve Agent', 'Cigarette Smoker Fiona - Arctic Monkeys', 'Going Under - Sefa']

def printUI():
    print("Hello I'm music-chatbot! Ask me anything you want about music.")
    print("To end the conversation type: 'exit'")

def generateResponse(s, user):
    # hacer las reglas y generar la respuesta
    global genre, artist, year
    p_in = processInput(s)
    if ('hello' in p_in or 'meet' in p_in or 'hi' in p_in or 'hey' in p_in):
        return greetings[random.randint(0, len(greetings) - 1)]
    if (('like' in p_in or 'favourit' in p_in or 'enjoy' in p_in) and '?' in p_in):
        if ('genr' in p_in):
            r = 'My favourite genres are '
            for i in genres:
                r += i + ', '
            return r
        elif ('artist' in p_in):
            r = 'My favourite artists are '
            for i in artists:
                r += i + ', '
            return r
        elif ('song' in p_in or 'music' in p_in):
            r = 'My favourite songs are '
            for i in songs:
                r += i + ', '
            return r

    if ('show' in p_in or 'want'):
        if ('genre' in p_in):    #buscaremos top 5 canciones de ese género
            r = 'Here are some good '
            arrayData = pd.DataFrame(ReadData.getByParameter(['artist', 'title', 'the genre of the track'])) #{[a1, t1, g1], [a2, t2, g2], [a3, t3, g3]}
            print(arrayData)
            print(arrayData[2])
            for index, row in arrayData.iterrows():
                if(row[2] in p_in):
                    genre = row[2]
            #for data in arrayData:
            #    if (data[2] in p_in):
            #        genre = data
            r += r + genre + ' songs: \n'

            genre_rows = arrayData[arrayData['the genre of the track'].str.contains(genre)]
            print(genre_rows)
            for i in range(5):
                random_line = random.choice(genre_rows)
                r += r + '- ' + random_line + '\n'
            return r
        elif ('artist' in p_in):    #buscaremos top 5 canciones de ese artista
            r = 'Here are some good '
            arrayData = ReadData.getByParameter([0, 1])
            for data in arrayData:
                if (data[:, 1] in p_in):
                    artist = data[:, 1]
            r += r + artist + ' songs: \n'
            for i in range(5):
                lines_with_pop = [line for line in arrayData if arrayData[:, 1] == artist in line]
                random_line = random.choice(lines_with_pop)
                r += r + '- ' + random_line + '\n'
            return r
        elif ('year' in p_in):    #buscaremos top 5 canciones de ese artista
            r = 'Here are some good '
            arrayData = ReadData.getByParameter([0, 1, 3])
            for data in arrayData:
                if (data[:, 2] in p_in):
                    year = data[:, 2]
            r += r + year + ' songs: \n'
            for i in range(5):
                lines_with_pop = [line for line in arrayData if arrayData[:, 2] == year in line]
                random_line = random.choice(lines_with_pop)
                r += r + '- ' + random_line + '\n'
            return r
        elif ('top' in p_in and 'songs' in p_in):
            #mostraremos el top 'x' canciones
            r = ''
            num = None
            for i in p_in:
                if (i.isnumeric()):
                    num = int(i)
            arrayData = ReadData.getByParameter([0, 1, 13])
            top = []
            #max_value = arrayData[:, 0]
            max_value = max(arrayData[:, 2])
            top.append(max_value)
            for data in arrayData:
                if (data[:, 2] > max_value[:, 2]):
                    max_value = data[:, 2]
                    top.append(max_value)
            r += r + 'Here´s your top ' + num + ' songs:\n'
            for i in range(num):
                r += r + '- ' + top[i] + '\n'
            return r
        elif ('song' in p_in or 'music' in p_in):
            r = 'My favourite songs are '
            for i in songs:
                r += i + ', '
            return r
    print(p_in)
    return 'a'

def processInput(input):
    # añadir otros procesados si fuese necesario
    porter = nltk.PorterStemmer()
    tokens = nltk.word_tokenize(input)
    stop_words = nltk.corpus.stopwords.words('english')
    filtered = []
    for word in tokens:
        if word not in stop_words:
            porter.stem(word)
            filtered.append(word)
    print(filtered)
    return filtered


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


def start():
    user = User.User()
    run = True
    while (run):
        print('user > ', end='')
        user_input = input()
        if (user_input == 'exit'):
            run = False
        print('bot > ' + generateResponse(user_input, user))


def main():
    #print(ReadData.getByParameter(['artist', 'title']))
    printUI()
    start()


if __name__ == "__main__":
    main()