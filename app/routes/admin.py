from flask import Blueprint, flash, redirect, url_for
from app.functions.permissions import rank_required
from app.model import db, LoginStatus
from app.functions.auth_utils import unlock_user

admin_routes = Blueprint(
    "admin", __name__, template_folder="../templates", static_folder="../static"
)


@admin_routes.route('/unlock/<int:user_id>', methods=['POST'])
@rank_required(["admin"])
def unlock_account(user_id):
    login_status = LoginStatus.query.get(user_id)

    if not login_status:
        flash('User not found', 'danger')
        return redirect(url_for('admin_dashboard'))

    unlock_user(login_status)
    flash(f'User {user_id} has been unlocked.', 'success')
    return redirect(url_for('admin_dashboard'))
