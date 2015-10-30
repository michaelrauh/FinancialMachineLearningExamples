from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR


def date_range(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))