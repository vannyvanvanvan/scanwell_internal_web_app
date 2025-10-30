from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Reserve, db
from app.functions.events import publish_update
from flask_login import current_user

def delete_reserve(rsv_id: int):
    try:
        reserve = Reserve.query.get_or_404(rsv_id)
        db.session.delete(reserve)
        db.session.commit()
        flash("Reserve deleted successfully!", "success")
        publish_update("reserve_changed", {"rsv_id": rsv_id, "spc_id": reserve.spc_id}, actor_id=current_user.id)
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
