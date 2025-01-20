from flask import Flask, jsonify
from driver import *
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
db_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '..', 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

# Ensure the instance folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

db.init_app(app)


@app.route('/data')
def get_data():
    with app.app_context():
        # Query schedules with joined data
        query = (
            db.session.query(Schedule)
            .options(
                joinedload(Schedule.spaces).joinedload(Space.reserves),
                joinedload(Schedule.spaces).joinedload(Space.bookings)
            )
            .order_by(
                Schedule.sch_id.asc(),
                # Space.spc_id.asc(),
                # Reserve.rsv_id.asc(),
                # Booking.bk_id.asc()
            )
        )

        sql_query = str(query.statement.compile(db.engine))
        print("Generated SQL Query:")
        print(sql_query)
        schedule_data = query.all()

        # Convert results to a list of dictionaries
        shipping_results = []
        schedule_data.sort()
        for schedule in schedule_data:
            schedule.spaces.sort()
            for space in schedule.spaces:
                space.reserves.sort()
                space.bookings.sort()

            shipping_results.append({
                'schedule_id': schedule.sch_id,
                'carrier': schedule.carrier,
                'service': schedule.service,
                'routing': schedule.routing,
                'MV': schedule.mv,
                'POL': schedule.pol,
                'POD': schedule.pod,
                'CY_Open': schedule.cyopen.strftime('%Y-%m-%d %H:%M:%S'),
                'SI_Cut_Off': schedule.sicutoff.strftime('%Y-%m-%d %H:%M:%S'),
                'CY_CY_CLS': schedule.cycvcls.strftime('%Y-%m-%d %H:%M:%S'),
                'ETD': schedule.etd.strftime('%Y-%m-%d %H:%M:%S'),
                'ETA': schedule.eta.strftime('%Y-%m-%d %H:%M:%S'),
                'spaces': [
                    {
                        'space_id': space.spc_id,
                        'size': space.size,
                        'average_rate': space.avgrate,
                        'suggested_rate': space.sugrate,
                        'status': space.spcstatus,
                        'last_modified_by': space.last_modified_by,
                        'last_modified_at': space.last_modified_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'reserve': [
                            {
                                'reserve_id': reserve.rsv_id,
                                'sales': reserve.sales,
                                'sale_price': reserve.saleprice,
                                'reservation_date': reserve.rsv_date.strftime('%Y-%m-%d %H:%M:%S'),
                                'confirmation_date': reserve.cfm_date.strftime('%Y-%m-%d %H:%M:%S') if reserve.cfm_date else None,
                                'confirmation_cs': reserve.cfm_cs,
                                'remark': reserve.remark
                            }
                            for reserve in space.reserves
                        ],
                        'bookings': [
                            {
                                'booking_id': booking.bk_id,
                                'SO': booking.so,
                                'shipper': booking.shipper,
                                'consignee': booking.consignee,
                                'term': booking.term,
                                'sale_price': booking.saleprice,
                                'remark': booking.remark
                            }
                            for booking in space.bookings
                        ]
                    }
                    for space in schedule.spaces
                ]
            })

        # Query users with roles and login status
        users_query = (
            db.session.query(User)
            .options(
                joinedload(User.role),
                joinedload(User.login_status)
            )
            .all()
        )

        users_results = []
        for user in users_query:
            users_results.append({
                'user_id': user.id,
                'username': user.username,
                'date_created': user.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'role': user.role.rank if user.role else None,
                'login_status': {
                    'status': user.login_status.status if user.login_status else None,
                    'failed_attempts': user.login_status.failed_attempts if user.login_status else None,
                    'last_login': user.login_status.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.login_status and user.login_status.last_login else None,
                    'last_logoff': user.login_status.last_logoff.strftime('%Y-%m-%d %H:%M:%S') if user.login_status and user.login_status.last_logoff else None,
                    'ip_connected': user.login_status.ip_connected if user.login_status else None
                }
            })

        # Return the results as JSON
        return jsonify(shipping_results, users_results)


if __name__ == '__main__':
    app.run(debug=True)
