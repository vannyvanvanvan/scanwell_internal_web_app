from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.functions.user.get import get_all_users_tuple_list
from app.model import Booking, Reserve, Space, db
from datetime import datetime

from app.functions.validate import (
    default_or_valid_number,
    is_checked_key,
    is_valid_booking_form,
)


def edit_booking_page(bk_id: int) -> str:
    try:
        booking = Booking.query.get_or_404(bk_id)
        return_to_confirm = request.args.get('return_to_confirm', '0')
        
        return render_template(
            "shipping_booking.html",
            mode="edit",
            data=booking,
            users_tuple_list=get_all_users_tuple_list(),
            return_to_confirm=return_to_confirm,
        )
    except NotFound:
        flash(
            "Booking not found, please try again. No changes were made to the database.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def invalid_booking_page(bk_id: int, form: dict) -> str:
    try:
        original_booking = Booking.query.get_or_404(bk_id)
        flash("Some of your changes are invalid. Please try again.", "danger")
        return_to_confirm = form.get('return_to_confirm', '0')
        
        return render_template(
            "shipping_booking.html",
            mode="edit",
            data=Booking(
                so=form["so"],
                findest=form["findest"],
                ct_cl=form["ct_cl"],
                shipper=form["shipper"],
                consignee=form["consignee"],
                term=form["term"],
                sales=form["sales"],
                saleprice=default_or_valid_number(
                    original_booking.saleprice, form["saleprice"]
                ),
                void=is_checked_key(form["void"]),
                remark=form["remark"],
            ),
            users_tuple_list=get_all_users_tuple_list(),
            return_to_confirm=return_to_confirm,
        )

    except NotFound:
        flash(
            "The booking you were trying to edit cannot be found. You can use this form to create a new schedule.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def edit_booking(bk_id: int) -> str:
    if not is_valid_booking_form(request.form):
        return invalid_booking_page(bk_id, request.form)
    try:
        booking_to_edit = Booking.query.get_or_404(bk_id)
        space = booking_to_edit.space
        is_confirmed = space.spcstatus == 'BK_CONFIRM'
        
        # Handle void for confirmed bookings
        if is_confirmed and is_checked_key(request.form, "void"):
            new_space_status = request.form.get("void_space_status", "BK_CANCEL")
            if new_space_status not in ["BK_CANCEL", "USABLE"]:
                flash("Invalid space status for void operation. Please select BK_CANCEL or USABLE.", "danger")
                return redirect(url_for("booking.booking_edit", bk_id=bk_id))
            
            # Update space status based on void
            space.spcstatus = new_space_status
            space.last_modified_by = current_user.id
            space.last_modified_at = datetime.utcnow() 
            # Check if space should marked as INVALID
            if new_space_status == "USABLE":
                # Check if space is still within the rate validity
                if space.ratevalid < datetime.utcnow():
                    space.spcstatus = "INVALID"
                    flash("Space marked as INVALID due to expired rate validity.")
        
        booking_to_edit.so = request.form["so"]
        booking_to_edit.findest = request.form["findest"]
        booking_to_edit.ct_cl = request.form["ct_cl"]
        booking_to_edit.shipper = request.form["shipper"]
        booking_to_edit.consignee = request.form["consignee"]
        booking_to_edit.term = request.form["term"]
        booking_to_edit.sales = int(request.form["sales"])
        booking_to_edit.saleprice = int(request.form["saleprice"])
        # Only update void field if it exists in the form
        if "void" in request.form:
            booking_void = is_checked_key(request.form, "void")
            booking_to_edit.void = booking_void
            # If booking is set to void also set reserves on the same space to void
            if booking_void:
                reserves = Reserve.query.filter_by(spc_id=booking_to_edit.spc_id).all()
                for reserve in reserves:
                    print("test")
                    reserve.void = True
                    
        booking_to_edit.remark = request.form["remark"]
        db.session.commit()
        flash("Booking updated successfully!", "success")
        
        if request.form.get('return_to_confirm') == '1':
            return redirect(url_for("booking.booking_confirm", bk_id=bk_id))
        
        return redirect(url_for("booking.booking_edit", bk_id=bk_id))

    except NotFound:
        flash(
            "Booking not found, please try again. No changes were made to the database.",
            "primary",
        )
        return invalid_booking_page(bk_id, request.form)
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
