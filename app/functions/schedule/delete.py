from app.model import Schedule
from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from driver import db

# Function to handle deleting a schedule
def delete_schedule(sch_id):
    try:
        schedule = Schedule.query.get_or_404(sch_id)

        db.session.delete(schedule)
        db.session.commit()
        flash("Schedule deleted successfully!", "success")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False
