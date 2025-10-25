from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from app.functions.user.get import get_all_users_names_dict
from sqlalchemy.exc import SQLAlchemyError
from app.model import Booking, Reserve, Space, db

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
        
        if not booking.so or booking.so.strip() == "":
            flash('Cannot confirm booking, SO must be filled in before confirmation.', 'danger')
            return redirect(url_for('booking.booking_confirm', bk_id=bk_id))
        
        if 'remark' in request.form:
            booking.remark = request.form['remark']

        space = Space.query.get(booking.spc_id)
        space.spcstatus = 'BK_CONFIRM'
        space.last_modified_by = current_user.id
        space.last_modified_at = datetime.utcnow()
        
        db.session.commit()
        flash('Booking confirmed successfully!', 'success')
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
        if 'remark' in request.form:
            booking.remark = request.form['remark']

        booking.void = True
        
        # Set all reserves on the same space to void
        reserves = Reserve.query.filter_by(spc_id=booking.spc_id).all()
        for reserve in reserves:
            print("test")
            reserve.void = True
        
        space = Space.query.get(booking.spc_id)
        space.spcstatus = 'USABLE'
        space.last_modified_by = current_user.id
        space.last_modified_at = datetime.utcnow()
        
        db.session.commit()
        flash('Booking declined successfully!', 'success')
        return redirect(url_for('user.user_home'))
    
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False