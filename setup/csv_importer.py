import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.model import Schedule, Space, Reserve, Booking, db

DATABASE_URL = 'sqlite:///instance/database.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Load CSV data
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Ensure required columns exist
required_columns = [
    'cs', 'week', 'carrier', 'service', 'mv', 'pol', 'pod', 'routing', 'cyopen', 'sicutoff', 'cycvcls', 'etd', 'eta',
    'size', 'avgrate', 'sugrate', 'ratevalid', 'proport', 'spcstatus', 'sales', 'saleprice', 'so', 'findest', 'ct_cl', 'shipper', 'consignee', 'term', 'remark'
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

# Convert date columns and handle errors
date_columns = ['cyopen', 'sicutoff', 'cycvcls', 'etd', 'eta', 'ratevalid']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Fill missing values with defaults
default_values = {
    'cs': '',
    'week': 0,
    'carrier': '',
    'service': '',
    'mv': '',
    'pol': '',
    'pod': '',
    'routing': '',
    'size': '',
    'avgrate': 0,
    'sugrate': 0,
    'ratevalid': pd.Timestamp('1970-01-01'),
    'proport': 'N',
    'spcstatus': 'USABLE',
    'sales': '',
    'saleprice': 0,
    'so': '',
    'findest': '',
    'ct_cl': '',
    'shipper': '',
    'consignee': '',
    'term': '',
    'remark': ''
}
df.fillna(default_values, inplace=True)

# Insert data into the database
for index, row in df.iterrows():
    try:
        # Create a schedule
        schedule = Schedule(
            cs=row['cs'],
            week=row['week'],
            carrier=row['carrier'],
            service=row['service'],
            mv=row['mv'],
            pol=row['pol'],
            pod=row['pod'],
            routing=row['routing'],
            cyopen=row['cyopen'],
            sicutoff=row['sicutoff'],
            cycvcls=row['cycvcls'],
            etd=row['etd'],
            eta=row['eta'],
            owner=1
        )
        session.add(schedule)
        session.flush()

        # Create a space
        space = Space(
            sch_id=schedule.sch_id,
            size=row['size'],
            avgrate=row['avgrate'],
            sugrate=row['sugrate'],
            ratevalid=row['ratevalid'],
            proport=row['proport'],
            spcstatus=row['spcstatus'],
            owner=1
        )
        session.add(space)
        session.flush()

        # Create a reservation
        reserve = Reserve(
            spc_id=space.spc_id,
            sales=row['sales'],
            saleprice=row['saleprice'],
            rsv_date=datetime.utcnow(),
            remark=row['remark'],
            owner=1
        )
        session.add(reserve)

        # Create a booking
        booking = Booking(
            spc_id=space.spc_id,
            so=row['so'],
            findest=row['findest'],
            ct_cl=row['ct_cl'],
            shipper=row['shipper'],
            consignee=row['consignee'],
            term=row['term'],
            sales=row['sales'],
            saleprice=row['saleprice'],
            remark=row['remark'],
            owner=1
        )
        session.add(booking)

    except Exception as e:
        print(f"Error processing row {index}: {e}")
        session.rollback()
        continue

# Commit the session
try:
    session.commit()
    print("Data imported successfully.")
except Exception as e:
    session.rollback()
    print(f"Error during commit: {e}")

# Close the session
session.close()
