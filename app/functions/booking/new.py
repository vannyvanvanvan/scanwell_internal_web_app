from app.functions.booking.action import pending_booking
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.model import Booking, Space, db
from app.functions.validate import (
    is_checked_key,
    is_valid_booking_form,
    zero_or_valid_number,
)


def new_booking_page(spc_id: int) -> str:
    return render_template(
        "shipping_booking.html",
        mode="add",
        data=Booking(
            spc_id=spc_id,
            so="",
            findest="",
            ct_cl="",
            shipper="",
            consignee="",
            term="",
            sales="",
            saleprice=0,
            void=False,
            remark="",
        ),
    )
    
def new_populated_booking_page(form: dict, spc_id: int) -> str:
    return render_template(
        "shipping_booking.html",
        mode="add",
        data=Booking(
            spc_id=spc_id,
            so=form["so"],
            findest=form["findest"],
            ct_cl=form["ct_cl"],
            shipper=form["shipper"],
            consignee=form["consignee"],
            term=form["term"],
            sales=form["sales"],
            saleprice=zero_or_valid_number(form["saleprice"]),
            void=form.get("void", ""),
            remark=form["remark"],
        ),
    )
    
def create_booking(form: dict, spc_id: int) -> int:
    if not is_valid_booking_form(form):
        flash("Some inputs are invalid. Please try again.", "danger")
        return new_populated_booking_page(form, spc_id)

    try:
        if not pending_booking(spc_id):
     
            flash('Failed to update space status', 'danger')
            return -1
        
        space=Space.query.get(spc_id)

        new_booking = Booking(
            spc_id=spc_id,
            so=form["so"],
            findest=form["findest"],
            ct_cl=form["ct_cl"],
            shipper=form["shipper"],
            consignee=form["consignee"],
            term=form["term"],
            sales=int(form["sales"]),
            saleprice=int(form["saleprice"]),
            void=is_checked_key(form, "void"),
            remark=form["remark"],
            owner=current_user.id,
        )
        db.session.add(new_booking)
        
        db.session.commit()
        flash("Booking created successfully!", "success")
        return redirect(
            url_for(
                "user.user_home",
                highlighted_schedule=space.sch_id,
                highlighted_space=space.spc_id,
                highlighted_booking=new_booking.bk_id,
            )
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return -1
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return -1