from flask_login import login_required
from app.functions.permissions import role_required
from app.functions.reserve.new import reserve_space, reserve_space_page
from app.functions.space.get import space_list_page
from app.functions.space.new import create_space, new_space_page
from app.functions.space.edit import edit_space, edit_space_page
from app.functions.space.delete import delete_space

from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
)

space_routes = Blueprint(
    "space",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@space_routes.route("/add/<int:sch_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def space_add(sch_id: int):
    if request.method == "POST":
        return create_space(request.form, sch_id)
    return new_space_page(sch_id)


@space_routes.route("/edit/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def space_edit(spc_id: int):
    if request.method == "POST":
        return edit_space(spc_id)
    return edit_space_page(spc_id)


@space_routes.route("/delete/<int:spc_id>", methods=["GET"])
@login_required
@role_required(["admin"])
def space_delete(spc_id: int):
    delete_space(spc_id)
    return redirect(url_for("user.user_home"))


@space_routes.route("/update/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs"])
def space_update(spc_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@space_routes.route("/search/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs", "sales"])
def space_search(query: dict):
    if request.method == "POST":
        pass
    else:
        pass


@space_routes.route("/list", methods=["GET"])
@login_required
@role_required(["admin", "cs", "sales"])
def space_list():
    return space_list_page()


@space_routes.route("/reserve/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required(["admin", "cs", "sales"])
def space_reserve(spc_id: int):
    if request.method == "POST":
        success = reserve_space(form=request.form, spc_id=spc_id)
        return (
            redirect(url_for("user.user_home"))
            if success
            else redirect(url_for("space.space_list"))
        )
    else:
        return reserve_space_page(spc_id)
