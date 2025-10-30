from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from app.functions.user.get import get_all_users_names_dict
from sqlalchemy.exc import SQLAlchemyError
from app.model import Booking, Reserve, Space, db
from app.functions.events import publish_update

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
    
def confirm_booking_page(bk_id: int) -> str:
    try:
        booking = Booking.query.get_or_404(bk_id)
        space = Space.query.get(booking.spc_id)
        users = get_all_users_names_dict()
        
        return render_template(
            "shipping_booking_space.html",
            booking=booking,
            space=space,
            users=users,
            data=booking,
            page_title="Booking Confirm"
        )
        
    except Exception as e:
        flash(f'Error loading booking: {str(e)}', 'error')
        return redirect(url_for('user.user_home'))

def confirm_booking(bk_id: int):
    try:
        booking = Booking.query.get_or_404(bk_id)
        
        if booking.void:
            flash('Cannot confirm booking, it has already been voided', 'warning')
            return redirect(url_for('user.user_home'))
        
        # Only allow confirm on the latest non-void
        space = Space.query.get(booking.spc_id)
        if not space or space.spcstatus != 'BK_PENDING':
            flash('Cannot confirm: Space is not in BK_PENDING state.', 'warning')
            return redirect(url_for('user.user_home'))
        latest = Booking.query.filter_by(spc_id=booking.spc_id, void=False).order_by(Booking.bk_id.desc()).first()
        if latest and latest.bk_id != booking.bk_id:
            flash('Cannot confirm: This booking has been superseded by a newer booking.', 'warning')
            return redirect(url_for('user.user_home'))
        
        if not booking.so or booking.so.strip() == "":
            flash('Cannot confirm booking, SO must be filled in before confirmation.', 'danger')
            return redirect(url_for('booking.booking_confirm', bk_id=bk_id))
        
        if 'remark' in request.form:
            booking.remark = request.form['remark']
        space.spcstatus = 'BK_CONFIRM'
        space.last_modified_by = current_user.id
        space.last_modified_at = datetime.utcnow()
        
        db.session.commit()
        flash('Booking confirmed successfully!', 'success')
        publish_update("booking_changed", {"bk_id": bk_id, "spc_id": booking.spc_id}, actor_id=current_user.id)
        if space:
            publish_update("space_changed", {"spc_id": space.spc_id, "sch_id": space.sch_id}, actor_id=current_user.id)
        return redirect(url_for('user.user_home'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False

def decline_booking_page(bk_id: int) -> str:
    try:
        booking = Booking.query.get_or_404(bk_id)
        space = Space.query.get(booking.spc_id)
        users = get_all_users_names_dict()
        
        return render_template(
            "shipping_booking_space.html",
            booking=booking,
            space=space,
            users=users,
            data=booking,
            page_title="Booking Reject"
            
        )
        
    except Exception as e:
        flash(f'Error loading booking: {str(e)}', 'error')
        return redirect(url_for('user.user_home'))

def decline_booking(bk_id: int):
    try:
        booking = Booking.query.get_or_404(bk_id)
        
        if booking.void:
            flash('Booking has already been voided', 'warning')
            return redirect(url_for('user.user_home'))
        # Only allow decline on latest non-void booking for this space while space is BK_PENDING
        space = Space.query.get(booking.spc_id)
        if not space or space.spcstatus != 'BK_PENDING':
            flash('Cannot decline: Space is not in BK_PENDING state.', 'warning')
            return redirect(url_for('user.user_home'))
        latest = Booking.query.filter_by(spc_id=booking.spc_id, void=False).order_by(Booking.bk_id.desc()).first()
        if latest and latest.bk_id != booking.bk_id:
            flash('Cannot decline: This booking has been superseded by a newer booking.', 'warning')
            return redirect(url_for('user.user_home'))
        
        if 'remark' in request.form:
            booking.remark = request.form['remark']

        booking.void = True
        
        # Set all reserves on the same space to void
        reserves = Reserve.query.filter_by(spc_id=booking.spc_id).all()
        for reserve in reserves:
            reserve.void = True
        
        space.spcstatus = 'USABLE'
        space.last_modified_by = current_user.id
        space.last_modified_at = datetime.utcnow()
        
        db.session.commit()
        flash('Booking declined successfully!', 'success')
        publish_update("booking_changed", {"bk_id": bk_id, "spc_id": booking.spc_id}, actor_id=current_user.id)
        if space:
            publish_update("space_changed", {"spc_id": space.spc_id, "sch_id": space.sch_id}, actor_id=current_user.id)
        return redirect(url_for('user.user_home'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False