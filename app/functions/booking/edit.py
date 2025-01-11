from flask import render_template, flash, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Booking, db

from app.functions.validate import (
    default_or_valid_number,
    is_checked_key,
    is_valid_booking_form,
)

def edit_booking_page(bk_id: int) -> str:
    try:
        booking = Booking.query.get_or_404(bk_id)
        return render_template("shipping_booking.html", mode="edit", data=booking)
    except NotFound:
        flash(
            "Booking not found, please try again. No changes were made to the database.",
            "primary",
        )
        return redirect(url_for("user.user_home"))

def invalid_booking_page(bk_id: int, form: dict) -> str:
    try:
        ChildProcessError = Booking.query.get_or_404(bk_id)
        flash("Some of your changes are invalid. Please try again.", "danger")
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
                saleprice=default_or_valid_number(original_booking.saleprice, form["saleprice"]),
                void=is_checked_key(form["void"]),
                remark=form["remark"],
            ),
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
        booking_to_edit.so = request.form["so"]
        booking_to_edit.findest = request.form["findest"]
        booking_to_edit.ct_cl = request.form["ct_cl"]
        booking_to_edit.shipper = request.form["shipper"]
        booking_to_edit.consignee = request.form["consignee"]
        booking_to_edit.term = request.form["term"]
        booking_to_edit.sales = request.form["sales"]
        booking_to_edit.saleprice = int(request.form["saleprice"])
        booking_to_edit.void = is_checked_key(request.form, "void")
        booking_to_edit.remark = request.form["remark"]
        db.session.commit()
        flash("Booking updated successfully!", "success")
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
    
       