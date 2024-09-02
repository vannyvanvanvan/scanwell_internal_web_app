from flask import Flask, jsonify
from app.model import Data_shipping_schedule, db
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/data')
def get_data():
    with app.app_context():
        # query with joinedload
        query = (
            db.session.query(Data_shipping_schedule)
            .options(
                joinedload(Data_shipping_schedule.bookings),
                joinedload(Data_shipping_schedule.confirm_orders)
            )
        )
        
        sql_query = str(query.statement.compile(db.engine))
        print("Generated SQL Query:")
        print(sql_query)
        
        # execute the query and fetch results
        user_data = query.all()
        
        # convert results to a list of dictionaries
        results = []
        for data in user_data:
            results.append({
                'id': data.id,
                'carrier': data.carrier,
                'service': data.service,
                'routing': data.routing,
                'MV': data.MV,
                'POL': data.POL,
                'POD': data.POD,
                'CY_Open': data.CY_Open.strftime('%Y-%m-%d %H:%M:%S'),
                'SI_Cut_Off': data.SI_Cut_Off.strftime('%Y-%m-%d %H:%M:%S'),
                'CY_CY_CLS': data.CY_CY_CLS.strftime('%Y-%m-%d %H:%M:%S'),
                'ETD': data.ETD.strftime('%Y-%m-%d %H:%M:%S'),
                'ETA': data.ETA.strftime('%Y-%m-%d %H:%M:%S'),
                'status': data.status,
                'bookings': [
                    {
                        'id': booking.id,
                        'CS': booking.CS,
                        'week': booking.week,
                        'size': booking.size,
                        'Final_Destination': booking.Final_Destination,
                        'Contract_or_Coloader': booking.Contract_or_Coloader,
                        'cost': booking.cost,
                        'Date_Valid': booking.Date_Valid.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for booking in data.bookings
                ],
                'confirm_orders': [
                    {
                        'id': confirm_order.id,
                        'shipper': confirm_order.shipper,
                        'consignee': confirm_order.consignee,
                        'term': confirm_order.term,
                        'salesman': confirm_order.salesman,
                        'cost': confirm_order.cost,
                        'Date_Valid': confirm_order.Date_Valid.strftime('%Y-%m-%d %H:%M:%S'),
                        'SR': confirm_order.SR,
                        'remark': confirm_order.remark
                    }
                    for confirm_order in data.confirm_orders
                ]
            })
        
        # return the results as JSON
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)