from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


def timestamps(days):

# Get the current date
    now = datetime.now()
    datetoday = datetime.date(now)
# Calculate the check-in date (2 days after the current date)
    checkin_date = datetoday + relativedelta(days=2)
    print()
# Calculate the check-out date
    checkout_date = checkin_date + relativedelta(days=days)
    date_1970 = date(1970, 1, 1)
    unix_timestamp_checkin = int((checkin_date - date_1970).total_seconds())


    unix_timestamp_checkout = int((checkout_date - date_1970).total_seconds())

    return unix_timestamp_checkin,unix_timestamp_checkout
