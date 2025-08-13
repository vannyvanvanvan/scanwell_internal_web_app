from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user
from app.model import Booking, Space, db

def pending_booking(spc_id: int) -> bool:
    try:
        space = Space.query.get(spc_id)
        if not space:
            flash('Space not found', 'error')
            return False
        
        space.spcstatus = 'BK_PENDING'
        space.last_modified_by = current_user.id
        space.last_modified_at = datetime.utcnow()
        return True
    
    except Exception as e:
        flash(f'Error updating booking status: {str(e)}', 'error')
        return False