from datetime import datetime
from app.model import Schedule
from app.permissions import rank_required
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
)
from flask_login import current_user, login_required
from app.functions.schedule.new import add_schedule
from app.functions.schedule.edit import edit_schedule
from app.functions.schedule.delete import delete_schedule

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
    if add_schedule():
        # Redirect to the view area leave this blank for now
        return redirect("schedule.list")
    # Do i still need this?
    return render_template(
        "edit_Schedule.html",
        mode="Add",
        data=Schedule(
            cs="",
            week=datetime.now().isocalendar().week,
            carrier="",
            service="",
            mv="",
            pol="",
            pod="",
            routing="",
            cyopen=datetime.now(),
            sicutoff=datetime.now(),
            cycvcls=datetime.now(),
            etd=datetime.now(),
            eta=datetime.now(),
            owner=current_user.id
        ),
    )


@schedule.route("/edit/<int:sch_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_edit(sch_id: int):
    if request.method == "POST":
        if edit_schedule(sch_id):
            # Returning to a new updated list
            return redirect("schedule.list")
        return render_template("edit_Schedule.html", mode="Edit")
    else:
        pass


@schedule.route("/delete/<int:sch_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_delete(sch_id: int):
    if request.method == "POST":
        if delete_schedule(sch_id):
            # Same again return to a new updated list
            return redirect("schedule.list")
        return redirect("schedule.list")
    else:
        pass
