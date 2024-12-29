# User Stories

## 1. Sales
- View submitted reserves, booking
- View all available spaces
- Search space with POL
- Search space with POD
- Search space with ETD
- Apply for space
- Be reminded of PROPORT with pop-up

## 2. CS
- Approve sales reservation
- Decline sales reservation
- Unconfirm sales reservation
- Record own booking with allocated SO
- Edit own booking
- Auto set or manually specify SPCSTATUS
- View, edit other CS booking
- Manually set space status
- See all records (at the moment)

## 3. Admin
- View all booking
- Manage `SPCSTATUS`
- See and change all records

# System Requirements

## Schedule
- Has at least 1 spaces
- Has any amount of reserves
- Has any amount of bookings

## Space
- Track status (`SPCSTATUS`): `USABLE`, `RV_SUBMIT`, `RV_CONFIRM`, `RF_CANCEL`, `BK_CONFIRM`, `BK_RESERVED`, `BK_PENDING`, `BK_CANCEL`
- Default status `USABLE`
- Usable space auto set to `INVALID` when <24hr until `SICUTOFF` GMT+8 18:00
- In space table, display only one space in each row
- Not allow sales to change `SPCSTATUS`, sales or admin only

## Reserve
- Update `SPCSTATUS` to `RV_` prefix status
- When reserve rejected by CS and space can be reused, set reserve `VOID=True`, space `SPCSTATUS=USABLE`
- If space also invalid, set space `SPCSTATUS=RV_CANCEL`
- Only allow reserve when space status `USABLE`

## Booking
- Update `SPCSTATUS` to `BK_` prefix status
- On booking creation, update space status to `BK_PENDING`
- When booking rejected and space can be released, set booking `VOID=True`, corresponding reserve `VOID=True`, space `SPCSTATUS=USABLE`
- Allow CS add remark on reject
- Only allow booking when space status `USABLE`
- In booking table, display only one booking in each row, even if same SO/SC/C

## Additional requirements
- No delete buttons on all forms (at the moment)
- In booking table move `WEEK`, `SO` on left side of Datetime created
- Implement permission system for CS
- Track all records, last edited user, time
- Specify query criteria