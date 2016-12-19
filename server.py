import socketio
import eventlet
import eventlet.wsgi
import os
from flask import Flask, render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
va = []

@socketio.on('my event')
def my_event(message):
    commend = 'wget -c ' + message['data']

    emit('my other event', {'data1':'ok'})
    va.append(commend)
    #print(os.system(message['data']))
    printout()

def printout():
    for i in va:
        print(va)

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')



if __name__ == '__main__':

    socketio.run(app)
