from app.permissions import rank_required
from flask import (
    Blueprint,
    request,
)
from flask_login import login_required

booking = Blueprint(
    "booking",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@booking.route("/add")
@login_required
@rank_required(["admin"])
def booking_add():
    pass


@booking.route("/edit/<int:bk_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def booking_edit(bk_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@booking.route("/delete/<int:bk_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def booking_delete(bk_id: int):
    if request.method == "POST":
        pass
    else:
        pass
