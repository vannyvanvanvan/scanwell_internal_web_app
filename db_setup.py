from datetime import datetime
from app.hashing import hash_string
from driver import *
from app.model import Data_booking, Data_confirm_order, Data_shipping_schedule, User_data

# Database context
# ------------------------------------------------------------------------------

with app.app_context():
    user1 = User_data(id=1, username='admin@mail.com',
                      password=hash_string("test1"), rank='admin')
    user2 = User_data(id=2, username='user@mail.com',
                      password=hash_string("test2"), rank='user')
    user3 = User_data(id=3, username='user2@mail.com',
                      password=hash_string("test3"), rank='user')
    
    schedule_1 = Data_shipping_schedule(id = 1, carrier = "X Company", service = "X Service", routing = "Hong Kong", MV = "X Ship", POL = "Ching", POD = "Ching", CY_Open = datetime.utcnow(), SI_Cut_Off = datetime.utcnow(), CY_CY_CLS = datetime.utcnow(), ETD = datetime.utcnow(), ETA = datetime.utcnow(), status = "s1",  user_id =  "1")
    booking_1 = Data_booking(id = 1, CS = "Vanny", week = "22", size = "10", Final_Destination = "Japan", Contract_or_Coloader = "X", cost = "100", Date_Valid = datetime.utcnow(), data_shipping_schedule_id = 1, user_id = "1")
    booking_2 = Data_booking(id = 2, CS = "Timmy", week = "50", size = "20", Final_Destination = "Japan", Contract_or_Coloader = "X", cost = "200", Date_Valid = datetime.utcnow(), data_shipping_schedule_id = 1, user_id = "1")
    confirm_order_1 = Data_confirm_order(id = 1,shipper = "X Shipper", consignee = "X consignee", term = "XXX", salesman = "X Salesman", SR = "20", remark = "Nil", data_shipping_schedule_id = 1, user_id = "1")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(schedule_1)
    db.session.add(booking_1)
    db.session.add(booking_2)
    db.session.add(confirm_order_1)

    db.session.commit()

# ------------------------------------------------------------------------------


def ResetDatabase():
    with app.app_context():
        db.drop_all()
        db.create_all()
