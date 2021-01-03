import attr
import datetime as dt
import requests

from geopy.geocoders import Nominatim
from geopy.location import Location

from .exceptions import LocationNotFoundError, PrayerAPIError


def get_location_from_city(city: str, state: str) -> Location:
    geolocator = Nominatim(user_agent="adhan-pi")
    location = geolocator.geocode(
        "{city}, {state}".format(city=city, state=state)
    )
    if location is None:
        raise LocationNotFoundError(city, state)
    return location


def extract_time(t: str):
    return dt.datetime.strptime(t[:5], "%H:%M").time()


@attr.s
class PrayerTimes(object):
    date = attr.ib(type=dt.date)
    fajr = attr.ib(type=dt.time, converter=extract_time)
    dhuhr = attr.ib(type=dt.time, converter=extract_time)
    asr = attr.ib(type=dt.time, converter=extract_time)
    maghrib = attr.ib(type=dt.time, converter=extract_time)
    isha = attr.ib(type=dt.time, converter=extract_time)


class PrayertimesAPI(object):
    API_URL = "http://api.aladhan.com/v1/calendar"

    def __init__(self):
        self.session = requests.Session()
        self.session.mount(
            "http://", requests.adapters.HTTPAdapter(max_retries=4)
        )

    def get_prayer_times(self, location: Location, date: dt.date):
        response = self.session.get(
            self.API_URL,
            params=dict(
                latitude=location.latitude,
                longitude=location.longitude,
                method="02",
                month=date.strftime("%m"),
                year=date.strftime("%y"),
            ),
            timeout=(0.5, 0.5),
        )
        if response.status_code != 200:
            raise PrayerAPIError(response=response)
        data = response.json()
        try:
            timings = data["data"][0]["timings"]
            return PrayerTimes(
                date=date,
                fajr=timings["Fajr"],
                dhuhr=timings["Dhuhr"],
                asr=timings["Asr"],
                maghrib=timings["Maghrib"],
                isha=timings["Isha"],
            )
        except (IndexError, KeyError):
            raise PrayerAPIError(data=data)
