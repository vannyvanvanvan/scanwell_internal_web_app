from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Schedule, db
from app.functions.events import publish_update
from flask_login import current_user


# Function to handle deleting a schedule
def delete_schedule(sch_id: int) -> None:
    try:
        schedule = Schedule.query.get_or_404(sch_id)
        db.session.delete(schedule)
        db.session.commit()
        flash("Schedule deleted successfully!", "success")
        publish_update("schedule_changed", {"sch_id": sch_id}, actor_id=current_user.id)
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
