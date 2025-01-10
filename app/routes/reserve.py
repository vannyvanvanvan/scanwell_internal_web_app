from app.functions.permissions import rank_required
from flask import (
    Blueprint,
    request,
)
from flask_login import login_required

reserve = Blueprint(
    "reserve",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@reserve.route("/add")
@login_required
@rank_required(["admin", "sales"])
def reserve_add():
    pass


@reserve.route("/edit/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def reserve_edit(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@reserve.route("/delete/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def reserve_delete(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@reserve.route("/confirm/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def reserve_confirm(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@reserve.route("/decline/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def reserve_decline(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@reserve.route("/unconfirm/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def reserve_unconfirm(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass
