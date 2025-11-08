from datetime import datetime, timedelta
from flask import current_app, render_template
from flask_login import current_user
from app.functions.schedule.get import get_schedule_pol_pod_etd
from app.model import Space, Schedule, db


def get_usable_spaces() -> list:    
    space_auto_invalid()
    accessible_statuses = ["USABLE"]
    if current_user.role and current_user.role.rank == "cs_sales":
        accessible_statuses.append("BK_RESERVED")

    usable_spaces = Space.query.filter(Space.spcstatus.in_(accessible_statuses)).all()
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
    # if SICUTOF - nowdate < 24
    # status -> invalid
    now = datetime.now()
    usable_spaces_with_schedules = db.session.query(Space, Schedule).join(Schedule).filter(
        Space.spcstatus == "USABLE"
    ).all()
    spaces_to_invalidate = [] 
    for space, schedule in usable_spaces_with_schedules:
        time_diff = schedule.sicutoff - now
        hours_remaining = time_diff.total_seconds() / 3600
        
        # could be used for later use?
        #print(f"Space ID: {space.spc_id}")
        #print(f"SICUTOFF: {schedule.sicutoff}")
        #print(f"Current time: {now}")
        #print(f"Time difference: {time_diff}")
        #print(f"Hours remaining: {hours_remaining:.2f} hours")
        #print(f"Should invalidate: {hours_remaining < 24}")
        
        if hours_remaining < 24:
            spaces_to_invalidate.append(space.spc_id)
    
    if spaces_to_invalidate:
        Space.query.filter(Space.spc_id.in_(spaces_to_invalidate)).update(
            {
                Space.spcstatus: "INVALID",
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
            print(f"Error updating spaces: {e}")
    else:
        print("No spaces need to be marked as INVALID at this time.")
    
