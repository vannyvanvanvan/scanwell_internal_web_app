from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user, logout_user
from app.model import db

def logout_page():
    # Update last logout time
    if current_user.is_authenticated:
        if current_user.login_status:
            current_user.login_status.last_logoff = datetime.utcnow()
            db.session.commit()
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("user.user_login"))
