from flask import flash, redirect, render_template, url_for
from flask_login import current_user, logout_user

from app.model import Schedule


def home_page():
    results=Schedule.query.all()
    return render_template("dashboard.html", current_user=current_user, results=results)