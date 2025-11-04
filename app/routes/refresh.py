from flask import Blueprint, render_template
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
    schedules = get_all_schedules()
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
    reserves = get_sales_reserve(current_user.id)
    return reserve_table_results(reserves)


@refresh_routes.route("/booking", methods=["GET"])
@login_required
@role_required(["sales"]) 
def refresh_booking():
    bookings = get_sales_booking(current_user.id)
    return booking_table_results(bookings)