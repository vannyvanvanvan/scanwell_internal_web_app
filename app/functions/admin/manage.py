from app.model import db, User, Role
from app.functions.hashing import hash_string


def get_user(user_id: int):
    return User.query.get(user_id)

# Could be extended to check for other roles in the future
# For now, only have 'admin', 'cs', and 'sales'
EXISTING_RANKS = {"admin", "cs", "sales"}

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

    # For Username
    if new_username is not None and new_username.strip() != "":
        requested_username = new_username.strip()
        username_taken = (
            User.query.filter(User.username == requested_username, User.id != user_id).first()
            is not None
        )
        if username_taken:
            return False, "Username already exists"
        user.username = requested_username

    # For Friendly name
    if new_friendly_name is not None and new_friendly_name.strip() != "":
        user.friendly_name = new_friendly_name.strip()

    # Role rank
    if new_rank is not None and new_rank.strip() != "":
        requested_rank = new_rank.strip().lower()
        if requested_rank not in EXISTING_RANKS:
            return False, "Invalid role rank"
        if user.role is None:
            user.role = Role(user_id=user.id, rank=requested_rank)
        else:
            user.role.rank = requested_rank

    # Password
    if new_password is not None and new_password != "":
        user.password = hash_string(new_password)

    db.session.commit()
    return True, "User updated successfully"


