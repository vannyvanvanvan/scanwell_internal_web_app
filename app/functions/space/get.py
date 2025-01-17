from flask import render_template
from flask_login import current_user
from app.model import Space


def get_usable_spaces() -> list:
    return Space.query.filter(Space.spcstatus == "USABLE").all()


def space_list_page() -> str:
    return render_template(
        "available_space.html", current_user=current_user, spaces=get_usable_spaces()
    )
