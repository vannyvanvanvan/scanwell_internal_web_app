from flask_login import login_required
from app.functions.booking.delete import delete_booking
from app.functions.booking.edit import edit_booking, edit_booking_page
from app.functions.booking.new import create_booking, new_booking_page
from app.functions.permissions import role_required
from flask import (
    Blueprint,
    request,
)


booking_routes = Blueprint(
    "booking",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@booking_routes.route("/add/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def booking_add(spc_id: int):
    if request.method == "POST":
        return create_booking(request.form, spc_id)
    return new_booking_page(spc_id)


@booking_routes.route("/edit/<int:bk_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def booking_edit(bk_id: int):
    if request.method == "POST":
        return edit_booking(bk_id)
    return edit_booking_page(bk_id)


@booking_routes.route("/delete/<int:bk_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def booking_delete(bk_id: int):
    return delete_booking(bk_id)
