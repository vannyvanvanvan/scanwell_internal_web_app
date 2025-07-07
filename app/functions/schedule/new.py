from flask import Response, redirect, render_template, flash, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.model import Schedule, db
from datetime import datetime

from app.functions.validate import (
    is_valid_schedule_form,
    now_or_valid_date,
    now_or_valid_datetime,
    now_or_valid_week,
)


def new_schedule_page() -> str:
    return render_template(
        "shipping_schedule.html",
        mode="add",
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
        ),
    )


def new_populated_schedule_page(form: dict) -> str:
    return render_template(
        "shipping_schedule.html",
        mode="add",
        data=Schedule(
            cs=form["cs"],
            week=now_or_valid_week(form["week"]),
            carrier=form["carrier"],
            service=form["service"],
            mv=form["mv"],
            pol=form["pol"],
            pod=form["pod"],
            routing=form["routing"],
            cyopen=now_or_valid_date(form["cyopen"]),
            sicutoff=now_or_valid_datetime(form["sicutoff"], form["sicutoff_time"]),
            cycvcls=now_or_valid_datetime(form["cycvcls"], form["cycvcls_time"]),
            etd=now_or_valid_date(form["etd"]),
            eta=now_or_valid_date(form["eta"]),
        ),
    )


# Function to handle adding a new schedule
# if add successful redirect to home with new schedule highlighted,
# if missing info return new schedule page with previously entered values,
# if backend error redirect to home with error messages
def create_schedule(form: dict) -> str | Response:

    # check validity of edited information
    if not is_valid_schedule_form(form):
        flash("Some of your changes are invalid. Please try again.", "danger")
        return new_populated_schedule_page(form)

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
        return redirect(
            url_for("user.user_home", highlighted_schedule=schedule_to_add.sch_id)
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
