import datetime as dt
import requests

from geopy.geocoders import Nominatim

from .dataclasses import Coordinates, PrayerTimes
from .exceptions import LocationNotFoundError, PrayerAPIError


def get_location_from_query(query: str) -> Coordinates:
    geolocator = Nominatim(user_agent="adhan-pi")
    location = geolocator.geocode(query)
    if location is None:
        raise LocationNotFoundError(query)
    return Coordinates(
        latitude=location.latitude, longitude=location.longitude
    )


class PrayertimesAPI(object):
    API_URL = "http://api.aladhan.com/v1/calendar"

    def __init__(self):
        self.session = requests.Session()
        self.session.mount(
            "http://", requests.adapters.HTTPAdapter(max_retries=4)
        )

    def get_prayer_times(
        self, location: Coordinates, date: dt.date
    ) -> PrayerTimes:
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
