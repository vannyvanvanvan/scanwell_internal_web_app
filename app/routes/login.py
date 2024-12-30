from datetime import timedelta
from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import login_required, login_user, logout_user
from wtforms.validators import InputRequired, Length

from app.hashing import hash_string
from app.model import User, db

b_login = Blueprint(
    "b_login", __name__, template_folder="../templates", static_folder="../static"
)


# Create a login form
class LoginForm(FlaskForm):
    request_username = StringField(
        "Username",
        validators=[
            InputRequired("A username is required!"),
            Length(min=5, max=30, message="Must be between 5 and 10 characters."),
        ],
    )
    request_password = PasswordField(
        "Password", validators=[InputRequired("Password is required!")]
    )
    remember_me = BooleanField("Remember me")


@b_login.before_request
def make_session_permanent():
    session.permanent = True
    b_login.permanent_session_lifetime = timedelta(minutes=30)


@b_login.route("/", methods=["GET"])
def index():
    return redirect(url_for("b_login.login"))


@b_login.route("/login", methods=["GET", "POST"])
def login():

    login_detail = LoginForm()

    if login_detail.validate_on_submit():

        # Pulling data from db to match with the request
        _request_username = login_detail.request_username.data
        _request_password = login_detail.request_password.data
        user = db.session.execute(
            db.select(User).filter_by(username=_request_username)
        ).scalars().first()
        if user is None:
            # Added for debugging
            flash("Invalid username or password, error message: 100")
            return render_template("login.html", login_detail=login_detail)

        # Hashing the requested password
        hashed_request_password = hash_string(_request_password)

        # Debugging delete later
        # ----------------------------------------------------------------
        # print(user.username)
        # print(_request_username)
        # print(hashed_request_password)
        # print(user.password)
        # ----------------------------------------------------------------

        remember = login_detail.remember_me.data

        if user.password == hashed_request_password and user.username == _request_username:
            login_user(user, remember=remember)

            if user.rank == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif user.rank == "customer_service":
                return redirect(url_for("customer_service.customer_service_dashboard"))
            elif user.rank == "salesperson":
                return redirect(url_for("sales.sales_dashboard"))

        flash("Invalid username or password, error code: 101")
        return render_template("login.html", login_detail=login_detail)


@b_login.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("b_login.login"))
