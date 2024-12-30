from datetime import datetime
from flask_login import current_user
from app.model import Schedule
from flask import request, flash
from sqlalchemy.exc import SQLAlchemyError
from driver import db

# Function to handle adding a new schedule
def add_schedule():
    try:
        new_schedule = Schedule(
                cs=request.form["cs"],
                week=int(request.form["week"]),
                carrier=request.form["carrier"],
                service=request.form["service"],
                mv=request.form["mv"],
                pol=request.form["pol"],
                pod=request.form["pod"],
                routing=request.form["routing"],
                cyopen=datetime.strptime(request.form["cyopen"], "%Y-%m-%d"),
                sicutoff=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["sicutoff"],
                        time=request.form["sicutoff_time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                cycvcls=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["cycvcls"],
                        time=request.form["cycvcls_time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                etd=datetime.strptime(request.form["etd"], "%Y-%m-%d"),
                eta=datetime.strptime(request.form["eta"], "%Y-%m-%d"),
                owner=current_user.id
        )
        db.session.add(new_schedule)
        db.session.commit()
        flash("Schedule added successfully!", "success")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return False