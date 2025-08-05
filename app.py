from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '7020'

socketio = SocketIO(app, cors_allowed_origins = '*')

messages = []

@app.route("/")
def root():
    return render_template('index.html')


## MANEJADORES DE EVENTOS ##


@socketio.on('connect')
def handle_connect():
    print("Usuario conectado")
    emit('cargar mensajes', messages)
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Usuario desconectado')
    
@socketio.on('new_message')
def new_message(data):
    print(f"Mensaje recibido: {data}")
    messages.append(data)
    emit('show_message', data, broadcast = True) 
    
@socketio.on('writting')
def writting(data):
    emit('usuario_escribiendo', data, broadcast=True, include_self=False)
    
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
    
    