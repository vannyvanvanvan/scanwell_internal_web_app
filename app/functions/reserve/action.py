from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user
from app.model import Reserve, Schedule, Space, db


def confirm_reserve(rsv_id):
    try:
        reserve = Reserve.query.get(rsv_id)
        if not reserve:
            flash("Reserve not found", "danger")
            return redirect(url_for("user.user_home"))

        elif reserve.cfm_cs == None:
            # update reserve status and their RVs
            reserve.cfm_date = datetime.utcnow()
            reserve.cfm_cs = current_user.id
            reserve.void = False

            space = Space.query.get(reserve.spc_id)
            if space:
                space.spcstatus = "RV_CONFIRM"

            db.session.commit()

            flash("Reserve approved successfully", "success")

            return redirect(
                url_for(
                    "user.user_home",
                    highlighted_schedule=space.sch_id,
                    highlighted_space=space.spc_id,
                    highlighted_reserve=reserve.rsv_id,
                )
            )

        else:
            flash("Reserve already confirmed, can not reconfirm", "warning")

            return redirect(
                url_for(
                    "user.user_home",
                    highlighted_schedule=space.sch_id,
                    highlighted_space=space.spc_id,
                    highlighted_reserve=reserve.rsv_id,
                )
            )

    except Exception as e:
        db.session.rollback()
        flash(f"Error updating booking status: {str(e)}", "error")
        return redirect(url_for("user.user_home"))


def decline_reserve(rsv_id):
    try:
        reserve = Reserve.query.get(rsv_id)
        if not reserve:
            flash("Reserve not found", "danger")
            return redirect(url_for("user.user_home"))

        elif reserve.cfm_cs == None:
            # update reserve status and their RVs
            space = Space.query.get(reserve.spc_id)
            schedule = Schedule.query.get(space.sch_id)

            # calculate time difference
            now = datetime.utcnow()
            time_diff = schedule.sicutoff - now
            hours_remaining = time_diff.total_seconds() / 3600

            # update reserve
            reserve.void = True
            reserve.cfm_date = datetime.utcnow()
            reserve.cfm_cs = current_user.username

            # if SICUTOF - nowdate > 24
            # status -> usable else RV_CANCEL
            if hours_remaining > 24:
                space.spcstatus = "USABLE"
                msg = "Reserve declined, Space released"
            else:
                space.spcstatus = "RV_CANCEL"
                msg = "Reserve declined, Space canceled (SICUTOFF < 24h)"

            db.session.commit()
            flash(msg, "success")
            return redirect(url_for("user.user_home"))

        else:
            flash("Reserve already confirmed, can not decline", "warning")
            return redirect(
                url_for(
                    "user.user_home",
                    highlighted_schedule=space.sch_id,
                    highlighted_space=space.spc_id,
                    highlighted_reserve=reserve.rsv_id,
                )
            )

    except Exception as e:
        db.session.rollback()
        flash(f"Error updating booking status: {str(e)}", "error")
        return redirect(url_for("user.user_home"))


def unconfirm_reserve(rsv_id):
    try:
        reserve = Reserve.query.get(rsv_id)
        if not reserve:
            flash("Reserve not found", "danger")
            return redirect(url_for("user.user_home"))

        elif reserve.cfm_cs != None:

            # update reserve status and their RVs
            reserve.cfm_date = None
            reserve.cfm_cs = None
            reserve.void = False

            space = Space.query.get(reserve.spc_id)
            if space:
                space.spcstatus = "RV_SUBMIT"

            db.session.commit()

            flash("Reserve unconfirmed successfully", "success")
            return redirect(
                url_for(
                    "user.user_home",
                    highlighted_schedule=space.sch_id,
                    highlighted_space=space.spc_id,
                    highlighted_reserve=reserve.rsv_id,
                )
            )

        else:
            flash("Reserve not confirmed, can not unconfirm", "warning")
            return redirect(
                url_for(
                    "user.user_home",
                    highlighted_schedule=space.sch_id,
                    highlighted_space=space.spc_id,
                    highlighted_reserve=reserve.rsv_id,
                )
            )

    except Exception as e:
        db.session.rollback()
        flash(f"Error updating booking status: {str(e)}", "error")
        return redirect(url_for("user.user_home"))
