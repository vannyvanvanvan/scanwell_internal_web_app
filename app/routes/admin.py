from flask_login import login_required
from flask import Blueprint, flash, redirect, url_for
from app.functions.permissions import role_required
from app.model import db, LoginStatus
from app.functions.auth_utils import lock_user, unlock_user


admin_routes = Blueprint(
    "admin", __name__, template_folder="../templates", static_folder="../static"
)

# Remove GET later for security reasons!!!!!!!!!!!!!!!
@admin_routes.route('/unlock/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def unlock_account(user_id):
    print(f"Attempting to unlock user ID: {user_id}")
    login_status = LoginStatus.query.get(user_id)

    if not login_status:
        flash('User not found', 'danger')
        return redirect(url_for('user.user_home'))

    unlock_user(login_status)
    flash(f'User {user_id} has been unlocked.', 'success')
    return redirect(url_for('user.user_home'))

@admin_routes.route('/lock/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def lock_account(user_id):
    print(f"Attempting to lock user ID: {user_id}")
    login_status = LoginStatus.query.get(user_id)

    if not login_status:
        flash('User not found', 'danger')
        return redirect(url_for('user.user_home'))

    lock_user(login_status)
    flash(f'User {user_id} has been locked.', 'success')
    return redirect(url_for('user.user_home'))