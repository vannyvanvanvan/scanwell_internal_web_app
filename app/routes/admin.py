from flask_login import login_required
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.functions.permissions import role_required
from app.model import db, LoginStatus, User
from app.functions.auth_utils import lock_user, unlock_user
from flask import jsonify
from app.functions.redis_config import redis_client
from app.functions.user.get import get_all_users
from app.functions.admin.manage import get_user, update_user_detail



admin_routes = Blueprint(
    "admin", __name__, template_folder="../templates", static_folder="../static"
)

# Admin Panel Home
@admin_routes.route('/', methods=['GET'])
@login_required
@role_required(["admin"])
def admin_home():
    return render_template('admin/home.html')

# Users list
@admin_routes.route('/users', methods=['GET'])
@login_required
@role_required(["admin"])
def admin_users_list():
    users = get_all_users()
    return render_template('admin/users_list.html', users=users)

# View user
@admin_routes.route('/users/<int:user_id>', methods=['GET'])
@login_required
@role_required(["admin"])
def admin_user_view(user_id: int):
    user = get_user(user_id)
    if user is None:
        flash('User not found', 'danger')
        return redirect(url_for('admin.admin_users_list'))
    return render_template('admin/user_view.html', user=user)

# Edit user
@admin_routes.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def admin_user_edit(user_id: int):
    user = get_user(user_id)
    if user is None:
        flash('User not found', 'danger')
        return redirect(url_for('admin.admin_users_list'))

    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        new_friendly_name = request.form.get('friendly_name', '').strip()
        new_rank = request.form.get('rank', '').strip().lower()
        new_password = request.form.get('password', '')

        success, message = update_user_detail(
            user_id,
            new_username=new_username or None,
            new_friendly_name=new_friendly_name or None,
            new_rank=new_rank or None,
            new_password=new_password or None,
        )
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('admin.admin_user_view', user_id=user_id))

    return render_template('admin/user_edit.html', user=user)

# Remove GET later for security reasons!!!!!!!!!!!!!!!
@admin_routes.route('/unlock/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def unlock_account(user_id):
    print(f"Attempting to unlock user ID: {user_id}")
    login_status_user_id = LoginStatus.query.get(user_id)

    if not login_status_user_id:
        flash('User not found', 'danger')
        return redirect(url_for('user.user_home'))

    unlock_user(login_status_user_id)
    flash(f'User {user_id} has been unlocked.', 'success')
    return redirect(url_for('user.user_home'))

@admin_routes.route('/lock/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def lock_account(user_id):
    print(f"Attempting to lock user ID: {user_id}")
    login_status_user_id = LoginStatus.query.get(user_id)

    if not login_status_user_id:
        flash('User not found', 'danger')
        return redirect(url_for('user.user_home'))

    lock_user(login_status_user_id)
    flash(f'User {user_id} has been locked.', 'success')
    return redirect(url_for('user.user_home'))


@admin_routes.route('/online-users', methods=['GET'])
@login_required
@role_required(["admin"])
def get_online_users():
    
    # Fetch all online users
    online_users = redis_client.keys("online_user:*")
    away_users = redis_client.keys("away_user:*")

    # Extract user IDs
    online_user_ids = [key.split(":")[-1] for key in online_users]
    away_user_ids = [key.split(":")[-1] for key in away_users]

    # Convert to ints value for db query
    def to_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    online_ids_int = [to_int(value) for value in online_user_ids]
    away_ids_int = [to_int(value) for value in away_user_ids]

    online_ids_int_filtered = [value for value in online_ids_int if value is not None]
    away_ids_int_filtered = [value for value in away_ids_int if value is not None]

    # Fetch users
    users_online = User.query.filter(User.id.in_(online_ids_int_filtered)).all() if online_ids_int_filtered else []
    users_away = User.query.filter(User.id.in_(away_ids_int_filtered)).all() if away_ids_int_filtered else []

    id_to_username_online = {str(u.id): u.username for u in users_online}
    id_to_username_away = {str(u.id): u.username for u in users_away}

    # Display data with id and username
    online = [
        {"id": uid, "username": id_to_username_online.get(uid, "Unknown")}
        for uid in online_user_ids
    ]
    away = [
        {"id": uid, "username": id_to_username_away.get(uid, "Unknown")}
        for uid in away_user_ids
    ]

    data = {"online_users": online, "away_users": away}
    return render_template('admin/online_users.html', data=data)