from flask import render_template
from flask_login import current_user
from app.functions.user.get import get_all_users_names_dict
from app.model import Booking


def get_sales_booking(userid: int) -> list:
    return Booking.query.filter(Booking.sales == userid).all()


def booking_table_results(bookings: list) -> str:
    return render_template(
        "booking_table_results.html",
        current_user=current_user,
        bookings=bookings,
        users=get_all_users_names_dict(),
    )
