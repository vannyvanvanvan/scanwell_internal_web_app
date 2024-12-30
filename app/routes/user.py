from datetime import timedelta
from flask import Blueprint, redirect, session, url_for
from flask_login import login_required, logout_user

from app.functions.user.login import show_login_form

user = Blueprint(
    "user", __name__, template_folder="../templates", static_folder="../static"
)


@user.before_request
def make_session_permanent():
    session.permanent = True
    user.permanent_session_lifetime = timedelta(minutes=30)


@user.route("/login", methods=["GET", "POST"])
def user_login():
    return show_login_form()


@user.route("/logout")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for("user.login"))

@user.route("/home")
@login_required
def user_home():
    return "home"
