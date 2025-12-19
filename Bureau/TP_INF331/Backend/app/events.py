from flask_socketio import emit, join_room, leave_room
from .extensions import db
from .models import Message

def init_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('join_room')
    def handle_join_room(data):
        room = data['room']
        username = data['username']
        join_room(room)
        emit('user_joined', {'username': username}, room=room, skip_sid=True)

    @socketio.on('leave_room')
    def handle_leave_room(data):
        room = data['room']
        leave_room(room)

    @socketio.on('send_message')
    def handle_send_message(data):
        room = data['room']
        content = data['content']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        product_id = data['product_id']
        username = data['username']
        # Save to db
        message = Message(content=content, sender_id=sender_id, receiver_id=receiver_id, product_id=product_id)
        db.session.add(message)
        db.session.commit()
        # Emit to room
        emit('receive_message', {
            'content': content,
            'sender': username,
            'sender_id': sender_id,
            'timestamp': message.created_at.isoformat()
        }, room=room)

    @socketio.on('typing')
    def handle_typing(data):
        room = data['room']
        username = data['username']
        emit('user_typing', {'username': username}, room=room, skip_sid=True)

    @socketio.on('stop_typing')
    def handle_stop_typing(data):
        room = data['room']
        emit('stop_typing', {}, room=room, skip_sid=True)