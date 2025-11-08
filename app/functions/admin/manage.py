from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from app.model import db, User, Role, LoginStatus
from app.functions.hashing import hash_string


def get_user(user_id: int):
    return User.query.get(user_id)

# Could be extended to check for other roles in the future
# For now, support admin, cs, sales, and cs_sales hybrid role
AVAILABLE_RANKS = ("admin", "cs", "sales", "cs_sales")
EXISTING_RANKS = set(AVAILABLE_RANKS)

def update_user_detail(
    user_id: int,
    new_username=None,
    new_friendly_name=None,
    new_rank=None,
    new_password=None,
):

    user = User.query.get(user_id)
    if user is None:
        return False, "User not found"

    # Changing username
    if new_username is not None and new_username.strip() != "":
        requested_username = new_username.strip()
        username_taken = (
            User.query.filter(User.username == requested_username, User.id != user_id).first()
            is not None
        )
        if username_taken:
            return False, "Username already exists"
        user.username = requested_username

    # Changing friendly name
    if new_friendly_name is not None and new_friendly_name.strip() != "":
        user.friendly_name = new_friendly_name.strip()

    # Selecting new role rank
    if new_rank is not None and new_rank.strip() != "":
        requested_rank = new_rank.strip().lower()
        if requested_rank not in EXISTING_RANKS:
            return False, "Invalid role rank"
        if user.role is None:
            user.role = Role(user_id=user.id, rank=requested_rank)
        else:
            user.role.rank = requested_rank

    # Resetting password
    if new_password is not None and new_password != "":
        user.password = hash_string(new_password)

    db.session.commit()
    return True, "User updated successfully"



def create_user(
    username: str,
    friendly_name: Optional[str],
    rank: str,
    password: str,
):
    normalized_username = (username or "").strip()
    normalized_rank = (rank or "").strip().lower()
    normalized_name = (friendly_name or "").strip() or None
    raw_password = password or ""

    if not normalized_username:
        return False, "Username is required"

    if not raw_password:
        return False, "New password is required"

    if normalized_rank not in EXISTING_RANKS:
        return False, "Invalid role rank"

    username_taken = User.query.filter_by(username=normalized_username).first()
    if username_taken is not None:
        return False, "Username already exists"

    new_user = User(
        username=normalized_username,
        password=hash_string(raw_password),
        friendly_name=normalized_name,
    )
    new_user.role = Role(rank=normalized_rank)
    new_user.login_status = LoginStatus()

    db.session.add(new_user)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return False, "Unable to create user. Please try again."

    return True, "User created successfully"