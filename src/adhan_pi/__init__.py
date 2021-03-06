import datetime as dt

from .dataclasses import Coordinates, Prayer, PrayerTimes
from .exceptions import PrayerAPIError
from .utils import get_prayer_times_for_month


def get_prayer_times(location: Coordinates, date: dt.date) -> PrayerTimes:
    data = get_prayer_times_for_month(location, date.year, date.month)
    try:
        timings = data[date.day - 1]
        return PrayerTimes(
            date=date,
            fajr=Prayer(name="fajr", time=timings["Fajr"]),
            dhuhr=Prayer(name="dhuhr", time=timings["Dhuhr"]),
            asr=Prayer(name="asr", time=timings["Asr"]),
            maghrib=Prayer(name="maghrib", time=timings["Maghrib"]),
            isha=Prayer(name="isha", time=timings["Isha"]),
        )
    except (IndexError, KeyError):
        raise PrayerAPIError(data=data)
