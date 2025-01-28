from flask_socketio import emit
from flask_login import current_user
from datetime import timedelta
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def mark_user_online(user_id, ip):
    # Check if user is already marked as online to avoid redundant updates
    if redis_client.get(f"online_user:{user_id}") is None:
        redis_client.setex(f"online_user:{user_id}", int(timedelta(minutes=10).total_seconds()), ip)
    redis_client.delete(f"away_user:{user_id}")  

def set_user_away(user_id):
    # Check if user is already away to avoid redundant updates
    if redis_client.get(f"away_user:{user_id}") is None:
        redis_client.setex(f"away_user:{user_id}", int(timedelta(minutes=5).total_seconds()), "away")
    redis_client.delete(f"online_user:{user_id}") 
        
def mark_user_offline(user_id):
    redis_client.delete(f"online_user:{user_id}")
    redis_client.delete(f"away_user:{user_id}")

def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        if current_user.is_authenticated:
            mark_user_online(current_user.get_id(), "WebSocket")
            emit("update_online_status", {"status": "online"}, broadcast=True)
        print(f"[DEBUG] User {current_user.get_id()} connected.")

    @socketio.on("disconnect")
    def handle_disconnect():
        if current_user.is_authenticated:
            mark_user_offline(current_user.get_id())
            emit("update_online_status", {"status": "offline"}, broadcast=True)
        print(f"[DEBUG] User {current_user.get_id()} disconnected.")

    @socketio.on("user_away")
    def handle_user_away():
        if current_user.is_authenticated:
            set_user_away(current_user.get_id())
            emit("update_online_status", {"status": "away"}, broadcast=True)
        print(f"[DEBUG] User {current_user.get_id()} is now away.")

    @socketio.on("user_active")
    def handle_user_active():
        if current_user.is_authenticated:
            mark_user_online(current_user.get_id(), "WebSocket")
            emit("update_online_status", {"status": "online"}, broadcast=True)
        print(f"[DEBUG] User {current_user.get_id()} is now active.")
