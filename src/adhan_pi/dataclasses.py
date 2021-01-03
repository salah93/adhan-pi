import attr
import datetime as dt

from collections.abc import Iterable, Iterator
from typing import NamedTuple, Union


def extract_time(t: Union[str, dt.datetime]) -> dt.time:
    if isinstance(t, dt.datetime):
        datetime = t
    else:
        datetime = dt.datetime.strptime(t[:5], "%H:%M")
    return datetime.time()


class Prayer(NamedTuple):
    name: str
    time: dt.time


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


@attr.s
class PrayerTimes(Iterable):
    date = attr.ib(type=dt.date)
    fajr = attr.ib(type=dt.time, converter=extract_time)
    dhuhr = attr.ib(type=dt.time, converter=extract_time)
    asr = attr.ib(type=dt.time, converter=extract_time)
    maghrib = attr.ib(type=dt.time, converter=extract_time)
    isha = attr.ib(type=dt.time, converter=extract_time)

    def __iter__(self):
        return PrayerIterator(self)


class PrayerIterator(Iterator):
    def __init__(self, pt: PrayerTimes):
        self.index = 0
        self.pt = pt

    def __iter__(self):
        return self

    def __next__(self) -> Prayer:
        if self.index == 0:
            prayer = Prayer(name="fajr", time=self.pt.fajr)
        elif self.index == 1:
            prayer = Prayer(name="dhuhr", time=self.pt.dhuhr)
        elif self.index == 2:
            prayer = Prayer(name="asr", time=self.pt.asr)
        elif self.index == 3:
            prayer = Prayer(name="maghrib", time=self.pt.maghrib)
        elif self.index == 4:
            prayer = Prayer(name="isha", time=self.pt.isha)
        else:
            raise StopIteration
        self.index += 1
        return prayer
