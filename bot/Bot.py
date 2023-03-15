import nltk
import random
import User
import ReadData

#gustos/saludos del bot
greetings=['Hello!', 'Whatz up?', 'Nice to meet you!', 'You look handsome!']
genres=['Hardcore','Techno', 'Rock']
artists=['Nerve Agent', 'Arctic Monkeys', 'Sefa']
songs=['Hoy estoy feliz - Nerve Agent', 'Cigarette Smoker Fiona - Arctic Monkeys', 'Going Under - Sefa']

def printUI():
    print("Hello I'm music-chatbot! Ask me anything you want about music.")
    print("To end the conversation type: 'exit'")

def generateResponse(s, user):
    #hacer las reglas y generar la respuesta
    p_in=processInput(s)
    if('hello' in p_in or 'meet' in p_in or 'hi' in p_in or 'hey' in p_in):
        return greetings[random.randint(0,len(greetings)-1)]
    if(('like' in p_in or 'favourit' in p_in or 'enjoy' in p_in) and '?' in p_in):
        if('genr' in p_in):
            r='My favourite genres are '
            for i in genres:
                r+=i + ', '
            return r
        elif('artist' in p_in):
            r='My favourite artists are '
            for i in artists:
                r=+i + ', '
            return r
        elif('song' in p_in or 'music' in p_in):
            r='My favourite songs are '
            for i in songs:
                r+=i + ', '
            return r
    print(p_in)
    return 'a'

def processInput(input):
    #añadir otros procesados si fuese necesario
    porter=nltk.PorterStemmer()
    tokens=nltk.word_tokenize(input)
    stop_words=nltk.corpus.stopwords.words('english')
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(porter.stem(word))
    return filtered

def start():
    user=User.User()
    run=True
    while(run):
        print('user > ', end='')
        user_input=input()
        if (user_input=='exit'):
            run=False
        print('bot > ' + generateResponse(user_input, user))
        

def main():
    printUI()
    start()


if __name__ == "__main__":
    main()