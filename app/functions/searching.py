from flask import render_template
from flask_login import current_user
from app.model import Schedule


def query_in_list(query: str, match_list: list) -> bool:
    match_list = list(map(str.lower, match_list))
    for item in match_list:
        if query in item:
            return True
    return False


def find_match(query: str) -> list:

    all_schedules = Schedule.query.all()
    results = []

    for schedule in all_schedules:
        if query_in_list(
            query,
            [
                schedule.carrier,
                schedule.service,
                schedule.routing,
                schedule.mv,
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
                    [reserve.sales, reserve.cfm_cs, reserve.remark],
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
    return render_template(
        "schedule_table_results.html", current_user=current_user, results=schedules
    )


def sort_schedules(schedules: list) -> list:
    for schedule in schedules:
        schedule.spaces.sort()
        for space in schedule.spaces:
            space.reserves.sort()
            space.bookings.sort()


def render_search_results(query: str):
    results = find_match(query)
    sort_schedules(results)
    return schedule_table_results(results)
