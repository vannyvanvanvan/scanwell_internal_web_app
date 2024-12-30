from app.permissions import rank_required
from flask import (
    Blueprint,
    request,
)
from flask_login import login_required

space = Blueprint(
    "space",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@space.route("/add")
@login_required
@rank_required(["admin"])
def space_add():
    pass


@space.route("/edit/<int:spc_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def space_edit(spc_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@space.route("/delete/<int:spc_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def space_delete(spc_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@space.route("/update/<int:spc_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs"])
def space_update(spc_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@space.route("/search/<int:spc_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin", "cs", "sales"])
def space_search(query: dict):
    if request.method == "POST":
        pass
    else:
        pass
