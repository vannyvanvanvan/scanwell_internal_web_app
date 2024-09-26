from datetime import datetime
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from app.restriction import role_required
from app.model import db, Data_shipping_schedule, Data_booking, Data_confirm_order
from sqlalchemy.orm import joinedload

user = Blueprint(
    "user", __name__, template_folder="../templates", static_folder="../static"
)


@user.route("/")
@login_required
@role_required("user")
def user_dashboard():
    all_data = Data_shipping_schedule.query.all()
    results = [data for data in all_data if data.user_id == current_user.id]
    return render_template(
        "dashboard.html", results=results, current_user_id=current_user.id
    )


# Routes for Data_shipping_schedule


@user.route("/add_shipping_schedule", methods=["GET", "POST"])
@login_required
@role_required("user")
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
                status="s1",
                user_id=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for("user.user_dashboard"))
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


@user.route("/edit_shipping_schedule/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("user")
def edit_shipping_data(id):
    shipping_data = Data_shipping_schedule.query.get_or_404(id)
    if shipping_data.user_id != current_user.id:
        return redirect(url_for("user.user_dashboard"))

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
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for("user.user_dashboard"))
    return render_template("shipping_schedule.html", mode="Edit", data=shipping_data)


@user.route("/delete_shipping_schedule/<int:id>", methods=["POST"])
@login_required
@role_required("user")
def delete_shipping_data(id):
    shipping_data = Data_shipping_schedule.query.get_or_404(id)
    if shipping_data.user_id != current_user.id:
        flash("You do not have permission to delete this item.")
        return redirect(url_for("user.user_dashboard"))

    db.session.delete(shipping_data)
    db.session.commit()
    flash("Shipping data has been deleted.", "success")
    return redirect(url_for("user.user_dashboard"))


# Routes for Data_booking


@user.route("/add_booking/<int:schedule_id>", methods=["GET", "POST"])
@login_required
@role_required("user")
def add_booking_data(schedule_id):
    shipping_data = Data_shipping_schedule.query.get_or_404(schedule_id)
    if shipping_data.user_id != current_user.id:
        flash("You are not allowed to add booking data for this schedule.")
        return redirect(url_for("user.user_dashboard"))
    if shipping_data.status == "s3":
        flash("Schedule already confirmed. Unable to add booking.")
        return redirect(url_for("user.user_dashboard"))

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
        return redirect(url_for("user.user_dashboard"))
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


@user.route("/edit_booking/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("user")
def edit_booking_data(id):
    booking_data = Data_booking.query.get_or_404(id)
    if booking_data.user_id != current_user.id:
        flash("You are not allowed to edit booking data for this schedule.")
        return redirect(url_for("user.user_dashboard"))

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
        return redirect(url_for("user.user_dashboard"))
    return render_template("edit_booking.html", mode="Edit", data=booking_data)


@user.route("/delete_booking/<int:id>", methods=["POST"])
@login_required
@role_required("user")
def delete_booking_data(id):
    booking_data = Data_booking.query.get_or_404(id)
    if booking_data.user_id != current_user.id:
        flash("You do not have permission to delete this item.")
        return redirect(url_for("user.user_dashboard"))

    db.session.delete(booking_data)
    db.session.commit()
    flash("Booking data has been deleted.", "success")
    return redirect(url_for("user.user_dashboard"))


# Routes for Data_confirm_order


@user.route("/add_confirm_order/<int:schedule_id>", methods=["GET", "POST"])
@login_required
@role_required("user")
def add_confirm_order_data(schedule_id):
    shipping_data = Data_shipping_schedule.query.get_or_404(schedule_id)
    if shipping_data.user_id != current_user.id or shipping_data.status != "s3":
        flash("You are not allowed to add confirm order data for this schedule.")
        return redirect(url_for("user.user_dashboard"))

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
                status="s3",
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("user.user_dashboard"))
    return render_template("user_add_confirm_order_data.html", schedule_id=schedule_id)


@user.route("/edit_confirm_order/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("user")
def edit_confirm_order_data(id):
    confirm_order_data = Data_confirm_order.query.get_or_404(id)
    if confirm_order_data.user_id != current_user.id:
        return redirect(url_for("user.user_dashboard"))

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
            confirm_order_data.data_shipping_schedule_id = request.form[
                "data_shipping_schedule_id"
            ]
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("user.user_dashboard"))
    return render_template(
        "user_edit_confirm_order_data.html", confirm_order_data=confirm_order_data
    )


@user.route("/delete_confirm_order/<int:id>", methods=["POST"])
@login_required
@role_required("user")
def delete_confirm_order_data(id):
    confirm_order_data = Data_confirm_order.query.get_or_404(id)
    if confirm_order_data.user_id != current_user.id:
        flash("You do not have permission to delete this item.")
        return redirect(url_for("user.user_dashboard"))

    db.session.delete(confirm_order_data)
    db.session.commit()
    flash("Confirm order data has been deleted.", "success")
    return redirect(url_for("user.user_dashboard"))


@user.route("/search", methods=["GET", "POST"])
@login_required
@role_required("user")
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
