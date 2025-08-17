from flask import Blueprint, render_template, request
from flask_login import login_required
from app.functions.permissions import role_required
from app.functions.searching import (
    search_all_results,
    search_available_spaces_results,
    search_sales_booking_results,
    search_sales_reserve_results,
)


search_routes = Blueprint("search", __name__)


@search_routes.route("/search/all", methods=["GET"])
@login_required
@role_required("admin")
def search_all():
    query = request.args.get("q", "").strip().lower()
    return search_all_results(query)


@search_routes.route("/search/sales_reserve", methods=["GET"])
@login_required
@role_required("sales")
def search_sales_reserve():
    query = request.args.get("q", "").strip().lower()
    return search_sales_reserve_results(query)


@search_routes.route("/search/sales_booking", methods=["GET"])
@login_required
@role_required("sales")
def search_sales_booking():
    query = request.args.get("q", "").strip().lower()
    return search_sales_booking_results(query)


@search_routes.route("/search/search_available_spaces", methods=["GET"])
@login_required
@role_required("sales")
def search_available_spaces():
    filters = {
        "pol": request.args.get("pol_filter", "").strip(),
        "pod": request.args.get("pod_filter", "").strip(),
        "etd": request.args.get("etd_filter", "").strip(),
        "size": request.args.get("size_filter", "").strip(),
        "avgrate": request.args.get("avgrate_filter", "").strip(),
        "sugrate": request.args.get("sugrate_filter", "").strip(),
        "ratevalid": request.args.get("ratevalid_filter", "").strip(),
        "proport": request.args.get("proport_filter", "").strip(),
        "global": request.args.get("global_search", "").strip(),
    }
    spaces = search_available_spaces_results(filters)
    return render_template("available_space_results.html", spaces=spaces)
