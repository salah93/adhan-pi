import datetime as dt

import pytest
import responses
from automock import get_mock

import adhan_pi.utils as utils


def test_get_location():
    location = utils.get_location_from_query("New York, NY")
    assert (0, 1) == tuple(location)
    assert location.latitude == 0
    assert location.longitude == 1
    mock = get_mock("adhan_pi.utils.Nominatim")
    mock.assert_called_with(user_agent="adhan-pi")
    mock().geocode.assert_called_with("New York, NY")


@responses.activate
def test_get_prayer_times(prayer_api_200_response):
    location = utils.get_location_from_query("New York, NY")
    p = utils.PrayertimesAPI()
    today = dt.date.today()
    prayer_times = p.get_prayer_times(location, today)
    assert isinstance(prayer_times, utils.PrayerTimes)
    assert prayer_times.fajr.name == "fajr"
    assert prayer_times.fajr.time == dt.time(hour=4, minute=58)
    assert prayer_times.date == today
    assert [
        ("fajr", dt.time(hour=4, minute=58)),
        ("dhuhr", dt.time(hour=12)),
        ("asr", dt.time(hour=14, minute=22)),
        ("maghrib", dt.time(hour=16, minute=40)),
        ("isha", dt.time(hour=18, minute=2)),
    ] == [(p.name, p.time) for p in prayer_times]


@responses.activate
def test_get_prayer_times_200_bad_response(
    prayer_api_200_response_different_version_response,
):
    location = utils.get_location_from_query("New York, NY")
    p = utils.PrayertimesAPI()
    today = dt.date.today()
    with pytest.raises(utils.PrayerAPIError):
        p.get_prayer_times(location, today)


@responses.activate
def test_get_prayer_times_400(prayer_api_400_response):
    location = utils.get_location_from_query("New York, NY")
    p = utils.PrayertimesAPI()
    today = dt.date.today()
    with pytest.raises(utils.PrayerAPIError):
        p.get_prayer_times(location, today)
