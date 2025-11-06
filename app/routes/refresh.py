from flask import Blueprint, render_template, request
from datetime import datetime
from typing import Optional, Tuple
from flask_login import login_required, current_user
from app.functions.permissions import role_required
from app.functions.schedule.get import get_all_schedules
from app.functions.searching import schedule_table_results
from app.functions.reserve.get import get_sales_reserve, reserve_table_results
from app.functions.booking.get import get_sales_booking, booking_table_results
from app.functions.space.get import get_usable_spaces


refresh_routes = Blueprint("refresh", __name__)


@refresh_routes.route("/schedule", methods=["GET"])
@login_required
@role_required(["admin", "cs"])
def refresh_schedule():
    etd_start = request.args.get("etd_start", "").strip()
    etd_end = request.args.get("etd_end", "").strip()
    space_status = request.args.get("space_status", "").strip() or None
    sales_filter = request.args.get("sales_filter", "").strip()

    etd_start_dt, etd_end_dt = (None, None)
    if etd_start:
        try:
            etd_start_dt = datetime.strptime(etd_start, "%Y-%m-%d")
        except ValueError:
            pass
    if etd_end:
        try:
            etd_end_dt = datetime.strptime(etd_end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError:
            pass

    sales_user_id = int(sales_filter) if sales_filter else None

    schedules = get_all_schedules(
        etd_start=etd_start_dt,
        etd_end=etd_end_dt,
        space_status=space_status,
        sales_user_id=sales_user_id,
    )
    return schedule_table_results(schedules)
@refresh_routes.route("/space", methods=["GET"])
@login_required
@role_required(["admin", "cs", "sales"]) 
def refresh_space():
    spaces = get_usable_spaces()
    return render_template("available_space_results.html", spaces=spaces)

@refresh_routes.route("/reserve", methods=["GET"])
@login_required
@role_required(["sales"]) 
def refresh_reserve():
    etd_start = request.args.get("etd_start", "").strip()
    etd_end = request.args.get("etd_end", "").strip()
    void_str = request.args.get("void", "").strip().lower()
    etd_start_dt, etd_end_dt = (None, None)
    if etd_start:
        try:
            etd_start_dt = datetime.strptime(etd_start, "%Y-%m-%d")
        except ValueError:
            pass
    if etd_end:
        try:
            etd_end_dt = datetime.strptime(etd_end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError:
            pass
    void_val = None
    if void_str in ("yes", "no"):
        void_val = (void_str == "yes")
    reserves = get_sales_reserve(current_user.id, etd_start=etd_start_dt, etd_end=etd_end_dt, void=void_val)
    return reserve_table_results(reserves)


@refresh_routes.route("/booking", methods=["GET"])
@login_required
@role_required(["sales"]) 
def refresh_booking():
    etd_start = request.args.get("etd_start", "").strip()
    etd_end = request.args.get("etd_end", "").strip()
    void_str = request.args.get("void", "").strip().lower()
    etd_start_dt, etd_end_dt = (None, None)
    if etd_start:
        try:
            etd_start_dt = datetime.strptime(etd_start, "%Y-%m-%d")
        except ValueError:
            pass
    if etd_end:
        try:
            etd_end_dt = datetime.strptime(etd_end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError:
            pass
    void_val = None
    if void_str in ("yes", "no"):
        void_val = (void_str == "yes")
    bookings = get_sales_booking(current_user.id, etd_start=etd_start_dt, etd_end=etd_end_dt, void=void_val)
    return booking_table_results(bookings)