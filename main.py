import random

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


if __name__ == '__main__':
    print('\033[95m',"Bot: Hola, soy un chatbot que recomienda música.\n      Puedes escribir 'Adiós' en cualquier momento para salir.\n      Me puedes preguntar que artistas conozco y que te recomiende alguna cancion suya",'\033[0m')
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() == "adiós":
            print(random.choice(respuestas["Adiós"]))
            break
        respuesta = buscar_respuesta(pregunta,artistas) ##Procesa la pregunta para generar respuesta
        if respuesta:
            print('\033[95m',"Bot:", respuesta,'\033[0m')
        else:
            print("Bot: No entiendo lo que quieres decir.") ##Si no encuentra ningunar respuesta

