from datetime import datetime


def is_valid_number(number: str) -> bool:
    return number.isdigit()


def zero_or_valid_number(check_number: str) -> int:
    return 0 if not is_valid_number(check_number) else int(check_number)


def is_valid_week(week: str) -> bool:
    return is_valid_number(week) and int(week) > 0 and int(week) <= 52


def now_or_valid_week(check_week: str) -> int:
    return (
        datetime.now().isocalendar().week
        if not is_valid_number(check_week)
        else int(check_week)
    )


def default_or_valid_week(default_week: int, check_week: str) -> int:
    return default_week if not is_valid_number(check_week) else int(check_week)


def is_valid_date(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def now_or_valid_date(check_date: str) -> str:
    return datetime.now() if not is_valid_date(check_date) else check_date


def default_or_valid_date(default_date: datetime, check_date: str) -> datetime:
    return default_date if not is_valid_date(check_date) else check_date


def is_valid_datetime(date: str, time: str) -> bool:
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def now_or_valid_datetime(check_date: str, check_time: str) -> datetime:
    return (
        datetime.now()
        if not is_valid_datetime(check_date, check_time)
        else datetime.strptime(f"{check_date} {check_time}", "%Y-%m-%d %H:%M")
    )


def default_or_valid_datetime(
    default_datetime: datetime, check_date: str, check_time: str
) -> datetime:
    return (
        default_datetime
        if not is_valid_datetime(check_date, check_time)
        else datetime.strptime(f"{check_date} {check_time}", "%Y-%m-%d %H:%M")
    )


def is_valid_schedule_form(form: dict) -> bool:
    return True
