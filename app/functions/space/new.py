from datetime import datetime
from flask_login import current_user
from flask import render_template, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.functions.validate import is_valid_space_form, now_or_valid_date, zero_or_valid_number
from app.model import Space, db


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
            spcstatus="USABLE"
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
    print("test2.1")
    if not is_valid_space_form(form):
        print("test2.1.1")
        flash("Some of your changes are invalid. Please try again.", "danger")
        return new_populated_space_page(form, sch_id)

    try:
        print("test2.1.2")
        new_space = Space(
            sch_id=sch_id,
            size=form["size"],
            avgrate=int(form["avgrate"]),
            sugrate=int(form["sugrate"]),
            ratevalid=datetime.strptime(form["ratevalid"], "%Y-%m-%d"),
            proport=form["proport"],
            spcstatus=form.get("spcstatus", "USABLE"),
            owner=current_user.id,
            last_modified_by=current_user.id,
            last_modified_at=datetime.utcnow
        )
        print("test2.2")
        db.session.add(new_space)
        db.session.commit()
        print("test2.3")
        flash("Space created successfully!", "success")
        return redirect(url_for("space.edit_space_page", spc_id=new_space.spc_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return -1
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return -1
