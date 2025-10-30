from datetime import datetime
import re


def is_checked_key(form: dict, key: str) -> bool:
    return key in form and form[key] == "on"


def is_valid_string(string: str) -> bool:
    # Return True/False if string is valid alphamumeric
    pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/? ]*$'
    return bool(re.match(pattern, string))


def is_valid_spcstatus(spcstatus: set) -> bool:
    return is_valid_string(spcstatus) and spcstatus in [
        "USABLE",
        "RV_SUBMIT",
        "RV_CONFIRM",
        "RV_CANCEL",
        "BK_CONFIRM",
        "BK_RESERVED",
        "BK_PENDING",
        "BK_CANCEL",
        "INVALID",
    ]


def default_or_valid_spcstatus(check_spcstatus: str) -> str:
    print(is_valid_spcstatus(check_spcstatus), check_spcstatus)
    return "USABLE" if not is_valid_spcstatus(check_spcstatus) else check_spcstatus


def is_valid_number(number: str) -> bool:
    # Return True/False if string is valid number
    return number.isdigit()


def zero_or_valid_number(check_number: str) -> int:
    # Return 0 if number is not valid, else return parsed integer
    return 0 if not is_valid_number(check_number) else int(check_number)


def default_or_valid_number(default_number: int, check_number: str) -> int:
    # Return default number if number is not valid, else return parsed integer
    return default_number if not is_valid_number(check_number) else int(check_number)


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
    return default_week if not is_valid_week(check_week) else int(check_week)


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


# Schedule
# =============================================================================
def is_valid_schedule_dict(form: dict) -> bool:
    # Check if dictionary contains all keys for schedule data
    return all(
        item in form
        for item in [
            "cs",
            "week",
            "carrier",
            "service",
            "vessel_name",
            "voyage",
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


def validate_schedule_date_sequence(form: dict) -> tuple[bool, str]:

    # Validate the date sequence logic ETA >= ETD > CY CV CLOSING >= SI CUTOFF > CY OPEN
    try:
        cyopen = datetime.strptime(form["cyopen"], "%Y-%m-%d")
        sicutoff = datetime.strptime(f"{form['sicutoff']} {form['sicutoff_time']}", "%Y-%m-%d %H:%M")
        cycvcls = datetime.strptime(f"{form['cycvcls']} {form['cycvcls_time']}", "%Y-%m-%d %H:%M")
        etd = datetime.strptime(form["etd"], "%Y-%m-%d")
        eta = datetime.strptime(form["eta"], "%Y-%m-%d")
        
        if eta < etd:
            return False, "ETA must be greater than or equal to ETD"
        
        if etd <= cycvcls:
            return False, "ETD must be greater than CY CV CLOSING"
        
        if cycvcls < sicutoff:
            return False, "CY CV CLOSING must be greater than or equal to SI CUTOFF"
        
        # Solved the problem where CYOPEN can not be the same day with SICUTOFF
        # SICUTOFF(datetime) against CY OPEN(date)
        cyopen_datetime = datetime.combine(cyopen.date(), datetime.max.time())
        if sicutoff <= cyopen_datetime:
            return False, "SI CUTOFF must be greater than CY OPEN"
        
        return True, ""
        
    except ValueError as e:
        return False, f"Date parsing error: {str(e)}"


def is_valid_schedule_form(form: dict) -> bool:
    # Return True/False if all key values are valid
    return (
        is_valid_schedule_dict(form)
        and is_valid_string(form["cs"])
        and is_valid_week(form["week"])
        and is_valid_string(form["carrier"])
        and is_valid_string(form["service"])
        and is_valid_string(form["vessel_name"])
        and is_valid_string(form["voyage"])
        and is_valid_string(form["pol"])
        and is_valid_string(form["pod"])
        and is_valid_string(form["routing"])
        and is_valid_date(form["cyopen"])
        and is_valid_datetime(form["sicutoff"], form["sicutoff_time"])
        and is_valid_datetime(form["cycvcls"], form["cycvcls_time"])
        and is_valid_date(form["etd"])
        and is_valid_date(form["eta"])
    )


# Space
# =============================================================================
def is_valid_space_dict(form: dict) -> bool:
    # Check if dictionary contains all keys for space data
    return all(
        item in form
        for item in [
            "size", 
            "avgrate", 
            "sugrate", 
            "ratevalid", 
            "spcstatus"
        ]
    )


def is_valid_space_form(form: dict) -> bool:
    # Return True/False if all key values are valid
    return (
        is_valid_space_dict(form)
        and is_valid_string(form["size"])
        and is_valid_number(form["avgrate"])
        and is_valid_number(form["sugrate"])
        and is_valid_date(form["ratevalid"])
        and is_valid_string(form["spcstatus"])
    )


# Reserve
# =============================================================================
def is_valid_reserve_dict(form: dict) -> bool:
    # Check if dictionary contains all keys for reserve data
    return all(
        item in form 
        for item in [
            "saleprice", 
            "rsv_date", 
            "cfm_cs", 
            "remark"
        ]
    )


def is_valid_reserve_form(form: dict) -> bool:
    # Return True/False if all key values are valid
    return (
        is_valid_reserve_dict(form)
        and is_valid_number(form["saleprice"])
        and is_valid_date(form["rsv_date"])
        and is_valid_date(form["cfm_date"])
        and is_valid_string(form["cfm_cs"])
        and is_valid_string(form["remark"])
    )

def is_valid_sales_reserve(form: dict) -> bool:
    return is_valid_number(form["saleprice"])

# Booking
# =============================================================================
def is_valid_booking_dict(form: dict) -> bool:
    # Check if dictionary contains all keys for booking data
    return all(
        item in form
        for item in [
            "so",
            "findest",
            "ct_cl",
            "shipper",
            "consignee",
            "term",
            "sales",
            "saleprice",
            "remark",
        ]
    )


def is_valid_booking_form(form: dict) -> bool:
    # Return True/False if all key values are valid
    return (
        is_valid_booking_dict(form)
        and is_valid_string(form["so"])
        and is_valid_string(form["findest"])
        and is_valid_string(form["ct_cl"])
        and is_valid_string(form["shipper"])
        and is_valid_string(form["consignee"])
        and is_valid_string(form["term"])
        and is_valid_number(form["sales"])
        and is_valid_number(form["saleprice"])
        and is_valid_string(form["remark"])
    )
