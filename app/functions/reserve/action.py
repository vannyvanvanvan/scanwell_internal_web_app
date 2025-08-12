from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user
from app.model import Reserve, Schedule, Space, db

def approve_reserve(rsv_id):
    reserve = Reserve.query.get(rsv_id)
    if not reserve:
        flash("Reserve not found", "danger")
        return redirect(url_for('user.user_home'))
    
    if reserve.cfm_cs == None:
        # update reserve status and their RVs
        reserve.cfm_date = datetime.utcnow()
        reserve.cfm_cs = current_user.username
        reserve.void = False 
        
        space = Space.query.get(reserve.spc_id)
        if space:
            space.spcstatus = 'RV_CONFIRM'
        
        db.session.commit()
        
        flash("Reserve approved successfully", "success")
        
        return redirect(url_for('user.user_home'))
    
    else:
        flash("Reserve already confirmed, can not reconfirm", "warning")
        
        return redirect(url_for('user.user_home'))
    
    
def decline_reserve(rsv_id):
    reserve = Reserve.query.get(rsv_id)
    if not reserve:
        flash("Reserve not found", "danger")
        return redirect(url_for('user.user_home'))
    
    if reserve.cfm_cs == None:
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
            space.spcstatus = 'USABLE'
            msg = "Reserve declined, Space released"
        else:
            space.spcstatus = 'RV_CANCEL'
            msg = "Reserve declined, Space canceled (SICUTOFF < 24h)"
            
        db.session.commit()
        flash(msg, "success")
        return redirect(url_for('user.user_home'))
    
    else:
        flash("Reserve already confirmed, can not decline", "warning")      
        return redirect(url_for('user.user_home'))
    
def unconfirm_reserve(rsv_id):
    reserve = Reserve.query.get(rsv_id)
    if not reserve:
        flash("Reserve not found", "danger")
        return redirect(url_for('user.user_home'))
    
    if reserve.cfm_cs != None:
        
        # update reserve status and their RVs
        reserve.cfm_date = None
        reserve.cfm_cs = None
        reserve.void = True
        
        space = Space.query.get(reserve.spc_id)
        if space:
            space.spcstatus = 'RV_SUBMIT'
        
        db.session.commit()
        
        flash("Reserve unconfirmed successfully", "success")
        return redirect(url_for('user.user_home'))
    
    else:
        flash("Reserve not confirmed, can not unconfirm", "warning")
        return redirect(url_for('user.user_home'))