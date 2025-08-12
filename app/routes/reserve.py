from flask_login import login_required
from app.functions.permissions import role_required
from app.functions.reserve.action import approve_reserve
from app.functions.reserve.new import create_reserve, new_reserve_page
from app.functions.reserve.edit import edit_reserve, edit_reserve_page
from app.functions.reserve.delete import delete_reserve
from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
)

reserve_routes = Blueprint(
    "reserve",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@reserve_routes.route("/add/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def reserve_add(spc_id: int):
    if request.method == "POST":
        return create_reserve(request.form, spc_id)
    return new_reserve_page(spc_id)


@reserve_routes.route("/edit/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def reserve_edit(rsv_id: int):
    if request.method == "POST":
        return edit_reserve(rsv_id)
    return edit_reserve_page(rsv_id)


@reserve_routes.route("/delete/<int:rsv_id>", methods=["POST"])
@login_required
@role_required(["admin"])
def reserve_delete(rsv_id: int):
    delete_reserve(rsv_id)
    return redirect(url_for("user.user_home"))


@reserve_routes.route("/confirm/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def reserve_confirm(rsv_id: int):
    if request.method == "POST":
        return approve_reserve(rsv_id)


@reserve_routes.route("/decline/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def reserve_decline(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@reserve_routes.route("/unconfirm/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def reserve_unconfirm(rsv_id: int):
    if request.method == "POST":
        pass
    else:
        pass
