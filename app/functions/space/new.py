from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.model import Space, db
from datetime import datetime
from app.functions.validate import (
    default_or_valid_spcstatus,
    is_checked_key,
    is_valid_space_form,
    now_or_valid_date,
    zero_or_valid_number,
)


def new_space_page(sch_id: int) -> str:
    return render_template(
        "shipping_space.html",
        mode="add",
        data=Space(
            sch_id=sch_id,
            size="",
            avgrate=0,
            sugrate=0,
            ratevalid=datetime.now(),
            proport=False,
            spcstatus="USABLE",
        ),
    )


def new_populated_space_page(form: dict, sch_id: int) -> str:
    return render_template(
        "shipping_space.html",
        mode="add",
        data=Space(
            sch_id=sch_id,
            size=form["size"],
            avgrate=zero_or_valid_number(form["avgrate"]),
            sugrate=zero_or_valid_number(form["sugrate"]),
            ratevalid=now_or_valid_date(form["ratevalid"]),
            proport=form.get("proport", ""),
            spcstatus=form.get("spcstatus", "USABLE"),
            owner=current_user.id,
        ),
    )


def create_space(form: dict, sch_id: int) -> int:
    if not is_valid_space_form(form):
        flash("Some of your changes are invalid. Please try again.", "danger")
        return new_populated_space_page(form, sch_id)

    try:
        print("add space")
        new_space = Space(
            sch_id=sch_id,
            size=form["size"],
            avgrate=int(form["avgrate"]),
            sugrate=int(form["sugrate"]),
            ratevalid=datetime.strptime(form["ratevalid"], "%Y-%m-%d"),
            proport=is_checked_key(form, "proport"),
            spcstatus=default_or_valid_spcstatus(form["spcstatus"]),
            owner=current_user.id,
            last_modified_by=current_user.id,
            last_modified_at=datetime.utcnow(),
        )
        print("good data")
        db.session.add(new_space)
        db.session.commit()
        flash("Space created successfully!", "success")
        print("added space")
        return redirect(url_for("space.space_edit", spc_id=new_space.spc_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return -1
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return -1
