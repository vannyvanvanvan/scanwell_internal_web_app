from flask_socketio import emit
from flask_login import current_user
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def register_socket_events(socketio):
    @socketio.on("user_active")
    def handle_user_active():
        if current_user.is_authenticated:
            # Update Redis to mark user as active
            if redis_client.get(f"online_user:{current_user.id}") is None:
                redis_client.set(f"online_user:{current_user.id}", "active")
                emit("update_online_status", {"status": "active"}, broadcast=True)
                redis_client.delete(f"away_user:{current_user.id}")  
                print(f"[DEBUG] User {current_user.id} is now online.")

    @socketio.on("user_away")
    def handle_user_away():
        if current_user.is_authenticated:
            # Update Redis to mark user as away
            if redis_client.get(f"away_user:{current_user.id}") is None:
                redis_client.set(f"away_user:{current_user.id}", "away")
                emit("update_online_status", {"status": "away"}, broadcast=True)
                redis_client.delete(f"online_user:{current_user.id}")
                print(f"[DEBUG] User {current_user.id} is now away.")

    @socketio.on("user_boot")
    def handle_user_boot():
        if current_user.is_authenticated:
            # Boot the user and remove them from Redis
            user_id = current_user.id
            redis_client.delete(f"away_user:{user_id}")
            # login_status_id = LoginStatus.query.filter_by(user_id=user_id).first()
            # if login_status_id:
            #     print("boot off user")
            # Boot user doesnt work for now, wip
            #     boot_user(user_id)
            print(f"[DEBUG] User {user_id} has been booted due to inactivity.")
            emit("update_online_status", {"status": "booted"}, broadcast=True)

    @socketio.on("disconnect")
    def handle_disconnect():
        if current_user.is_authenticated:
            # Remove user from Redis on disconnect
            user_id = current_user.id
            redis_client.delete(f"online_user:{user_id}")
            print(f"[DEBUG] User {user_id} has disconnected.")