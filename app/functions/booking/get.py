from flask import render_template
from flask_login import current_user
from app.functions.reserve.get import get_sales_reserve
from app.model import Booking


def get_sales_booking(userid: int) -> list:
    sales_rsv_ids = [reserve.rsv_id for reserve in get_sales_reserve(userid)]
    return Booking.query.filter(Booking.rsv_id.in_(sales_rsv_ids)).all()


def booking_table_results(reserves: list) -> str:
    return render_template(
        "reserve_table_results.html", current_user=current_user, reserves=reserves
    )
