from flask import flash, redirect, url_for
from flask_login import logout_user


def logout_page():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("user.user_login"))
