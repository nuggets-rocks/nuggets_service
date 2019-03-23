#import datetime
from datetime import datetime, timezone


def date_for_x_days_before_today(dayCount):
    #today = datetime.date.today()
    #return today - datetime.timedelta(days=dayCount)
    #return datetime.date(2019, 3,25, tzinfo=timezone.utc);
    # https://docs.python.org/3/library/datetime.html#module-datetime
    return datetime(2019, 3, 25, hour=0, minute=0, second=0, microsecond=0,tzinfo=timezone.utc)