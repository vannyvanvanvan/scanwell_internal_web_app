from flask import request
from flask_socketio import SocketIO, emit
from flask_login import current_user
from app.model import db, LoginStatus

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        try:
            login_status = LoginStatus.query.filter_by(user_id=current_user.id).first()
            if not login_status:
                login_status = LoginStatus(user_id=current_user.id, status="online", ip_connected=request.remote_addr)
                db.session.add(login_status)
            # Prevent overriding away status
            elif login_status.status != "away":
                login_status.status = "online"
                login_status.ip_connected = request.remote_addr
            db.session.commit()
            print(f"User {current_user.username} connected. Status: {login_status.status}")
        except Exception as e:
            print(f"Error updating user status: {e}")

@socketio.on('user_status')
def handle_status(data):
    if current_user.is_authenticated:
        try:
            status = data.get("status")
            login_status = LoginStatus.query.filter_by(user_id=current_user.id).first()
            
            if login_status:
                login_status.status = status
                db.session.commit()
            
            print(f"User {current_user.username} status updated to: {status}")
        except Exception as e:
            print(f"Error updating user status: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        try:
            login_status = LoginStatus.query.filter_by(user_id=current_user.id).first()
             
            login_status.status = "offline"
            db.session.commit()
            print(f"User {current_user.username} disconnected.")
        except Exception as e:
            print(f"Error updating user status on disconnect: {e}")
