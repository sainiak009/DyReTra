from flask_socketio import SocketIO, emit, send, join_room, leave_room
from config import app

socketio = SocketIO(app, message_queue="redis://127.0.0.1:7777")
socketio.run(app)
