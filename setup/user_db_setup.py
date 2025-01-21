from app.functions.hashing import hash_string
from app.model import Role, User, LoginStatus, db
from driver import create_app

app = create_app()


# Database context
# ------------------------------------------------------------------------------

with app.app_context():
    # Creating users
    user1 = User(username='admin@mail.com', password=hash_string("test1"))
    user2 = User(username='cs@mail.com', password=hash_string("test2"))
    user3 = User(username='sales@mail.com', password=hash_string("test3"))
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    db.session.flush()

    # Assigning roles
    role1 = Role(user_id=user1.id, rank='admin')
    role2 = Role(user_id=user2.id, rank='cs')
    role3 = Role(user_id=user3.id, rank='sp')

    # Creating default login status
    login_status1 = LoginStatus(user_id=user1.id, status='offline', failed_attempts=0)
    login_status2 = LoginStatus(user_id=user2.id, status='offline', failed_attempts=0)
    login_status3 = LoginStatus(user_id=user3.id, status='offline', failed_attempts=0)

    db.session.add_all([role1, role2, role3, login_status1, login_status2, login_status3])
    
    db.session.commit()

# ------------------------------------------------------------------------------

