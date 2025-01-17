from flask import render_template
from flask_login import current_user

from app.functions.booking.get import get_sales_booking
from app.functions.reserve.get import get_sales_reserve
from app.functions.schedule.get import get_all_schedules


def home_page() -> str:
    if current_user.rank == "admin":
        return admin_home_page()
    elif current_user.rank == "cs":
        return admin_home_page()
    elif current_user.rank == "sp":
        return sales_home_page()


def admin_home_page() -> str:
    return render_template(
        "home_page.html",
        current_user=current_user,
        results=get_all_schedules(),
    )


def sales_home_page() -> str:
    sales_reserves = get_sales_reserve(current_user.id)
    sales_bookings = get_sales_booking(current_user.id)
    return render_template(
        "home_page.html",
        current_user=current_user,
        reserves=sales_reserves,
        bookings=sales_bookings,
    )
