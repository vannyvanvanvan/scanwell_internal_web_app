from functools import wraps
from flask import abort
from flask_login import current_user

# Role-Based Decorators: Created a decorator to enforce role-based access
# Only admin can acess to admin dashboard and user to user dashboard
def role_required(rank):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rank != rank:
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return decorated_view
    return decorator