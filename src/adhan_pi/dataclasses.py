import attr
import datetime as dt

from collections.abc import Iterable, Iterator
from typing import NamedTuple, Union


def extract_time(t: Union[dt.datetime, str]) -> dt.time:
    if isinstance(t, str):
        t = dt.datetime.strptime(t[:5], "%H:%M")
    return t.time()


@attr.s
class Prayer(object):
    name = attr.ib(type=str)
    time = attr.ib(type=dt.time, converter=extract_time)


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


@attr.s
class PrayerTimes(Iterable):
    date = attr.ib(type=dt.date)
    fajr = attr.ib(type=Prayer)
    dhuhr = attr.ib(type=Prayer)
    asr = attr.ib(type=Prayer)
    maghrib = attr.ib(type=Prayer)
    isha = attr.ib(type=Prayer)

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
            prayer = self.pt.fajr
        elif self.index == 1:
            prayer = self.pt.dhuhr
        elif self.index == 2:
            prayer = self.pt.asr
        elif self.index == 3:
            prayer = self.pt.maghrib
        elif self.index == 4:
            prayer = self.pt.isha
        else:
            raise StopIteration
        self.index += 1
        return prayer
