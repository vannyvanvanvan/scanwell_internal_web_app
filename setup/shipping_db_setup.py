from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta
from app.model import db, User, Schedule, Space, Reserve, Booking

fake = Faker()

# Create random test users
def create_users(n=5):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            rank=choice(["user", "admin"]),
            date_created=datetime.utcnow(),
        )
        db.session.add(user)
    db.session.commit()
    print(f"Created {n} users.")

# Create random schedules
def create_schedules(n=10):
    users = User.query.all()
    for _ in range(n):
        schedule = Schedule(
            carrier=fake.company(),
            service=fake.bs(),
            routing=fake.city(),
            mv=fake.lexify(text="MV ?????"),
            pol=fake.city(),
            pod=fake.city(),
            cyopen=datetime.utcnow() + timedelta(days=randint(1, 10)),
            sicutoff=datetime.utcnow() + timedelta(days=randint(11, 20)),
            cycvcls=datetime.utcnow() + timedelta(days=randint(21, 30)),
            etd=datetime.utcnow() + timedelta(days=randint(31, 40)),
            eta=datetime.utcnow() + timedelta(days=randint(41, 50)),
            owner=choice(users).user_id,
        )
        db.session.add(schedule)
    db.session.commit()
    print(f"Created {n} schedules.")

# Create random spaces
def create_spaces(n=20):
    schedules = Schedule.query.all()
    users = User.query.all()
    for _ in range(n):
        space = Space(
            sch_id=choice(schedules).sch_id,
            size=choice(["20ft", "40ft", "40ft HC"]),
            avgrate=randint(1000, 5000),
            sugrate=randint(1000, 5000),
            ratevalid=datetime.utcnow() + timedelta(days=randint(1, 30)),
            proport=choice(["Y", "N"]),
            spcstatus=choice(["USABLE", "RV_SUBMIT", "BK_RESERVED", "INVALID"]),
            void=choice(["F", "T"]),
            owner=choice(users).user_id,
        )
        db.session.add(space)
    db.session.commit()
    print(f"Created {n} spaces.")

# Create random reservations
def create_reservations(n=15):
    spaces = Space.query.filter_by(spcstatus="USABLE").all()
    users = User.query.all()
    for _ in range(min(n, len(spaces))):
        space = choice(spaces)
        reservation = Reserve(
            spc_id=space.spc_id,
            sales=fake.name(),
            saleprice=randint(1500, 6000),
            rsv_date=datetime.utcnow(),
            remark=fake.sentence(),
            void="F",
            owner=choice(users).user_id,
        )
        space.spcstatus = "RV_SUBMIT"  # Update space status
        db.session.add(reservation)
    db.session.commit()
    print(f"Created {n} reservations.")

# Create random bookings
def create_bookings(n=10):
    spaces = Space.query.filter_by(spcstatus="RV_SUBMIT").all()
    users = User.query.all()
    for _ in range(min(n, len(spaces))):
        space = choice(spaces)
        booking = Booking(
            spc_id=space.spc_id,
            so=fake.unique.lexify(text="SO??????"),
            findest=fake.city(),
            ct_cl=choice(["FOB", "CIF"]),
            shipper=fake.name(),
            consignee=fake.name(),
            term=choice(["CFR", "EXW", "FOB"]),
            sales=fake.name(),
            saleprice=randint(2000, 7000),
            void="F",
            remark=fake.sentence(),
            owner=choice(users).user_id,
        )
        space.spcstatus = "BK_CONFIRM"  # Update space status
        db.session.add(booking)
    db.session.commit()
    print(f"Created {n} bookings.")

if __name__ == "__main__":
    with db.session.begin():
        create_users()
        create_schedules()
        create_spaces()
        create_reservations()
        create_bookings()
    print("Database population complete.")
