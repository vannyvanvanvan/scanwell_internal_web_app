from datetime import datetime

from flask_login import current_user
from app.model import Schedule
from flask import request, flash
from sqlalchemy.exc import SQLAlchemyError
from driver import db

# Function to handle editing an existing schedule


def edit_schedule(sch_id):
    try:
        # Fetching by ID
        Schedule_data = Schedule.query.get_or_404(sch_id)

        Schedule_data.cs = request.form["cs"]
        Schedule_data.week = int(request.form["week"])
        Schedule_data.carrier = request.form["carrier"]
        Schedule_data.service = request.form["service"]
        Schedule_data.mv = request.form["mv"]
        Schedule_data.pol = request.form["pol"]
        Schedule_data.pod = request.form["pod"]
        Schedule_data.routing = request.form["routing"]
        Schedule_data.cyopen = datetime.strptime(
            request.form["cyopen"], "%Y-%m-%d"
        )
        Schedule_data.sicutoff = datetime.strptime(
            "{year} {time}".format(
                year=request.form["sicutoff"],
                time=request.form["sicutoff_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        Schedule_data.cycvcls = datetime.strptime(
            "{year} {time}".format(
                year=request.form["cycvcls"],
                time=request.form["cycvcls_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        Schedule_data.etd = datetime.strptime(
            request.form["etd"], "%Y-%m-%d")
        Schedule_data.eta = datetime.strptime(
            request.form["eta"], "%Y-%m-%d")
        Schedule_data.owner = current_user.id
        db.session.commit()
        flash("Schedule updated successfully!", "success")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return False
