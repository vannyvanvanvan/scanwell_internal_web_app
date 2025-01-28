from flask import Blueprint, request
from flask_login import login_required
from app.functions.permissions import role_required
from app.functions.searching import search_all_results, search_sales_reserve_results

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

