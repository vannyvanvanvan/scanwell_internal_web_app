from flask import render_template, request
from flask_login import current_user

from app.functions.booking.get import get_sales_booking
from app.functions.reserve.get import get_sales_reserve
from app.functions.schedule.get import get_all_schedules


def home_page() -> str:

    highlighted: dict = {}

    if request.args["highlighted_schedule"]:
        highlighted["schedule"] = int(request.args["highlighted_schedule"])

    if current_user.role.rank == "admin":
        return admin_home_page(highlighted=highlighted)
    elif current_user.role.rank == "cs":
        return cs_home_page(highlighted=highlighted)
    elif current_user.role.rank == "sales":
        return sales_home_page(highlighted=highlighted)
    else:
        return "Please contain the admin to get a proper role to access this page."


def admin_home_page(highlighted: dict) -> str:
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        results=get_all_schedules(),
    )


def cs_home_page(highlighted: dict) -> str:
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        results=get_all_schedules(),
    )


def sales_home_page(highlighted: dict) -> str:
    sales_reserves = get_sales_reserve(current_user.id)
    sales_bookings = get_sales_booking(current_user.id)
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        reserves=sales_reserves,
        bookings=sales_bookings,
    )
