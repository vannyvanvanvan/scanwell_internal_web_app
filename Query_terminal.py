from flask import Flask
from app.model import Data_shipping_schedule, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    shipping_schedule = Data_shipping_schedule.query.all()
    for i in shipping_schedule:
        for j in i.data_booking:
            print(j.id)