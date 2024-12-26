from datetime import datetime
from io import StringIO
import os
from flask import (
    Blueprint,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import current_user, login_required
import pandas as pd
from ..restriction import role_required
from app.model import db, User, Schedule, Space, Reserve, Booking
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from __main__ import app
import uuid

admin = Blueprint(
    "admin", __name__, template_folder="../../templates", static_folder="../../static"
)


@admin.route("/")
@login_required
@role_required("admin")
def admin_dashboard():
    results = Schedule.query.all()
    # Admin can see all shipping data
    return render_template("dashboard.html", results=results, current_user=current_user)

# Routes for Schedule
#----------------------------------------------------------------------------------------
@admin.route("/add_Schedule", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_Schedule_data():
    if request.method == "POST":
        try:
            new_data = Schedule(
                cs=request.form["cs"],
                week=int(request.form["week"]),
                carrier=request.form["carrier"],
                service=request.form["service"],
                mv=request.form["mv"],
                pol=request.form["pol"],
                pod=request.form["pod"],
                routing=request.form["routing"],
                cyopen=datetime.strptime(request.form["cyopen"], "%Y-%m-%d"),
                sicutoff=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["sicutoff"],
                        time=request.form["sicutoff_time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                cycvcls=datetime.strptime(
                    "{year} {time}".format(
                        year=request.form["cycvcls"],
                        time=request.form["cycvcls_time"],
                    ),
                    "%Y-%m-%d %H:%M",
                ),
                etd=datetime.strptime(request.form["etd"], "%Y-%m-%d"),
                eta=datetime.strptime(request.form["eta"], "%Y-%m-%d"),
                owner=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            # Handle the error and provide feedback to the user
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "edit_Schedule.html",
        mode="Add",
        data=Schedule(
            cs="",
            week=datetime.now().isocalendar().week,
            carrier="",
            service="",
            mv="",
            pol="",
            pod="",
            routing="",
            cyopen=datetime.now(),
            sicutoff=datetime.now(),
            cycvcls=datetime.now(),
            etd=datetime.now(),
            eta=datetime.now(),
            owner=current_user.id
        ),
    )


@admin.route("/edit_Schedule/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_Schedule_data(sch_id):
    Schedule_data = Schedule.query.get_or_404(sch_id)
    if request.method == "POST":
        try:
            Schedule_data.cs = request.form["cs"]
            Schedule_data.week = int(request.form["week"])
            Schedule_data.carrier = request.form["carrier"]
            Schedule_data.service = request.form["service"]
            Schedule_data.mv = request.form["mv"]
            Schedule_data.pol = request.form["pol"]
            Schedule_data.pod = request.form["pod"]
            Schedule_data.routing = request.form["routing"]
            Schedule_data.cyopen = datetime.strptime(
                request.form["cyopen"], "%Y-%m-%d"
            )
            Schedule_data.sicutoff = datetime.strptime(
                "{year} {time}".format(
                    year=request.form["sicutoff"],
                    time=request.form["sicutoff_time"],
                ),
                "%Y-%m-%d %H:%M",
            )
            Schedule_data.cycvcls = datetime.strptime(
                "{year} {time}".format(
                    year=request.form["cycvcls"],
                    time=request.form["cycvcls_time"],
                ),
                "%Y-%m-%d %H:%M",
            )
            Schedule_data.etd = datetime.strptime(
                request.form["etd"], "%Y-%m-%d")
            Schedule_data.eta = datetime.strptime(
                request.form["eta"], "%Y-%m-%d")
            Schedule_data.owner = current_user.id
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_Schedule.html", mode="Edit", data=Schedule_data)


@admin.route("/delete_Schedule/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_shipping_data(sch_id):
    Schedule_data = Schedule.query.get_or_404(sch_id)
    db.session.delete(Schedule_data)
    db.session.commit()
    flash("Shipping data has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Routes for Space
#----------------------------------------------------------------------------------------
@admin.route("/add_Space/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_Space_data(sch_id):
    # shipping_data = Schedule.query.get_or_404(Schedule_id)
    # if shipping_data.status == "s3":
    #     flash("Schedule already confirmed. Unable to add Booking.")
    #     return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        try:
            new_data = Space(
                sch_id = sch_id,
                size=request.form["size"],
                avgrate=int(request.form["avgrate"]),
                sugrate=int(request.form["sugrate"]),
                ratevalid=datetime.strptime(request.form["ratevalid"], "%Y-%m-%d"),
                proport=request.form["proport"],
                spcstatus=request.form["spcstatus"],
                void=request.form["void"],
                last_modified_by=current_user.id,
                last_modified_at=datetime.utcnow(),
                owner=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "edit_Space.html",
        sch_id=sch_id,
        mode="Add",
        data=Space(
            size="",
            avgrate=0,
            sugrate=0,
            size="",
            ratevalid=datetime.now(),
            proport="",
            spcstatus="USABLE",
            void="",
            last_modified_by=current_user.id,
            last_modified_at=datetime.utcnow(),
            owner=current_user.id
        ),
    )


@admin.route("/edit_Space/<int:spc_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_Space_data(spc_id):
    Space_data = Space.query.get_or_404(spc_id)

    if request.method == "POST":
        try:
            
            Space_data.size = request.form["size"]
            Space_data.avgrate = int(request.form["avgrate"])
            Space_data.sugrate = int(request.form["sugrate"])
            Space_data.ratevalid = datetime.strptime(request.form["ratevalid"], "%Y-%m-%d")
            Space_data.proport = int(request.form["proport"])
            Space_data.spcstatus = request.form["spcstatus"]
            Space_data.void = request.form["void"]
            Space_data.last_modified_by = current_user.id
            Space_data.last_modified_at = datetime.utcnow()
            Space_data.owner = current_user.id
            
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_Space.html", mode="Edit", data=Space_data)


@admin.route("/delete_Space/<int:spc_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_Space_data(spc_id):
    Space_data = Schedule.query.get_or_404(spc_id)

    # shipping_Schedule = Schedule.query.get_or_404(
    #     Booking_data.data_shipping_Schedule_id
    # )

    # if len(shipping_Schedule.Bookings) <= 0:
    #     shipping_Schedule.status = "s1"

    db.session.delete(Space_data)

    db.session.commit()
    flash("Booking data has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))

# Routes for Reserve
#----------------------------------------------------------------------------------------
@admin.route("/add_Reserve/<int:Schedule_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_Reserve_data(spc_id):
    # shipping_data = Data_shipping_Schedule.query.get_or_404(Schedule_id)
    # if shipping_data.status != "s2":
    #     flash("Booking required before confirming order.")
    #     return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        try:
            new_data = Reserve(
                spc_id = spc_id,
                sales=request.form["sales"],
                saleprice=int(request.form["saleprice"]),
                rsv_date=datetime.strptime(request.form["rsv_date"], "%Y-%m-%d"),
                cfm_date=datetime.strptime(request.form["cfm_date"], "%Y-%m-%d"),
                cfm_cs=request.form["cfm_cs"],
                void=request.form["void"],
                remark=request.form["remark"],
                owner=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "edit_Reserve.html",
        spc_id=spc_id,
        data=Reserve(
            sales="",
            salesprice=0,
            rsv_date=datetime.now(),
            cfm_date=datetime.now(),
            cfm_cs="",
            void="",
            remark="",
            owner=current_user.id
        ),
    )


@admin.route("/edit_Reserve/<int:rsv_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_Reserve_data(rsv_id):
    Reserve_data = Reserve.query.get_or_404(rsv_id)

    if request.method == "POST":
        try:
            
            Reserve_data.sales = request.form["sales"]
            Reserve_data.saleprice = int(request.form["saleprice"])
            Reserve_data.rsv_date = datetime.strptime(request.form["rsv_date"], "%Y-%m-%d")
            Reserve_data.cfm_date = datetime.strptime(request.form["cfm_date"], "%Y-%m-%d")
            Reserve_data.cfm_cs = int(request.form["cfm_cs"])
            Reserve_data.void = int(request.form["void"])
            Reserve_data.remark = request.form["remark"]
            Reserve_data.owner = current_user.id
            
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_Reserve.html", data=Reserve_data)


@admin.route("/delete_Reserve/<int:rsv_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_Reserve_data(rsv_id):
    Reserve_data = Reserve.query.get_or_404(rsv_id)
    # shipping_Schedule = Data_shipping_Schedule.query.get_or_404(
    #     confirm_order_data.data_shipping_Schedule_id
    # )
    db.session.delete(Reserve_data)
    # shipping_Schedule.status = "s2"
    db.session.commit()
    flash("Order confirmation has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Routes for Booking
#----------------------------------------------------------------------------------------
@admin.route("/add_Booking/<int:bk_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_Booking_data(spc_id):
    # shipping_data = Data_shipping_Schedule.query.get_or_404(Schedule_id)
    # if shipping_data.status != "s2":
    #     flash("Booking required before confirming order.")
    #     return redirect(url_for("admin.admin_dashboard"))

    if request.method == "POST":
        try:
            new_data = Booking(
                sch_id = spc_id,
                so=request.form["so"],
                findest=request.form["findest"],
                ct_cl=request.form["ct_cl"],
                shipper=request.form["ct_cl"],
                consignee=request.form["ct_cl"],
                term=request.form["ct_cl"],
                sales=request.form["ct_cl"],
                saleprice=int(request.form["ct_cl"]),
                void=request.form["void"],
                remark=request.form["remark"],
                owner=current_user.id,
            )
            db.session.add(new_data)
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template(
        "edit_Reserve.html",
        spc_id=spc_id,
        data=Reserve(
            so="",
            findest="",
            ct_cl="",
            shipper="",
            consignee="",
            term="",
            sales="",
            saleprice=0,
            void="",
            remark="",     
            owner=current_user.id
        ),
    )


@admin.route("/edit_Booking/<int:bk_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_Booking_data(rsv_id):
    Booking_data = Booking.query.get_or_404(rsv_id)

    if request.method == "POST":
        try:
            
            Booking_data.so = request.form["so"]
            Booking_data.findest = request.form["findest"]
            Booking_data.ct_cl = request.form["ct_cl"]
            Booking_data.shipper = request.form["shipper"]
            Booking_data.consignee = request.form["consignee"]
            Booking_data.term = request.form["term"]
            Booking_data.sales = request.form["sales"]
            Booking_data.saleprice = request.form["saleprice"]
            Booking_data.void = request.form["void"]
            Booking_data.remark = request.form["remark"]
            Booking_data.owner = current_user.id
            
            db.session.commit()
        except ValueError as e:
            return f"An error occurred: {str(e)}"
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_Booking.html", data=Booking_data)


@admin.route("/delete_Booking/<int:bk_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_Booking_data(bk_id):
    Booking_data = Booking.query.get_or_404(bk_id)
    # shipping_Schedule = Data_shipping_Schedule.query.get_or_404(
    #     confirm_order_data.data_shipping_Schedule_id
    # )
    db.session.delete(Booking_data)
    # shipping_Schedule.status = "s2"
    db.session.commit()
    flash("Order confirmation has been deleted.", "success")
    return redirect(url_for("admin.admin_dashboard"))







# Routes for search method
#----------------------------------------------------------------------------------------
@admin.route("/search", methods=["GET", "POST"])
@login_required
@role_required("admin")
def search():
    # print("Search route")  # Debugging line
    q = request.args.get("q")
    show_all = request.args.get("show-all")

    query = (
        db.session.query(Schedule)
        .options(
                joinedload(Schedule.spaces).joinedload(Space.reserves),
                joinedload(Schedule.spaces).joinedload(Space.bookings)
            )
        )

    if q:
        # print(f"Search query: {q}")  # Debugging line
        results = (
            query.filter(
                (Schedule.cs.ilike(f"%{q}%"))
                | (Schedule.week.ilike(f"%{q}%"))
                | (Schedule.carrier.ilike(f"%{q}%"))
                | (Schedule.service.ilike(f"%{q}%"))
                | (Schedule.mv.ilike(f"%{q}%"))
                | (Schedule.pol.ilike(f"%{q}%"))
                | (Schedule.pod.ilike(f"%{q}%"))
                | (Schedule.routing.ilike(f"%{q}%"))
                | (Schedule.cyopen.ilike(f"%{q}%"))
                | (Schedule.sicutoff.ilike(f"%{q}%"))
                | (Schedule.cycvcls.ilike(f"%{q}%"))
                | (Schedule.etd.ilike(f"%{q}%"))
                | (Schedule.eta.ilike(f"%{q}%"))
            )
            .order_by(
                Schedule.sch_id.asc(),
                Space.spc_id.asc(),
                Reserve.rsv_id.asc(),
                Booking.bk_id.asc(),
            )
            .limit(100)
            .all()
        )
        print(f"Results count: {len(results)}")  # Debugging line
    else:
        results = Schedule.query.all()

    if show_all is None:
        results = [data for data in results if data.user_id == current_user.id]

    # print(current_user.id == results[0].user_id) # Debugging line
    return render_template(
        "shipping_table_results.html", results=results, current_user=current_user
    )


# @admin.route("/csv/export", methods=["GET", "POST"])
# @login_required
# @role_required("admin")
# def export_csv():

#     # Query the database for all relevant data
#     Schedules = Schedule.query.all()
#     Bookings = Data_Booking.query.all()
#     confirm_orders = Data_confirm_order.query.all()

#     # Create a dictionary to store confirm orders by shipping Schedule ID
#     confirm_order_dict = {
#         order.Schedule_id: order for order in confirm_orders}

#     # Combine data into a pandas DataFrame
#     data = []

#     for Schedule in Schedules:
#         # Get all Bookings associated with this Schedule
#         associated_Bookings = [
#             b for b in Bookings if b.Schedule_id == Schedule.id]

#         if not associated_Bookings:
#             # If there are no Bookings, still add an entry for the Schedule with empty fields
#             data.append(
#                 {
#                     "carrier": Schedule.carrier,
#                     "service": Schedule.service,
#                     "routing": Schedule.routing,
#                     "MV": Schedule.MV,
#                     "POL": Schedule.POL,
#                     "POD": Schedule.POD,
#                     "CY_Open": Schedule.CY_Open,
#                     "SI_Cut_Off": Schedule.SI_Cut_Off,
#                     "CY_CY_CLS": Schedule.CY_CY_CLS,
#                     "ETD": Schedule.ETD,
#                     "ETA": Schedule.ETA,
#                     "CS": "",
#                     "week": "",
#                     "size": "",
#                     "Final_Destination": "",
#                     "Contract_or_Coloader": "",
#                     "cost": 0,
#                     "Date_Valid": None,
#                     "shipper": "",
#                     "consignee": "",
#                     "term": "",
#                     "salesman": "",
#                     "SR": "",
#                     "remark": "",
#                 }
#             )
#         else:
#             # If there are Bookings, add each Booking with the corresponding Schedule data
#             for Booking in associated_Bookings:
#                 confirm_order = confirm_order_dict.get(Schedule.id, None)

#                 data.append(
#                     {
#                         "carrier": Schedule.carrier,
#                         "service": Schedule.service,
#                         "routing": Schedule.routing,
#                         "MV": Schedule.MV,
#                         "POL": Schedule.POL,
#                         "POD": Schedule.POD,
#                         "CY_Open": Schedule.CY_Open,
#                         "SI_Cut_Off": Schedule.SI_Cut_Off,
#                         "CY_CY_CLS": Schedule.CY_CY_CLS,
#                         "ETD": Schedule.ETD,
#                         "ETA": Schedule.ETA,
#                         "CS": Booking.CS,
#                         "week": Booking.week,
#                         "size": Booking.size,
#                         "Final_Destination": Booking.Final_Destination,
#                         "Contract_or_Coloader": Booking.Contract_or_Coloader,
#                         "cost": Booking.cost,
#                         "Date_Valid": Booking.Date_Valid,
#                         "shipper": confirm_order.shipper if confirm_order else "",
#                         "consignee": confirm_order.consignee if confirm_order else "",
#                         "term": confirm_order.term if confirm_order else "",
#                         "salesman": confirm_order.salesman if confirm_order else "",
#                         "SR": confirm_order.SR if confirm_order else "",
#                         "remark": confirm_order.remark if confirm_order else "",
#                     }
#                 )

#     # Convert the data to a pandas DataFrame
#     df = pd.DataFrame(data)

#     # Create a CSV from the DataFrame
#     csv_output = StringIO()
#     df.to_csv(csv_output, index=False)
#     csv_output.seek(0)

#     # Send the CSV file as a response
#     response = make_response(csv_output.getvalue())
#     response.headers["Content-Disposition"] = "attachment; filename=data_export.csv"
#     response.headers["Content-Type"] = "text/csv"

#     # For frontend members
#     # Put this <a href="{{ url_for('admin.export_csv') }}" class="btn btn-primary">Export Data to CSV</a> to a suitable place
#     # It will directly download the file
#     return response


# @admin.route("/csv/import", methods=["GET", "POST"])
# @login_required
# @role_required("admin")
# def import_csv():
#     if request.method == "POST":
#         # check if the post request has the file part
#         if "file" not in request.files:
#             flash("File not found. Please try again.")
#             return redirect(request.url)

#         file = request.files["file"]

#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == "":
#             flash("File not selected. Please try again.")
#             return redirect(request.url)
#         if file and is_filetype(file.filename, "csv"):
#             # Save uploaded csv file temporarily using random uuid
#             fileid = str(uuid.uuid4())
#             filename = "%s.%s" % (fileid, "csv")
#             file.save(os.path.join(app.config["TEMP_FOLDER"], filename))
#             return redirect(url_for("admin.import_preview", id=fileid))

#         return redirect(url_for("admin.import_csv"))
#     return render_template("csv_import.html", current_user=current_user)


# def is_filetype(filename, extension):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() == extension


# @admin.route("/csv/import/<string:id>", methods=["GET", "POST"])
# @login_required
# @role_required("admin")
# def import_preview(id):

#     # Build csv path from temp folder and filename using filenameid
#     csv_path = os.path.join(app.config["TEMP_FOLDER"], "%s.%s" % (id, "csv"))

#     # If csv doesn't exist in temp folder return user to import csv page
#     if not os.path.isfile(csv_path):
#         flash("File invalid, please try again with another file.")
#         return redirect(url_for("admin.import_csv"))

#     # If file exists, try to read as dataframe, if exception return to import page
#     try:
#         df = pd.read_csv(csv_path, keep_default_na=False)

#         # Convert date columns
#         date_columns = ["CY_Open", "ETD", "ETA", "Date_Valid"]
#         for col in date_columns:
#             df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

#         # Convert datetime columns
#         date_columns = ["SI_Cut_Off", "CY_CY_CLS"]
#         for col in date_columns:
#             df[col] = pd.to_datetime(
#                 df[col], errors="coerce").astype("datetime64[s]")

#         Schedules = []

#         for index, row in df.iterrows():
#             print(index)
#             Schedule_columns = [
#                 "carrier",
#                 "service",
#                 "routing",
#                 "MV",
#                 "POL",
#                 "POD",
#                 "CY_Open",
#                 "SI_Cut_Off",
#                 "CY_CY_CLS",
#                 "ETD",
#                 "ETA",
#             ]
#             # Check if all Schedule columns exists in current row
#             if all(column in row for column in Schedule_columns):
#                 print("can create Schedule")
#                 Schedule = {
#                     "date_created": (
#                         row["date_created"] if "date_created" in row else datetime.now()
#                     ),
#                     "carrier": row["carrier"],
#                     "service": row["service"],
#                     "routing": row["routing"],
#                     "MV": row["MV"],
#                     "POL": row["POL"],
#                     "POD": row["POD"],
#                     "CY_Open": row["CY_Open"],
#                     "SI_Cut_Off": row["SI_Cut_Off"],
#                     "CY_CY_CLS": row["CY_CY_CLS"],
#                     "ETD": row["ETD"],
#                     "ETA": row["ETA"],
#                 }
#                 Schedule["id"] = index
#                 Schedules.append(Schedule)
#         print(Schedules)
#     except Exception as e:
#         flash("CSV file invalid, please try again.")
#         return redirect(url_for("admin.import_csv"))

#     return render_template(
#         "csv_import_preview.html", results=Schedules, current_user=current_user
#     )
