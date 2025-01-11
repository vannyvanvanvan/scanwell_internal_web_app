from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Space
from app.model import db


def delete_space(spc_id: int) -> None:
    try:
        space = Space.query.get_or_404(spc_id)
        db.session.delete(space)
        db.session.commit()
        flash("Space deleted successfully!", "success")
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
