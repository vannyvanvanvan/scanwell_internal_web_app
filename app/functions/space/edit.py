from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Space, Booking, db
from datetime import datetime

from app.functions.validate import (
    default_or_valid_date,
    default_or_valid_number,
    is_checked_key,
    is_valid_space_form,
)


def has_confirmed_booking(spc_id: int) -> bool:
    # Check if space has any confirmed booking that is not void
    confirmed_bookings = Booking.query.filter_by(
        spc_id=spc_id, 
        void=False
    ).join(Space).filter(
        Space.spcstatus == 'BK_CONFIRM'
    ).all()
    return len(confirmed_bookings) > 0

def edit_space_page(spc_id: int) -> str:
    try:
        space = Space.query.get_or_404(spc_id)
        
        # Check if space has confirmed booking
        if has_confirmed_booking(spc_id):
            flash(
                "Cannot edit space with confirmed booking. Please void the booking first through Edit Booking.",
                "warning",
            )
            return redirect(url_for("user.user_home"))
            
        return render_template("shipping_space.html", mode="edit", data=space)
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def invalid_space_page(spc_id: int, form: dict) -> str:
    try:
        original_space = Space.query.get_or_404(spc_id)
        flash("Some of your changes are invalid. Please try again.", "danger")
        return render_template(
            "shipping_space.html",
            mode="edit",
            data=Space(
                size=form["size"],
                avgrate=default_or_valid_number(
                    original_space.avgrate, form["avgrate"]
                ),
                sugrate=default_or_valid_number(
                    original_space.sugrate, form["sugrate"]
                ),
                ratevalid=default_or_valid_date(
                    original_space.ratevalid, form["ratevalid"]
                ),
                proport=is_checked_key(form["proport"]),
                spcstatus=form["spcstatus"],
            ),
        )

    except NotFound:
        flash(
            "The space you were trying to edit cannot be found. You can use this form to create a new schedule.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def edit_space(spc_id: int) -> str:

    if not is_valid_space_form(request.form):
        return invalid_space_page(spc_id, request.form)

    try:
        space_to_edit = Space.query.get_or_404(spc_id)
        
        # Check if space has confirmed booking
        if has_confirmed_booking(spc_id):
            flash(
                "Cannot edit space with confirmed booking, please void the booking first through Edit Booking.",
                "warning",
            )
            return redirect(url_for("user.user_home"))
        space_to_edit.size = request.form["size"]
        space_to_edit.avgrate = int(request.form["avgrate"])
        space_to_edit.sugrate = int(request.form["sugrate"])
        space_to_edit.ratevalid = datetime.strptime(
            request.form["ratevalid"], "%Y-%m-%d"
        )
        space_to_edit.proport = is_checked_key(request.form, "proport")
        space_to_edit.spcstatus = request.form["spcstatus"]
        space_to_edit.last_modified_by = current_user.id
        db.session.commit()
        flash("Space updated successfully!", "success")
        return redirect(url_for("space.space_edit", spc_id=spc_id))
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database.",
            "primary",
        )
        return invalid_space_page(spc_id, request.form)
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
