from datetime import timedelta
from flask import Blueprint, session
from flask_login import current_user, current_user, login_required

from app.functions.auth_utils import boot_user
from app.functions.user.home import home_page
from app.functions.user.login import login_page
from app.functions.user.logout import logout_page
from app.model import db, LoginStatus

user_routes = Blueprint(
    "user", __name__, template_folder="../templates", static_folder="../static"
)


@user_routes.before_request
def make_session_permanent():
    # I don't think this is needed
    # session.permanent = True
    # user_routes.permanent_session_lifetime = timedelta(minutes=30)
    if current_user.is_authenticated:
        login_status = LoginStatus.query.filter_by(user_id=current_user.id).first()
        if login_status:
            boot_user(login_status)


@user_routes.route("/login", methods=["GET", "POST"])
def user_login():
    return login_page()


@user_routes.route("/logout")
@login_required
def user_logout():
    return logout_page()


@user_routes.route("/home")
@login_required
def user_home():
    return home_page()


