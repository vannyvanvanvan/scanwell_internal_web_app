from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Booking, db

def delete_booking(sch_id: int) -> None:
    try:
        booking = Booking.query.get_or_404(sch_id)
        db.session.delete(booking)
        db.session.commit()
        flash("Booking deleted successfully!", "success")
    except NotFound:
        flash(
            "Booking not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")