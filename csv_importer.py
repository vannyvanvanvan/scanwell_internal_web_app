import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.model import Data_booking, Data_shipping_schedule, Data_confirm_order

# Database setup
DATABASE_URL = 'sqlite:///instance/database.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Load CSV data
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Ensure that 'user_id' and 'status' column exists and default it to 1 or 's1' if missing
if 'user_id' not in df.columns or 'status' not in df.columns:
    df['user_id'] = 1                                                                # Default to admin user ID
    df['status'] = 's1'                                                              # Default to status

# Convert date columns and handle errors
date_columns = ['CY_Open', 'SI_Cut_Off', 'CY_CY_CLS', 'ETD', 'ETA', 'Date_Valid']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')                               # Handle invalid date formats

# Fill NaN values with appropriate default values
df.fillna({
    'CS': '',
    'week': 0,
    'carrier': '',
    'service': '',
    'MV': '',
    'SO': '',
    'size': '',
    'POL': '',
    'POD': '',
    'Final_Destination': '',
    'routing': '',
    'CY_Open': pd.Timestamp('1970-01-01'),
    'SI_Cut_Off': pd.Timestamp('1970-01-01'),
    'CY_CY_CLS': pd.Timestamp('1970-01-01'),
    'ETD': pd.Timestamp('1970-01-01'),
    'ETA': pd.Timestamp('1970-01-01'),
    'Contract_or_Coloader': '',
    'shipper': '',
    'consignee': '',
    'term': '',
    'salesman': '',
    'cost': 0,
    'Date_Valid': pd.Timestamp('1970-01-01'),
    'SR': 0,
    'remark': '',
    'status': 's1',                                                                 # Default status
    'user_id': 1                                                                    # Default to admin user ID
}, inplace=True)

# Insert data into the three tables
for index, row in df.iterrows():
    # Insert into Data_shipping_schedule
    new_schedule = Data_shipping_schedule(
        carrier=row['carrier'],
        service=row['service'],
        routing=row['routing'],
        MV=row['MV'],
        POL=row['POL'],
        POD=row['POD'],
        CY_Open=row['CY_Open'],
        SI_Cut_Off=row['SI_Cut_Off'],
        CY_CY_CLS=row['CY_CY_CLS'],
        ETD=row['ETD'],
        ETA=row['ETA'],
        date_created=datetime.utcnow(),
        status=row['status'],
        user_id=row['user_id']
    )
    
    try:
        session.add(new_schedule)
        session.flush()  # Ensure new_schedule gets an ID before proceeding
    except Exception as e:
        print(f"Error inserting into Data_shipping_schedule at row {index}: {e}")
        session.rollback()
        continue

    # Insert into Data_booking 
    new_booking = Data_booking(
        CS=row['CS'],
        week=row['week'],
        size=row['size'],
        Final_Destination=row['Final_Destination'],
        Contract_or_Coloader=row['Contract_or_Coloader'],
        cost=row['cost'],
        Date_Valid=row['Date_Valid'],
        date_created=datetime.utcnow(),
        data_shipping_schedule_id=new_schedule.id,  # Foreign key to shipping schedule
        user_id=row['user_id']
    )
    
    try:
        session.add(new_booking)
    except Exception as e:
        print(f"Error inserting into Data_booking at row {index}: {e}")
        session.rollback()
        continue

    # Insert into Data_confirm_order
    new_order = Data_confirm_order(
        shipper=row['shipper'],
        consignee=row['consignee'],
        term=row['term'],
        salesman=row['salesman'],
        cost=row['cost'],
        Date_Valid=row['Date_Valid'],
        SR=row['SR'],
        remark=row['remark'],
        date_created=datetime.utcnow(),
        data_shipping_schedule_id=new_schedule.id,  # Foreign key to shipping schedule
        user_id=row['user_id']
    )
    
    try:
        session.add(new_order)
    except Exception as e:
        print(f"Error inserting into Data_confirm_order at row {index}: {e}")
        session.rollback()

# Commit the session and handle errors
try:
    session.commit()
except Exception as e:
    session.rollback()
    print(f"An error occurred during commit: {e}")

# Close the session
session.close()
