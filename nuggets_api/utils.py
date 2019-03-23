import datetime

def date_for_x_days_before_today(dayCount):
    today = datetime.date.today()
    return  today - datetime.timedelta(days=dayCount)