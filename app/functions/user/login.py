from datetime import datetime
from flask import flash, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import login_user
from wtforms.validators import InputRequired, Length
from sqlalchemy.orm import joinedload

from app.functions.auth_utils import handle_failed_attempts, is_locked, reset_failed_attempts
from app.functions.hashing import hash_string
from app.model import User, db, LoginStatus


class LoginForm(FlaskForm):
    request_username = StringField(
        "Username",
        validators=[
            InputRequired("A username is required!"),
            Length(min=5, max=30, message="Must be between 5 and 30 characters."),
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
        db.session.query(User)
        .options(joinedload(User.role), joinedload(User.login_status))
        .filter_by(username=_form_username)
        .first()
    )

    if matched_user is None:
        flash("Invalid username or password", "danger")
        return render_template("login.html", login_detail=form)
    
    if is_locked(matched_user.id):
        return render_template("login.html", login_detail=form)
    
    _password_hash = hash_string(_form_password)
    _remember_login = form.remember_me.data

    print(_form_username)
    print(matched_user.username)
    print(_password_hash)
    print(matched_user.password)
    print(matched_user.login_status)

    # Check if user is locked
    if matched_user.login_status.lock_status == 'locked':
        is_locked(matched_user.id)
        flash('Account is locked. Try again later or contact admin.', 'danger')
        return render_template("login.html", login_detail=form)

    # Successful login
    elif _form_username == matched_user.username and _password_hash == matched_user.password and matched_user.login_status.lock_status == "unlocked":

        if matched_user.login_status:
            # Update last login time
            matched_user.login_status.last_login = datetime.utcnow()
            reset_failed_attempts(matched_user.login_status)
            db.session.commit()
            # Added to ensure session is permanent
            session.permanent = True
        print("Logged in")
        login_user(user=matched_user, remember=_remember_login)
        return redirect(url_for("user.user_home"))
    else:
        print("Failed login")
        handle_failed_attempts(matched_user.login_status)
        flash("Invalid username or password", "danger")

        return render_template("login.html", login_detail=form)


def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return validate_login(login_form)

    else:
        return render_template("login.html", login_detail=login_form)
