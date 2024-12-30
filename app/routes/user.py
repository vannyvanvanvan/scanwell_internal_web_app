from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

user = Blueprint(
    "user", __name__, template_folder="../templates", static_folder="../static"
)


@user.route("/login", methods=["GET", "POST"])
def login():
    pass


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))
