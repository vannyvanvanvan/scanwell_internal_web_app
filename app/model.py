from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


# UTC time for every section
# Each Schedule has multiple Spaces, Each Space has multiple Reserves and Bookings
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    friendly_name = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship(
        "Role", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    login_status = db.relationship(
        "LoginStatus",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User: id={self.id}, username={self.username}>"

    def __lt__(self, other):
        return self.id < other.id

    def pretty_rank(self):
        if self.role.rank == "admin":
            return "Admin"
        elif self.role.rank == "cs":
            return "Customer Service"
        elif self.role.rank == "sales":
            return "Sales"
        else:
            return "Invalid User"


class Role(db.Model):
    __tablename__ = "role"
    # 3 user role: admin, cs, sales. 1 system role: system
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    rank = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role: user_id={self.user_id}, rank={self.rank}>"


class LoginStatus(db.Model):
    __tablename__ = "login_status"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    lock_status = db.Column(db.String(50), nullable=False, default="unlocked")
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    last_logoff = db.Column(db.DateTime, nullable=True)
    ip_connected = db.Column(db.String(100), nullable=True)

    user = db.relationship("User", back_populates="login_status")

    def __repr__(self):
        return f"<LoginStatus: user_id={self.user_id}, status={self.lock_status}, last_login={self.last_login}>"


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
        return f"<Space: id={self.spc_id}, schedule={self.sch_id}, spcstatus={self.spcstatus}>"

    def __lt__(self, other):
        return self.spc_id < other.spc_id

    def update_status(self, new_status, user_id):
        # Updates the SPCSTATUS and logs the user making the change.
        self.spcstatus = new_status
        self.last_modified_by = user_id
        self.last_modified_at = datetime.utcnow()

    def proport_yesno(self):
        return "Yes" if self.proport else "No"


class Reserve(db.Model):
    __tablename__ = "reserve"

    rsv_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey("space.spc_id"), nullable=False)
    saleprice = db.Column(db.Integer, nullable=False)
    rsv_date = db.Column(db.DateTime, default=datetime.utcnow())
    cfm_date = db.Column(db.DateTime, nullable=True)
    cfm_cs = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    void = db.Column(db.Boolean, nullable=False, default=False)
    remark = db.Column(db.String(300), nullable=True)

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Reserve: id={self.rsv_id}, space={self.spc_id}, sales={self.sales}, void={self.void}>"

    def __lt__(self, other):
        return self.rsv_id < other.rsv_id

    def void_yesno(self):
        return "Yes" if self.void else "No"


class Booking(db.Model):
    __tablename__ = "booking"

    bk_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey("space.spc_id"), nullable=False)
    # Foreign Key to Reserve
    rsv_id = db.Column(db.Integer, db.ForeignKey("reserve.rsv_id"), nullable=True)

    so = db.Column(db.String(100), nullable=False)
    findest = db.Column(db.String(100), nullable=False)
    ct_cl = db.Column(db.String(100), nullable=False)
    shipper = db.Column(db.String(100), nullable=False)
    consignee = db.Column(db.String(200), nullable=False)
    term = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    saleprice = db.Column(db.Integer, nullable=False)
    void = db.Column(db.Boolean, nullable=False, default=False)
    remark = db.Column(db.String(300), nullable=True)

    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Booking: id={self.bk_id}, space={self.spc_id}, so={self.so}, void={self.void}>"

    def __lt__(self, other):
        return self.bk_id < other.bk_id

    def void_yesno(self):
        return "Yes" if self.void else "No"
