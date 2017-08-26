from gevent import monkey
monkey.patch_all()

import redis
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

@app.route('/')
def main():
    # c = db.incr('counter')
    return render_template('main.html')

@socketio.on('connect', namespace='/sockets')
def ws_conn():
    c = db.incr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/sockets")

@socketio.on('disconnect', namespace='/sockets')
def ws_disconn():
    c = db.decr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/sockets")


if __name__ == "__main__":              # check only if this file is called directly (not by importing somewhere else)
    socketio.run(app)