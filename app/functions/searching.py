from datetime import datetime
from flask import render_template
from flask_login import current_user
from sqlalchemy import or_
from app.model import Schedule, Space, Reserve, Booking

# Function for making a search query in the database
def search_database(query: str):
    
    results = []

    schedules = (
        Schedule.query.filter(
            or_(
                Schedule.carrier.ilike(f"%{query}%"),
                Schedule.service.ilike(f"%{query}%"),
                Schedule.routing.ilike(f"%{query}%"),
                Schedule.mv.ilike(f"%{query}%"),
                Schedule.pol.ilike(f"%{query}%"),
                Schedule.pod.ilike(f"%{query}%"),
            )
        )
        .limit(50)
        .all()
    )
    results.extend(schedules)

    spaces = (
        Space.query.filter(
            or_(
                Space.size.ilike(f"%{query}%"),
                Space.spcstatus.ilike(f"%{query}%"),
            )
        )
        .limit(50)
        .all()
    )
    results.extend(spaces)

    reserves = (
        Reserve.query.filter(
            or_(
                Reserve.sales.ilike(f"%{query}%"),
                Reserve.remark.ilike(f"%{query}%"),
            )
        )
        .limit(50)
        .all()
    )
    results.extend(reserves)

    bookings = (
        Booking.query.filter(
            or_(
                Booking.so.ilike(f"%{query}%"),
                Booking.findest.ilike(f"%{query}%"),
                Booking.ct_cl.ilike(f"%{query}%"),
                Booking.shipper.ilike(f"%{query}%"),
                Booking.consignee.ilike(f"%{query}%"),
                Booking.sales.ilike(f"%{query}%"),
                Booking.remark.ilike(f"%{query}%"),
            )
        )
        .limit(50)
        .all()
    )
    results.extend(bookings)
    
    print(f"Search query: {query}")
    print(f"Total results found: {len(results)}")

    print(f"Schedules found: {len(schedules)}")
    print(f"Spaces found: {len(spaces)}")
    print(f"Reserve found: {len(reserves)}")
    print(f"Booking found: {len(bookings)}")
    return results


def render_search_results(query: str):
    results = search_database(query)
    return render_template("shipping_table_results.html", current_user=current_user,  results=results)
