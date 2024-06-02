from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket

app = Flask(__name__)
socketio = SocketIO(app)

rig_host = 'localhost'
rig_port = 4532

def get_rig_data(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((rig_host, rig_port))
            s.sendall(command.encode('utf-8'))
            response = s.recv(1024).decode('utf-8').strip()
            return response
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_frequency')
def handle_get_frequency():
    frequency = get_rig_data('f\n')
    emit('frequency', {'frequency': frequency})

@socketio.on('get_mode')
def handle_get_mode():
    mode = get_rig_data('m\n')
    emit('mode', {'mode': mode})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)