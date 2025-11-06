from datetime import datetime, timedelta
from app.functions.searching import sort_schedules
from app.model import Schedule


def get_all_schedules(
    etd_start: datetime = None,
    etd_end: datetime = None,
    space_status: str | None = None,
    sales_user_id: int | None = None,
) -> list:
    query = Schedule.query

    if etd_start:
        query = query.filter(Schedule.etd >= etd_start)
    if etd_end:
        query = query.filter(Schedule.etd <= etd_end)

    schedules = query.all()

    # memory filters for space_status and sales_user_id
    if space_status or sales_user_id:
        filtered: list[Schedule] = []
        for schedule in schedules:
            has_match = False
            for space in schedule.spaces:
                # Space status filter
                if space_status and space.spcstatus != space_status:
                    continue

                # if either a reserve owner or booking.sales equals target
                if sales_user_id is not None:
                    sales_match = False
                    for reserve in space.reserves:
                        if reserve.owner == sales_user_id:
                            sales_match = True
                            break
                    if not sales_match:
                        for booking in space.bookings:
                            if booking.sales == sales_user_id:
                                sales_match = True
                                break
                    if not sales_match:
                        continue

                has_match = True
                break

            if has_match:
                filtered.append(schedule)
        schedules = filtered

    sort_schedules(schedules)
    return schedules


def get_schedule_by_id(sch_id: int) -> Schedule:
    return Schedule.query.filter_by(sch_id=sch_id).first()


def get_schedule_pol_pod_etd(sch_id: int) -> dict:
    schedule = get_schedule_by_id(sch_id)
    return {
        "service": schedule.service,
        "vessel_name": schedule.vessel_name,
        "voyage": schedule.voyage,
        "pol": schedule.pol,
        "pod": schedule.pod,
        "etd": schedule.etd,
    }
