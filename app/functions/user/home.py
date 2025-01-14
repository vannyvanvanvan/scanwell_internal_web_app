from flask import render_template
from flask_login import current_user

from app.functions.searching import sort_schedules
from app.model import Reserve, Schedule


def home_page() -> str:
    schedules = Schedule.query.all()
    sort_schedules(schedules)
    return render_template(
        "home_page.html",
        current_user=current_user,
        results=schedules,
    )


def sales_home_page() -> str:
    print(current_user.id)
    reserves = Reserve.query.filter(Reserve.owner == 1).all()
    print(reserves)
    return render_template(
        "home_page.html",
        current_user=current_user,
        reserves=reserves,
    )
