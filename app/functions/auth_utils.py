from datetime import datetime, timedelta

from flask import flash
import redis
from app.model import db, LoginStatus

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Check if the user is locked and prevent login if locked
def is_locked(user_id):    
    login_status = LoginStatus.query.filter_by(user_id=user_id).first()

    if not login_status:
        login_status = LoginStatus(user_id=user_id, status="unlocked", failed_attempts=0)
        db.session.add(login_status)
        db.session.commit()
        
    if login_status.lock_status == "timedout":
        print(login_status.locked_until)
        print(datetime.utcnow())
        if login_status.locked_until and datetime.utcnow() < login_status.locked_until:
            flash(f"Account is locked until {login_status.locked_until}.", "danger")
            return True
        elif login_status.locked_until and datetime.utcnow() >= login_status.locked_until and login_status.failed_attempts >= 3:
            # Unlock user if the lock time has passed
            print("Unlocking user")
            login_status.lock_status = "unlocked"
            login_status.locked_until = None
            db.session.commit()
    
    
    
    return False

# Increase the failed attempts and set lockout counter
def handle_failed_attempts(login_status: LoginStatus):
    
    if login_status.lock_status == "unlocked":
        login_status.failed_attempts += 1 
        if login_status.failed_attempts >= 9:
            # Permanent lock
            login_status.locked_until = None
            flash("Your account has been permanently locked. Please contact the admin.", "danger")
            login_status.lock_status = "locked"
        elif login_status.failed_attempts == 6:
            login_status.locked_until = datetime.utcnow() + timedelta(minutes=0.09)
            flash("Too many failed attempts. Account locked for 10 minutes.", "danger")
            login_status.lock_status = "timedout"
        elif login_status.failed_attempts == 3:
            login_status.locked_until = datetime.utcnow() + timedelta(minutes=0.04)
            flash("Too many failed attempts. Account locked for 5 minutes.", "warning")
            login_status.lock_status = "timedout"

    db.session.commit()

# Unlock the user account (Admin ONLY)
def unlock_user(login_status: LoginStatus):
    login_status.failed_attempts = 0
    login_status.locked_until = None
    login_status.lock_status = "unlocked"
    db.session.commit()
    
# Reset the failed attempts
def reset_failed_attempts(login_status: LoginStatus):
    login_status.failed_attempts = 0
    db.session.commit()

def lock_user(login_status: LoginStatus):
    login_status.failed_attempts = 9
    login_status.locked_until = None
    login_status.lock_status = "locked"
    db.session.commit()
    
def boot_user(login_status: LoginStatus):
    login_status.failed_attempts = 0
    login_status.locked_until = None
    login_status.lock_status = "unlocked"
    db.session.commit()
    
def is_user_online(user_id):
    # Check if the user is online from Redis instead of the database
    return redis_client.exists(f"online_user:{user_id}")

def set_user_online(user_id, ip):
    # Mark user as online in Redis
    redis_client.setex(f"online_user:{user_id}", timedelta(minutes=5), ip)

def set_user_away(user_id):
    # Mark user as away but still trackable
    redis_client.setex(f"away_user:{user_id}", timedelta(minutes=2), "away")

def remove_user_online(user_id):
    # Remove user from Redis when they go offline
    redis_client.delete(f"online_user:{user_id}")
    redis_client.delete(f"away_user:{user_id}")