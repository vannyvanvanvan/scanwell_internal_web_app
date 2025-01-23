from flask_socketio import emit
from flask_login import current_user
from datetime import datetime, timedelta
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def mark_user_online(user_id, ip):
    redis_client.setex(f"online_user:{user_id}", timedelta(minutes=10), ip)
    
# def set_user_away(user_id):
#     redis_client.setex(f"away_user:{user_id}", timedelta(minutes=3), "away")

def mark_user_offline(user_id):
    redis_client.delete(f"online_user:{user_id}")
    redis_client.delete(f"away_user:{user_id}")

def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        print(f"[DEBUG] User {current_user.get_id()} connected.")
        if current_user.is_authenticated:
            mark_user_online(current_user.get_id(), "WebSocket")
            emit("update_online_status", {"status": "online"}, broadcast=True)

    @socketio.on("disconnect")
    def handle_disconnect():
        if current_user.is_authenticated:
            mark_user_offline(current_user.get_id())
            print(f"User {current_user.get_id()} disconnected.")
            emit("update_online_status", {"status": "offline"}, broadcast=True)

    # @socketio.on("user_away")
    # def handle_user_away():
    #     if current_user.is_authenticated:
    #         set_user_away(current_user.get_id())
    #         emit("update_online_status", {"status": "away"}, broadcast=True)
    #     print(f"[DEBUG] User {current_user.get_id()} is now away.")

    # @socketio.on("user_active")
    # def handle_user_active():
    #     if current_user.is_authenticated:
    #         mark_user_online(current_user.get_id(), "WebSocket")
    #         emit("update_online_status", {"status": "online"}, broadcast=True)
    #     print(f"[DEBUG] User {current_user.get_id()} is now active.")