from app.permissions import rank_required
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
)
from flask_login import current_user, login_required

from app.functions.schedule.new import new_schedule, new_schedule_page
from app.functions.schedule.edit import edit_schedule
from app.functions.schedule.delete import delete_schedule

schedule_routes = Blueprint(
    "schedule",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@schedule_routes.route("/add", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_add():
    print("hi", current_user.rank)
    return "dlllm"
    # if request.method == "POST":
    #     new_schedule_id = new_schedule(request.form)
    #     if new_schedule_id != -1:
    #         return schedule_edit(new_schedule_id)
    # else:
    #     return new_schedule_page()


# @schedule_routes.route("/edit/<int:sch_id>", methods=["GET", "POST"])
# @login_required
# @rank_required(["admin"])
# def schedule_edit(sch_id: int):
#     if request.method == "POST":
#         if edit_schedule(sch_id):
#             # Returning to a new updated list
#             return redirect("schedule_routes.list")

#     else:
#         return render_template("edit_Schedule.html", mode="Edit")


# @schedule_routes.route("/delete/<int:sch_id>", methods=["POST"])
# @login_required
# @rank_required(["admin"])
# def schedule_delete(sch_id: int):
#     delete_schedule(sch_id)
#     return redirect("schedule_routes.list")
