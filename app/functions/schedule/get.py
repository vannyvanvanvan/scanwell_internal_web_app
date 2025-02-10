from app.functions.searching import sort_schedules
from app.model import Schedule


def get_all_schedules() -> list:
    all_schedules = Schedule.query.all()
    sort_schedules(all_schedules)
    return all_schedules


def get_schedule_by_id(sch_id: int) -> Schedule:
    return Schedule.query.filter_by(sch_id=sch_id).first()


def get_schedule_pol_pod_etd(sch_id: int) -> dict:
    schedule = get_schedule_by_id(sch_id)
    return {
        "pol": schedule.pol,
        "pod": schedule.pod,
        "etd": schedule.etd,
    }
