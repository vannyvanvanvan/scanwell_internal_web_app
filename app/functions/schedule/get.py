from app.functions.searching import sort_schedules
from app.model import Schedule


def get_all_schedules() -> list:
    all_schedules = Schedule.query.all()
    sort_schedules(all_schedules)
    return all_schedules
