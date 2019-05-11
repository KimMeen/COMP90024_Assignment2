"""
convert time format into datetime
"""
from datetime import datetime
from email.utils import parsedate_tz


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    date, time = str(dt).split()
    return date+"T"+time


if __name__ == "__main__":
    to_datetime("MON JAN 29 05:00:32 +0000 2019")