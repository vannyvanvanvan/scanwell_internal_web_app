from app.functions.hashing import hash_string
from app.model import Role, User, LoginStatus, db
from driver import app


# Database context
# ------------------------------------------------------------------------------

with app.app_context():
    # Creating users
    users = [
        User(
            username="admin@mail.com",
            friendly_name="default_admin",
            password=hash_string("test1"),
        ),
        User(
            username="cs@mail.com",
            friendly_name="default_cs",
            password=hash_string("test2"),
        ),
        User(
            username="sales@mail.com",
            friendly_name="default_sales",
            password=hash_string("test3"),
        ),
        User(
            username="fanny",
            friendly_name="fanny",
            password=hash_string("fanny"),
        ),
        User(
            username="eric",
            friendly_name="eric",
            password=hash_string("eric"),
        ),
        User(
            username="chi-chris",
            friendly_name="chi-chris",
            password=hash_string("chi-chris"),
        ),
    ]
    db.session.add_all(users)
    db.session.commit()
    db.session.flush()

    # Assigning roles
    roles = [
        Role(user_id=users[0].id, rank="admin"),
        Role(user_id=users[1].id, rank="cs"),
        Role(user_id=users[2].id, rank="sales"),
        Role(user_id=users[3].id, rank="cs"),
        Role(user_id=users[4].id, rank="sales"),
        Role(user_id=users[5].id, rank="sales"),
    ]

    db.session.add_all(roles)
    db.session.commit()

    # Creating default login status
    login_statuses = [
        LoginStatus(user_id=users[0].id, lock_status="unlocked", failed_attempts=0),
        LoginStatus(user_id=users[1].id, lock_status="unlocked", failed_attempts=0),
        LoginStatus(user_id=users[2].id, lock_status="unlocked", failed_attempts=0),
        LoginStatus(user_id=users[3].id, lock_status="unlocked", failed_attempts=0),
        LoginStatus(user_id=users[4].id, lock_status="unlocked", failed_attempts=0),
        LoginStatus(user_id=users[5].id, lock_status="unlocked", failed_attempts=0),
    ]

    db.session.add_all(login_statuses)

    db.session.commit()

# ------------------------------------------------------------------------------
