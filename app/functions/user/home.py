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
        users=get_all_users_names_dict()
    )


def cs_home_page(highlighted: dict) -> str:
    return render_template(
        "home_page.html",
        current_user=current_user,
        highlighted=highlighted,
        results=get_all_schedules(),
        users=get_all_users_names_dict()
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
        users=get_all_users_names_dict()
    )
