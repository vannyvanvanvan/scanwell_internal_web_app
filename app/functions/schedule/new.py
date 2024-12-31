from datetime import datetime
from flask_login import current_user
from app.model import Schedule
from flask import render_template, flash
from sqlalchemy.exc import SQLAlchemyError
from app.model import db


def new_schedule_page() -> str:
    return render_template(
        "shipping_schedule.html",
        mode="Add",
        data=Schedule(
            cs="",
            week=datetime.now().isocalendar().week,
            carrier="",
            service="",
            mv="",
            pol="",
            pod="",
            routing="",
            cyopen=datetime.now(),
            sicutoff=datetime.now(),
            cycvcls=datetime.now(),
            etd=datetime.now(),
            eta=datetime.now(),
            owner=current_user.id,
        ),
    )


# Function to handle adding a new schedule
# if add successful return sch_id, else return -1
def new_schedule(form: dict) -> int:
    try:
        schedule_to_add = Schedule(
            cs=form["cs"],
            week=int(form["week"]),
            carrier=form["carrier"],
            service=form["service"],
            mv=form["mv"],
            pol=form["pol"],
            pod=form["pod"],
            routing=form["routing"],
            cyopen=datetime.strptime(form["cyopen"], "%Y-%m-%d"),
            sicutoff=datetime.strptime(
                "{year} {time}".format(
                    year=form["sicutoff"],
                    time=form["sicutoff_time"],
                ),
                "%Y-%m-%d %H:%M",
            ),
            cycvcls=datetime.strptime(
                "{year} {time}".format(
                    year=form["cycvcls"],
                    time=form["cycvcls_time"],
                ),
                "%Y-%m-%d %H:%M",
            ),
            etd=datetime.strptime(form["etd"], "%Y-%m-%d"),
            eta=datetime.strptime(form["eta"], "%Y-%m-%d"),
            owner=current_user.id,
        )
        db.session.add(schedule_to_add)
        db.session.commit()
        flash("Schedule added successfully!", "success")
        return schedule_to_add.sch_id
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return -1
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return -1
