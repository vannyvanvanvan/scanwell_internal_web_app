from flask import redirect, render_template, request, flash, url_for
from datetime import datetime
from werkzeug.exceptions import NotFound
from app.functions.schedule.new import new_populated_schedule_page
from app.model import Schedule, db

from sqlalchemy.exc import SQLAlchemyError
from app.functions.validate import (
    default_or_valid_date,
    default_or_valid_datetime,
    default_or_valid_week,
    is_valid_schedule_form,
)


# Schedule edit page when user clicked edit from user home
def edit_schedule_page(sch_id: int) -> str:

    # If schedule is found, return edit page with existing schedule information
    try:
        schedule = Schedule.query.get_or_404(sch_id)
        return render_template("shipping_schedule.html", mode="edit", data=schedule)

    # If schedule not found, return redirect to user home
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


# Schedule edit page when user submit invalid changes
def invalid_schedule_page(sch_id: int, form: dict) -> str:

    # If schedule is found, show edit page with valid proposed user changes,
    # invalid changes fall back to original info
    try:
        original_schedule = Schedule.query.get_or_404(sch_id)
        flash("Some of your changes are invalid. Please try again.", "danger")
        return render_template(
            "shipping_schedule.html",
            mode="edit",
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
    # If original schedule not found, return new schedule page with valid user changes,
    # invalid changes fall back to now
    except NotFound:
        flash(
            "The schedule you were trying to edit cannot be found. You can use this form to create a new schedule.",
            "primary",
        )
        return new_populated_schedule_page(form)


# Function to handle editing an existing schedule
def edit_schedule(sch_id: int):

    # check validity of edited information
    if not is_valid_schedule_form(request.form):
        return invalid_schedule_page(sch_id, request.form)

    # If input valid, find original schedule and update
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
        db.session.commit()
        flash("Schedule updated successfully!", "success")
        return edit_schedule_page(sch_id)
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database.",
            "primary",
        )
        return invalid_schedule_page(sch_id, request.form)
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
