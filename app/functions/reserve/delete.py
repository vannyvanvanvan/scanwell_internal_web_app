from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Reserve 
from app.model import db

def delete_reserve(rsv_id: int):
    try:
        reserve = Reserve.query.get_or_404(rsv_id)
        db.session.delete(reserve)
        db.session.commit()
        flash("Reserve deleted successfully!", "success")
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
