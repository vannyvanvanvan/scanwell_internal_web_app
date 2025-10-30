from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from app.model import Reserve, db
from app.functions.events import publish_update
from datetime import datetime

from app.functions.validate import (
    default_or_valid_date,
    default_or_valid_number,
    is_checked_key,
    is_valid_reserve_form,
)


def edit_reserve_page(rsv_id: int) -> str:
    try:
        reserve = Reserve.query.get_or_404(rsv_id)
        
        # Pass user role to template to control field editing
        is_sales_user = current_user.role.rank == "sales"
        
        return render_template(
            "shipping_reserve.html", 
            mode="edit", 
            data=reserve,
            is_sales_user=is_sales_user
        )
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
        
        # Pass user role to template to control field editing
        is_sales_user = current_user.role.rank == "sales"
        
        return render_template(
            "shipping_reserve.html",
            mode="edit",
            data=Reserve(
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
            is_sales_user=is_sales_user,
        )

    except NotFound:
        flash(
            "The reserve you were trying to edit cannot be found. You can use this form to create a new schedule.",
            "primary",
        )
        return redirect(url_for("user.user_home"))


def edit_reserve(rsv_id: int) -> str:
    if not is_valid_reserve_form(request.form):
        return invalid_reserve_page(rsv_id, request.form)
    try:
        reserve_to_edit = Reserve.query.get_or_404(rsv_id)
        
        if current_user.role.rank == "sales":
            # Sales can only edit saleprice and remark
            reserve_to_edit.saleprice = int(request.form["saleprice"])
            reserve_to_edit.remark = request.form["remark"]
        else:
            # Admin can edit all fields (no 'sales' field on Reserve)
            reserve_to_edit.saleprice = int(request.form["saleprice"])
            reserve_to_edit.rsv_date = datetime.strptime(
                request.form["rsv_date"], "%Y-%m-%d"
            )
            reserve_to_edit.cfm_date = datetime.strptime(
                request.form["cfm_date"], "%Y-%m-%d"
            )
            reserve_to_edit.cfm_cs = request.form["cfm_cs"]
            reserve_to_edit.void = is_checked_key(request.form, "void")
            reserve_to_edit.remark = request.form["remark"]
        
        db.session.commit()
        flash("Reserve updated successfully!", "success")
        # Notify clients to refresh reserves and nested schedule views
        publish_update("reserve_changed", {"rsv_id": rsv_id, "spc_id": reserve_to_edit.spc_id}, actor_id=current_user.id)
        publish_update("space_changed", {"spc_id": reserve_to_edit.spc_id}, actor_id=current_user.id)
        return redirect(url_for("user.user_home"))

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
