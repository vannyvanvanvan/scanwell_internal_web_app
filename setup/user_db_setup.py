from app.functions.hashing import hash_string
from driver import *


# Database context
# ------------------------------------------------------------------------------

with app.app_context():
    user1 = User(id=1, username='admin@mail.com',
                      password=hash_string("test1"), rank='admin')
    user2 = User(id=2, username='cs@mail.com',
                      password=hash_string("test2"), rank='cs')
    user3 = User(id=3, username='sales@mail.com',
                      password=hash_string("test3"), rank='sp')


    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    
    db.session.commit()

# ------------------------------------------------------------------------------


def ResetDatabase():
    with app.app_context():
        db.drop_all()
        db.create_all()
