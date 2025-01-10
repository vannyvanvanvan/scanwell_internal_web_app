from datetime import datetime


def is_valid_string(string: str) -> bool:
    # Return True/False if string is valid alphamumeric
    return string.isidentifier()


def is_valid_number(number: str) -> bool:
    # Return True/False if string is valid number
    return number.isdigit()


def zero_or_valid_number(check_number: str) -> int:
    # Return 0 if number is not valid, else return parsed integer
    return 0 if not is_valid_number(check_number) else int(check_number)


def is_valid_week(week: str) -> bool:
    # Return True if week is parsable integer and within 1-52, else False
    return is_valid_number(week) and int(week) > 0 and int(week) <= 52


def now_or_valid_week(check_week: str) -> int:
    # Return today's week if week input invalid, else return valid week input
    return (
        datetime.now().isocalendar().week
        if not is_valid_week(check_week)
        else int(check_week)
    )


def default_or_valid_week(default_week: int, check_week: str) -> int:
    # Return first parameter if second parameter is invalid week
    return default_week if not is_valid_number(check_week) else int(check_week)


def is_valid_date(date: str) -> bool:
    # Return True/False if string can be parsed as date
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def now_or_valid_date(check_date: str) -> datetime:
    # Return today's datetime if string not valid date, else return parsed datetime
    return (
        datetime.now()
        if not is_valid_date(check_date)
        else datetime.strptime(check_date, "%Y-%m-%d")
    )


def default_or_valid_date(default_date: datetime, check_date: str) -> datetime:
    # Return first parameter if second parameter cannot be parsed as date, else return second parameter
    return (
        default_date
        if not is_valid_date(check_date)
        else datetime.strptime(check_date, "%Y-%m-%d")
    )


def is_valid_datetime(date: str, time: str) -> bool:
    # Return True/False if string can be parsed as datetime
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def now_or_valid_datetime(check_date: str, check_time: str) -> datetime:
    # Return now datetime if string not valid datetime, else return parsed datetime
    return (
        datetime.now()
        if not is_valid_datetime(check_date, check_time)
        else datetime.strptime(f"{check_date} {check_time}", "%Y-%m-%d %H:%M")
    )


def default_or_valid_datetime(
    default_datetime: datetime, check_date: str, check_time: str
) -> datetime:
    # Return first parameter if second parameter cannot be parsed as datetime, else return second parameter
    return (
        default_datetime
        if not is_valid_datetime(check_date, check_time)
        else datetime.strptime(f"{check_date} {check_time}", "%Y-%m-%d %H:%M")
    )


def is_valid_schedule_dict(form: dict) -> bool:
    # Check if dictionary contains all keys for schedule data
    return all(
        item in form
        for item in [
            "cs",
            "week",
            "carrier",
            "service",
            "mv",
            "pol",
            "pod",
            "routing",
            "cyopen",
            "sicutoff",
            "sicutoff_time",
            "cycvcls",
            "cycvcls_time",
            "etd",
            "eta",
        ]
    )


def is_valid_schedule_form(form: dict) -> bool:
    # Return True/False if all key values are valid
    return (
        is_valid_schedule_dict(form)
        and is_valid_string(form["cs"])
        and is_valid_week(form["week"])
        and is_valid_string(form["carrier"])
        and is_valid_string(form["service"])
        and is_valid_string(form["mv"])
        and is_valid_string(form["pol"])
        and is_valid_string(form["pod"])
        and is_valid_string(form["routing"])
        and is_valid_date(form["cyopen"])
        and is_valid_datetime(form["sicutoff"], form["sicutoff_time"])
        and is_valid_datetime(form["cycvcls"], form["cycvcls_time"])
        and is_valid_date(form["etd"])
        and is_valid_date(form["eta"])
    )
