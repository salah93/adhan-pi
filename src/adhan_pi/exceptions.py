import requests

from typing import Dict, Optional


class PrayerAPIError(Exception):
    def __init__(
        self,
        response: Optional[requests.Response] = None,
        data: Optional[Dict] = None,
    ):
        if response:
            super().__init__(
                "Could not find prayertimes status={status}".format(
                    status=response.status_code
                )
            )
        elif data:
            super().__init__(
                "Could not find prayertimes data={data}".format(data=data)
            )
        else:
            super().__init__()


class LocationNotFoundError(Exception):
    def __init__(self, city: str, state: str):
        super().__init__(
            "Could not find location for {city}, {state}".format(
                city=city, state=state
            )
        )
