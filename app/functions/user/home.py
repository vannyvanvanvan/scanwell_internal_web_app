from datetime import datetime, timedelta
from flask import render_template, request
from flask_login import current_user

from app.functions.booking.get import get_sales_booking
from app.functions.reserve.get import get_sales_reserve
from app.functions.schedule.get import get_all_schedules
from app.functions.user.get import get_all_users_names_dict


def home_page() -> str:

    highlighted: dict = {}

    if "highlighted_schedule" in request.args:
        highlighted["schedule"] = int(request.args["highlighted_schedule"])
    if "highlighted_space" in request.args:
        highlighted["space"] = int(request.args["highlighted_space"])
    if "highlighted_reserve" in request.args:
        highlighted["reserve"] = int(request.args["highlighted_reserve"])
    if "highlighted_booking" in request.args:
        highlighted["booking"] = int(request.args["highlighted_booking"])

    if current_user.role.rank == "admin":
        return admin_home_page(highlighted=highlighted)
    elif current_user.role.rank == "cs":
        return cs_home_page(highlighted=highlighted)
    elif current_user.role.rank in ("sales", "cs_sales"):
        return sales_home_page(highlighted=highlighted)
    else:
        return "Please contain the admin to get a proper role to access this page."


def get_etd_filter_dates():
    etd_start = None
    etd_end = None
    
    if "etd_start" in request.args and request.args["etd_start"]:
        try:
            etd_start = datetime.strptime(request.args["etd_start"], "%Y-%m-%d")
        except ValueError:
            pass
    
    if "etd_end" in request.args and request.args["etd_end"]:
        try:
            etd_end = datetime.strptime(request.args["etd_end"], "%Y-%m-%d")
            etd_end = etd_end.replace(hour=23, minute=59, second=59)
        except ValueError:
            pass
    
    if not etd_start and not etd_end:
        etd_end = datetime.utcnow()
        etd_start = etd_end - timedelta(days=90)
    
    return etd_start, etd_end


def admin_home_page(highlighted: dict) -> str:
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        results=get_all_schedules(),
        users=get_all_users_names_dict()
    )


def cs_home_page(highlighted: dict) -> str:
    etd_start, etd_end = get_etd_filter_dates()
    # Read optional filters for CS interface
    space_status = request.args.get("space_status") or None
    sales_filter_raw = request.args.get("sales_filter") or None
    sales_user_id = int(sales_filter_raw) if sales_filter_raw else None

    schedules = get_all_schedules(
        etd_start=etd_start,
        etd_end=etd_end,
        space_status=space_status,
        sales_user_id=sales_user_id,
    )
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        results=schedules,
        users=get_all_users_names_dict(),
        etd_start=etd_start,
        etd_end=etd_end
    )


def sales_home_page(highlighted: dict) -> str:
    etd_start, etd_end = get_etd_filter_dates()
    void_str = request.args.get("void", "").strip().lower()
    void_val = None
    if void_str in ("yes", "no"):
        void_val = (void_str == "yes")

    sales_reserves = get_sales_reserve(
        current_user.id,
        etd_start=etd_start,
        etd_end=etd_end,
        void=void_val,
    )
    sales_bookings = get_sales_booking(
        current_user.id,
        etd_start=etd_start,
        etd_end=etd_end,
        void=void_val,
    )
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        reserves=sales_reserves,
        bookings=sales_bookings,
        users=get_all_users_names_dict(),
        etd_start=etd_start,
        etd_end=etd_end
    )
