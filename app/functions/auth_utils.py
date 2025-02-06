from datetime import datetime, timedelta
from flask import flash
from flask_login import logout_user
from app.model import db, LoginStatus
import redis


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Check if the user is locked and prevent login if locked
def is_locked(user_id):    
    login_status_user_id = LoginStatus.query.filter_by(user_id=user_id).first()

    if not login_status_user_id:
        login_status_user_id = LoginStatus(user_id=user_id, status="unlocked", failed_attempts=0)
        db.session.add(login_status_user_id)
        db.session.commit()
        
    if login_status_user_id.lock_status == "timedout":
        print(login_status_user_id.locked_until)
        print(datetime.utcnow())
        if login_status_user_id.locked_until and datetime.utcnow() < login_status_user_id.locked_until:
            flash(f"Account is locked until {login_status_user_id.locked_until}.", "danger")
            return True
        elif login_status_user_id.locked_until and datetime.utcnow() >= login_status_user_id.locked_until and login_status_user_id.failed_attempts >= 3:
            # Unlock user if the lock time has passed
            print("Unlocking user")
            login_status_user_id.lock_status = "unlocked"
            login_status_user_id.locked_until = None
            db.session.commit()
    
    
    
    return False

# Increase the failed attempts and set lockout counter
def handle_failed_attempts(login_status_user_id: LoginStatus):
    
    if login_status_user_id.lock_status == "unlocked":
        login_status_user_id.failed_attempts += 1 
        if login_status_user_id.failed_attempts >= 9:
            # Permanent lock
            login_status_user_id.locked_until = None
            flash("Your account has been permanently locked. Please contact the admin.", "danger")
            login_status_user_id.lock_status = "locked"
        elif login_status_user_id.failed_attempts == 6:
            login_status_user_id.locked_until = datetime.utcnow() + timedelta(minutes=10)
            flash("Too many failed attempts. Account locked for 10 minutes.", "danger")
            login_status_user_id.lock_status = "timedout"
        elif login_status_user_id.failed_attempts == 3:
            login_status_user_id.locked_until = datetime.utcnow() + timedelta(minutes=5)
            flash("Too many failed attempts. Account locked for 5 minutes.", "warning")
            login_status_user_id.lock_status = "timedout"

    db.session.commit()

# Unlock the user account (Admin ONLY)
def unlock_user(login_status_user_id: LoginStatus):
    login_status_user_id.failed_attempts = 0
    login_status_user_id.locked_until = None
    login_status_user_id.lock_status = "unlocked"
    db.session.commit()
    
# Reset the failed attempts
def reset_failed_attempts(login_status_user_id: LoginStatus):
    login_status_user_id.failed_attempts = 0
    db.session.commit()

def lock_user(login_status_user_id: LoginStatus):
    login_status_user_id.failed_attempts = 9
    login_status_user_id.locked_until = None
    login_status_user_id.lock_status = "locked"
    db.session.commit()
    
def boot_user(login_status_user_id: LoginStatus):
    login_status_user_id.failed_attempts = 0
    login_status_user_id.locked_until = None
    login_status_user_id.lock_status = "unlocked"
    login_status_user_id.last_logoff = datetime.utcnow()
    db.session.commit()
    logout_user()