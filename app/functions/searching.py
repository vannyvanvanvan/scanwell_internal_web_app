from flask import render_template
from flask_login import current_user
from app.functions.booking.get import booking_table_results, get_sales_booking
from app.functions.reserve.get import get_sales_reserve, reserve_table_results
from app.model import Schedule, Space, db, User

from datetime import datetime


def flatten_string_lower(var: any) -> str:
    return str(var).lower()


def query_in_list(query: str, match_list: list) -> bool:
    match_list = list(map(flatten_string_lower, match_list))
    for item in match_list:
        if query in item:
            return True
    return False


def find_all_match(query: str) -> list:
    all_schedules = Schedule.query.all()
    results = []

    for schedule in all_schedules:
        if query_in_list(
            query,
            [
                schedule.carrier,
                schedule.service,
                schedule.routing,
                (schedule.vessel_name or ""),
                (schedule.voyage or ""),
                schedule.pol,
                schedule.pod,
            ],
        ):
            results.append(schedule)
            break
        for space in schedule.spaces:
            match_found = False
            if query_in_list(query, [space.size, space.spcstatus]):
                results.append(schedule)
                break
            for reserve in space.reserves:
                if query_in_list(
                    query,
                    [reserve.owner, reserve.cfm_cs, reserve.remark],
                ):
                    results.append(schedule)
                    match_found = True
                    break
            if match_found:
                break
            for booking in space.bookings:
                if query_in_list(
                    query,
                    [
                        booking.so,
                        booking.findest,
                        booking.ct_cl,
                        booking.shipper,
                        booking.consignee,
                        booking.term,
                        booking.sales,
                        booking.remark,
                    ],
                ):
                    results.append(schedule)
                    break

    return results


def schedule_table_results(schedules: list) -> str:
    users = {user.id: user.username for user in User.query.all()}
    return render_template(
        "schedule_table_results.html",
        current_user=current_user,
        results=schedules,
        highlighted={},
        users=users,
    )


def sort_schedules(schedules: list) -> list:
    for schedule in schedules:
        schedule.spaces.sort()
        for space in schedule.spaces:
            space.reserves.sort()
            space.bookings.sort()


def search_all_results(query: str):
    results = find_all_match(query)
    sort_schedules(results)
    return schedule_table_results(results)


def search_sales_reserve_results(query: str):
    all_reserves = get_sales_reserve(current_user.id)
    results = []

    if not query:
        results = all_reserves
    else:
        for reserve in all_reserves:
            if query_in_list(
                query,
                [
                    reserve.saleprice,
                    reserve.rsv_date,
                    reserve.cfm_date,
                    reserve.cfm_cs,
                    reserve.remark,
                ],
            ):
                results.append(reserve)
    return reserve_table_results(results)


def search_sales_booking_results(query: str):
    all_bookings = get_sales_booking(current_user.id)
    all_bookings.sort()
    results = []

    if not query:
        results = all_bookings
    else:
        for booking in all_bookings:
            if query_in_list(
                query,
                [
                    booking.so,
                    booking.findest,
                    booking.ct_cl,
                    booking.shipper,
                    booking.consignee,
                    booking.term,
                    booking.saleprice,
                    booking.remark,
                ],
            ):
                results.append(booking)
    return booking_table_results(results)


def search_available_spaces_results(filters):
    query = db.session.query(Schedule, Space).join(
        Space, Schedule.sch_id == Space.sch_id
    )
    if filters["pol"]:
        query = query.filter(Schedule.pol.ilike(f'%{filters["pol"]}%'))
    if filters["pod"]:
        query = query.filter(Schedule.pod.ilike(f'%{filters["pod"]}%'))
    if filters["etd"]:
        try:
            etd_date = datetime.strptime(filters["etd"], "%Y-%m-%d").date()
            query = query.filter(db.func.date(Schedule.etd) == etd_date)
        except ValueError:
            pass
    if filters["size"]:
        query = query.filter(Space.size.ilike(f'%{filters["size"]}%'))
    if filters["avgrate"]:
        query = query.filter(Space.avgrate == int(filters["avgrate"]))
    if filters["sugrate"]:
        query = query.filter(Space.sugrate == int(filters["sugrate"]))
    if filters["ratevalid"]:
        try:
            valid_date = datetime.strptime(filters["ratevalid"], "%Y-%m-%d").date()
            query = query.filter(db.func.date(Space.ratevalid) == valid_date)
        except ValueError:
            pass
    if filters["proport"]:
        is_proport = filters["proport"] == "yes"
        query = query.filter(Space.proport == is_proport)

    query = query.filter(Space.spcstatus == "USABLE")

    return query.all()
