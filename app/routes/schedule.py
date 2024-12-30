from app.permissions import rank_required
from flask import (
    Blueprint,
    request,
)
from flask_login import login_required

schedule = Blueprint(
    "schedule",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@schedule.route("/add")
@login_required
@rank_required(["admin"])
def schedule_add():
    pass


@schedule.route("/edit/<int:sch_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_edit(sch_id: int):
    if request.method == "POST":
        pass
    else:
        pass


@schedule.route("/delete/<int:sch_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_delete(sch_id: int):
    if request.method == "POST":
        pass
    else:
        pass
