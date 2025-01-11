from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


# UTC time for every section
# Each Schedule has multiple Spaces, Each Space has multiple Reserves and Bookings
class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<User: id={self.id}, username={self.username}, rank={self.rank}>"

    def __lt__(self, other):
        return self.id < other.id


class Schedule(db.Model):

    __tablename__ = "schedule"

    sch_id = db.Column(db.Integer, primary_key=True)
    cs = db.Column(db.String(100), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    carrier = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    mv = db.Column(db.String(150), nullable=False)
    pol = db.Column(db.String(100), nullable=False)
    pod = db.Column(db.String(100), nullable=False)
    routing = db.Column(db.String(100), nullable=False)
    cyopen = db.Column(db.DateTime, default=datetime.utcnow())
    sicutoff = db.Column(db.DateTime, default=datetime.utcnow())
    cycvcls = db.Column(db.DateTime, default=datetime.utcnow())
    etd = db.Column(db.DateTime, default=datetime.utcnow())
    eta = db.Column(db.DateTime, default=datetime.utcnow())

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    spaces = db.relationship("Space", backref="schedule", lazy="joined")

    def __repr__(self):
        return f"<Schedule: id={self.sch_id}, cs={self.cs}, week={self.week}>"

    def __lt__(self, other):
        return self.sch_id < other.sch_id


class Space(db.Model):
    __tablename__ = "space"

    spc_id = db.Column(db.Integer, primary_key=True)
    sch_id = db.Column(db.Integer, db.ForeignKey("schedule.sch_id"), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    avgrate = db.Column(db.Integer, nullable=False)
    sugrate = db.Column(db.Integer, nullable=False)
    ratevalid = db.Column(db.DateTime, default=datetime.utcnow())
    proport = db.Column(db.Boolean, nullable=False, default=False)
    spcstatus = db.Column(db.String(20), nullable=False, default="USABLE")
    last_modified_by = db.Column(db.Integer, nullable=True)
    last_modified_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    reserves = db.relationship("Reserve", backref="space", lazy="joined")
    bookings = db.relationship("Booking", backref="space", lazy="joined")

    def __repr__(self):
        return f"<Space: id={self.spc_id}, schedule={self.sch_id}, spcstatus={self.spcstatus}, void={self.void}>"

    def __lt__(self, other):
        return self.spc_id < other.spc_id

    def update_status(self, new_status, user_id):
        # Updates the SPCSTATUS and logs the user making the change.
        self.spcstatus = new_status
        self.last_modified_by = user_id
        self.last_modified_at = datetime.utcnow()


class Reserve(db.Model):
    __tablename__ = "reserve"

    rsv_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey("space.spc_id"), nullable=False)
    sales = db.Column(db.String(100), nullable=False)
    saleprice = db.Column(db.Integer, nullable=False)
    rsv_date = db.Column(db.DateTime, default=datetime.utcnow())
    cfm_date = db.Column(db.DateTime, nullable=True)
    cfm_cs = db.Column(db.String(100), nullable=True)
    void = db.Column(db.Boolean, nullable=False, default=False)
    remark = db.Column(db.String(300), nullable=True)

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Reserve: id={self.rsv_id}, space={self.spc_id}, sales={self.sales}, void={self.void}>"

    def __lt__(self, other):
        return self.rsv_id < other.rsv_id


class Booking(db.Model):
    __tablename__ = "booking"

    bk_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey("space.spc_id"), nullable=False)
    so = db.Column(db.String(100), nullable=False)
    findest = db.Column(db.String(100), nullable=False)
    ct_cl = db.Column(db.String(100), nullable=False)
    shipper = db.Column(db.String(100), nullable=False)
    consignee = db.Column(db.String(200), nullable=False)
    term = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.String(100), nullable=False)
    saleprice = db.Column(db.Integer, nullable=False)
    void = db.Column(db.Boolean, nullable=False, default=False)
    remark = db.Column(db.String(300), nullable=True)

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Booking: id={self.bk_id}, space={self.spc_id}, so={self.so}, void={self.void}>"

    def __lt__(self, other):
        return self.bk_id < other.bk_id
