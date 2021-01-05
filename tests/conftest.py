import pytest
import responses


@pytest.fixture(scope="session")
def prayer_api_url():
    return "https://api.aladhan.com/v1/calendar"


@pytest.fixture(scope="session")
def prayer_api_200_response(prayer_api_url):
    response = {
        "code": 200,
        "status": "OK",
        "data": [
            {
                "timings": {
                    "Fajr": "04:58 (EST)",
                    "Sunrise": "07:20 (EST)",
                    "Dhuhr": "12:00 (EST)",
                    "Asr": "14:22 (EST)",
                    "Sunset": "16:40 (EST)",
                    "Maghrib": "16:40 (EST)",
                    "Isha": "18:02 (EST)",
                    "Imsak": "05:48 (EST)",
                    "Midnight": "00:00 (EST)",
                }
            }
        ],
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=200,
        match_querystring=False,
    )
    return response


@pytest.fixture(scope="session")
def prayer_api_200_response_different_version_response(prayer_api_url):
    response = {
        "code": 200,
        "status": "OK",
        "data": [
            {
                "timings": {
                    "The Fajr": "04:58 (EST)",
                    "The Sunrise": "07:20 (EST)",
                    "The Dhuhr": "12:00 (EST)",
                    "The Asr": "14:22 (EST)",
                    "The Sunset": "16:40 (EST)",
                    "The Maghrib": "16:40 (EST)",
                    "The Isha": "18:02 (EST)",
                    "The Imsak": "05:48 (EST)",
                    "The Midnight": "00:00 (EST)",
                }
            }
        ],
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=200,
        match_querystring=False,
    )
    return response


@pytest.fixture(scope="session")
def prayer_api_400_response(prayer_api_url):
    response = {
        "code": 400,
        "status": "BAD",
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=400,
        match_querystring=False,
    )
