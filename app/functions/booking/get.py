from datetime import datetime
from flask import render_template
from flask_login import current_user
from app.functions.user.get import get_all_users_names_dict
from app.model import Booking, Space, Schedule, db
from sqlalchemy.orm import joinedload


def get_sales_booking(userid: int, etd_start: datetime = None, etd_end: datetime = None) -> list:
    query = (
        Booking.query.options(joinedload(Booking.space))
        .filter(Booking.sales == userid)
    )
    
    if etd_start or etd_end:
        query = query.join(Space, Booking.spc_id == Space.spc_id).join(Schedule, Space.sch_id == Schedule.sch_id)
        if etd_start:
            query = query.filter(Schedule.etd >= etd_start)
        if etd_end:
            query = query.filter(Schedule.etd <= etd_end)
    
    return query.all()


def booking_table_results(bookings: list) -> str:
    return render_template(
        "booking_table_results.html",
        current_user=current_user,
        bookings=bookings,
        users=get_all_users_names_dict(),
    )
