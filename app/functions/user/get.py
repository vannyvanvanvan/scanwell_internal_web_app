from app.functions.reserve.get import get_sales_reserve
from app.model import User


def get_all_users() -> list:
    return User.query.all()


def get_all_users_names_dict() -> dict:
    names_dict = {}
    for user in get_all_users():
        names_dict[user.id] = user.friendly_name
    return names_dict
