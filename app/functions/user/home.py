from flask import flash, redirect, render_template, url_for
from flask_login import current_user, logout_user

from app.functions.searching import sort_schedules
from app.model import Schedule


def home_page() -> str:
    schedules = Schedule.query.all()
    sort_schedules(schedules)
    return render_template(
        "dashboard.html",
        results=schedules,
    )
