from flask import Flask, render_template, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# In-memory store for connected users and the server's role
users = []
server = None  # No server initially

# Web route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Web route to get users list
@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(users=users)

# SocketIO event when a user joins
@socketio.on('connect')
def on_connect():
    # Add user to the list
    username = f"User{random.randint(1000, 9999)}"
    session['username'] = username
    users.append(username)
    emit('user_connected', {'username': username}, broadcast=True)

    # Assign the first user as the server
    if len(users) == 1:
        global server
        server = username
        emit('server_assigned', {'server': server}, broadcast=True)

    # Notify the user who the current server is
    emit('server_update', {'server': server})

# SocketIO event when a user sends a message
@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    username = session['username']

    # If the user is the server, broadcast the message to all users
    if username == server:
        emit('new_message', {'message': message, 'username': username}, broadcast=True)
    else:
        # Send the message only to the server
        emit('new_message', {'message': message, 'username': username}, room=server)

# SocketIO event when a user disconnects
@socketio.on('disconnect')
def on_disconnect():
    username = session.get('username')
    if username in users:
        users.remove(username)

    # If the server disconnects, assign a new server
    if username == server:
        global server
        if users:
            server = users[0]  # Assign the first user as the new server
            emit('server_assigned', {'server': server}, broadcast=True)

    # Broadcast the server update
    emit('server_update', {'server': server}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
