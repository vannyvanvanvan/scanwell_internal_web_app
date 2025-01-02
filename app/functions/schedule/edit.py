from datetime import datetime
from werkzeug.exceptions import NotFound

from flask_login import current_user
from app.functions.schedule.validate import (
    default_or_valid_date,
    default_or_valid_datetime,
    default_or_valid_week,
    is_valid_date,
    now_or_valid_date,
    now_or_valid_datetime,
    now_or_valid_week,
)
from app.model import Schedule
from flask import redirect, render_template, request, flash, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.model import db


def edit_schedule_page(sch_id: int) -> str:
    try:
        schedule = Schedule.query.get_or_404(sch_id)
        return render_template("shipping_schedule.html", mode="Edit", data=schedule)
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database."
        )
        return redirect(url_for("user.user_home"))


def edit_invalid_schedule_page(sch_id: int, form: dict) -> str:
    try:
        original_schedule = Schedule.query.get_or_404(sch_id)
        return render_template(
            "shipping_schedule.html",
            mode="Add",
            data=Schedule(
                cs=form["cs"],
                week=default_or_valid_week(original_schedule.week, form["week"]),
                carrier=form["carrier"],
                service=form["service"],
                mv=form["mv"],
                pol=form["pol"],
                pod=form["pod"],
                routing=form["routing"],
                cyopen=default_or_valid_date(original_schedule.cyopen, form["cyopen"]),
                sicutoff=default_or_valid_datetime(
                    original_schedule.sicutoff, form["sicutoff"], form["sicutoff_time"]
                ),
                cycvcls=default_or_valid_datetime(
                    original_schedule.sicutoff, form["cycvcls"], form["cycvcls_time"]
                ),
                etd=default_or_valid_date(original_schedule.cyopen, form["etd"]),
                eta=default_or_valid_date(original_schedule.cyopen, form["eta"]),
            ),
        )
    except NotFound:
        return render_template(
            "shipping_schedule.html",
            mode="Add",
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


# Function to handle editing an existing schedule
def edit_schedule(sch_id: int):
    try:
        # Fetching by ID
        schedule_to_edit = Schedule.query.get_or_404(sch_id)

        schedule_to_edit.cs = request.form["cs"]
        schedule_to_edit.week = int(request.form["week"])
        schedule_to_edit.carrier = request.form["carrier"]
        schedule_to_edit.service = request.form["service"]
        schedule_to_edit.mv = request.form["mv"]
        schedule_to_edit.pol = request.form["pol"]
        schedule_to_edit.pod = request.form["pod"]
        schedule_to_edit.routing = request.form["routing"]
        schedule_to_edit.cyopen = datetime.strptime(request.form["cyopen"], "%Y-%m-%d")
        schedule_to_edit.sicutoff = datetime.strptime(
            "{year} {time}".format(
                year=request.form["sicutoff"],
                time=request.form["sicutoff_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        schedule_to_edit.cycvcls = datetime.strptime(
            "{year} {time}".format(
                year=request.form["cycvcls"],
                time=request.form["cycvcls_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        schedule_to_edit.etd = datetime.strptime(request.form["etd"], "%Y-%m-%d")
        schedule_to_edit.eta = datetime.strptime(request.form["eta"], "%Y-%m-%d")
        schedule_to_edit.owner = current_user.id
        db.session.commit()
        flash("Schedule updated successfully!", "success")
        return True
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database."
        )
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return False
