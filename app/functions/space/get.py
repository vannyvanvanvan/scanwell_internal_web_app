from datetime import datetime, timedelta
from flask import current_app, render_template
from flask_login import current_user
from app.functions.schedule.get import get_schedule_pol_pod_etd
from app.model import Space, Schedule, db


def get_usable_spaces() -> list:    
    space_auto_invalid()
    usable_spaces = Space.query.filter(Space.spcstatus == "USABLE").all()
    # Need to accompany usable spaces with scheduled POL, POD, ETD
    results = []
    for space in usable_spaces:
        schedule = get_schedule_pol_pod_etd(space.sch_id)
        results.append([schedule, space])
    return results


def space_list_page() -> str:
    return render_template(
        "available_space.html", current_user=current_user, spaces=get_usable_spaces()
    )


def get_space_by_id(spc_id: int) -> Space:
    return Space.query.filter(Space.spc_id == spc_id).first()

def space_auto_invalid():    
    now = datetime.now()
    # If SICUTOF - nowdate <= 24
    # Status -> Invalid
    invalid_space_ids = db.session.query(Space.spc_id).join(Schedule).filter(
        Space.spcstatus == "USABLE",
        Schedule.sicutoff - now < timedelta(hours=24)
    ).all()
    
    invalid_space_ids = [id_tuple[0] for id_tuple in invalid_space_ids]
    if invalid_space_ids:
        print(f"Invalid space IDs: {invalid_space_ids}")
        current_app.logger.info(f"Updating id of {len(invalid_space_ids)} spaces to INVALID status.")
        Space.query.filter(Space.spc_id.in_(invalid_space_ids)).update(
            {
                Space.spcstatus: "INVALID",
                # Added the role "System" for auto update but could use "Admin"
                Space.last_modified_by: "System",
                Space.last_modified_at: now
            },
            synchronize_session=False
        )
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to update spaces status to INVALID: {e}")
            db.session.rollback()
    
