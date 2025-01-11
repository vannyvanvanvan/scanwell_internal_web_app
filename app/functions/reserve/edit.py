from flask import render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.functions.validate import (
    default_or_valid_date,
    default_or_valid_number,
    is_checked_key,
    is_valid_reserve_form,
)
from app.model import Reserve, db
from datetime import datetime
from werkzeug.exceptions import NotFound


def edit_reserve_page(rsv_id: int) -> str:
    try:
        reserve = Reserve.query.get_or_404(rsv_id)
        return render_template("shipping_reserve.html", mode="edit", data=reserve)
    except NotFound:
        flash(
            "Space not found, please try again. No changes were made to the database.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def invalid_reserve_page(rsv_id: int, form: dict) -> str:
    try:
        original_reserve = Reserve.query.get_or_404(rsv_id)
        flash("Some of your changes are invalid. Please try again.", "danger")
        return render_template(
            "shipping_reserve.html",
            mode="edit",
            data=Reserve(
                sales=form["sales"],
                saleprice=default_or_valid_number(
                    original_reserve.saleprice, form["saleprice"]
                ),
                rsv_date=default_or_valid_date(
                    original_reserve.rsv_date, form["rsv_date"]
                ),
                cfm_date=default_or_valid_date(
                    original_reserve.cfm_date, form["cfm_date"]
                ),
                cfm_cs=form["cfm_cs"],
                void=is_checked_key(form["void"]),
                remark=form["remark"],
            ),
        )

    except NotFound:
        flash(
            "The reserve you were trying to edit cannot be found. You can use this form to create a new schedule.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def edit_reserve(rsv_id: int, form: dict):
    if not is_valid_reserve_form(request.form):

        # Do we need to add feedback for error
        # flash("Some inputs are invalid. Please try again.", "danger")

        return invalid_reserve_page(rsv_id, request.form)
    try:
        reserve_to_edit = Reserve.query.get_or_404(rsv_id)
        reserve_to_edit.sales = request.form["sales"]
        reserve_to_edit.saleprice = int(request.form["saleprice"])
        reserve_to_edit.rsv_date = datetime.strptime(
            request.form["rsv_date"], "%Y-%m-%d"
        )
        reserve_to_edit.cfm_date = datetime.strptime(
            request.form["cfm_date"], "%Y-%m-%d"
        )
        reserve_to_edit.cfm_cs = request.form["cfm_cs"]

        # wait edit later
        reserve_to_edit.void = is_checked_key(request.form, "void")

        reserve_to_edit.remark = request.form["remark"]
        db.session.commit()
        flash("Reserve updated successfully!", "success")
        return redirect(url_for("reserve.reserve_edit", rsv_id=rsv_id))

    except NotFound:
        flash(
            "Reserve not found, please try again. No changes were made to the database.",
            "primary",
        )
        return invalid_reserve_page(rsv_id, request.form)
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return redirect(url_for("user.user_home"))
