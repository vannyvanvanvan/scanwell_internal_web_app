from flask import render_template
from flask_login import current_user
from app.functions.schedule.get import get_schedule_pol_pod_etd
from app.model import Space


def get_usable_spaces() -> list:
    usable_spaces = Space.query.filter(Space.spcstatus == "USABLE").all()

    # Need to accompany usable spaces with scheduled POL, POD, ETD
    results = []
    for space in usable_spaces:
        schedule = get_schedule_pol_pod_etd(space.sch_id)
        results.append([schedule, space])
    return results


def space_list_page() -> str:
    return render_template(
        "available_space.html", current_user=current_user, spaces=get_usable_spaces()
    )
