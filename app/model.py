from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User_data(db.Model, UserMixin):

    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    # UTC time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User_data %r>' % self.id


class Data_shipping_schedule(db.Model):

    __tablename__ = 'data_shipping_schedule'

    id = db.Column(db.Integer, primary_key=True)
    carrier = db.Column(db.String(100), nullable= False)                                    #   Shipping company
    service = db.Column(db.String(100), nullable=False)                                     #   Shipping service
    routing = db.Column(db.String(100), nullable=False)                                     #   Routing 
    MV = db.Column(db.String(100), nullable=False)                                          #   Master vessel (ship name)
    POL = db.Column(db.String(100), nullable=False)                                         #   Port of loading 
    POD = db.Column(db.String(100), nullable=False)                                         #   Port of discharge 
    CY_Open = db.Column(db.DateTime, nullable=False)                                        #   Container yard open (should be in datetime format)
    SI_Cut_Off = db.Column(db.DateTime, nullable=False)                                     #   Shipping information off (should be in datetime format)
    CY_CY_CLS = db.Column(db.DateTime, nullable=False)                                      #   Closing date (should be in datetime format)
    ETD =  db.Column(db.DateTime, nullable=False)                                           #   Estimated Time of Departure (should be in datetime format)
    ETA =  db.Column(db.DateTime, nullable=False)                                           #   Estimated Time of Arrival (should be in datetime format)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)                                       # Status s1 -> s2 -> s3

    # One-to-many relationship with Data_booking
    bookings = db.relationship('Data_booking', backref='data_shipping_schedule', lazy=True)
    # One-to-one relationship with Data_confirm_order
    confirm_orders = db.relationship('Data_confirm_order', backref='data_shipping_schedule', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)

    def __repr__(self):
        return '<Data_shipping_schedule %r>' % self.id


class Data_booking(db.Model):
    __tablename__ = 'data_booking'

    id = db.Column(db.Integer, primary_key=True)
    CS = db.Column(db.String(50), nullable=False)                                           #   Customer service 
    week = db.Column(db.Integer, nullable=False)                                            #
    size = db.Column(db.String(100), nullable=False) #Will change later                     #   Container size
    Final_Destination = db.Column(db.String(100), nullable= False)                          #   Final destination
    Contract_or_Coloader = db.Column(db.String(100), nullable=False) #Will change later     #   Contract/Co-loader
    cost = db.Column(db.Integer, nullable=False)                                            #   Cost
    Date_Valid = db.Column(db.DateTime, nullable=False)                                     #   Rate valid (should be in datetime format)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    data_shipping_schedule_id = db.Column(db.Integer, db.ForeignKey('data_shipping_schedule.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)

    def __repr__(self):
        return '<Data_booking %r>' % self.id


class Data_confirm_order(db.Model):
    __tablename__ = 'data_confirm_order'

    id = db.Column(db.Integer, primary_key=True)
    shipper = db.Column(db.String(100), nullable=False)                                     #   Shipper 
    consignee = db.Column(db.String(100), nullable=False)                                   #   Consignee 
    term = db.Column(db.String(100), nullable=False)                                        #   Shipping term
    salesman = db.Column(db.String(100), nullable=False)                                    #   Salesman
    cost = db.Column(db.Integer, nullable=False)                                            #   Cost
    Date_Valid = db.Column(db.DateTime, nullable=False)                                     #   Rate valid (should be in datetime format)
    SR = db.Column(db.Integer, nullable=False)  #Will change later                          #   Selling rate 
    remark = db.Column(db.String(1000), nullable=False)                                     #   Comments
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    data_shipping_schedule_id = db.Column(db.Integer, db.ForeignKey('data_shipping_schedule.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)

    def __repr__(self):
        return '<Data_confirm_order %r>' % self.id
