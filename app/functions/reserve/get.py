from datetime import datetime
from flask import render_template
from flask_login import current_user
from app.functions.user.get import get_all_users_names_dict
from app.model import Reserve, Space, Schedule, db
from sqlalchemy.orm import joinedload


def get_sales_reserve(userid: int, etd_start: datetime = None, etd_end: datetime = None) -> list:
    query = (
        Reserve.query.options(joinedload(Reserve.space))
        .filter(Reserve.owner == userid)
    )
    
    if etd_start or etd_end:
        query = query.join(Space, Reserve.spc_id == Space.spc_id).join(Schedule, Space.sch_id == Schedule.sch_id)
        if etd_start:
            query = query.filter(Schedule.etd >= etd_start)
        if etd_end:
            query = query.filter(Schedule.etd <= etd_end)
    
    return query.all()


def reserve_table_results(reserves: list) -> str:
    return render_template(
        "reserve_table_results.html",
        current_user=current_user,
        reserves=reserves,
        users=get_all_users_names_dict(),
    )
