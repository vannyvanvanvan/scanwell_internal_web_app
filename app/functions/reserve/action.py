from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user
from app.model import Reserve, Space, db


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
        flash("Reserve already confirmed", "warning")
        
        return redirect(url_for('user.user_home'))