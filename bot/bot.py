import nltk
import random
import User as User

questions={'genres':'What genres of music do you like?', 'artists':'What artists do you like?', 'songs':'What songs do you like?'}

def printUI():
    print("Hello I'm music-chatbot!")

def askQuestion(user):
    #añadir mas preguntas y hacer q elija una aleatoria
    print(questions['genres'])
    user_response=input()
    p_response=processResponse(user_response)
    user.setQuestionAnswer('genres', p_response)

def generateResponse(user):
    #hacer las reglas y generar la respuesta
    return

def processResponse(response):
    #añadir otros procesados si fuese necesario
    tokens=nltk.word_tokenize(response)
    stop_words=nltk.corpus.stopwords.words('english')
    filtered = []
    for word in tokens:
        if word not in stop_words:
            filtered.append(word)
    return filtered

def start():
    user=User.User()
    while(True):
        askQuestion(user)
        bot_response=generateResponse(user)
        user.printUser()
        #generateResponse(user)

def main():
    printUI()
    start()


if __name__ == "__main__":
    main()