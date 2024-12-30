from datetime import timedelta
from flask import Blueprint, redirect, session, url_for
from flask_login import login_required, logout_user

from app.functions.user.login import login_page
from app.functions.user.logout import logout_page

user = Blueprint(
    "user", __name__, template_folder="../templates", static_folder="../static"
)


@user.before_request
def make_session_permanent():
    session.permanent = True
    user.permanent_session_lifetime = timedelta(minutes=30)


@user.route("/login", methods=["GET", "POST"])
def user_login():
    return login_page()


@user.route("/logout")
@login_required
def user_logout():
    return logout_page()

@user.route("/home")
@login_required
def user_home():
    return "home"
