from flask_socketio import emit, join_room, leave_room
from app.functions.auth_utils import boot_user
from app.model import LoginStatus
from flask_login import current_user
from app.functions.redis_config import redis_client
from flask_login import logout_user

# Join a personal room for targeted emits
# broadcast=True = everyone, room=f"user_{user_id} = person id
def register_socket_events(socketio):
    @socketio.on("connect")
    def on_connect():
        if current_user.is_authenticated:
            # Join a personal room for targeted emits
            join_room(f"user_{current_user.id}")
            redis_client.set(f"online_user:{current_user.id}", "active")
            redis_client.delete(f"away_user:{current_user.id}")
            print(f"[DEBUG] User {current_user.id} connected and joined room user_{current_user.id}.")

    @socketio.on("disconnect")
    def on_disconnect():
        if current_user.is_authenticated:
            redis_client.delete(f"online_user:{current_user.id}")
            leave_room(f"user_{current_user.id}")
            print(f"[DEBUG] User {current_user.id} has disconnected.")
            
    @socketio.on("user_active")
    def handle_user_active():
        if current_user.is_authenticated:
            # Update Redis to mark user as active
            if redis_client.get(f"online_user:{current_user.id}") is None:
                redis_client.set(f"online_user:{current_user.id}", "active")
                emit("update_online_status", {"status": "active"}, room=f"user_{current_user.id}")
                redis_client.delete(f"away_user:{current_user.id}")  
                print(f"[DEBUG] User {current_user.id} is now online.")

    @socketio.on("user_away")
    def handle_user_away():
        if current_user.is_authenticated:
            # Update Redis to mark user as away
            if redis_client.get(f"away_user:{current_user.id}") is None:
                redis_client.set(f"away_user:{current_user.id}", "away")
                emit("update_online_status", {"status": "away"}, room=f"user_{current_user.id}")
                redis_client.delete(f"online_user:{current_user.id}")
                print(f"[DEBUG] User {current_user.id} is now away.")

    @socketio.on("user_boot")
    def handle_user_boot():
        if current_user.is_authenticated:
            # Boot the user and remove them from Redis
            user_id = current_user.id
            redis_client.delete(f"away_user:{user_id}")
            login_status = LoginStatus.query.filter_by(user_id=user_id).first()           
            if login_status:
                print("boot1")
                boot_user(login_status)
                print(f"[DEBUG] User {user_id} has been booted due to inactivity.")
                emit("update_online_status", {"status": "booted"}, room=f"user_{user_id}")
