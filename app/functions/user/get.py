from app.model import User


def get_all_users() -> list:
    return User.query.all()


def get_all_users_names_dict() -> dict:
    names_dict = {}
    for user in get_all_users():
        names_dict[user.id] = user.friendly_name
    return names_dict


def get_all_users_tuple_list() -> list:
    tuple_list = []
    for user in get_all_users():
        tuple_list.append((user.id, user.friendly_name))
    return tuple_list
