from flask import Blueprint, flash, render_template, request
from flask_login import login_required
from app.functions.permissions import rank_required
from app.functions.searching import render_search_results, search_database

search_routes = Blueprint("search", __name__)

@search_routes.route("/search", methods=["GET"])
@login_required
@rank_required('admin')
def search():
    query = request.args.get("q", "").strip()
    if not query:
        flash("Please enter a search query.")
        # return render_search_results(query)
    return render_search_results(query)
