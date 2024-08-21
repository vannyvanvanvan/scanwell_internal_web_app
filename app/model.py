from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User_data(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    #UTC time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User_data %r>' % self.id
    
class Shipping_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #UTC time
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Above for debugging purposes
    CS = db.Column(db.String(50), nullable=False)                                           #   Customer service 
    week = db.Column(db.Integer, nullable=False)                                            #
    carrier = db.Column(db.String(100), nullable= False)                                    #   Shipping company
    service = db.Column(db.String(100), nullable=False)                                     #   Shipping service
    MV = db.Column(db.String(100), nullable=False)                                          #   Master vessel (ship name)
    SO = db.Column(db.String(100), nullable=False)                                          #   Shipping order
    size = db.Column(db.String(100), nullable=False) #Will change later                     #   Container size
    POL = db.Column(db.String(100), nullable=False)                                         #   Port of loading 
    POD = db.Column(db.String(100), nullable=False)                                         #   Port of discharge 
    Final_Destination = db.Column(db.String(100), nullable= False)                          #   Final destination 
    routing = db.Column(db.String(100), nullable=False)                                     #   Routing 
    CY_Open = db.Column(db.DateTime, nullable=False)                                        #   Container yard open (should be in datetime format)
    SI_Cut_Off = db.Column(db.DateTime, nullable=False) #Will change later                  #   Shipping information off (should be in datetime format)
    CY_CY_CLS = db.Column(db.DateTime, nullable=False) #Will change later                   #   Closing date (should be in datetime format)
    ETD =  db.Column(db.DateTime, nullable=False) #Will change later                        #   Estimated Time of Departure (should be in datetime format)
    ETA =  db.Column(db.DateTime, nullable=False) #Will change later                        #   Estimated Time of Arrival (should be in datetime format)
    Contract_or_Coloader = db.Column(db.String(100), nullable=False) #Will change later     #   Contract/Co-loader 
    shipper = db.Column(db.String(100), nullable=False)                                     #   Shipper 
    consignee = db.Column(db.String(100), nullable=False)                                   #   Consignee 
    term = db.Column(db.String(100), nullable=False)                                        #   Shipping term
    salesman = db.Column(db.String(100), nullable=False)                                    #   Salesman
    cost = db.Column(db.Integer, nullable=False)                                            #   Cost
    Date_Valid = db.Column(db.DateTime, nullable=False)                                     #   Rate valid (should be in datetime format)
    SR = db.Column(db.Integer, nullable=False)  #Will change later                          #   Selling rate 
    remark = db.Column(db.String(1000), nullable=False)                                     #   Comments
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)
    
    def __repr__(self):
        return '<Shipping_data %r>' % self.id
    