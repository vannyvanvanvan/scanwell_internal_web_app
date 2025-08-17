from datetime import datetime
from driver import app
from app.model import db, Schedule, Space, Reserve, Booking

def to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')


# Database context
# ------------------------------------------------------------------------------
with app.app_context():
    Schedule.query.delete()
    Space.query.delete()
    Reserve.query.delete()
    Booking.query.delete()
    db.session.commit()

    # Schedule

    schedule1 = Schedule(
        sch_id=1, cs='Fanny', week=29, carrier='ONE', service='PN2',
        mv='NAVIOS UNISON V.020E', pol='YANTIAN', pod='TACOMA,WA',
        routing='ALL WATER', cyopen=to_date('2024-07-09'), sicutoff=to_datetime('2024-07-15 10:00'),
        cycvcls=to_datetime('2024-07-15 10:00'), etd=to_date('2024-07-19'), eta=to_date('2024-08-03'),
        owner=1
    )
    schedule2 = Schedule(
        sch_id=2, cs='Fanny', week=29, carrier='ONE', service='PS4',
        mv='YM MUTUALITY V.102E', pol='YANTIAN', pod='LOS ANGELES,CA',
        routing='ALL WATER', cyopen=to_date('2024-07-13'), sicutoff=to_datetime('2024-07-17 16:00'),
        cycvcls=to_datetime('2024-07-18 09:00'), etd=to_date('2024-07-19'), eta=to_date('2024-08-09'),
        owner=1
    )
    schedule3 = Schedule(
        sch_id=3, cs='Fanny', week=29, carrier='ONE', service='PN2',
        mv='SEASPAN FALCON V.009E', pol='YANTIAN', pod='TACOMA,WA',
        routing='ALL WATER', cyopen=to_date('2024-07-17'), sicutoff=to_datetime('2024-07-23 10:00'),
        cycvcls=to_datetime('2024-07-23 10:00'), etd=to_date('2024-07-24'), eta=to_date('2024-08-16'),
        owner=1
    )
    schedule4 = Schedule(
        sch_id=4, cs='Fanny', week=29, carrier='MSC', service='CHINOOK',
        mv='MSC MARINA UK429A', pol='YANTIAN', pod='PORTLAND,OR',
        routing='ALL WATER', cyopen=to_date('2024-07-13'), sicutoff=to_datetime('2024-07-18 12:00'),
        cycvcls=to_datetime('2024-07-19 12:00'), etd=to_date('2024-07-21'), eta=to_date('2024-08-21'),
        owner=1
    )

    schedule5 = Schedule(
        sch_id=5, cs='Fanny', week=29, carrier='ONE', service='PS4',
        mv='YM UBIQUITY V.065E', pol='YANTIAN', pod='LOS ANGELES,CA',
        routing='ALL WATER', cyopen=to_date('2024-07-16'), sicutoff=to_datetime('2024-07-21 18:00'),
        cycvcls=to_datetime('2024-07-22 9:00'), etd=to_date('2024-07-26'), eta=to_date('2024-08-15'),
        owner=1
    )

    db.session.add_all([schedule1, schedule2, schedule3, schedule4, schedule5])

    # Space
    space1 = Space(
        spc_id=1, sch_id=1, size='40HQ', avgrate=7447, sugrate=7550,
        ratevalid=to_date('2024-12-31'), proport=True, spcstatus='BK_PENDING', owner=1
    )
    space2 = Space(
        spc_id=2, sch_id=1, size='20GP', avgrate=3247, sugrate=3550,
        ratevalid=to_date('2024-12-31'), proport=True, spcstatus='USABLE', owner=1
    )
    space3 = Space(
        spc_id=3, sch_id=1, size='40GP', avgrate=7447, sugrate=7550,
        ratevalid=to_date('2024-11-30'), proport=True, spcstatus='BK_RESERVED', owner=1
    )
    space4 = Space(
        spc_id=4, sch_id=2, size='45HQ', avgrate=7684, sugrate=7800,
        ratevalid=to_date('2024-07-31'), proport=False, spcstatus='USABLE', owner=1
    )
    space5 = Space(
        spc_id=5, sch_id=2, size='40HQ', avgrate=7447, sugrate=7600,
        ratevalid=to_date('2024-07-31'), proport=True, spcstatus='INVALID', owner=1
    )
    space6 = Space(
        spc_id=6, sch_id=3, size='20GP', avgrate=2601, sugrate=2680,
        ratevalid=to_date('2024-09-30'), proport=False, spcstatus='USABLE', owner=1
    )

    db.session.add_all([space1, space2, space3, space4, space5, space6])

    # Reserve
    reserve1 = Reserve(
        rsv_id=1, spc_id=1, sales=5, saleprice=8000, rsv_date=to_date('2024-07-01'),
        cfm_date=to_date('2024-07-01'), cfm_cs=4, void=False, remark='TEST', owner=5
    )

    db.session.add(reserve1)

    # Booking
    booking1 = Booking(
        bk_id=1, spc_id=1, so='SZPEJ4609700', findest='HOUSTON,TX',
        ct_cl='Contract', shipper='CMECH', consignee='DZN CONCEPTS INC.',
        term='CIF', sales=5, saleprice=8000, void=False, remark='取消', owner=1
    )
    booking2 = Booking(
        bk_id=2, spc_id=2, so='SZPEL0126600', findest='CINCINNATI,OH',
        ct_cl='Contract', shipper='EXPRESS SOLUTIONS',
        consignee='BOOKING UNION (USA) INC', term='FOB',
        sales=6, saleprice=8184, void=False, remark='', owner=1
    )
    booking3 = Booking(
        bk_id=3, spc_id=3, so='SZPEL0138900', findest='HOUSTON,TX',
        ct_cl='Contract', shipper='', consignee='',
        term='', sales=None, saleprice='', void=False, remark='', owner=1
    )
    booking4 = Booking(
        bk_id=4, spc_id=4, so='181AY0245399880D1', findest='',
        ct_cl='CO-LOAD', shipper='CHEUNG HING PLASTIC', consignee='GOODCO',
        term='FOB', sales=6, saleprice=8184, void=True, remark='', owner=1
    )

    db.session.add_all([booking1, booking2, booking3, booking4])

    # Commit changes
    db.session.commit()

# ------------------------------------------------------------------------------
