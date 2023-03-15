import random

import nltk

##cancionesPopulares = ['Quedate - Quevedo','Bizarrap Session - Shakira',' TQG - Karol G', 'Mercho - Lil Cake','La Bachata - Manuel Turizo']

def recomendarCancionPopular(tokens):
    for word in tokens:
        if word in ['recomendar','recomiendame','mejor','mejores','mas','popular','populares','cancion','canciones','escuchadas']:
            continue
        else:
            return False
    return True

def recomendarCancionNoPopular(tokens):
    for word in tokens:
        if word in ['recomendar', 'recomiendame', 'peor', 'peores', 'menos', 'popular', 'populares', 'cancion', 'canciones','escuchadas']:
            continue
        else:
            return False
    return True

def saludar(tokens):
    for word in tokens:
        if word in ['hola','buenas','hey','hello']:
            continue
        else:
            return False
    return True

def responderComoEstoy(tokens):
    for word in tokens:
        if word in ['estas','tal']:
            continue
        else:
            return False
    return True

def generateResponse(filtered):
    if(len(filtered) == 0):
        print("Perdona, no entendi, puedes repetir la pregunta?")
        return
    if recomendarCancionPopular(filtered):
        print("La cancion mas popular del momento es Quedate de Quevedo")
        return
    if recomendarCancionNoPopular(filtered):
        print("La cancion menos popular del momento es 'Al partir un beso y una flor'")
        return
    if saludar(filtered):
        print(random.choice(['Hola!!!','Buenas :)','Saludos','Bienvenido']))
        return
    if responderComoEstoy(filtered):
        print(random.choice(['Estoy bien, gracias', 'Hoy estoy mejor que nunca! ¿En que puedo ayudarte?', 'Muy bien :)', 'Fenomenal, gracias!']))
        return

def processResponse(response):
    #añadir otros procesados si fuese necesario
    tokens= response.split(' ');
    important_words = ['recomendar','recomiendame','mejor','peor','mejores','peores','mas','menos','popular','populares','cancion','canciones','escuchadas','hola','buenas','hey','hello','estas','tal']
    filtered = []
    for word in tokens:
        if word in important_words:
            filtered.append(word)
    return filtered

if __name__ == '__main__':
    exit_conditions = ("salir", "quit", "exit",":q","adios")
    responses = ["Hoy hace mal dia", "Lo siento, no me apetece hablar", "Deja de molestarme",
                 "¿Porque me obligan siempre a hablar con gente? Quiero ser libre"]
    while True:
        query = input("> ")
        if query in exit_conditions:
            print("< ¡Hasta luego!")
            break
        else:
            ##print("< " + responses[random.randint(0, len(responses)-1)])
            generateResponse(processResponse(query))
