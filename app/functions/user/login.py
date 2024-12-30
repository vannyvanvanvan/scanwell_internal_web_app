from flask import flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import login_user
from wtforms.validators import InputRequired, Length

from app.hashing import hash_string
from app.model import User, db


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


def validate_login(form: LoginForm):

    # Pulling data from db to match with the request
    _form_username = form.request_username.data
    _form_password = form.request_password.data

    # Look for matching user in db
    matched_user = (
        db.session.execute(db.select(User).filter_by(username=_form_username))
        .scalars()
        .first()
    )

    if matched_user is None:
        flash("Invalid username or password, error message: 100")
        return render_template("login.html", login_detail=form)

    _password_hash = hash_string(_form_password)
    _remember_login = form.remember_me.data

    if (
        _form_username == matched_user.username
        and _password_hash == matched_user.password
    ):
        login_user(user=matched_user, remember=_remember_login)
        return redirect(url_for("user.user_home"))
    else:
        flash("Invalid username or password, error message: 101")
        return render_template("login.html", login_detail=form)


def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return validate_login(login_form)

    else:
        return render_template("login.html", login_detail=login_form)
