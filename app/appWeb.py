import json

from bottle import Bottle, request, response, template
from main import *

from bot.ReadData import read_csv_column
from bot.Bot import playlist, generateResponse, contextLog

app = Bottle()

# Ejemplo de uso
csv_file = 'artists.csv'
print("Cargando Csv")
artists_db = read_csv_column(csv_file, 'artist_mb')
contextLog.append("mainContext")


# Ruta principal
@app.route('/')
def home():
    return template('index.html')


# Ruta para recibir las solicitudes del usuario y generar respuestas
@app.route('/chat', method=['OPTIONS', 'POST'])
def chat():
    user_message = request.forms.get('user_input')
    response = generateResponse(user_message, artists_db)
    print(response)
    print(contextLog)
    return response

# Ruta para obtener la playlist
@app.route('/playlist', method=['OPTIONS', 'GET'])
def get_playlist():
    return json.dumps(playlist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
