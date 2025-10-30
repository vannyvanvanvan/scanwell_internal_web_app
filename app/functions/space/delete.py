from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Space, db
from app.functions.events import publish_update
from flask_login import current_user


def delete_space(spc_id: int) -> None:
    try:
        space = Space.query.get_or_404(spc_id)
        db.session.delete(space)
        db.session.commit()
        flash("Space deleted successfully!", "success")
        publish_update("space_changed", {"spc_id": spc_id, "sch_id": space.sch_id}, actor_id=current_user.id)
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
