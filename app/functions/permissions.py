from functools import wraps
from typing import List
from flask import abort
from flask_login import current_user


# Restrict access based on list of ranks
def role_required(ranks:List[str]):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # Only allow access if user has required rank
            if current_user.role.rank in ranks:
              return func(*args, **kwargs)
            else:
               # Forbidden 
              return abort(403)
        return decorated_view
    return decorator