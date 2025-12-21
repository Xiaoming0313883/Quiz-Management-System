import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def clear_console():
    os.system('cls')

def timestampToDateTime(timestamp):
    utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tz_utc8 = ZoneInfo("Asia/Singapore")
    dt_utc8 = utc_dt.astimezone(tz_utc8)
    dt_utc8_naive = dt_utc8.replace(tzinfo=None)
    return dt_utc8_naive