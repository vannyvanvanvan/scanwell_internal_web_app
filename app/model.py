from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User_data(db.Model, UserMixin):

    __tablename__ = 'user_data'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    # UTC time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User_data %r>' % self.user_id

class Schedule_data(db.Model):

    __tablename__ = 'schedule_data'

    sch_id = db.Column(db.Integer, primary_key=True)
    cs = db.Column(db.String(100), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    carrier = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    mv = db.Column(db.String(150), nullable=False)
    pol = db.Column(db.String(100), nullable=False)
    pod = db.Column(db.String(100), nullable=False)
    routing = db.Column(db.String(100), nullable=False)
    cyopen = db.Column(db.DateTime, default=datetime.utcnow)
    sicutoff = db.Column(db.DateTime, default=datetime.utcnow)
    cycvcls = db.Column(db.DateTime, default=datetime.utcnow)
    etd = db.Column(db.DateTime, default=datetime.utcnow)
    eta = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'), nullable=False)

    def __repr__(self):
        return '<schedule_data %r>' % self.spc_id


class Space_data(db.Model):
    __tablename__ = 'space_data'

    spc_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey('data_booking.spc_id'), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    avgrate= db.Column(db.Integer, nullable=False)
    sugrate = db.Column(db.Integer, nullable=False)
    ratevalid = db.Column(db.DateTime, default=datetime.utcnow)
    proport = db.Column(db.String(50), nullable=False)
    spcstatus = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'), nullable=False)

    def __repr__(self):
        return '<space_data %r>' % self.spc_id


class Reserve_data(db.Model):
    __tablename__ = 'reserve_data'

    rsv_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey('data_booking.spc_id'), nullable=False)
    sales = db.Column(db.String(100), nullable=False)
    saleprice = db.Column(db.Integer, nullable=False)
    rsv_date = db.Column(db.DateTime, default=datetime.utcnow)
    cfm_date = db.Column(db.DateTime, nullable=True)
    cfm_cs = db.Column(db.String(100), nullable=True)
    void = db.Column(db.String(1), default='F')
    remark = db.Column(db.String(300), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'), nullable=False)

    def __repr__(self):
        return '<reserve_data %r>' % self.rsv_id
    
    
class Booking_data(db.Model):
    __tablename__ = 'booking_data'

    bk_id = db.Column(db.Integer, primary_key=True)
    spc_id = db.Column(db.Integer, db.ForeignKey('data_booking.spc_id'), nullable=False)
    so = db.Column(db.String(100), nullable=False)
    findest = db.Column(db.String(100), nullable=False)
    ct_cl = db.Column(db.String(100), nullable=False)
    shipper = db.Column(db.String(100), nullable=False)
    consignee = db.Column(db.String(200), nullable=False)
    term = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.String(100), nullable=False)
    saleprice = db.Column(db.Integer, nullable=False)
    void = db.Column(db.String(1), default='F')
    remark = db.Column(db.String(300), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'), nullable=False)

    def __repr__(self):
        return '<booking_data %r>' % self.bk_id

