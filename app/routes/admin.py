from datetime import datetime
from io import StringIO
from flask import Blueprint, make_response, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
import pandas as pd
from ..restriction import role_required
from app.model import db, Data_shipping_schedule, Data_booking, Data_confirm_order
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


admin = Blueprint(
    "admin", __name__, template_folder="../../templates", static_folder="../../static"
)


@admin.route("/")
@login_required
@role_required("admin")
def admin_dashboard():
    results = Data_shipping_schedule.query.all()  # Admin can see all shipping data
    return render_template("dashboard.html", results=results, current_user=current_user)


@admin.route("/add_shipping_schedule", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_shipping_data():
    if request.method == "POST":
        try:
            new_data = Data_shipping_schedule(
                carrier=request.form["carrier"],
                service=request.form["service"],
                routing=request.form["routing"],
                MV=request.form["MV"],
                POL=request.form["POL"],
                POD=request.form["POD"],
                CY_Open=datetime.strptime(request.form["CY_Open"], "%Y-%m-%d"),
                SI_Cut_Off=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["SI_Cut_Off"],
                        time=request.form["SI_Cut_Off_Time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                CY_CY_CLS=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["CY_CY_CLS"],
                        time=request.form["CY_CY_CLS_Time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                ETD=datetime.strptime(request.form["ETD"], "%Y-%m-%d"),
                ETA=datetime.strptime(request.form["ETA"], "%Y-%m-%d"),
                status=request.form["status"],
                user_id=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "shipping_schedule.html",
        mode="Add",
        data=Data_shipping_schedule(
            carrier="",
            service="",
            routing="",
            MV="",
            POL="",
            POD="",
            CY_Open=datetime.now(),
            SI_Cut_Off=datetime.now(),
            CY_CY_CLS=datetime.now(),
            ETD=datetime.now(),
            ETA=datetime.now(),
            status="s1",
            user_id=current_user.id,
        ),
    )


@admin.route("/edit_shipping_schedule/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_shipping_data(id):
    shipping_data = Data_shipping_schedule.query.get_or_404(id)

    if request.method == "POST":
        try:
            shipping_data.carrier = request.form["carrier"]
            shipping_data.service = request.form["service"]
            shipping_data.routing = request.form["routing"]
            shipping_data.MV = request.form["MV"]
            shipping_data.POL = request.form["POL"]
            shipping_data.POD = request.form["POD"]
            shipping_data.CY_Open = datetime.strptime(
                request.form["CY_Open"], "%Y-%m-%d"
            )
            shipping_data.SI_Cut_Off = datetime.strptime(
                "{year} {time}".format(
                    year=request.form["SI_Cut_Off"],
                    time=request.form["SI_Cut_Off_Time"],
                ),
                "%Y-%m-%d %H:%M",
            )
            shipping_data.CY_CY_CLS = datetime.strptime(
                "{year} {time}".format(
                    year=request.form["CY_CY_CLS"],
                    time=request.form["CY_CY_CLS_Time"],
                ),
                "%Y-%m-%d %H:%M",
            )
            shipping_data.ETD = datetime.strptime(request.form["ETD"], "%Y-%m-%d")
            shipping_data.ETA = datetime.strptime(request.form["ETA"], "%Y-%m-%d")
            shipping_data.status = request.form["status"]
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("shipping_schedule.html", mode="Edit", data=shipping_data)


@admin.route("/delete_shipping_schedule/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_shipping_data(id):
    shipping_data = Data_shipping_schedule.query.get_or_404(id)
    db.session.delete(shipping_data)
    db.session.commit()
    flash("Shipping data has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Routes for Data_booking


@admin.route("/add_booking/<int:schedule_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_booking_data(schedule_id):
    shipping_data = Data_shipping_schedule.query.get_or_404(schedule_id)
    if shipping_data.status == "s3":
        flash("Schedule already confirmed. Unable to add booking.")
        return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        try:
            new_data = Data_booking(
                CS=request.form["CS"],
                week=int(request.form["week"]),
                size=request.form["size"],
                Final_Destination=request.form["Final_Destination"],
                Contract_or_Coloader=request.form["Contract_or_Coloader"],
                cost=int(request.form["cost"]),
                Date_Valid=datetime.strptime(request.form["Date_Valid"], "%Y-%m-%d"),
                data_shipping_schedule_id=schedule_id,
                user_id=current_user.id,
            )
            db.session.add(new_data)

            shipping_data.status = "s2"
            db.session.commit()

        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "edit_booking.html",
        schedule_id=schedule_id,
        mode="Add",
        data=Data_booking(
            CS="",
            week=datetime.now().isocalendar().week,
            size="",
            Final_Destination="",
            Contract_or_Coloader="",
            cost=0,
            Date_Valid=datetime.now(),
            data_shipping_schedule_id=schedule_id,
            user_id=current_user.id,
        ),
    )


@admin.route("/edit_booking/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_booking_data(id):
    booking_data = Data_booking.query.get_or_404(id)

    if request.method == "POST":
        try:
            booking_data.CS = request.form["CS"]
            booking_data.week = int(request.form["week"])
            booking_data.size = request.form["size"]
            booking_data.Final_Destination = request.form["Final_Destination"]
            booking_data.Contract_or_Coloader = request.form["Contract_or_Coloader"]
            booking_data.cost = int(request.form["cost"])
            booking_data.Date_Valid = datetime.strptime(
                request.form["Date_Valid"], "%Y-%m-%d"
            )
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_booking.html", mode="Edit", data=booking_data)


@admin.route("/delete_booking/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_booking_data(id):
    booking_data = Data_booking.query.get_or_404(id)
    db.session.delete(booking_data)
    db.session.commit()
    flash("Booking data has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Routes for Data_confirm_order


@admin.route("/add_confirm_order/<int:schedule_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_confirm_order_data(schedule_id):
    shipping_data = Data_shipping_schedule.query.get_or_404(schedule_id)
    if shipping_data.status != "s2":
        flash("Booking required before confirming order.")
        return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        try:
            new_data = Data_confirm_order(
                shipper=request.form["shipper"],
                consignee=request.form["consignee"],
                term=request.form["term"],
                salesman=request.form["salesman"],
                cost=int(request.form["cost"]),
                Date_Valid=datetime.strptime(request.form["Date_Valid"], "%Y-%m-%d"),
                SR=int(request.form["SR"]),
                remark=request.form["remark"],
                data_shipping_schedule_id=schedule_id,
                user_id=current_user.id,
            )
            db.session.add(new_data)

            shipping_data.status = "s3"
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "confirm_order.html",
        schedule_id=schedule_id,
        data=Data_confirm_order(
            shipper="",
            consignee="",
            term="",
            salesman="",
            cost=0,
            Date_Valid=datetime.now(),
            SR=0,
            remark="",
        ),
    )


@admin.route("/edit_confirm_order/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_confirm_order_data(id):
    confirm_order_data = Data_confirm_order.query.get_or_404(id)

    if request.method == "POST":
        try:
            confirm_order_data.shipper = request.form["shipper"]
            confirm_order_data.consignee = request.form["consignee"]
            confirm_order_data.term = request.form["term"]
            confirm_order_data.salesman = request.form["salesman"]
            confirm_order_data.cost = int(request.form["cost"])
            confirm_order_data.Date_Valid = datetime.strptime(
                request.form["Date_Valid"], "%Y-%m-%d"
            )
            confirm_order_data.SR = int(request.form["SR"])
            confirm_order_data.remark = request.form["remark"]
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "confirm_order.html", data=confirm_order_data
    )


@admin.route("/delete_confirm_order/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_confirm_order_data(id):
    confirm_order_data = Data_confirm_order.query.get_or_404(id)
    db.session.delete(confirm_order_data)
    shipping_schedule = Data_shipping_schedule.query.get_or_404(
        confirm_order_data.schedule_id
    )
    shipping_schedule.status = "s2"
    db.session.commit()
    flash("Order confirmation has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@admin.route("/search", methods=["GET", "POST"])
@login_required
@role_required("admin")
def search():
    # print("Search route")  # Debugging line
    q = request.args.get("q")
    show_all = request.args.get("show-all")

    query = (
        db.session.query(Data_shipping_schedule)
        .join(
            Data_booking,
            and_(Data_shipping_schedule.id == Data_booking.data_shipping_schedule_id),
        )
        .join(
            Data_confirm_order,
            and_(
                Data_shipping_schedule.id
                == Data_confirm_order.data_shipping_schedule_id
            ),
        )
        .options(
            joinedload(Data_shipping_schedule.bookings),
            joinedload(Data_shipping_schedule.confirm_orders),
        )
    )

    if q:
        # print(f"Search query: {q}")  # Debugging line
        results = (
            query.filter(
                (Data_shipping_schedule.carrier.ilike(f"%{q}%"))
                | (Data_shipping_schedule.service.ilike(f"%{q}%"))
                | (Data_shipping_schedule.routing.ilike(f"%{q}%"))
                | (Data_shipping_schedule.MV.ilike(f"%{q}%"))
                | (Data_shipping_schedule.POL.ilike(f"%{q}%"))
                | (Data_shipping_schedule.POD.ilike(f"%{q}%"))
                | (Data_shipping_schedule.CY_Open.ilike(f"%{q}%"))
                | (Data_shipping_schedule.SI_Cut_Off.ilike(f"%{q}%"))
                | (Data_shipping_schedule.POD.ilike(f"%{q}%"))
                | (Data_shipping_schedule.CY_CY_CLS.ilike(f"%{q}%"))
                | (Data_shipping_schedule.ETD.ilike(f"%{q}%"))
                | (Data_shipping_schedule.ETA.ilike(f"%{q}%"))
                | (Data_booking.CS.ilike(f"%{q}%"))  # Added status field
            )
            .order_by(
                Data_shipping_schedule.carrier.asc(),
                Data_shipping_schedule.service.desc(),
            )
            .limit(100)
            .all()
        )
        print(f"Results count: {len(results)}")  # Debugging line
    else:
        results = Data_shipping_schedule.query.all()

    if show_all is None:
        results = [data for data in results if data.user_id == current_user.id]

    # print(current_user.id == results[0].user_id) # Debugging line
    return render_template(
        "shipping_table_results.html", results=results, current_user=current_user
    )

@admin.route('/csv/export', methods=["GET", "POST"])
@login_required
@role_required("admin")
def export_csv():
    
    # Query the database for all relevant data
    schedules = Data_shipping_schedule.query.all()
    bookings = Data_booking.query.all()
    confirm_orders = Data_confirm_order.query.all()

    # Combine data into a pandas DataFrame
    data = []

    for schedule in schedules:
        booking = next((b for b in bookings if b.data_shipping_schedule_id == schedule.id), None)
        confirm_order = next((c for c in confirm_orders if c.data_shipping_schedule_id == schedule.id), None)

        data.append({
            'carrier': schedule.carrier,
            'service': schedule.service,
            'routing': schedule.routing,
            'MV': schedule.MV,
            'POL': schedule.POL,
            'POD': schedule.POD,
            'CY_Open': schedule.CY_Open,
            'SI_Cut_Off': schedule.SI_Cut_Off,
            'CY_CY_CLS': schedule.CY_CY_CLS,
            'ETD': schedule.ETD,
            'ETA': schedule.ETA,
            #'status': schedule.status,
            #'user_id': schedule.user_id,
            'CS': booking.CS if booking else '',
            'week': booking.week if booking else '',
            'size': booking.size if booking else '',
            'Final_Destination': booking.Final_Destination if booking else '',
            'Contract_or_Coloader': booking.Contract_or_Coloader if booking else '',
            'cost': booking.cost if booking else '',
            'Date_Valid': booking.Date_Valid if booking else '',
            'shipper': confirm_order.shipper if confirm_order else '',
            'consignee': confirm_order.consignee if confirm_order else '',
            'term': confirm_order.term if confirm_order else '',
            'salesman': confirm_order.salesman if confirm_order else '',
            'SR': confirm_order.SR if confirm_order else '',
            'remark': confirm_order.remark if confirm_order else ''
        })

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a CSV from the DataFrame
    csv_output = StringIO()
    df.to_csv(csv_output, index=False)
    csv_output.seek(0)

    # Send the CSV file as a response
    response = make_response(csv_output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=data_export.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    #For frontend members
    #Put this <a href="{{ url_for('admin.export_csv') }}" class="btn btn-primary">Export Data to CSV</a> to a suitable place
    #It will directly download the file
    return response